#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------
# Utilities
# ---------------------------

def read_text_safely(path: Path) -> str:
    data = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(enc)
        except Exception:
            continue
    return data.decode("latin-1", errors="replace")

def read_json_safely(path: Path) -> Any:
    txt = read_text_safely(path)
    return json.loads(txt)

def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for p in [cur] + list(cur.parents):
        if (p / "data").exists() and ((p / "state").exists() or (p / "clocks").exists() or (p / "logs").exists()):
            return p
    # fallback: current directory
    return cur

def newest_file(globbed: List[Path]) -> Optional[Path]:
    if not globbed:
        return None
    return max(globbed, key=lambda p: p.stat().st_mtime)

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", s.lower()).strip("_")

# ---------------------------
# Clock extraction (schema-agnostic)
# ---------------------------

@dataclass
class ClockView:
    name: str
    current: int
    maximum: int
    ratio: float
    source: str

def _as_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default

def extract_clocks(obj: Any, source: str, prefix: str = "") -> List[ClockView]:
    clocks: List[ClockView] = []

    # Common patterns:
    # { "clocks": { "<id>": { "name": "...", "current": 2, "max": 8 } } }
    # { "clock": { "current": 1, "max": 4 } }
    # { "current_progress": 4, "max_progress": 8 }
    # etc.
    if isinstance(obj, dict):
        # direct clock-like dict
        has_current = any(k in obj for k in ("current", "current_progress", "filled", "progress"))
        has_max = any(k in obj for k in ("max", "maximum", "max_progress", "max_segments", "total_segments"))
        has_name = "name" in obj or "title" in obj

        if has_current and has_max and has_name:
            name = str(obj.get("name") or obj.get("title") or prefix or "Unnamed Clock")
            cur = _as_int(obj.get("current", obj.get("current_progress", obj.get("filled", obj.get("progress", 0)))), 0)
            mx = _as_int(obj.get("max", obj.get("maximum", obj.get("max_progress", obj.get("max_segments", obj.get("total_segments", 0))))), 0)
            if mx > 0:
                clocks.append(ClockView(
                    name=name,
                    current=cur,
                    maximum=mx,
                    ratio=cur / mx,
                    source=source
                ))

        # recurse
        for k, v in obj.items():
            new_prefix = f"{prefix}.{k}" if prefix else str(k)
            clocks.extend(extract_clocks(v, source, new_prefix))

    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            clocks.extend(extract_clocks(v, source, f"{prefix}[{i}]"))

    return clocks

# ---------------------------
# PC parsing helpers
# ---------------------------

RANK_TO_VALUE = {
    "Great (+4)": 4,
    "Good (+3)": 3,
    "Fair (+2)": 2,
    "Average (+1)": 1
}

BONUS_RE = re.compile(r"^\s*(.+?)\s*\(\s*([+-]?\d+)\s*\)\s*$")

def parse_bonus_list(bonus_list: Any) -> Dict[str, int]:
    out: Dict[str, int] = {}
    if not isinstance(bonus_list, list):
        return out
    for s in bonus_list:
        if not isinstance(s, str):
            continue
        m = BONUS_RE.match(s)
        if not m:
            continue
        sk = m.group(1).strip()
        val = int(m.group(2))
        out[sk] = out.get(sk, 0) + val
    return out

def pyramid_base_skills(pc: Dict[str, Any]) -> Dict[str, int]:
    base: Dict[str, int] = {}
    skills = pc.get("skills", {})
    if not isinstance(skills, dict):
        return base
    for rank, sks in skills.items():
        v = RANK_TO_VALUE.get(rank)
        if v is None or not isinstance(sks, list):
            continue
        for sk in sks:
            if isinstance(sk, str):
                base[sk] = v
    return base

def compute_effective_skills(repo: Path, pc: Dict[str, Any]) -> Dict[str, Any]:
    # Prefer precomputed derived.effective_skills if present
    derived = pc.get("derived", {})
    if isinstance(derived, dict) and isinstance(derived.get("effective_skills"), dict):
        return {
            "base": pyramid_base_skills(pc),
            "racial_bonus": derived.get("bonus_sources", {}).get("race", {}),
            "standing_stone_bonus": derived.get("bonus_sources", {}).get("standing_stone", {}),
            "effective": derived.get("effective_skills", {})
        }

    base = pyramid_base_skills(pc)

    # Race bonuses: try embedded on PC, else try data/racial_traits.json or data/races.json
    race_name = pc.get("race")
    racial_bonus: Dict[str, int] = {}

    # 1) direct on pc if it exists
    if isinstance(pc.get("racial_bonuses"), dict):
        racial_bonus = parse_bonus_list(pc["racial_bonuses"].get("skill_bonuses", []))

    # 2) look up from repo data files
    if not racial_bonus and race_name:
        for candidate in (repo / "data" / "races.json", repo / "data" / "racial_traits.json"):
            if candidate.exists():
                try:
                    data = read_json_safely(candidate)
                    races = data.get("races") if isinstance(data, dict) else None
                    if isinstance(races, list):
                        for r in races:
                            if isinstance(r, dict) and r.get("name") == race_name:
                                racial_bonus = parse_bonus_list(r.get("skill_bonuses", []))
                                break
                except Exception:
                    pass
            if racial_bonus:
                break

    # Standing stone bonus: simple parser from data/standing_stones.json for "+1 to Athletics" patterns
    stone_bonus: Dict[str, int] = {}
    stone_name = pc.get("standing_stone")
    stones_path = repo / "data" / "standing_stones.json"
    if stone_name and stones_path.exists():
        try:
            stones = read_json_safely(stones_path)
            for s in stones.get("standing_stones", []):
                if isinstance(s, dict) and s.get("name") == stone_name:
                    gm = ((s.get("effect") or {}).get("game_mechanic")) or ""
                    m = re.search(r"([+-]?\d+)\s*to\s*([A-Za-z]+)", gm)
                    if m:
                        stone_bonus[m.group(2)] = int(m.group(1))
        except Exception:
            pass

    eff = dict(base)
    for sk, b in racial_bonus.items():
        eff[sk] = eff.get(sk, 0) + b
    for sk, b in stone_bonus.items():
        eff[sk] = eff.get(sk, 0) + b

    return {
        "base": base,
        "racial_bonus": racial_bonus,
        "standing_stone_bonus": stone_bonus,
        "effective": eff
    }

# ---------------------------
# Mid-session protocol
# ---------------------------

def pick_primary_pc(repo: Path, state: Dict[str, Any]) -> Optional[Path]:
    # Try state pointers first
    for key in ("active_pc", "active_pc_id", "pc_id", "player_character_id"):
        v = state.get(key)
        if isinstance(v, str):
            # common naming pattern: data/pcs/pc_<id>.json
            cand = repo / "data" / "pcs" / f"{v}.json"
            if cand.exists():
                return cand
            cand2 = repo / "data" / "pcs" / f"pc_{v}.json"
            if cand2.exists():
                return cand2

    # Fallback: first json in data/pcs
    pcs_dir = repo / "data" / "pcs"
    if pcs_dir.exists():
        pcs = sorted(pcs_dir.glob("*.json"))
        return pcs[0] if pcs else None
    return None

def summarize_relationships(state: Dict[str, Any]) -> List[Tuple[str, Any]]:
    rel = state.get("faction_relationships")
    if isinstance(rel, dict):
        items = sorted(rel.items(), key=lambda kv: kv[1], reverse=True)
        return items[:6]
    return []

def top_clocks(repo: Path) -> List[ClockView]:
    clock_sources: List[Tuple[str, Path]] = []

    for folder in ("clocks",):
        d = repo / folder
        if d.exists():
            for p in d.rglob("*.json"):
                clock_sources.append((str(p.relative_to(repo)), p))

    # Some repos keep clocks under data/clocks
    d2 = repo / "data" / "clocks"
    if d2.exists():
        for p in d2.rglob("*.json"):
            clock_sources.append((str(p.relative_to(repo)), p))

    all_clocks: List[ClockView] = []
    for label, p in clock_sources:
        try:
            obj = read_json_safely(p)
            all_clocks.extend(extract_clocks(obj, source=label))
        except Exception:
            continue

    # De-dup loosely by (name, source)
    uniq: Dict[Tuple[str, str], ClockView] = {}
    for c in all_clocks:
        key = (c.name, c.source)
        if key not in uniq or uniq[key].ratio < c.ratio:
            uniq[key] = c

    clocks = list(uniq.values())
    clocks.sort(key=lambda c: (c.ratio, c.current), reverse=True)
    return clocks[:10]

def latest_log(repo: Path) -> Optional[Path]:
    logs_dir = repo / "logs"
    if not logs_dir.exists():
        return None
    # Prefer canonical session logs
    latest = newest_file(sorted(logs_dir.glob("*_LATEST.md")))
    if latest:
        return latest
    # Fallback to any md except dragonbreak_log
    candidates = [p for p in logs_dir.glob("*.md") if p.name != "dragonbreak_log.md"]
    return newest_file(sorted(candidates)) if candidates else None

def checkpoint_append(log_path: Path, text: str) -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    block = f"\n\n---\n## Mid-Session Checkpoint ({stamp})\n{text.strip()}\n"
    existing = read_text_safely(log_path) if log_path.exists() else ""
    log_path.write_text(existing + block, encoding="utf-8")

def dragonbreak_heuristic(clocks: List[ClockView], state: Dict[str, Any]) -> str:
    # Simple heuristic: if any clock >= 75% or any 'major_event' flags, suggest DB potential.
    hot = [c for c in clocks if c.maximum > 0 and c.ratio >= 0.75]
    flags = []
    for k in ("major_death", "timeline_fracture", "dragonbreak", "mythic_fracture"):
        if state.get(k):
            flags.append(k)

    if flags or hot:
        pieces = []
        if flags:
            pieces.append(f"State flags: {', '.join(flags)}")
        if hot:
            pieces.append("High-pressure clocks: " + ", ".join([f"{c.name} ({c.current}/{c.maximum})" for c in hot[:3]]))
        return "POTENTIAL DRAGONBREAK TRIGGER: " + " | ".join(pieces)
    return "No explicit Dragonbreak trigger found. (Heuristic: no clocks >= 75% and no state fracture flags.)"

def authenticity_tri_check(repo: Path, state: Dict[str, Any], pc: Dict[str, Any]) -> List[str]:
    notes: List[str] = []

    # Relevance check: do we have modules directory + any known topic keys?
    modules_dir = repo / "modules"
    if not modules_dir.exists():
        notes.append("Relevance: modules/ not found (OK if this repo doesn’t use modules).")
    else:
        notes.append(f"Relevance: modules/ present ({len(list(modules_dir.glob('*')))} entries).")

    # Preparedness: check that any 'current_npcs' have stat sheets
    current_npcs = state.get("current_npcs") or state.get("scene_npcs") or []
    if isinstance(current_npcs, list) and current_npcs:
        missing = []
        for npc in current_npcs:
            if not isinstance(npc, str):
                continue
            sheet = repo / "data" / "npc_stat_sheets" / f"{slug(npc)}.json"
            if not sheet.exists():
                missing.append(npc)
        if missing:
            notes.append("Preparedness: missing NPC stat sheets for: " + ", ".join(missing[:8]))
        else:
            notes.append("Preparedness: NPC stat sheets look good for current scene.")
    else:
        notes.append("Preparedness: no current_npcs listed in state (that’s fine; GM can supply ad hoc).")

    # Narrative fulfillment: do we have a current objective?
    obj = state.get("current_objective") or state.get("session_objective")
    if not obj:
        notes.append("Narrative: current_objective not set in state (recommend setting it for cleaner options generation).")
    else:
        notes.append(f"Narrative: objective locked — {obj}")

    # Mechanical readiness: do we have core PC fields?
    for field in ("aspects", "skills", "stunts"):
        if field not in pc:
            notes.append(f"Mechanics: PC missing '{field}' field (tools may output weaker summaries).")
    return notes

def build_options(state: Dict[str, Any], pc: Dict[str, Any], eff: Dict[str, Any]) -> List[str]:
    # Lightweight, generic, but tailored by objective + a few stunts
    objective = state.get("current_objective") or state.get("session_objective") or "Advance the current objective."
    location = state.get("current_location") or state.get("starting_location") or "Unknown location"
    stunts = pc.get("stunts", [])
    stunt_names = []
    if isinstance(stunts, list):
        for s in stunts[:6]:
            if isinstance(s, str):
                stunt_names.append(s.split(":")[0].strip())
            elif isinstance(s, dict) and "name" in s:
                stunt_names.append(str(s["name"]))

    has_thuum = False
    extras = pc.get("extras", [])
    if isinstance(extras, list):
        has_thuum = any(isinstance(x, dict) and "Thu" in str(x.get("name", "")) for x in extras)

    es = eff.get("effective", {})
    fight = es.get("Fight", eff.get("base", {}).get("Fight", 0))
    stealth = es.get("Stealth", eff.get("base", {}).get("Stealth", 0))
    ath = es.get("Athletics", eff.get("base", {}).get("Athletics", 0))
    rap = es.get("Rapport", eff.get("base", {}).get("Rapport", 0))
    will = es.get("Will", eff.get("base", {}).get("Will", 0))

    opts = []
    opts.append(f"1) Stealth-first play: Use Stealth ({stealth}) + your positioning to bypass attention and push: {objective}")
    opts.append(f"2) Social leverage: Use Rapport ({rap}) / Deceive to turn an NPC into a door-key (info, access, pardon) at {location}")
    opts.append(f"3) Direct action: Use Fight ({fight}) or Athletics ({ath}) to force a clean outcome (capture, break-through, chase, extraction)")
    opts.append("4) Investigation: Create advantages with Notice/Lore to surface the *real* constraint (who/what/where is actually blocking you)")
    if has_thuum:
        opts.append(f"5) Thu'um angle: Use Will ({will}) to Create Advantage/Overcome with a shout to reframe the scene (mobility, fear, positioning)")
    else:
        opts.append("5) Wildcard: Spend a Fate Point to declare a helpful detail (a contact, a shortcut, a weakness) and capitalize immediately")
    return opts

def main() -> int:
    ap = argparse.ArgumentParser(description="Mid-session protocol: recap + clocks + options + checkpoint.")
    ap.add_argument("--checkpoint", default="", help="If provided, appends a Mid-Session Checkpoint block to the latest log.")
    args = ap.parse_args()

    repo = find_repo_root(Path.cwd())

    # Load state
    state_path = repo / "state" / "campaign_state.json"
    state: Dict[str, Any] = {}
    if state_path.exists():
        try:
            state = read_json_safely(state_path)
        except Exception as e:
            print(f"[WARN] Could not parse {state_path}: {e}")
    else:
        print("[WARN] state/campaign_state.json not found. Output will be partial.")

    # Load primary PC
    pc_path = pick_primary_pc(repo, state)
    pc: Dict[str, Any] = {}
    if not pc_path:
        print("[WARN] No primary PC found. Run Session Zero to create a character in data/pcs/ and set state.active_pc_id.")
    elif pc_path.exists():
        try:
            pc = read_json_safely(pc_path)
        except Exception as e:
            print(f"[WARN] Could not parse {pc_path}: {e}")
    else:
        print("[WARN] No PC json found in data/pcs/. Output will be partial.")

    # Compute effective skills
    eff = compute_effective_skills(repo, pc)

    # Clocks
    clocks = top_clocks(repo)

    # Latest log
    log_path = latest_log(repo)

    # Output
    print("=" * 78)
    print("MID-SESSION PROTOCOL")
    print("=" * 78)
    print(f"Repo Root: {repo}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if log_path:
        print(f"Latest Log: {log_path.relative_to(repo)}")
    else:
        print("Latest Log: (none found)")
    print("-" * 78)

    scene_id = state.get("current_scene_id") or state.get("scene_id") or "UNKNOWN"
    location = state.get("current_location") or state.get("starting_location") or "UNKNOWN"
    objective = state.get("current_objective") or state.get("session_objective") or "(not set)"
    active_hold = state.get("active_hold") or "—"

    print(f"Scene ID: {scene_id}")
    print(f"Location: {location}")
    print(f"Active Hold: {active_hold}")
    print(f"Objective: {objective}")

    # PC summary
    pc_name = pc.get("name") or pc.get("character_name") or (pc_path.stem if pc_path else "PC")
    fp = pc.get("fate_points", pc.get("fp", ""))
    refresh = pc.get("refresh", "")
    print("-" * 78)
    print(f"PC: {pc_name}  |  Refresh: {refresh}  |  Fate Points: {fp}")
    print("Effective Skills (quick): " + ", ".join(
        [f"{k}={v}" for k, v in sorted(eff.get("effective", {}).items()) if k in ("Fight", "Athletics", "Stealth", "Rapport", "Will", "Lore", "Notice")]
    ))

    # PC aspects + compel hooks (GM aid)
    aspects = pc.get("aspects", {})
    if isinstance(aspects, dict):
        print("-" * 78)
        print("PC Aspects:")
        hc = aspects.get("high_concept")
        tr = aspects.get("trouble")
        if hc:
            print(f" - High Concept: {hc}")
        if tr:
            print(f" - Trouble: {tr}")

        oa = aspects.get("other_aspects", [])
        if isinstance(oa, list) and oa:
            for a in oa[:6]:
                if isinstance(a, str):
                    print(f" - Aspect: {a}")

        lib = aspects.get("compel_library", {})
        if isinstance(lib, dict):
            ideas = lib.get("ideas", [])
            if isinstance(ideas, list) and ideas:
                print("-" * 78)
                print("PC Compel Hooks (Trouble):")
                for i, idea in enumerate(ideas[:5], start=1):
                    title = idea.get("title") or idea.get("id") or "Compel"
                    when = idea.get("when", "").strip()
                    line = f" {i}) {title}"
                    if when:
                        line += f" — {when}"
                    print(line)

                ex = lib.get("exceptions", [])
                if isinstance(ex, list) and ex:
                    print(" Exceptions:")
                    for e in ex[:3]:
                        if isinstance(e, dict):
                            print(f"  - {e.get('tag','exception')}: {e.get('description','')}")

    # Trust dynamics
    rels = summarize_relationships(state)
    if rels:
        print("-" * 78)
        print("Faction/Trust Snapshot:")
        for k, v in rels:
            print(f" - {k}: {v}")

    # Top clocks
    print("-" * 78)
    print("Top Clocks (by urgency):")
    for c in clocks[:3]:
        print(f" - {c.name}: {c.current}/{c.maximum} ({int(c.ratio*100)}%)  [{c.source}]")

    # Dragonbreak heuristic
    print("-" * 78)
    print(dragonbreak_heuristic(clocks, state))

    # Authenticity tri-check
    print("-" * 78)
    print("Authenticity Tri-Check:")
    for line in authenticity_tri_check(repo, state, pc):
        print(f" - {line}")

    # Options 1-5
    print("-" * 78)
    print("PLAYER OPTIONS (1–5):")
    for opt in build_options(state, pc, eff):
        print(f" {opt}")

    # Optional checkpoint append
    if args.checkpoint:
        if not log_path:
            # Create a new log if none exists
            logs_dir = repo / "logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            new_name = f"{datetime.now().strftime('%Y-%m-%d')}_mid-session.md"
            log_path = logs_dir / new_name

        checkpoint_append(log_path, args.checkpoint)
        print("-" * 78)
        print(f"[OK] Checkpoint appended to: {log_path.relative_to(repo)}")

    print("=" * 78)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
