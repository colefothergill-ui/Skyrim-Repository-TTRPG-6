#!/usr/bin/env python3
"""
Tests for Silver Hand faction expansion.

Covers:
- data/factions/silver_hand.json is valid and has required fields.
- data/npc_stat_sheets/high_purifier_valdrek.json is valid (Hostile NPC).
- data/npc_stat_sheets/sister_kaari.json is valid (Hostile NPC).
- data/pcs/pc_template.json has beast_blood and sovngarde_blessing fields.
- data/quests/silver_hand_dynamic.json has all four Silver Hand quests.
- campaign_state.json has silver_hand_state and companions_state blocks.
- StoryManager.increment_silver_hand_awareness() increments awareness_level.
- StoryManager.trigger_silver_hand_event() returns correct events per level.
- trigger_silver_hand_event() returns None when beast blood is not active.
- StoryManager.check_silver_hand_quest_eligibility() gates quests correctly.
"""

import json
import sys
import tempfile
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

from story_manager import StoryManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_beastblooded_state(tmpdir: Path, awareness: int = 0) -> Path:
    """Write a minimal campaign_state.json with beast blood active."""
    state = {
        "campaign_id": "test_silver_hand",
        "current_act": 2,
        "civil_war_state": {
            "player_alliance": "neutral",
            "battle_of_whiterun_status": "approaching",
            "imperial_victories": 0,
            "stormcloak_victories": 0,
            "key_battles_completed": [],
            "faction_relationship": {"imperial_legion": 0, "stormcloaks": 0},
        },
        "main_quest_state": {},
        "thalmor_arc": {"active_plots": [], "thalmor_schemes_discovered": []},
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
        "companions_state": {
            "beast_blood": True,
            "beast_blood_tier": 1,
            "sovngarde_blessing_tier": 0,
            "companions_rank": "Companion",
            "kodlak_quest_complete": False,
            "harbinger": False,
        },
        "silver_hand_state": {
            "awareness_level": awareness,
            "active_hunts": [],
            "high_purifier_alive": True,
        },
    }
    state_path = tmpdir / "campaign_state.json"
    state_path.write_text(json.dumps(state, indent=2))
    return state_path


def _make_sm(tmpdir: Path, awareness: int = 0) -> StoryManager:
    state_dir = tmpdir / "state"
    state_dir.mkdir(exist_ok=True)
    _make_beastblooded_state(state_dir, awareness)
    return StoryManager(data_dir=str(_REPO_ROOT / "data"), state_dir=str(state_dir))


# ---------------------------------------------------------------------------
# Data file tests
# ---------------------------------------------------------------------------

class TestSilverHandFactionFile:
    """Validate data/factions/silver_hand.json structure."""

    def setup_method(self):
        path = _REPO_ROOT / "data" / "factions" / "silver_hand.json"
        with open(path) as f:
            self.data = json.load(f)

    def test_required_fields_present(self):
        for field in ("id", "name", "ideology", "public_face", "structure", "escalation_clock"):
            assert field in self.data, f"silver_hand.json missing field: {field}"

    def test_id_is_silver_hand(self):
        assert self.data["id"] == "silver_hand"

    def test_escalation_clock_structure(self):
        clock = self.data["escalation_clock"]
        assert clock["current"] == 0
        assert clock["max"] == 6

    def test_structure_fields(self):
        structure = self.data["structure"]
        assert "cells" in structure
        assert "leadership" in structure

    def test_internal_branches_present(self):
        branches = self.data.get("internal_branches", {})
        for branch in ("purists", "radicals", "shadow_patrons"):
            assert branch in branches, f"Missing branch: {branch}"


class TestHighPurifierValdrekNPCSheet:
    """Validate data/npc_stat_sheets/high_purifier_valdrek.json."""

    def setup_method(self):
        path = _REPO_ROOT / "data" / "npc_stat_sheets" / "high_purifier_valdrek.json"
        with open(path) as f:
            self.data = json.load(f)

    def test_required_fields(self):
        for field in ("name", "id", "category", "faction", "aspects", "skills", "stress"):
            assert field in self.data, f"high_purifier_valdrek.json missing: {field}"

    def test_category_is_hostile_npc(self):
        assert self.data["category"] == "Hostile NPC"

    def test_faction_is_silver_hand(self):
        assert "Silver Hand" in self.data["faction"]

    def test_aspects_structure(self):
        aspects = self.data["aspects"]
        assert "high_concept" in aspects
        assert "trouble" in aspects


class TestSisterKaariNPCSheet:
    """Validate data/npc_stat_sheets/sister_kaari.json."""

    def setup_method(self):
        path = _REPO_ROOT / "data" / "npc_stat_sheets" / "sister_kaari.json"
        with open(path) as f:
            self.data = json.load(f)

    def test_required_fields(self):
        for field in ("name", "id", "category", "faction", "aspects", "skills", "stress"):
            assert field in self.data, f"sister_kaari.json missing: {field}"

    def test_category_is_hostile_npc(self):
        assert self.data["category"] == "Hostile NPC"

    def test_trust_clock_enabled(self):
        trust = self.data.get("trust_clock", {})
        assert trust.get("enabled") is True
        assert "description" in trust


class TestPCTemplateFile:
    """Validate data/pcs/pc_template.json has beast_blood and sovngarde_blessing."""

    def setup_method(self):
        path = _REPO_ROOT / "data" / "pcs" / "pc_template.json"
        with open(path) as f:
            self.data = json.load(f)

    def test_companions_progression_present(self):
        assert "companions_progression" in self.data, "pc_template.json missing companions_progression"

    def test_beast_blood_field(self):
        prog = self.data["companions_progression"]
        assert "beast_blood" in prog
        bb = prog["beast_blood"]
        assert bb["tier"] == 0
        assert bb["max_tier"] == 3

    def test_sovngarde_blessing_field(self):
        prog = self.data["companions_progression"]
        assert "sovngarde_blessing" in prog
        sb = prog["sovngarde_blessing"]
        assert sb["tier"] == 0
        assert sb["max_tier"] == 3


class TestSilverHandQuestFile:
    """Validate data/quests/silver_hand_dynamic.json."""

    def setup_method(self):
        path = _REPO_ROOT / "data" / "quests" / "silver_hand_dynamic.json"
        with open(path) as f:
            self.data = json.load(f)

    def test_all_four_quests_present(self):
        expected = {
            "silver_hand_hunt_the_beast",
            "silver_hand_siege_of_jorrvaskr",
            "silver_hand_purification_ritual",
            "silver_hand_high_purifier_showdown",
        }
        assert expected.issubset(set(self.data.keys())), \
            f"Missing quests: {expected - set(self.data.keys())}"

    def test_each_quest_has_required_fields(self):
        for quest_id, quest in self.data.items():
            for field in ("id", "name", "description", "faction", "activation_conditions"):
                assert field in quest, f"{quest_id} missing field: {field}"

    def test_faction_is_silver_hand(self):
        for quest_id, quest in self.data.items():
            assert quest["faction"] == "silver_hand", \
                f"{quest_id} has wrong faction: {quest['faction']}"


class TestCampaignStateBlocks:
    """Validate that campaign_state.json has silver_hand_state and companions_state."""

    def setup_method(self):
        path = _REPO_ROOT / "state" / "campaign_state.json"
        with open(path) as f:
            self.state = json.load(f)

    def test_silver_hand_state_present(self):
        assert "silver_hand_state" in self.state

    def test_silver_hand_state_fields(self):
        sh = self.state["silver_hand_state"]
        assert "awareness_level" in sh
        assert "active_hunts" in sh
        assert "high_purifier_alive" in sh
        assert sh["awareness_level"] == 0
        assert sh["high_purifier_alive"] is True

    def test_companions_state_present(self):
        assert "companions_state" in self.state

    def test_companions_state_beast_blood(self):
        cs = self.state["companions_state"]
        assert "beast_blood" in cs
        assert "beast_blood_tier" in cs
        assert "sovngarde_blessing_tier" in cs


# ---------------------------------------------------------------------------
# StoryManager Silver Hand logic tests
# ---------------------------------------------------------------------------

class TestIncrementSilverHandAwareness:
    """Tests for StoryManager.increment_silver_hand_awareness()."""

    def test_increments_by_one_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=0)
            state = sm.load_campaign_state()
            updated = sm.increment_silver_hand_awareness(state=state, amount=1)
            assert updated["silver_hand_state"]["awareness_level"] == 1

    def test_caps_at_six(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=5)
            state = sm.load_campaign_state()
            updated = sm.increment_silver_hand_awareness(state=state, amount=3)
            assert updated["silver_hand_state"]["awareness_level"] == 6

    def test_persists_to_disk(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=2)
            state = sm.load_campaign_state()
            sm.increment_silver_hand_awareness(state=state, amount=1)
            reloaded = sm.load_campaign_state()
            assert reloaded["silver_hand_state"]["awareness_level"] == 3

    def test_initializes_missing_silver_hand_state(self):
        """Incrementing on state that lacks silver_hand_state should create it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = tmpdir
            state = {
                "campaign_id": "bare",
                "companions_state": {"beast_blood": True},
            }
            (Path(state_dir) / "campaign_state.json").write_text(json.dumps(state))
            sm = StoryManager(
                data_dir=str(_REPO_ROOT / "data"),
                state_dir=state_dir,
            )
            updated = sm.increment_silver_hand_awareness(amount=1)
            assert updated["silver_hand_state"]["awareness_level"] == 1


class TestTriggerSilverHandEvent:
    """Tests for StoryManager.trigger_silver_hand_event()."""

    def test_returns_none_when_no_beast_blood(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = tmpdir
            state = {
                "campaign_id": "t",
                "companions_state": {"beast_blood": False},
                "silver_hand_state": {"awareness_level": 4, "active_hunts": [], "high_purifier_alive": True},
            }
            (Path(state_dir) / "campaign_state.json").write_text(json.dumps(state))
            sm = StoryManager(data_dir=str(_REPO_ROOT / "data"), state_dir=state_dir)
            assert sm.trigger_silver_hand_event() is None

    def test_returns_none_when_awareness_zero(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=0)
            assert sm.trigger_silver_hand_event() is None

    def test_level_one_returns_scouts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=1)
            result = sm.trigger_silver_hand_event()
            assert result is not None
            assert result["level"] == 1
            assert "scout" in result["event"]

    def test_level_two_returns_ambush(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=2)
            result = sm.trigger_silver_hand_event()
            assert result["event"] == "silver_hand_ambush"

    def test_level_five_returns_jorrvaskr_assault(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=5)
            result = sm.trigger_silver_hand_event()
            assert result["event"] == "silver_hand_jorrvaskr_assault"

    def test_level_six_returns_final_purge(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=6)
            result = sm.trigger_silver_hand_event()
            assert result["event"] == "silver_hand_final_purge"

    def test_all_six_levels_return_events(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            for level in range(1, 7):
                sm = _make_sm(Path(tmpdir), awareness=level)
                result = sm.trigger_silver_hand_event()
                assert result is not None, f"Expected event at level {level}"
                assert result["level"] == level


class TestCheckSilverHandQuestEligibility:
    """Tests for StoryManager.check_silver_hand_quest_eligibility()."""

    def test_hunt_the_beast_requires_awareness_2(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=1)
            assert sm.check_silver_hand_quest_eligibility("silver_hand_hunt_the_beast") is False

    def test_hunt_the_beast_eligible_at_awareness_2(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=2)
            assert sm.check_silver_hand_quest_eligibility("silver_hand_hunt_the_beast") is True

    def test_siege_requires_beast_blood(self):
        """silver_hand_siege_of_jorrvaskr requires beast_blood — should fail without it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = tmpdir
            state = {
                "campaign_id": "t",
                "companions_state": {"beast_blood": False},
                "silver_hand_state": {"awareness_level": 5, "active_hunts": [], "high_purifier_alive": True},
            }
            (Path(state_dir) / "campaign_state.json").write_text(json.dumps(state))
            sm = StoryManager(data_dir=str(_REPO_ROOT / "data"), state_dir=state_dir)
            assert sm.check_silver_hand_quest_eligibility("silver_hand_siege_of_jorrvaskr") is False

    def test_purification_ritual_no_beast_blood_required(self):
        """silver_hand_purification_ritual does not require beast_blood."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_dir = tmpdir
            state = {
                "campaign_id": "t",
                "companions_state": {"beast_blood": False},
                "silver_hand_state": {"awareness_level": 3, "active_hunts": [], "high_purifier_alive": True},
            }
            (Path(state_dir) / "campaign_state.json").write_text(json.dumps(state))
            sm = StoryManager(data_dir=str(_REPO_ROOT / "data"), state_dir=state_dir)
            assert sm.check_silver_hand_quest_eligibility("silver_hand_purification_ritual") is True

    def test_unknown_quest_returns_false(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = _make_sm(Path(tmpdir), awareness=6)
            assert sm.check_silver_hand_quest_eligibility("nonexistent_quest") is False
