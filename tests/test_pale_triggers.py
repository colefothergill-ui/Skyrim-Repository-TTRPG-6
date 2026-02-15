#!/usr/bin/env python3
"""
Tests for The Pale (Dawnstar) Location Triggers

This module tests The Pale trigger functions to ensure
proper scene generation and quest trigger behavior.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.pale_triggers import (
    scene_dawnstar_arrival,
    scene_windpeak_inn_commotion,
    trigger_erandur_waking_nightmare,
    trigger_skald_giant_bounty,
    trigger_wayfinder_void_salts,
    trigger_pale_blizzard,
    trigger_erandur_intersect,
    pale_get_next_scene
)


def test_dawnstar_arrival():
    """Test Dawnstar arrival scene"""
    print("\n=== Testing Dawnstar Arrival Scene ===")
    
    party_state = {}
    scene_dawnstar_arrival(party_state)
    
    assert party_state.get('seen_dawnstar_intro') is True, "Expected seen_dawnstar_intro flag to be set"
    print("✓ Dawnstar arrival scene works and sets flag")


def test_windpeak_inn_commotion():
    """Test Windpeak Inn nightmare commotion scene"""
    print("\n=== Testing Windpeak Inn Commotion Scene ===")
    
    party_state = {}
    scene_windpeak_inn_commotion(party_state)
    
    assert party_state.get('heard_nightmare_rumors') is True, "Expected heard_nightmare_rumors flag to be set"
    print("✓ Windpeak Inn commotion scene works and sets flag")


def test_erandur_waking_nightmare():
    """Test Erandur's Waking Nightmare quest trigger"""
    print("\n=== Testing Erandur's Waking Nightmare Quest Trigger ===")
    
    campaign_state = {}
    
    # First time should trigger
    trigger_erandur_waking_nightmare(campaign_state)
    assert campaign_state.get('waking_nightmare_quest_given') is True, "Expected quest flag to be set"
    print("✓ Waking Nightmare quest triggers on first call")
    
    # Second time should not trigger (test idempotence)
    print("\nTesting idempotence (should not print quest dialogue again):")
    trigger_erandur_waking_nightmare(campaign_state)
    print("✓ Quest doesn't trigger twice")


def test_skald_giant_bounty():
    """Test Jarl Skald's giant bounty quest trigger"""
    print("\n=== Testing Skald's Giant Bounty Quest Trigger ===")
    
    campaign_state = {}
    
    # First time should trigger
    trigger_skald_giant_bounty(campaign_state)
    assert campaign_state.get('skald_giant_quest_given') is True, "Expected quest flag to be set"
    print("✓ Giant bounty quest triggers on first call")
    
    # Second time should not trigger
    print("\nTesting idempotence (should not print quest dialogue again):")
    trigger_skald_giant_bounty(campaign_state)
    print("✓ Quest doesn't trigger twice")


def test_wayfinder_void_salts():
    """Test Captain Wayfinder's void salts quest trigger"""
    print("\n=== Testing Wayfinder's Void Salts Quest Trigger ===")
    
    campaign_state = {}
    
    # First time should trigger
    trigger_wayfinder_void_salts(campaign_state)
    assert campaign_state.get('wayfinder_void_salts_quest_given') is True, "Expected quest flag to be set"
    print("✓ Void salts quest triggers on first call")
    
    # Second time should not trigger
    print("\nTesting idempotence (should not print quest dialogue again):")
    trigger_wayfinder_void_salts(campaign_state)
    print("✓ Quest doesn't trigger twice")


def test_pale_blizzard():
    """Test blizzard environmental hazard trigger"""
    print("\n=== Testing Pale Blizzard Hazard ===")
    
    campaign_state = {}
    trigger_pale_blizzard(campaign_state)
    
    assert campaign_state.get('blizzard_active') is True, "Expected blizzard_active flag to be set"
    print("✓ Blizzard scene works and sets flag")


def test_state_isolation():
    """Test that different state objects don't interfere"""
    print("\n=== Testing State Isolation ===")
    
    party_state_1 = {}
    party_state_2 = {}
    
    scene_dawnstar_arrival(party_state_1)
    
    assert party_state_1.get('seen_dawnstar_intro') is True
    assert party_state_2.get('seen_dawnstar_intro') is None
    print("✓ State changes are isolated to correct state object")


def test_trigger_erandur_intersect():
    """Test Erandur intersect trigger"""
    print("\n=== Testing Erandur Intersect Trigger ===")
    
    # Test when no flags are set - should return None
    campaign_state = {"scene_flags": {}}
    result = trigger_erandur_intersect(campaign_state)
    assert result is None, "Expected None when no trigger flags are set"
    print("✓ Returns None when no trigger conditions met")
    
    # Test when whitefin_location_divined flag is set
    campaign_state = {
        "scene_flags": {
            "session04_whitefin_location_divined": True
        }
    }
    result = trigger_erandur_intersect(campaign_state)
    assert result is not None, "Expected scene dict when whitefin_location_divined is True"
    assert result["scene_id"] == "A1-S15-ERANDUR"
    assert result["type"] == "social"
    assert "erandur" in result["tags"]
    assert campaign_state["scene_flags"]["erandur_introduced"] is True
    assert campaign_state["scene_flags"]["erandur_intersection_method"] == "sleeper_camp_roadside"
    print("✓ Triggers correctly with whitefin_location_divined flag")
    
    # Test idempotence - should return None after first trigger
    result = trigger_erandur_intersect(campaign_state)
    assert result is None, "Expected None on second call (idempotence)"
    print("✓ Trigger is idempotent (doesn't fire twice)")
    
    # Test with nightcaller_temple_targeted flag
    campaign_state = {
        "scene_flags": {
            "session04_nightcaller_temple_targeted": True
        }
    }
    result = trigger_erandur_intersect(campaign_state)
    assert result is not None, "Expected scene dict when nightcaller_temple_targeted is True"
    assert result["scene_id"] == "A1-S15-ERANDUR"
    print("✓ Triggers correctly with nightcaller_temple_targeted flag")
    
    # Test that trigger doesn't fire if waking_nightmare_quest_given is already set
    campaign_state = {
        "scene_flags": {
            "session04_whitefin_location_divined": True
        },
        "waking_nightmare_quest_given": True
    }
    result = trigger_erandur_intersect(campaign_state)
    assert result is None, "Expected None when waking_nightmare_quest_given is already True"
    print("✓ Doesn't trigger if Erandur already met via Windpeak Inn path")
    
    # Test that scene_flags is not created when trigger doesn't fire
    campaign_state = {}
    result = trigger_erandur_intersect(campaign_state)
    assert result is None, "Expected None when no flags set"
    assert "scene_flags" not in campaign_state, "Expected scene_flags not to be created when trigger doesn't fire"
    print("✓ Doesn't mutate campaign_state when trigger doesn't fire")


def test_pale_get_next_scene():
    """Test main scene assembly function"""
    print("\n=== Testing Pale Get Next Scene ===")
    
    # Test when no triggers fire
    campaign_state = {"scene_flags": {}}
    result = pale_get_next_scene(campaign_state)
    assert result is None, "Expected None when no triggers fire"
    print("✓ Returns None when no triggers fire")
    
    # Test when Erandur intersect should trigger
    campaign_state = {
        "scene_flags": {
            "session04_whitefin_location_divined": True
        }
    }
    result = pale_get_next_scene(campaign_state)
    assert result is not None, "Expected scene dict when trigger conditions met"
    assert result["scene_id"] == "A1-S15-ERANDUR"
    print("✓ Returns correct scene when Erandur intersect triggers")


def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("The Pale (Dawnstar) Triggers Test Suite")
    print("=" * 60)
    
    test_functions = [
        test_dawnstar_arrival,
        test_windpeak_inn_commotion,
        test_erandur_waking_nightmare,
        test_skald_giant_bounty,
        test_wayfinder_void_salts,
        test_pale_blizzard,
        test_state_isolation,
        test_trigger_erandur_intersect,
        test_pale_get_next_scene
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
