#!/usr/bin/env python3
"""
Tests for Silver Hand HQ module — escalation system and dungeon unlock.

Covers:
- trigger_silver_hand_escalation() unlocks Frostmere Vigil at awareness >= 6.
- trigger_silver_hand_escalation() does not re-unlock if already discovered.
- increment_silver_hand_awareness() caps at 6 and unlocks hunter tiers.
- get_silver_hand_state() initialises default state when absent.
- record_silver_hand_outcome() applies correct state changes for each outcome.
- NPC stat sheet JSON files are valid and contain required fields.
- Dungeon JSON is valid and contains required zones and boss references.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

from story_manager import StoryManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_minimal_state(tmpdir: Path, silver_hand_state: dict | None = None) -> Path:
    """Write a minimal campaign_state.json into tmpdir/state and return its path."""
    state = {
        "campaign_id": "test_silver_hand",
        "current_act": 2,
        "civil_war_state": {
            "player_alliance": "neutral",
            "battle_of_whiterun_status": "active",
            "imperial_victories": 0,
            "stormcloak_victories": 0,
            "key_battles_completed": [],
            "faction_relationship": {"imperial_legion": 0, "stormcloaks": 0},
        },
        "main_quest_state": {},
        "thalmor_arc": {},
        "branching_decisions": {},
        "world_consequences": {"major_choices": []},
        "active_story_arcs": [],
        "companions": {
            "active_companions": [],
            "available_companions": [],
            "dismissed_companions": [],
        },
        "college_state": {
            "active_quest": None,
            "completed_quests": [],
            "quest_progress": {},
            "eye_instability": 0,
            "ancano_suspicion": 0,
            "internal_politics": 0,
        },
    }
    if silver_hand_state is not None:
        state["silver_hand_state"] = silver_hand_state

    state_dir = tmpdir / "state"
    state_dir.mkdir(exist_ok=True)
    state_path = state_dir / "campaign_state.json"
    state_path.write_text(json.dumps(state, indent=2))
    return state_path


def _make_story_manager(tmpdir: Path, silver_hand_state: dict | None = None) -> StoryManager:
    """Create a StoryManager pointing at real data but a temp state dir."""
    _make_minimal_state(tmpdir, silver_hand_state)
    return StoryManager(
        data_dir=str(_REPO_ROOT / "data"),
        state_dir=str(tmpdir / "state"),
    )


# ---------------------------------------------------------------------------
# Tests — escalation logic
# ---------------------------------------------------------------------------

class TestSilverHandEscalation:
    """Tests for trigger_silver_hand_escalation and related helpers."""

    def test_get_silver_hand_state_initialises_defaults(self):
        """get_silver_hand_state() should create default state when absent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            state = {}
            sh = sm.get_silver_hand_state(state)

        assert sh["awareness_level"] == 0
        assert sh["hq_discovered"] is False
        assert sh["high_purifier_alive"] is True
        assert "frostmere_vigil" in sh["active_cells"]
        assert sh["hunter_tiers_unlocked"] == []
        print("  ✓ get_silver_hand_state initialises defaults when absent")

    def test_trigger_escalation_below_threshold_does_not_unlock(self):
        """trigger_silver_hand_escalation() should not unlock HQ below level 6."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            state = {}
            sh = sm.get_silver_hand_state(state)
            sh["awareness_level"] = 5

            _, unlocked = sm.trigger_silver_hand_escalation(state=state, save=False)

        assert unlocked is False
        assert state["silver_hand_state"]["hq_discovered"] is False
        print("  ✓ escalation below threshold does not unlock HQ")

    def test_trigger_escalation_at_threshold_unlocks_hq(self):
        """trigger_silver_hand_escalation() should unlock HQ when awareness >= 6."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            state = {}
            sh = sm.get_silver_hand_state(state)
            sh["awareness_level"] = 6

            _, unlocked = sm.trigger_silver_hand_escalation(state=state, save=False)

        assert unlocked is True
        assert state["silver_hand_state"]["hq_discovered"] is True
        print("  ✓ escalation at level 6 unlocks Frostmere Vigil HQ")

    def test_trigger_escalation_does_not_re_unlock(self):
        """trigger_silver_hand_escalation() should not re-unlock an already-discovered HQ."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            state = {}
            sh = sm.get_silver_hand_state(state)
            sh["awareness_level"] = 6
            sh["hq_discovered"] = True  # Already discovered

            _, unlocked = sm.trigger_silver_hand_escalation(state=state, save=False)

        assert unlocked is False
        print("  ✓ escalation does not re-unlock already-discovered HQ")

    def test_increment_awareness_caps_at_six(self):
        """increment_silver_hand_awareness() should not exceed 6."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            state = {}
            sh = sm.get_silver_hand_state(state)
            sh["awareness_level"] = 5

            sm.increment_silver_hand_awareness(amount=5, state=state, save=False)

        assert state["silver_hand_state"]["awareness_level"] == 6
        print("  ✓ increment_silver_hand_awareness caps at 6")

    def test_increment_awareness_unlocks_hunter_tiers(self):
        """increment_silver_hand_awareness() should unlock tiers progressively."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            state = {}
            sm.get_silver_hand_state(state)  # initialise

            sm.increment_silver_hand_awareness(amount=1, state=state, save=False)
            assert "scout" in state["silver_hand_state"]["hunter_tiers_unlocked"]

            sm.increment_silver_hand_awareness(amount=1, state=state, save=False)
            assert "wolf_hunters" in state["silver_hand_state"]["hunter_tiers_unlocked"]

            sm.increment_silver_hand_awareness(amount=1, state=state, save=False)
            assert "purifier_squad" in state["silver_hand_state"]["hunter_tiers_unlocked"]

            sm.increment_silver_hand_awareness(amount=1, state=state, save=False)
            assert "high_purifiers_chosen" in state["silver_hand_state"]["hunter_tiers_unlocked"]

        print("  ✓ hunter tiers unlock progressively with awareness increments")

    def test_increment_does_not_duplicate_tiers(self):
        """increment_silver_hand_awareness() should not add duplicate tier entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            state = {}
            sm.get_silver_hand_state(state)

            for _ in range(5):
                sm.increment_silver_hand_awareness(amount=1, state=state, save=False)

        tiers = state["silver_hand_state"]["hunter_tiers_unlocked"]
        assert len(tiers) == len(set(tiers)), "Duplicate tiers found"
        print("  ✓ no duplicate hunter tier entries")


class TestSilverHandOutcomes:
    """Tests for record_silver_hand_outcome()."""

    def _run_outcome(self, outcome_key, initial_level=6):
        """Helper: create state, set awareness, run outcome, return sh dict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            state = {}
            sh = sm.get_silver_hand_state(state)
            sh["awareness_level"] = initial_level
            sh["hq_discovered"] = True

            sm.record_silver_hand_outcome(outcome_key, state=state, save=False)
            return state["silver_hand_state"]

    def test_all_leaders_killed_marks_purifier_dead(self):
        sh = self._run_outcome("all_leaders_killed")
        assert sh["high_purifier_alive"] is False
        assert sh["awareness_level"] == 3  # 6 - 3
        assert "gallows_rock" in sh["active_cells"]
        print("  ✓ all_leaders_killed outcome marks purifier dead and fragments cells")

    def test_valdrek_alive_preserves_hq_discovered(self):
        sh = self._run_outcome("valdrek_alive")
        assert sh["hq_discovered"] is True
        assert sh["high_purifier_alive"] is True
        print("  ✓ valdrek_alive outcome preserves hq_discovered")

    def test_both_leaders_spared_reduces_awareness(self):
        sh = self._run_outcome("both_leaders_spared")
        assert sh["hq_discovered"] is True
        assert sh["awareness_level"] == 4  # 6 - 2
        print("  ✓ both_leaders_spared outcome reduces awareness by 2")

    def test_kaari_takes_command_clears_purifier(self):
        sh = self._run_outcome("kaari_takes_command")
        assert sh["high_purifier_alive"] is False
        print("  ✓ kaari_takes_command marks high_purifier_alive as False")


# ---------------------------------------------------------------------------
# Tests — static data validation
# ---------------------------------------------------------------------------

class TestSilverHandDataFiles:
    """Validate that all required Silver Hand JSON data files are well-formed."""

    _DATA_DIR = _REPO_ROOT / "data"

    def _load_json(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_high_purifier_valdrek_npc_sheet(self):
        """Valdrek stat sheet should have required fields and correct id."""
        path = self._DATA_DIR / "npc_stat_sheets" / "npc_stat_high_purifier_valdrek.json"
        assert path.exists(), f"Missing NPC sheet: {path}"
        data = self._load_json(path)

        assert data.get("id") == "npc_stat_high_purifier_valdrek"
        assert data.get("category") == "Hostile NPC"
        assert "aspects" in data
        assert "skills" in data
        assert "stunts" in data
        assert data["aspects"].get("high_concept"), "Missing high_concept aspect"
        print("  ✓ Valdrek NPC stat sheet is valid")

    def test_sister_kaari_npc_sheet(self):
        """Sister Kaari stat sheet should have required fields and correct id."""
        path = self._DATA_DIR / "npc_stat_sheets" / "npc_stat_sister_kaari.json"
        assert path.exists(), f"Missing NPC sheet: {path}"
        data = self._load_json(path)

        assert data.get("id") == "npc_stat_sister_kaari"
        assert data.get("category") == "Hostile NPC"
        assert "aspects" in data
        assert "skills" in data
        assert "stunts" in data
        assert "boss_mechanics" in data
        print("  ✓ Sister Kaari NPC stat sheet is valid")

    def test_torhild_wolf_bane_npc_sheet(self):
        """Torhild stat sheet should have required fields and correct id."""
        path = self._DATA_DIR / "npc_stat_sheets" / "npc_stat_torhild_wolf_bane.json"
        assert path.exists(), f"Missing NPC sheet: {path}"
        data = self._load_json(path)

        assert data.get("id") == "npc_stat_torhild_wolf_bane"
        assert data.get("category") == "Hostile NPC"
        assert "aspects" in data
        assert "skills" in data
        assert "stunts" in data
        assert "spared_branch" in data, "Missing spared_branch for no-dead-end requirement"
        print("  ✓ Torhild Wolf-Bane NPC stat sheet is valid")

    def test_dungeon_json_structure(self):
        """Frostmere Vigil dungeon JSON should have 5 zones and required boss refs."""
        path = self._DATA_DIR / "dungeons" / "silver_hand_frostmere_vigil.json"
        assert path.exists(), f"Missing dungeon file: {path}"
        data = self._load_json(path)

        assert data.get("id") == "silver_hand_frostmere_vigil"
        assert "unlock_condition" in data
        zones = data.get("zones", [])
        assert len(zones) == 5, f"Expected 5 zones, got {len(zones)}"

        zone_ids = {z["id"] for z in zones}
        assert "courtyard" in zone_ids
        assert "chapel" in zone_ids
        assert "ritual_chamber" in zone_ids

        boss_refs = {z.get("boss") for z in zones if z.get("boss")}
        assert "npc_stat_sister_kaari" in boss_refs
        assert "npc_stat_high_purifier_valdrek" in boss_refs
        assert "npc_stat_torhild_wolf_bane" in boss_refs
        print("  ✓ Frostmere Vigil dungeon JSON is valid (5 zones, all bosses referenced)")

    def test_silver_hand_clocks_json(self):
        """Silver Hand clocks JSON should be well-formed with awareness clock."""
        path = self._DATA_DIR / "clocks" / "silver_hand_clocks.json"
        assert path.exists(), f"Missing clocks file: {path}"
        data = self._load_json(path)

        clocks = data.get("silver_hand_clocks", {}).get("clocks", {})
        assert "silver_hand_awareness" in clocks
        awareness = clocks["silver_hand_awareness"]
        assert awareness.get("total_segments") == 6
        print("  ✓ Silver Hand clocks JSON is valid")

    def test_campaign_state_has_silver_hand_state(self):
        """campaign_state.json should contain silver_hand_state block."""
        path = _REPO_ROOT / "state" / "campaign_state.json"
        assert path.exists(), f"Missing campaign state: {path}"
        data = self._load_json(path)

        sh = data.get("silver_hand_state")
        assert sh is not None, "silver_hand_state not found in campaign_state.json"
        assert "awareness_level" in sh
        assert "hq_discovered" in sh
        assert "high_purifier_alive" in sh
        assert "active_cells" in sh
        assert "hunter_tiers_unlocked" in sh
        print("  ✓ campaign_state.json contains silver_hand_state block")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all_tests():
    print("=" * 60)
    print("SILVER HAND HQ MODULE — TEST SUITE")
    print("=" * 60)

    test_classes = [
        TestSilverHandEscalation,
        TestSilverHandOutcomes,
        TestSilverHandDataFiles,
    ]
    passed = 0
    failed = 0

    for cls in test_classes:
        instance = cls()
        methods = [m for m in dir(instance) if m.startswith("test_")]
        print(f"\n[{cls.__name__}]")
        for method_name in methods:
            try:
                getattr(instance, method_name)()
                passed += 1
            except AssertionError as e:
                print(f"  ✗ {method_name} FAILED: {e}")
                failed += 1
            except Exception as e:
                import traceback
                print(f"  ✗ {method_name} ERROR: {e}")
                traceback.print_exc()
                failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
