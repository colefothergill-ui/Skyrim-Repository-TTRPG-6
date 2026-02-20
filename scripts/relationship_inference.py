#!/usr/bin/env python3
"""
Relationship Inference Helper

Provides a conservative backstory-to-favor inference system for NPC relationships.
Checks player character backstory keywords against NPC-specific resonance patterns
to infer a starting favor bonus without overriding existing relationship data.

Supported NPCs include Ulfric Stormcloak kinship/familiarity inference.
"""

import json
import os
from pathlib import Path


# ---------------------------------------------------------------------------
# NPC inference rules
# Each entry maps npc_id -> list of rule dicts.
# A rule has:
#   "flag"        - string flag name written into the state
#   "keywords"    - list of keyword strings (any match = hit)
#   "bonus_text"  - human-readable bonus description
#   "bonus_value" - numeric bonus (positive integer)
# ---------------------------------------------------------------------------
_INFERENCE_RULES = {
    "npc_stat_ulfric_stormcloak": [
        {
            "flag": "ulfric_stormcloak_kinship",
            "keywords": ["Ulfric", "Stormcloak", "Windhelm", "Eastmarch", "Talos", "rebellion"],
            "bonus_text": "+1 to first social roll with Ulfric (kinship/familiarity)",
            "bonus_value": 1,
        },
        {
            "flag": "ulfric_stormcloak_war_veteran",
            "keywords": ["Great War", "Thalmor", "prisoner", "Helgen", "Markarth"],
            "bonus_text": "+1 to first Will or Provoke roll in Ulfric's presence (shared veteran experience)",
            "bonus_value": 1,
        },
    ],
    "npc_stat_jarl_balgruuf": [
        {
            "flag": "balgruuf_whiterun_familiar",
            "keywords": ["Balgruuf", "Whiterun", "Kodlak", "Jorrvaskr", "Companions", "Dragonsreach"],
            "bonus_text": "+1 to first rapport or empathy roll with Balgruuf (local familiarity)",
            "bonus_value": 1,
        },
    ],
    "npc_stat_hadvar": [
        {
            "flag": "hadvar_helgen_bond",
            "keywords": ["Hadvar", "Helgen", "Legion", "Imperial", "Riverwood", "Alvor"],
            "bonus_text": "+1 to first teamwork roll with Hadvar (Helgen bond / shared Imperial history)",
            "bonus_value": 1,
        },
    ],
    "npc_stat_ralof": [
        {
            "flag": "ralof_stormcloak_bond",
            "keywords": ["Ralof", "Helgen", "Stormcloak", "Riverwood", "Gerdur", "Nord"],
            "bonus_text": "+1 to first teamwork roll with Ralof (Helgen bond / shared Stormcloak history)",
            "bonus_value": 1,
        },
    ],
    "npc_stat_galmar_stonefist": [
        {
            "flag": "galmar_warrior_respect",
            "keywords": ["Stormcloak", "Nord", "Windhelm", "Ulfric", "rebellion", "warrior"],
            "bonus_text": "+1 to first Fight or Provoke roll in Galmar's presence (warrior recognition)",
            "bonus_value": 1,
        },
    ],
    "npc_stat_legate_rikke": [
        {
            "flag": "rikke_imperial_bond",
            "keywords": ["Imperial", "Legion", "Tullius", "Solitude", "Great War", "Talos"],
            "bonus_text": "+1 to first Rapport or Empathy roll with Rikke (shared Imperial/Nord heritage)",
            "bonus_value": 1,
        },
    ],
}


def _extract_backstory_text(pc_data):
    """
    Extract all backstory-relevant text from a PC data dict as a single lowercase string.

    Searches common backstory fields: background, backstory, history,
    aspects (all), notes, and character_concept.
    """
    fragments = []

    for field in ("background", "backstory", "history", "notes", "character_concept"):
        val = pc_data.get(field)
        if isinstance(val, str):
            fragments.append(val)
        elif isinstance(val, list):
            fragments.extend(str(item) for item in val)

    # Aspects
    aspects = pc_data.get("aspects", {})
    if isinstance(aspects, dict):
        for v in aspects.values():
            if isinstance(v, str):
                fragments.append(v)
            elif isinstance(v, list):
                fragments.extend(str(x) for x in v)
            elif isinstance(v, dict):
                # compel_library or nested structures
                for inner_v in v.values():
                    if isinstance(inner_v, str):
                        fragments.append(inner_v)
                    elif isinstance(inner_v, list):
                        fragments.extend(str(x) for x in inner_v)

    return " ".join(fragments).lower()


def infer_for_npc(pc_data, npc_id):
    """
    Infer backstory-based favor bonuses for a single NPC.

    Args:
        pc_data (dict): Parsed PC JSON data.
        npc_id  (str):  NPC identifier (e.g. 'npc_stat_ulfric_stormcloak').

    Returns:
        List of dicts, each with keys:
            'flag'        - string identifier for the inferred bonus
            'bonus_text'  - human-readable description
            'bonus_value' - numeric bonus value
        Returns empty list if no inference rules match.
    """
    rules = _INFERENCE_RULES.get(npc_id, [])
    if not rules:
        return []

    backstory = _extract_backstory_text(pc_data)
    triggered = []

    for rule in rules:
        if any(kw.lower() in backstory for kw in rule["keywords"]):
            triggered.append({
                "flag": rule["flag"],
                "bonus_text": rule["bonus_text"],
                "bonus_value": rule["bonus_value"],
            })

    return triggered


def apply_inference_to_state(state_path, pc_path, npc_ids):
    """
    Apply relationship inference results to campaign state.

    Reads the PC file and state file, computes inferences for each requested
    NPC, and writes any new flags into state['relationship_inference'][pc_id]
    without overwriting already-set values (setdefault semantics).

    Args:
        state_path (str): Path to campaign_state.json.
        pc_path    (str): Path to the PC JSON file.
        npc_ids    (list[str]): List of NPC IDs to infer for.

    Returns:
        dict: Mapping of npc_id -> list of triggered inference results that
              were written to state (skips already-present flags).
    """
    state_path = Path(state_path)
    pc_path = Path(pc_path)

    if not state_path.exists():
        raise FileNotFoundError(f"State file not found: {state_path}")
    if not pc_path.exists():
        raise FileNotFoundError(f"PC file not found: {pc_path}")

    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    with open(pc_path, "r", encoding="utf-8") as f:
        pc_data = json.load(f)

    pc_id = pc_data.get("id") or pc_path.stem
    ri = state.setdefault("relationship_inference", {})
    pc_ri = ri.setdefault(pc_id, {})

    written = {}

    for npc_id in npc_ids:
        results = infer_for_npc(pc_data, npc_id)
        new_results = []
        for result in results:
            flag = result["flag"]
            if flag not in pc_ri:
                pc_ri[flag] = {
                    "npc_id": npc_id,
                    "bonus_text": result["bonus_text"],
                    "bonus_value": result["bonus_value"],
                    "consumed": False,
                }
                new_results.append(result)
        if new_results:
            written[npc_id] = new_results

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    return written


def get_bonus(state, pc_id, npc_id, flag):
    """
    Retrieve an unconsumed inference bonus from state.

    Args:
        state  (dict): Loaded campaign state dict.
        pc_id  (str):  PC identifier.
        npc_id (str):  NPC identifier (used for documentation; not filtered here).
        flag   (str):  The specific inference flag to retrieve.

    Returns:
        dict with keys 'bonus_value' and 'bonus_text' if the bonus exists and
        has not been consumed, otherwise None.
    """
    ri = state.get("relationship_inference", {})
    pc_ri = ri.get(pc_id, {})
    entry = pc_ri.get(flag)

    if entry and not entry.get("consumed", False):
        return {
            "bonus_value": entry["bonus_value"],
            "bonus_text": entry["bonus_text"],
        }

    return None


def consume_bonus(state, pc_id, flag):
    """
    Mark an inference bonus as consumed so it cannot be used again.

    Args:
        state (dict): Loaded campaign state dict (mutated in place).
        pc_id (str):  PC identifier.
        flag  (str):  The inference flag to consume.

    Returns:
        True if the bonus was found and marked consumed, False otherwise.
    """
    ri = state.get("relationship_inference", {})
    pc_ri = ri.get(pc_id, {})
    entry = pc_ri.get(flag)

    if entry and not entry.get("consumed", False):
        entry["consumed"] = True
        return True

    return False
