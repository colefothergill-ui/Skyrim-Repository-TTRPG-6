#!/usr/bin/env python3
import json
import re
from pathlib import Path

RANK_TO_VALUE = {
    "Great (+4)": 4,
    "Good (+3)": 3,
    "Fair (+2)": 2,
    "Average (+1)": 1
}

BONUS_RE = re.compile(r"^\s*(.+?)\s*\(\s*([+-]?\d+)\s*\)\s*$")

def parse_bonus_strings(bonus_list):
    """
    Converts ["Fight (+1)", "Athletics (+1)"] into {"Fight": 1, "Athletics": 1}
    """
    out = {}
    if not isinstance(bonus_list, list):
        return out
    for s in bonus_list:
        if not isinstance(s, str):
            continue
        m = BONUS_RE.match(s)
        if not m:
            continue
        skill = m.group(1).strip()
        val = int(m.group(2))
        out[skill] = out.get(skill, 0) + val
    return out

def pyramid_to_base_skills(pc):
    """
    PC format: pc["skills"] = {"Good (+3)": ["Fight", "Stealth"], ...}
    -> {"Fight": 3, "Stealth": 3, ...}
    """
    base = {}
    skills = pc.get("skills", {})
    if not isinstance(skills, dict):
        return base

    for rank, skill_list in skills.items():
        v = RANK_TO_VALUE.get(rank)
        if v is None:
            continue
        if not isinstance(skill_list, list):
            continue
        for sk in skill_list:
            if isinstance(sk, str):
                base[sk] = v
    return base

def load_standing_stone_bonus(data_dir, stone_name):
    """
    Reads data/standing_stones.json (effect.game_mechanic contains '+1 to Athletics...')
    Returns {"Athletics": 1} etc.
    """
    data_dir = Path(data_dir)
    stones_path = data_dir / "standing_stones.json"
    if not stones_path.exists() or not stone_name:
        return {}

    # Use Unicode-safe loading
    data = stones_path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            stones = json.loads(data.decode(enc))
            break
        except Exception:
            continue
    else:
        stones = json.loads(data.decode("latin-1", errors="replace"))
    
    for s in stones.get("standing_stones", []):
        if s.get("name") == stone_name:
            gm = (s.get("effect") or {}).get("game_mechanic", "")
            # Very small parser for the common pattern "+1 to Athletics"
            # If you expand stone effects later, upgrade this parser.
            m = re.search(r"([+-]?\d+)\s*to\s*([A-Za-z]+)", gm)
            if m:
                return {m.group(2): int(m.group(1))}
    return {}

def compute_effective_skills(pc, data_dir="data"):
    base = pyramid_to_base_skills(pc)

    racial = pc.get("racial_bonuses", {}) or {}
    racial_skill_bonus = parse_bonus_strings(racial.get("skill_bonuses", []))

    stone_bonus = load_standing_stone_bonus(data_dir, pc.get("standing_stone"))

    effective = dict(base)
    for sk, b in racial_skill_bonus.items():
        effective[sk] = effective.get(sk, 0) + b
    for sk, b in stone_bonus.items():
        effective[sk] = effective.get(sk, 0) + b

    return {
        "base": base,
        "racial_bonus": racial_skill_bonus,
        "standing_stone_bonus": stone_bonus,
        "effective": effective
    }

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--pc", required=True, help="Path to PC json (e.g., data/pcs/example_pc.json)")
    ap.add_argument("--data-dir", default="data", help="Data directory containing standing_stones.json")
    args = ap.parse_args()

    p = Path(args.pc)
    # Use Unicode-safe loading (matches export_repo.py approach)
    data = p.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            pc = json.loads(data.decode(enc))
            break
        except Exception:
            continue
    else:
        pc = json.loads(data.decode("latin-1", errors="replace"))
    
    out = compute_effective_skills(pc, data_dir=args.data_dir)
    print(json.dumps(out, indent=2, ensure_ascii=False))
