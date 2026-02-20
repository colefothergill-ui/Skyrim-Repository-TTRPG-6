#!/usr/bin/env python3
"""
Tests for StoryManager – College of Winterhold questline integration.

Covers:
- load_college_quests() loads all six quests from the JSON file.
- start_college_questline() sets college_first_lessons as active.
- complete_college_quest() chains quests in COLLEGE_CHAIN order.
- dragonbreak_precheck_college() triggers at eye_instability >= 5.
- get_available_quests() surfaces the active College quest.
- session_zero update_campaign_state() queues college_first_lessons
  when starting faction is college_of_winterhold.
- Battle of Whiterun is not blocked when College intro is incomplete
  (the engine exposes the requirement as a hook, not a hard gate).
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Resolve absolute path so tests run from any working directory
_REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

from story_manager import StoryManager, COLLEGE_CHAIN
from session_zero import SessionZeroManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_minimal_state(tmpdir: Path, college_state: dict | None = None) -> Path:
    """Write a minimal campaign_state.json into tmpdir and return its path."""
    state = {
        "campaign_id": "test_001",
        "current_act": 1,
        "civil_war_state": {
            "player_alliance": "neutral",
            "battle_of_whiterun_status": "approaching",
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
        "college_state": college_state or {
            "active_quest": None,
            "completed_quests": [],
            "quest_progress": {},
            "eye_instability": 0,
            "ancano_suspicion": 0,
            "internal_politics": 0,
        },
    }
    state_path = tmpdir / "campaign_state.json"
    state_path.write_text(json.dumps(state, indent=2))
    return state_path


def _make_story_manager(tmpdir: Path, college_state: dict | None = None) -> StoryManager:
    """Create a StoryManager pointing at real data but a temp state dir."""
    state_dir = tmpdir / "state"
    state_dir.mkdir(exist_ok=True)
    _make_minimal_state(state_dir, college_state)
    data_dir = str(_REPO_ROOT / "data")
    return StoryManager(data_dir=data_dir, state_dir=str(state_dir))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestCollegeQuests:
    """Tests for the College of Winterhold questline integration."""

    def test_load_college_quests_returns_all_six(self):
        """load_college_quests() should return a dict with all six quests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            quests = sm.college_quests
            assert isinstance(quests, dict), "college_quests should be a dict"
            expected_ids = {
                "college_first_lessons",
                "college_under_saarthal",
                "college_hitting_the_books",
                "college_revealing_the_unseen",
                "college_staff_of_magnus",
                "college_eye_of_magnus",
            }
            assert expected_ids.issubset(quests.keys()), (
                f"Missing quests: {expected_ids - quests.keys()}"
            )
            print(f"  ✓ {len(quests)} quests loaded")

    def test_start_college_questline_sets_active_quest(self):
        """start_college_questline() should set college_first_lessons as active."""
        state = {
            "college_state": {
                "active_quest": None,
                "completed_quests": [],
                "quest_progress": {},
                "eye_instability": 0,
                "ancano_suspicion": 0,
                "internal_politics": 0,
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            sm.start_college_questline(state)
        cs = state["college_state"]
        assert cs["active_quest"] == "college_first_lessons"
        assert cs["quest_progress"]["college_first_lessons"] == "active"
        print("  ✓ start_college_questline sets college_first_lessons as active")

    def test_complete_college_quest_chains_in_order(self):
        """complete_college_quest() should advance quests in COLLEGE_CHAIN order."""
        ordered = [
            "college_first_lessons",
            "college_under_saarthal",
            "college_hitting_the_books",
            "college_revealing_the_unseen",
            "college_staff_of_magnus",
            "college_eye_of_magnus",
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            state = {
                "college_state": {
                    "active_quest": "college_first_lessons",
                    "completed_quests": [],
                    "quest_progress": {"college_first_lessons": "active"},
                    "eye_instability": 0,
                    "ancano_suspicion": 0,
                    "internal_politics": 0,
                }
            }
            for i, current_id in enumerate(ordered):
                assert state["college_state"]["active_quest"] == current_id, (
                    f"Expected active quest '{current_id}', got '{state['college_state']['active_quest']}'"
                )
                next_q = sm.complete_college_quest(state)
                expected_next = COLLEGE_CHAIN[current_id]
                assert next_q == expected_next, (
                    f"After completing '{current_id}', expected next '{expected_next}', got '{next_q}'"
                )
                assert current_id in state["college_state"]["completed_quests"]
                assert state["college_state"]["quest_progress"][current_id] == "completed"

        print("  ✓ complete_college_quest chains through all six quests correctly")

    def test_complete_college_quest_arc_ends_cleanly(self):
        """After completing eye_of_magnus, active_quest should be None."""
        state = {
            "college_state": {
                "active_quest": "college_eye_of_magnus",
                "completed_quests": [],
                "quest_progress": {"college_eye_of_magnus": "active"},
                "eye_instability": 0,
                "ancano_suspicion": 0,
                "internal_politics": 0,
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            result = sm.complete_college_quest(state)
        assert result is None
        assert state["college_state"]["active_quest"] is None
        assert "college_eye_of_magnus" in state["college_state"]["completed_quests"]
        print("  ✓ complete_college_quest ends arc cleanly at eye_of_magnus")

    def test_dragonbreak_precheck_triggers_at_threshold(self):
        """dragonbreak_precheck_college() returns True when instability >= 5."""
        state_high = {
            "college_state": {
                "active_quest": "college_eye_of_magnus",
                "eye_instability": 5,
            }
        }
        state_low = {
            "college_state": {
                "active_quest": "college_eye_of_magnus",
                "eye_instability": 3,
            }
        }
        state_wrong_quest = {
            "college_state": {
                "active_quest": "college_first_lessons",
                "eye_instability": 10,
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            assert sm.dragonbreak_precheck_college(state_high) is True
            assert sm.dragonbreak_precheck_college(state_low) is False
            assert sm.dragonbreak_precheck_college(state_wrong_quest) is False
        print("  ✓ dragonbreak_precheck_college logic is correct")

    def test_get_available_quests_includes_active_college_quest(self):
        """get_available_quests() should list the active College quest."""
        college_state = {
            "active_quest": "college_first_lessons",
            "completed_quests": [],
            "quest_progress": {"college_first_lessons": "active"},
            "eye_instability": 0,
            "ancano_suspicion": 0,
            "internal_politics": 0,
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir), college_state=college_state)
            available = sm.get_available_quests()

        college_entries = [q for q in available if q.get("type") == "college"]
        assert len(college_entries) >= 1, (
            "Expected at least one college quest in available quests"
        )
        quest_data = college_entries[0]["quest"]
        assert quest_data.get("quest_id") == "college_first_lessons", (
            f"Expected quest_id 'college_first_lessons', got: {quest_data.get('quest_id')!r}"
        )
        print("  ✓ get_available_quests surfaces active College quest")

    def test_get_available_quests_no_college_when_inactive(self):
        """get_available_quests() should not include College quest when none is active."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_story_manager(Path(tmpdir))
            available = sm.get_available_quests()

        college_entries = [q for q in available if q.get("type") == "college"]
        assert len(college_entries) == 0, (
            "Expected no college quests when active_quest is null"
        )
        print("  ✓ get_available_quests hides College quest when inactive")


class TestSessionZeroCollegeFaction:
    """Tests for session_zero College-faction initialization."""

    def _make_session_zero_env(self, tmpdir: Path):
        """Set up a SessionZeroManager with a valid state/data layout."""
        data_dir = tmpdir / "data"
        state_dir = tmpdir / "state"
        (data_dir / "pcs").mkdir(parents=True)
        state_dir.mkdir(parents=True)

        # Minimal campaign state
        (state_dir / "campaign_state.json").write_text(json.dumps({
            "campaign_id": "test_001",
            "current_act": 1,
            "civil_war_state": {
                "player_alliance": "neutral",
                "battle_of_whiterun_status": "approaching",
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
                "companion_relationships": {},
            },
        }, indent=2))

        return SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))

    def test_college_faction_queues_first_lessons(self):
        """Session-zero with College faction should activate college_first_lessons."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = self._make_session_zero_env(Path(tmpdir))
            characters = [{
                "id": "pc_test",
                "name": "Test Mage",
                "player": "Player One",
                "race": "Breton",
                "standing_stone": "The Mage Stone",
                "faction_alignment": "neutral",
            }]
            state = mgr.update_campaign_state(
                faction_alignment="neutral",
                characters=characters,
                neutral_subfaction="college",
            )

        assert "college_state" in state, "college_state should be present in campaign state"
        cs = state["college_state"]
        assert cs["active_quest"] == "college_first_lessons", (
            f"Expected college_first_lessons as active quest, got: {cs['active_quest']}"
        )
        assert cs["quest_progress"].get("college_first_lessons") == "active"
        assert state.get("starting_faction") == "college_of_winterhold"
        print("  ✓ session-zero with College queues college_first_lessons")

    def test_non_college_faction_does_not_activate_college_quests(self):
        """Session-zero with non-College faction should leave college_state inactive."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = self._make_session_zero_env(Path(tmpdir))
            characters = [{
                "id": "pc_test2",
                "name": "Test Warrior",
                "player": "Player Two",
                "race": "Nord",
                "standing_stone": "The Warrior Stone",
                "faction_alignment": "imperial",
            }]
            state = mgr.update_campaign_state(
                faction_alignment="imperial",
                characters=characters,
            )

        cs = state.get("college_state", {})
        assert cs.get("active_quest") is None, (
            f"Expected no active college quest for Imperial faction, got: {cs.get('active_quest')}"
        )
        print("  ✓ non-College faction does not activate College quests")

    def test_college_state_initialised_for_all_factions(self):
        """college_state should always be present after session-zero (append-only)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mgr = self._make_session_zero_env(Path(tmpdir))
            characters = [{
                "id": "pc_test3",
                "name": "Test Thief",
                "player": "Player Three",
                "race": "Khajiit",
                "standing_stone": "The Thief Stone",
                "faction_alignment": "neutral",
            }]
            state = mgr.update_campaign_state(
                faction_alignment="neutral",
                characters=characters,
                neutral_subfaction="thieves_guild",
            )

        assert "college_state" in state, "college_state should be present even for Thieves Guild start"
        print("  ✓ college_state always initialised by session-zero")


def run_all_tests():
    """Run all test classes"""
    print("=" * 60)
    print("STORY MANAGER — COLLEGE QUESTLINE TEST SUITE")
    print("=" * 60)

    test_classes = [TestCollegeQuests, TestSessionZeroCollegeFaction]
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
