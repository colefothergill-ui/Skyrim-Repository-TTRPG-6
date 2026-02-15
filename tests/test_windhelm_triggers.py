#!/usr/bin/env python3
"""
Tests for Windhelm Location Triggers

This module tests the windhelm_location_triggers function to ensure
proper event generation based on location and campaign state, including
quest hooks for Blood on the Ice and The White Phial.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.windhelm_triggers import windhelm_location_triggers


def test_gray_quarter_trigger():
    """Test that Gray Quarter triggers appropriate events"""
    print("\n=== Testing Gray Quarter Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = windhelm_location_triggers("windhelm_gray_quarter", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Gray Quarter"
    assert any("Gray Quarter" in event for event in events), "Expected Gray Quarter description"
    assert any("Dunmer" in event or "Dark Elf" in event for event in events), "Expected reference to Dunmer/Dark Elves"
    print(f"✓ Gray Quarter trigger works: {events}")


def test_graveyard_trigger_nighttime():
    """Test that graveyard at night triggers Blood on the Ice quest hook"""
    print("\n=== Testing Graveyard Nighttime Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "time_of_day": "night",
        "quests": {
            "active": [],
            "completed": []
        }
    }
    
    events = windhelm_location_triggers("windhelm_graveyard", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for graveyard at night"
    assert any("graveyard" in event.lower() for event in events), "Expected graveyard description"
    assert any("shouts" in event.lower() or "murder" in event.lower() for event in events), "Expected Blood on the Ice quest hook"
    print(f"✓ Graveyard nighttime trigger works: {events}")


def test_graveyard_trigger_daytime():
    """Test that graveyard during day triggers subtle hints"""
    print("\n=== Testing Graveyard Daytime Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "time_of_day": "day",
        "quests": {
            "active": [],
            "completed": []
        }
    }
    
    events = windhelm_location_triggers("windhelm_graveyard", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for graveyard during day"
    assert any("graveyard" in event.lower() for event in events), "Expected graveyard description"
    # Should still have some hint about murders
    assert any("murder" in event.lower() or "butcher" in event.lower() for event in events), "Expected subtle quest hint"
    print(f"✓ Graveyard daytime trigger works: {events}")


def test_graveyard_quest_active():
    """Test that graveyard doesn't trigger quest hook if already active"""
    print("\n=== Testing Graveyard with Active Quest ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "time_of_day": "night",
        "quests": {
            "active": ["blood_on_the_ice"],
            "completed": []
        }
    }
    
    events = windhelm_location_triggers("windhelm_graveyard", campaign_state)
    
    # Should still have graveyard description but not the quest discovery hook
    assert len(events) > 0, "Expected at least one event for graveyard"
    # The specific quest start event should not appear
    assert not any("Another one!" in event for event in events), "Should not trigger quest start if already active"
    print(f"✓ Graveyard with active quest works correctly: {events}")


def test_market_white_phial_trigger():
    """Test that marketplace triggers White Phial quest hook"""
    print("\n=== Testing Market White Phial Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "quests": {
            "active": [],
            "completed": []
        }
    }
    
    events = windhelm_location_triggers("windhelm_market", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for market"
    assert any("market" in event.lower() for event in events), "Expected marketplace description"
    assert any("White Phial" in event or "Nurelion" in event for event in events), "Expected White Phial quest hook"
    print(f"✓ Market White Phial trigger works: {events}")


def test_market_quest_active():
    """Test that market doesn't trigger quest hook if already active"""
    print("\n=== Testing Market with Active Quest ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "quests": {
            "active": ["the_white_phial"],
            "completed": []
        }
    }
    
    events = windhelm_location_triggers("windhelm_market", campaign_state)
    
    # Should have market description but not the quest hook
    assert len(events) > 0, "Expected at least one event for market"
    assert not any("Quintus" in event and "Phial must be found" in event for event in events), "Should not trigger quest hook if already active"
    print(f"✓ Market with active quest works correctly: {events}")


def test_palace_of_the_kings_trigger():
    """Test that Palace of the Kings triggers appropriate events"""
    print("\n=== Testing Palace of the Kings Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = windhelm_location_triggers("windhelm_palace_of_the_kings", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Palace"
    assert any("Palace of the Kings" in event for event in events), "Expected Palace description"
    assert any("Ulfric" in event for event in events), "Expected reference to Ulfric"
    print(f"✓ Palace of the Kings trigger works: {events}")


def test_general_windhelm_entrance():
    """Test that general Windhelm entrance triggers appropriate events"""
    print("\n=== Testing General Windhelm Entrance ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "time_of_day": "day"
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Windhelm entrance"
    assert any("Windhelm" in event for event in events), "Expected Windhelm description"
    assert any("City of Kings" in event or "ancient" in event.lower() for event in events), "Expected historical reference"
    print(f"✓ General Windhelm entrance trigger works: {events}")


def test_companion_stenvar_commentary():
    """Test that Stenvar provides commentary in Windhelm"""
    print("\n=== Testing Stenvar Companion Commentary ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Stenvar"]
        }
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event"
    assert any("Stenvar" in event for event in events), "Expected Stenvar commentary"
    print(f"✓ Stenvar commentary trigger works: {events}")


def test_companion_stenvar_dict_format():
    """Test that Stenvar in dict format provides commentary"""
    print("\n=== Testing Stenvar Companion (Dict Format) ===")
    
    campaign_state = {
        "companions": {
            "active_companions": [
                {"name": "Stenvar", "npc_id": "stenvar"}
            ]
        }
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event"
    assert any("Stenvar" in event for event in events), "Expected Stenvar commentary"
    print(f"✓ Stenvar (dict format) commentary trigger works: {events}")


def test_companion_uthgerd_commentary():
    """Test that Uthgerd provides commentary in Windhelm"""
    print("\n=== Testing Uthgerd Companion Commentary ===")
    
    campaign_state = {
        "companions": {
            "active_companions": [{"name": "Uthgerd the Unbroken", "npc_id": "uthgerd"}]
        }
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event"
    assert any("Uthgerd" in event for event in events), "Expected Uthgerd commentary"
    assert any("Ysgramor" in event or "oldest city" in event for event in events), "Expected historical commentary from Uthgerd"
    print(f"✓ Uthgerd commentary trigger works: {events}")


def test_empty_companions():
    """Test that triggers work with no companions"""
    print("\n=== Testing Empty Companions ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event even without companions"
    print(f"✓ Triggers work with empty companions: {events}")


def test_missing_campaign_state():
    """Test that triggers handle missing campaign state gracefully"""
    print("\n=== Testing Missing Campaign State ===")
    
    campaign_state = {}
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    # Should still return basic location description
    assert len(events) > 0, "Expected at least one event even with minimal state"
    print(f"✓ Triggers handle missing state gracefully: {events}")


def test_candlehearth_hall_trigger():
    """Test that Candlehearth Hall triggers appropriate events"""
    print("\n=== Testing Candlehearth Hall Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = windhelm_location_triggers("windhelm_candlehearth_hall", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Candlehearth Hall"
    assert any("Candlehearth" in event for event in events), "Expected Candlehearth Hall description"
    print(f"✓ Candlehearth Hall trigger works: {events}")


def test_civil_war_stormcloak_victory():
    """Test that Windhelm celebrates Stormcloak victory at Whiterun"""
    print("\n=== Testing Civil War: Stormcloak Victory at Whiterun ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "whiterun_control": "stormcloak"
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event"
    assert any("Victory for Ulfric" in event or "celebration" in event.lower() for event in events), "Expected victory celebration"
    assert any("Balgruuf" in event for event in events), "Expected reference to Balgruuf's surrender"
    assert campaign_state.get("windhelm_heard_whiterun_win") == True, "Expected flag to be set"
    print(f"✓ Stormcloak victory celebration works: {events}")


def test_civil_war_stormcloak_victory_only_once():
    """Test that Stormcloak victory celebration only fires once"""
    print("\n=== Testing Civil War: Victory Celebration Fires Once ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "whiterun_control": "stormcloak",
        "windhelm_heard_whiterun_win": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    # Should have basic windhelm description but not the victory event
    assert len(events) > 0, "Expected at least one event"
    assert not any("Victory for Ulfric" in event for event in events), "Should not trigger victory event twice"
    print(f"✓ Victory celebration only fires once: {events}")


def test_civil_war_imperial_victory():
    """Test that Windhelm reacts to Imperial victory at Whiterun"""
    print("\n=== Testing Civil War: Imperial Victory at Whiterun ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "whiterun_control": "imperial"
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event"
    assert any("hush" in event.lower() or "failed" in event.lower() for event in events), "Expected somber reaction"
    assert any("Balgruuf" in event for event in events), "Expected reference to Balgruuf staying with Empire"
    assert campaign_state.get("windhelm_heard_whiterun_loss") == True, "Expected flag to be set"
    print(f"✓ Imperial victory reaction works: {events}")


def test_civil_war_imperial_victory_only_once():
    """Test that Imperial victory reaction only fires once"""
    print("\n=== Testing Civil War: Loss Reaction Fires Once ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "whiterun_control": "imperial",
        "windhelm_heard_whiterun_loss": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    # Should have basic windhelm description but not the loss reaction event
    assert len(events) > 0, "Expected at least one event"
    assert not any("hush has fallen" in event for event in events), "Should not trigger loss reaction twice"
    print(f"✓ Loss reaction only fires once: {events}")


def test_civil_war_battle_for_windhelm():
    """Test that Battle for Windhelm siege triggers appropriately"""
    print("\n=== Testing Civil War: Battle for Windhelm Siege ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "battle_for_windhelm_started": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event"
    assert any("Imperials are at the gates" in event or "siege" in event.lower() for event in events), "Expected siege alert"
    assert any("barricades" in event.lower() for event in events), "Expected description of fortifications"
    assert campaign_state.get("windhelm_siege_alert") == True, "Expected flag to be set"
    print(f"✓ Battle for Windhelm siege works: {events}")


def test_civil_war_battle_for_windhelm_only_once():
    """Test that Battle for Windhelm siege alert only fires once"""
    print("\n=== Testing Civil War: Siege Alert Fires Once ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "battle_for_windhelm_started": True,
        "windhelm_siege_alert": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    # Should have basic description but not the siege alert
    assert len(events) > 0, "Expected at least one event"
    assert not any("Alarms ring out" in event for event in events), "Should not trigger siege alert twice"
    print(f"✓ Siege alert only fires once: {events}")


def test_civil_war_season_unending_truce():
    """Test that Season Unending truce triggers appropriate events"""
    print("\n=== Testing Civil War: Season Unending Truce ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "truce_active": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    assert len(events) > 0, "Expected at least one event"
    assert any("truce" in event.lower() or "ceasefire" in event.lower() for event in events), "Expected truce mention"
    assert any("Imperial emissaries" in event or "uneasy peace" in event for event in events), "Expected description of tense peace"
    assert campaign_state.get("windhelm_truce_noticed") == True, "Expected flag to be set"
    print(f"✓ Season Unending truce works: {events}")


def test_civil_war_truce_only_once():
    """Test that truce event only fires once"""
    print("\n=== Testing Civil War: Truce Event Fires Once ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "truce_active": True,
        "windhelm_truce_noticed": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    # Should have basic description but not the truce event
    assert len(events) > 0, "Expected at least one event"
    assert not any("uneasy peace has settled" in event for event in events), "Should not trigger truce event twice"
    print(f"✓ Truce event only fires once: {events}")


def test_civil_war_no_flags():
    """Test that civil war triggers don't fire without appropriate flags"""
    print("\n=== Testing Civil War: No Triggers Without Flags ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    # Should have basic windhelm description but no civil war events
    assert len(events) > 0, "Expected at least one event"
    assert not any("Victory for Ulfric" in event for event in events), "Should not trigger victory without flag"
    assert not any("hush has fallen" in event for event in events), "Should not trigger loss without flag"
    assert not any("Imperials are at the gates" in event for event in events), "Should not trigger siege without flag"
    assert not any("Imperial emissaries" in event for event in events), "Should not trigger truce without flag"
    print(f"✓ No civil war triggers without appropriate flags: {events}")


def test_civil_war_multiple_events():
    """Test that multiple civil war events can be queued if appropriate"""
    print("\n=== Testing Civil War: Multiple Events ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "whiterun_control": "stormcloak",
        "truce_active": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    # Should have both victory celebration and truce event
    assert len(events) >= 3, "Expected at least 3 events (basic + victory + truce)"
    assert any("Victory for Ulfric" in event for event in events), "Expected victory celebration"
    assert any("truce" in event.lower() or "Imperial emissaries" in event for event in events), "Expected truce event"
    print(f"✓ Multiple civil war events can fire: {events}")


def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("Running Windhelm Location Trigger Tests")
    print("=" * 60)
    
    test_functions = [
        test_gray_quarter_trigger,
        test_graveyard_trigger_nighttime,
        test_graveyard_trigger_daytime,
        test_graveyard_quest_active,
        test_market_white_phial_trigger,
        test_market_quest_active,
        test_palace_of_the_kings_trigger,
        test_general_windhelm_entrance,
        test_companion_stenvar_commentary,
        test_companion_stenvar_dict_format,
        test_companion_uthgerd_commentary,
        test_empty_companions,
        test_missing_campaign_state,
        test_candlehearth_hall_trigger,
        test_civil_war_stormcloak_victory,
        test_civil_war_stormcloak_victory_only_once,
        test_civil_war_imperial_victory,
        test_civil_war_imperial_victory_only_once,
        test_civil_war_battle_for_windhelm,
        test_civil_war_battle_for_windhelm_only_once,
        test_civil_war_season_unending_truce,
        test_civil_war_truce_only_once,
        test_civil_war_no_flags,
        test_civil_war_multiple_events
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
