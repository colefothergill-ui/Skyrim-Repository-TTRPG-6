#!/usr/bin/env python3
"""
Tests for Trigger Utility Functions

This module tests the shared utility functions used by location trigger modules.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.trigger_utils import is_companion_present, is_quest_active, is_night_time


def test_is_companion_present_string():
    """Test companion detection with string format"""
    print("\n=== Testing is_companion_present with Strings ===")
    
    companions = ["Lydia", "Hadvar", "Ralof"]
    
    assert is_companion_present(companions, "lydia"), "Should find Lydia (case-insensitive)"
    assert is_companion_present(companions, "Hadvar"), "Should find Hadvar"
    assert not is_companion_present(companions, "Stenvar"), "Should not find Stenvar"
    
    print("✓ String format companion detection works")


def test_is_companion_present_dict():
    """Test companion detection with dictionary format"""
    print("\n=== Testing is_companion_present with Dicts ===")
    
    companions = [
        {"name": "Lydia", "npc_id": "lydia"},
        {"name": "Hadvar", "npc_id": "hadvar"}
    ]
    
    assert is_companion_present(companions, "lydia"), "Should find Lydia by name"
    assert is_companion_present(companions, "Hadvar"), "Should find Hadvar"
    assert not is_companion_present(companions, "Stenvar"), "Should not find Stenvar"
    
    print("✓ Dictionary format companion detection works")


def test_is_companion_present_partial():
    """Test companion detection with partial names"""
    print("\n=== Testing is_companion_present with Partial Names ===")
    
    companions = ["Lydia the Housecarl", "Stenvar the Mercenary"]
    
    assert is_companion_present(companions, "lydia"), "Should find Lydia with partial match"
    assert is_companion_present(companions, "stenvar"), "Should find Stenvar with partial match"
    
    print("✓ Partial name matching works")


def test_is_companion_present_empty():
    """Test companion detection with empty companions list"""
    print("\n=== Testing is_companion_present with Empty List ===")
    
    assert not is_companion_present([], "lydia"), "Should return False for empty list"
    assert not is_companion_present([], "anyone"), "Should return False for empty list"
    
    print("✓ Empty companions list handling works")


def test_is_quest_active_string():
    """Test quest state detection with string format"""
    print("\n=== Testing is_quest_active with Strings ===")
    
    campaign_state = {
        "quests": {
            "active": ["quest1", "quest2"],
            "completed": ["quest3"]
        }
    }
    
    assert is_quest_active(campaign_state, "quest1"), "Should find active quest1"
    assert is_quest_active(campaign_state, "quest3"), "Should find completed quest3"
    assert not is_quest_active(campaign_state, "quest4"), "Should not find quest4"
    
    print("✓ String format quest detection works")


def test_is_quest_active_dict():
    """Test quest state detection with dictionary format"""
    print("\n=== Testing is_quest_active with Dicts ===")
    
    campaign_state = {
        "quests": {
            "active": [{"id": "quest1", "stage": 2}],
            "completed": [{"id": "quest3"}]
        }
    }
    
    assert is_quest_active(campaign_state, "quest1"), "Should find active quest1"
    assert is_quest_active(campaign_state, "quest3"), "Should find completed quest3"
    assert not is_quest_active(campaign_state, "quest4"), "Should not find quest4"
    
    print("✓ Dictionary format quest detection works")


def test_is_quest_active_empty():
    """Test quest state detection with missing data"""
    print("\n=== Testing is_quest_active with Empty State ===")
    
    assert not is_quest_active({}, "quest1"), "Should handle empty state"
    assert not is_quest_active({"quests": {}}, "quest1"), "Should handle empty quests"
    
    print("✓ Empty state handling works")


def test_is_night_time_string():
    """Test night time detection with string format"""
    print("\n=== Testing is_night_time with Strings ===")
    
    assert is_night_time({"time_of_day": "night"}), "Should detect 'night'"
    assert is_night_time({"time_of_day": "evening"}), "Should detect 'evening'"
    assert is_night_time({"time_of_day": "midnight"}), "Should detect 'midnight'"
    assert not is_night_time({"time_of_day": "day"}), "Should not detect 'day' as night"
    assert not is_night_time({"time_of_day": "morning"}), "Should not detect 'morning' as night"
    
    print("✓ String format night detection works")


def test_is_night_time_int():
    """Test night time detection with integer format"""
    print("\n=== Testing is_night_time with Integers ===")
    
    # Night is 20-23 and 0-5
    assert is_night_time({"time_of_day": 22}), "Should detect 22:00 as night"
    assert is_night_time({"time_of_day": 2}), "Should detect 02:00 as night"
    assert not is_night_time({"time_of_day": 12}), "Should not detect 12:00 as night"
    assert not is_night_time({"time_of_day": 18}), "Should not detect 18:00 as night"
    
    print("✓ Integer format night detection works")


def test_is_night_time_edge_cases():
    """Test night time detection edge cases"""
    print("\n=== Testing is_night_time Edge Cases ===")
    
    assert is_night_time({"time_of_day": 20}), "Should detect 20:00 (8 PM) as night start"
    assert is_night_time({"time_of_day": 5}), "Should detect 05:00 as night end"
    assert not is_night_time({"time_of_day": 6}), "Should not detect 06:00 as night"
    assert not is_night_time({}), "Should handle missing time_of_day"
    
    print("✓ Edge case handling works")


def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("Running Trigger Utility Tests")
    print("=" * 60)
    
    test_functions = [
        test_is_companion_present_string,
        test_is_companion_present_dict,
        test_is_companion_present_partial,
        test_is_companion_present_empty,
        test_is_quest_active_string,
        test_is_quest_active_dict,
        test_is_quest_active_empty,
        test_is_night_time_string,
        test_is_night_time_int,
        test_is_night_time_edge_cases
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
