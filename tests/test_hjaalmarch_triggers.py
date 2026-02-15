#!/usr/bin/env python3
"""
Tests for Hjaalmarch (Morthal) Location Triggers

This module tests the hjaalmarch_location_triggers function to ensure
proper event generation based on location and campaign state.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.hjaalmarch_triggers import hjaalmarch_location_triggers


def test_highmoon_hall_trigger():
    """Test Highmoon Hall (Jarl's longhouse) trigger"""
    print("\n=== Testing Highmoon Hall Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = hjaalmarch_location_triggers("morthal_highmoon_hall", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Highmoon Hall"
    assert any("Highmoon Hall" in event and "Idgrod" in event for event in events), "Expected Highmoon Hall description with Idgrod"
    print(f"✓ Highmoon Hall trigger works: {len(events)} event(s)")


def test_moorside_inn_trigger():
    """Test Moorside Inn trigger"""
    print("\n=== Testing Moorside Inn Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = hjaalmarch_location_triggers("morthal_moorside_inn", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Moorside Inn"
    assert any("Moorside Inn" in event or "Jonna" in event for event in events), "Expected Moorside Inn description"
    print(f"✓ Moorside Inn trigger works: {len(events)} event(s)")


def test_swamp_perimeter_trigger():
    """Test Morthal Swamp Perimeter trigger"""
    print("\n=== Testing Swamp Perimeter Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    # Test various perimeter-related location names
    for loc in ["morthal_swamp_perimeter", "morthal_outskirts", "morthal_swamp"]:
        events = hjaalmarch_location_triggers(loc, campaign_state)
        assert len(events) > 0, f"Expected at least one event for {loc}"
        assert any("marsh" in event.lower() or "falion" in event.lower() for event in events), "Expected swamp/marsh description"
    
    print(f"✓ Swamp perimeter triggers work")


def test_general_morthal_entrance():
    """Test general Morthal entrance trigger"""
    print("\n=== Testing General Morthal Entrance ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for general Morthal"
    assert any("morthal" in event.lower() or "mist" in event.lower() or "fog" in event.lower() for event in events), "Expected Morthal entrance description"
    print(f"✓ General Morthal entrance trigger works: {len(events)} event(s)")


def test_laid_to_rest_night_burned_house():
    """Test Laid to Rest quest hook at night near burned house"""
    print("\n=== Testing Laid to Rest (Night, Burned House) ===")
    
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
    
    events = hjaalmarch_location_triggers("morthal_burned_house", campaign_state)
    
    assert len(events) > 0, "Expected events for burned house at night"
    # Should trigger ghost appearance and vampire attack
    assert any("helgi" in event.lower() or "girl" in event.lower() or "ghost" in event.lower() for event in events), "Expected ghost appearance"
    assert any("laelette" in event.lower() or "vampire" in event.lower() for event in events), "Expected vampire attack"
    print(f"✓ Laid to Rest night trigger works: {len(events)} event(s)")


def test_laid_to_rest_day_burned_house():
    """Test Laid to Rest quest hook during day near burned house"""
    print("\n=== Testing Laid to Rest (Day, Burned House) ===")
    
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
    
    events = hjaalmarch_location_triggers("morthal_burned_house", campaign_state)
    
    assert len(events) > 0, "Expected events for burned house during day"
    assert any("gossip" in event.lower() or "hroggar" in event.lower() or "alva" in event.lower() for event in events), "Expected day gossip"
    print(f"✓ Laid to Rest day trigger works: {len(events)} event(s)")


def test_laid_to_rest_night_graveyard():
    """Test Laid to Rest quest hook at night near graveyard"""
    print("\n=== Testing Laid to Rest (Night, Graveyard) ===")
    
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
    
    events = hjaalmarch_location_triggers("morthal_graveyard", campaign_state)
    
    assert len(events) > 0, "Expected events for graveyard at night"
    # Should trigger ghost appearance in graveyard and vampire attack
    assert any("graveyard" in event.lower() and ("girl" in event.lower() or "mound" in event.lower()) for event in events), "Expected graveyard ghost appearance"
    assert any("laelette" in event.lower() or "vampire" in event.lower() for event in events), "Expected vampire attack"
    print(f"✓ Laid to Rest night graveyard trigger works: {len(events)} event(s)")


def test_laid_to_rest_day_graveyard():
    """Test Laid to Rest quest hook during day near graveyard"""
    print("\n=== Testing Laid to Rest (Day, Graveyard) ===")
    
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
    
    events = hjaalmarch_location_triggers("morthal_graveyard", campaign_state)
    
    assert len(events) > 0, "Expected events for graveyard during day"
    assert any("graveyard" in event.lower() and ("caretaker" in event.lower() or "helgi" in event.lower()) for event in events), "Expected day graveyard description"
    print(f"✓ Laid to Rest day graveyard trigger works: {len(events)} event(s)")


def test_movarth_lair_quest_active():
    """Test Movarth's Lair trigger when quest is active"""
    print("\n=== Testing Movarth's Lair (Quest Active) ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "quests": {
            "active": ["laid_to_rest"],
            "completed": []
        }
    }
    
    events = hjaalmarch_location_triggers("movarths_lair", campaign_state)
    
    assert len(events) > 0, "Expected events for Movarth's Lair"
    assert any("movarth" in event.lower() and ("fresh blood" in event.lower() or "vampire" in event.lower()) for event in events), "Expected active quest description"
    print(f"✓ Movarth's Lair (quest active) trigger works: {len(events)} event(s)")


def test_movarth_lair_quest_not_active():
    """Test Movarth's Lair trigger when quest is not active"""
    print("\n=== Testing Movarth's Lair (Quest Not Active) ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "quests": {
            "active": [],
            "completed": []
        }
    }
    
    events = hjaalmarch_location_triggers("movarths_lair", campaign_state)
    
    assert len(events) > 0, "Expected events for Movarth's Lair"
    assert any("bones" in event.lower() or "unsettling" in event.lower() or "door" in event.lower() for event in events), "Expected general lair description"
    print(f"✓ Movarth's Lair (quest not active) trigger works: {len(events)} event(s)")


def test_falion_ritual_night():
    """Test Falion's ritual trigger at night"""
    print("\n=== Testing Falion's Ritual (Night) ===")
    
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
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    # Should mention Falion's ritual
    assert any("falion" in event.lower() and ("ritual" in event.lower() or "soul gem" in event.lower()) for event in events), "Expected Falion ritual description"
    print(f"✓ Falion's ritual trigger works: {len(events)} event(s)")


def test_falion_ritual_not_at_night():
    """Test that Falion's ritual doesn't trigger during day"""
    print("\n=== Testing Falion's Ritual (Day - Should Not Trigger) ===")
    
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
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    # Should not mention ritual during day
    falion_ritual_events = [e for e in events if "falion" in e.lower() and "ritual" in e.lower() and "soul gem" in e.lower()]
    assert len(falion_ritual_events) == 0, "Falion's ritual should not trigger during day"
    print(f"✓ Falion's ritual correctly doesn't trigger during day")


def test_benor_companion_commentary():
    """Test that Benor provides commentary when in Morthal"""
    print("\n=== Testing Benor Companion Commentary ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Benor"]
        }
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    assert len(events) > 0, "Expected events when Benor is present"
    benor_event = [e for e in events if "benor" in e.lower()]
    assert len(benor_event) > 0, "Expected Benor to comment about Morthal"
    print(f"✓ Benor commentary works: {benor_event[0]}")


def test_benor_case_insensitive():
    """Test that Benor detection is case-insensitive"""
    print("\n=== Testing Benor (Case Insensitive) ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["benor"]
        }
    }
    
    events = hjaalmarch_location_triggers("Morthal", campaign_state)
    
    benor_event = [e for e in events if "benor" in e.lower()]
    assert len(benor_event) > 0, "Expected Benor commentary with lowercase companion name"
    print(f"✓ Case-insensitive Benor detection works")


def test_stormcloak_takeover():
    """Test Stormcloak takeover trigger"""
    print("\n=== Testing Stormcloak Takeover ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "jarl_hjaalmarch": "sorli"
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    assert len(events) > 0, "Expected events for Stormcloak takeover"
    stormcloak_event = [e for e in events if "stormcloak" in e.lower() or "sorli" in e.lower()]
    assert len(stormcloak_event) > 0, "Expected Stormcloak takeover description"
    assert campaign_state.get("morthal_stormcloak_banner") is True, "Expected flag to be set"
    print(f"✓ Stormcloak takeover trigger works")


def test_stormcloak_takeover_idempotent():
    """Test that Stormcloak takeover only triggers once"""
    print("\n=== Testing Stormcloak Takeover (Idempotent) ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "jarl_hjaalmarch": "sorli",
        "morthal_stormcloak_banner": True
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    # Should not trigger takeover message again
    stormcloak_event = [e for e in events if "stormcloak" in e.lower() and "takeover" in e.lower()]
    assert len(stormcloak_event) == 0, "Stormcloak takeover should not trigger twice"
    print(f"✓ Stormcloak takeover correctly doesn't trigger twice")


def test_imperial_restoration():
    """Test Imperial restoration trigger"""
    print("\n=== Testing Imperial Restoration ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "civil_war_phase": "imperial_victory",
        "jarl_hjaalmarch": "sorli",  # Not Idgrod, so should trigger restoration
        "morthal_stormcloak_banner": True  # Already saw Stormcloak takeover, now seeing restoration
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    assert len(events) > 0, "Expected events for Imperial restoration"
    imperial_event = [e for e in events if "imperial" in e.lower() and ("restored" in e.lower() or "idgrod" in e.lower())]
    assert len(imperial_event) > 0, "Expected Imperial restoration description"
    assert campaign_state.get("morthal_imperial_restored") is True, "Expected flag to be set"
    print(f"✓ Imperial restoration trigger works")


def test_empty_companions_list():
    """Test handling of empty companions list"""
    print("\n=== Testing Empty Companions List ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    assert len(events) > 0, "Expected events even with no companions"
    benor_event = [e for e in events if "benor" in e.lower()]
    assert len(benor_event) == 0, "Expected no Benor commentary with empty companions"
    print(f"✓ Handles empty companions list correctly")


def test_missing_companions_key():
    """Test handling of missing companions key in campaign state"""
    print("\n=== Testing Missing Companions Key ===")
    
    campaign_state = {}
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    # Should not crash, just return location events without companion commentary
    assert len(events) > 0, "Expected events even without companions key"
    print(f"✓ Handles missing companions key gracefully")


def test_complex_companion_objects():
    """Test with companion as dictionary objects (more realistic)"""
    print("\n=== Testing Complex Companion Objects ===")
    
    campaign_state = {
        "companions": {
            "active_companions": [
                {
                    "name": "Benor",
                    "npc_id": "benor",
                    "loyalty": 70
                }
            ]
        }
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    
    assert len(events) > 0, "Expected events when Benor dict is present"
    benor_event = [e for e in events if "benor" in e.lower()]
    assert len(benor_event) > 0, "Expected Benor commentary with dictionary companion"
    print(f"✓ Function handles complex companion objects correctly")


def test_location_case_insensitive():
    """Test that location matching is case-insensitive"""
    print("\n=== Testing Location Case Insensitive ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    # Test various case combinations
    for loc in ["Morthal", "MORTHAL", "morthal", "MoRtHaL"]:
        events = hjaalmarch_location_triggers(loc, campaign_state)
        assert len(events) > 0, f"Expected events for {loc}"
    
    print(f"✓ Location matching is case-insensitive")


def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("Hjaalmarch (Morthal) Triggers Test Suite")
    print("=" * 60)
    
    test_functions = [
        test_highmoon_hall_trigger,
        test_moorside_inn_trigger,
        test_swamp_perimeter_trigger,
        test_general_morthal_entrance,
        test_laid_to_rest_night_burned_house,
        test_laid_to_rest_day_burned_house,
        test_laid_to_rest_night_graveyard,
        test_laid_to_rest_day_graveyard,
        test_movarth_lair_quest_active,
        test_movarth_lair_quest_not_active,
        test_falion_ritual_night,
        test_falion_ritual_not_at_night,
        test_benor_companion_commentary,
        test_benor_case_insensitive,
        test_stormcloak_takeover,
        test_stormcloak_takeover_idempotent,
        test_imperial_restoration,
        test_empty_companions_list,
        test_missing_companions_key,
        test_complex_companion_objects,
        test_location_case_insensitive,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {test_func.__name__}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {test_func.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
