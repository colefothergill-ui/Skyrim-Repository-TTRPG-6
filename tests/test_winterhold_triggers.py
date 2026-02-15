#!/usr/bin/env python3
"""
Tests for Winterhold Location Triggers

This module tests the winterhold_location_triggers function to ensure
proper event generation based on location and campaign state.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.winterhold_triggers import winterhold_location_triggers


def test_winterhold_town_first_arrival():
    """Test first arrival in Winterhold triggers proper atmospheric description"""
    print("\n=== Testing Winterhold Town First Arrival ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {},
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("winterhold", campaign_state)
    
    assert len(events) > 0, "Expected events for Winterhold"
    assert any("Great Collapse" in event for event in events), "Expected Great Collapse reference"
    assert campaign_state["scene_flags"].get("winterhold_first_arrival"), "Flag should be set"
    print(f"✓ First arrival works: {len(events)} events generated")
    for event in events:
        print(f"  - {event[:80]}...")


def test_winterhold_imperial_tension():
    """Test Imperial alliance triggers tension in Stormcloak-leaning Winterhold"""
    print("\n=== Testing Imperial Tension ===")
    
    campaign_state = {
        "scene_flags": {"winterhold_first_arrival": True},
        "player": {},
        "civil_war_state": {
            "player_alliance": "Imperial"
        }
    }
    
    events = winterhold_location_triggers("winterhold", campaign_state)
    
    assert any("Imperial" in event or "occupation" in event for event in events), "Expected Imperial tension"
    assert campaign_state["scene_flags"].get("winterhold_imperial_tension"), "Tension flag should be set"
    print(f"✓ Imperial tension works: found faction awareness")


def test_frozen_hearth_inn():
    """Test Frozen Hearth inn triggers"""
    print("\n=== Testing Frozen Hearth Inn ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {},
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("winterhold_frozen_hearth", campaign_state)
    
    assert len(events) > 0, "Expected events for Frozen Hearth"
    assert any("stew" in event or "wool" in event or "listening" in event for event in events), "Expected inn atmosphere"
    print(f"✓ Frozen Hearth works: {events[0][:80]}...")


def test_college_bridge_non_member():
    """Test College bridge triggers admission test for non-members"""
    print("\n=== Testing College Bridge (Non-Member) ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {
            "college_member": False
        },
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("winterhold_college_bridge", campaign_state)
    
    assert any("Faralda" in event for event in events), "Expected Faralda appearance"
    assert any("spell" in event.lower() for event in events), "Expected admission test reference"
    assert campaign_state["scene_flags"].get("college_admission_test_offered"), "Test flag should be set"
    print(f"✓ College admission test triggers correctly")


def test_college_bridge_member():
    """Test College bridge recognizes members"""
    print("\n=== Testing College Bridge (Member) ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {
            "college_member": True,
            "college_rank": "Adept"
        },
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("college_bridge", campaign_state)
    
    assert any("Adept" in event for event in events), "Expected rank recognition"
    assert any("wards recognize" in event.lower() for event in events), "Expected ward recognition"
    print(f"✓ College member recognition works")


def test_college_courtyard():
    """Test College courtyard triggers"""
    print("\n=== Testing College Courtyard ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {
            "college_member": True
        },
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("college_courtyard", campaign_state)
    
    assert len(events) > 0, "Expected courtyard events"
    assert any("Tolfdir" in event for event in events), "Expected Tolfdir reference for members"
    assert campaign_state["scene_flags"].get("college_first_lessons_hook"), "First lessons hook should trigger"
    print(f"✓ College courtyard works with member hooks")


def test_arcanaeum():
    """Test Arcanaeum library triggers"""
    print("\n=== Testing Arcanaeum ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {},
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("college_arcanaeum", campaign_state)
    
    assert len(events) > 0, "Expected Arcanaeum events"
    assert any("Urag" in event for event in events), "Expected Urag gro-Shub reference"
    assert any("ink" in event.lower() or "shelves" in event.lower() or "silence" in event.lower() 
               for event in events), "Expected book/library atmosphere"
    print(f"✓ Arcanaeum atmosphere works")


def test_saarthal():
    """Test Saarthal excavation site triggers"""
    print("\n=== Testing Saarthal ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {},
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("saarthal_excavation", campaign_state)
    
    assert len(events) > 0, "Expected Saarthal events"
    assert any("draugr" in event.lower() for event in events), "Expected draugr reference"
    assert any("Tolfdir" in event for event in events), "Expected Eye of Magnus hook"
    assert campaign_state["scene_flags"].get("saarthal_eye_of_magnus_hook"), "Eye hook should trigger"
    print(f"✓ Saarthal Eye of Magnus hook works")


def test_staff_of_cinders_recognition():
    """Test Staff of Cinders artifact recognition across locations"""
    print("\n=== Testing Staff of Cinders Recognition ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {
            "has_staff_of_cinders": True
        },
        "civil_war_state": {}
    }
    
    # Test in town
    events_town = winterhold_location_triggers("winterhold", campaign_state)
    assert any("Cindershroud" in event for event in events_town), "Expected staff recognition in town"
    
    # Reset flag for next test
    campaign_state["scene_flags"] = {}
    
    # Test at College bridge
    campaign_state["player"]["college_member"] = True
    events_college = winterhold_location_triggers("college_bridge", campaign_state)
    assert any("runes" in event.lower() and "enchantment" in event.lower() for event in events_college), "Expected staff recognition at College"
    
    print(f"✓ Staff of Cinders recognition works across locations")


def test_hall_of_elements():
    """Test Hall of the Elements triggers"""
    print("\n=== Testing Hall of the Elements ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {},
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("college_hall_of_elements", campaign_state)
    
    assert len(events) > 0, "Expected Hall of Elements events"
    assert any("sparks" in event.lower() or "frost" in event.lower() or "danger" in event.lower() 
               for event in events), "Expected magical atmosphere"
    print(f"✓ Hall of Elements atmosphere works")


def test_the_midden():
    """Test The Midden dark atmosphere"""
    print("\n=== Testing The Midden ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {},
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("college_midden", campaign_state)
    
    assert len(events) > 0, "Expected Midden events"
    assert any("cold" in event.lower() or "intent" in event.lower() or "regret" in event.lower() 
               for event in events), "Expected ominous atmosphere"
    print(f"✓ Midden dark atmosphere works")


def test_jarl_korir_court():
    """Test Jarl's Longhouse with College member"""
    print("\n=== Testing Jarl Korir's Court ===")
    
    campaign_state = {
        "scene_flags": {},
        "player": {
            "college_member": True
        },
        "civil_war_state": {}
    }
    
    events = winterhold_location_triggers("winterhold_jarls_longhouse", campaign_state)
    
    assert len(events) > 0, "Expected longhouse events"
    assert any("Korir" in event for event in events), "Expected Jarl reaction to College member"
    assert campaign_state["scene_flags"].get("jarl_reacts_to_college"), "Jarl reaction flag should be set"
    print(f"✓ Jarl's court College tension works")


def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("WINTERHOLD & COLLEGE TRIGGERS TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_winterhold_town_first_arrival,
        test_winterhold_imperial_tension,
        test_frozen_hearth_inn,
        test_college_bridge_non_member,
        test_college_bridge_member,
        test_college_courtyard,
        test_arcanaeum,
        test_saarthal,
        test_staff_of_cinders_recognition,
        test_hall_of_elements,
        test_the_midden,
        test_jarl_korir_court
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
