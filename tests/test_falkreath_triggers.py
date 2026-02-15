#!/usr/bin/env python3
"""
Tests for Falkreath Location Triggers

This module tests the Falkreath trigger functions to ensure
proper scene generation and quest trigger behavior.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.falkreath_triggers import (
    scene_falkreath_arrival,
    scene_falkreath_graveyard,
    trigger_siddgeir_bandit_bounty,
    trigger_dengeir_vampire_hunt,
    trigger_dark_brotherhood_contact,
    scene_astrid_abduction,
    trigger_sanctuary_discovery,
    trigger_sanctuary_entry,
    trigger_sinding_jail_encounter,
    scene_bloated_mans_grotto,
    scene_moonlight_kill_sinding,
    scene_moonlight_spare_sinding
)


def test_falkreath_arrival():
    """Test Falkreath arrival scene"""
    print("\n=== Testing Falkreath Arrival Scene ===")
    
    party_state = {}
    scene_falkreath_arrival(party_state)
    
    assert party_state.get('seen_falkreath_intro') is True, "Expected seen_falkreath_intro flag to be set"
    print("✓ Falkreath arrival scene works and sets flag")


def test_graveyard_scene():
    """Test Falkreath graveyard scene"""
    print("\n=== Testing Graveyard Scene ===")
    
    party_state = {}
    scene_falkreath_graveyard(party_state)
    
    assert party_state.get('witnessed_graveyard_scene') is True, "Expected witnessed_graveyard_scene flag to be set"
    print("✓ Graveyard scene works and sets flag")


def test_siddgeir_bandit_bounty():
    """Test Siddgeir's bandit bounty quest trigger"""
    print("\n=== Testing Siddgeir Bandit Bounty ===")
    
    campaign_state = {}
    trigger_siddgeir_bandit_bounty(campaign_state)
    
    assert campaign_state.get('falkreath_bandit_quest_given') is True, "Expected quest flag to be set"
    print("✓ Siddgeir bandit bounty trigger works")
    
    # Test that it doesn't trigger again
    campaign_state_copy = campaign_state.copy()
    trigger_siddgeir_bandit_bounty(campaign_state)
    assert campaign_state == campaign_state_copy, "Quest should not trigger twice"
    print("✓ Quest correctly does not trigger twice")


def test_dengeir_vampire_hunt():
    """Test Dengeir's vampire hunt quest trigger"""
    print("\n=== Testing Dengeir Vampire Hunt ===")
    
    campaign_state = {}
    trigger_dengeir_vampire_hunt(campaign_state)
    
    assert campaign_state.get('dengeir_vampire_quest_given') is True, "Expected quest flag to be set"
    print("✓ Dengeir vampire hunt trigger works")
    
    # Test that it doesn't trigger again
    campaign_state_copy = campaign_state.copy()
    trigger_dengeir_vampire_hunt(campaign_state)
    assert campaign_state == campaign_state_copy, "Quest should not trigger twice"
    print("✓ Quest correctly does not trigger twice")


def test_dark_brotherhood_contact_innocence_lost():
    """Test Dark Brotherhood contact after Innocence Lost quest"""
    print("\n=== Testing DB Contact (Innocence Lost) ===")
    
    party_actions = {'innocence_lost_completed': True}
    campaign_state = {}
    
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    
    assert campaign_state.get('dark_brotherhood_contacted') is True, "Expected DB contact flag to be set"
    print("✓ Dark Brotherhood contact triggers after Innocence Lost")


def test_dark_brotherhood_contact_murder():
    """Test Dark Brotherhood contact after murder"""
    print("\n=== Testing DB Contact (Murder) ===")
    
    party_actions = {'murder_committed': True}
    campaign_state = {}
    
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    
    assert campaign_state.get('dark_brotherhood_contacted') is True, "Expected DB contact flag to be set"
    print("✓ Dark Brotherhood contact triggers after murder")


def test_dark_brotherhood_no_contact():
    """Test that DB contact doesn't trigger without qualifying actions"""
    print("\n=== Testing DB No Contact (No Qualifying Actions) ===")
    
    party_actions = {}
    campaign_state = {}
    
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    
    assert campaign_state.get('dark_brotherhood_contacted') is not True, "DB contact should not trigger"
    print("✓ Dark Brotherhood correctly does not contact without qualifying actions")


def test_dark_brotherhood_contact_once():
    """Test that DB contact only happens once"""
    print("\n=== Testing DB Contact Only Once ===")
    
    party_actions = {'murder_committed': True}
    campaign_state = {}
    
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    assert campaign_state.get('dark_brotherhood_contacted') is True
    
    # Try to trigger again
    campaign_state_copy = campaign_state.copy()
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    assert campaign_state == campaign_state_copy, "DB contact should not trigger twice"
    print("✓ Dark Brotherhood contact correctly triggers only once")


def test_astrid_abduction():
    """Test Astrid abduction scene"""
    print("\n=== Testing Astrid Abduction Scene ===")
    
    campaign_state = {'dark_brotherhood_contacted': True}
    scene_astrid_abduction(campaign_state)
    
    assert campaign_state.get('astrid_abduction_scene') is True, "Expected abduction scene flag to be set"
    print("✓ Astrid abduction scene works")


def test_astrid_abduction_no_contact():
    """Test that abduction doesn't happen without DB contact"""
    print("\n=== Testing Astrid Abduction (No Contact) ===")
    
    campaign_state = {}
    scene_astrid_abduction(campaign_state)
    
    assert campaign_state.get('astrid_abduction_scene') is not True, "Abduction should not occur without DB contact"
    print("✓ Astrid abduction correctly doesn't trigger without DB contact")


def test_astrid_abduction_already_joined():
    """Test that abduction doesn't happen if already joined DB"""
    print("\n=== Testing Astrid Abduction (Already Joined) ===")
    
    campaign_state = {
        'dark_brotherhood_contacted': True,
        'dark_brotherhood_joined': True
    }
    scene_astrid_abduction(campaign_state)
    
    assert campaign_state.get('astrid_abduction_scene') is not True, "Abduction should not occur if already joined DB"
    print("✓ Astrid abduction correctly doesn't trigger for existing members")


def test_sanctuary_discovery():
    """Test sanctuary discovery trigger"""
    print("\n=== Testing Sanctuary Discovery ===")
    
    player_location = "Dark Brotherhood Sanctuary entrance"
    campaign_state = {}
    
    trigger_sanctuary_discovery(player_location, campaign_state)
    
    assert campaign_state.get('dark_brotherhood_sanctuary_discovered') is True, "Expected sanctuary discovered flag"
    print("✓ Sanctuary discovery trigger works")


def test_sanctuary_discovery_once():
    """Test that sanctuary discovery only triggers once"""
    print("\n=== Testing Sanctuary Discovery Only Once ===")
    
    player_location = "Dark Brotherhood Sanctuary entrance"
    campaign_state = {}
    
    trigger_sanctuary_discovery(player_location, campaign_state)
    campaign_state_copy = campaign_state.copy()
    
    # Try to trigger again
    trigger_sanctuary_discovery(player_location, campaign_state)
    assert campaign_state == campaign_state_copy, "Sanctuary discovery should not trigger twice"
    print("✓ Sanctuary discovery correctly triggers only once")


def test_sanctuary_entry():
    """Test sanctuary entry scene"""
    print("\n=== Testing Sanctuary Entry ===")
    
    campaign_state = {'dark_brotherhood_member': True}
    trigger_sanctuary_entry(campaign_state)
    
    assert campaign_state.get('dark_brotherhood_sanctuary_entered') is True, "Expected sanctuary entered flag"
    print("✓ Sanctuary entry trigger works")


def test_sanctuary_entry_no_member():
    """Test that sanctuary entry doesn't trigger for non-members"""
    print("\n=== Testing Sanctuary Entry (Non-Member) ===")
    
    campaign_state = {}
    trigger_sanctuary_entry(campaign_state)
    
    assert campaign_state.get('dark_brotherhood_sanctuary_entered') is not True, "Entry should not occur for non-members"
    print("✓ Sanctuary entry correctly doesn't trigger for non-members")


def test_scene_functions_with_none_state():
    """Test that scene functions handle None state gracefully"""
    print("\n=== Testing Scene Functions with None State ===")
    
    try:
        scene_falkreath_arrival(None)
        scene_falkreath_graveyard(None)
        print("✓ Scene functions handle None state gracefully")
    except Exception as e:
        raise AssertionError(f"Scene functions should handle None state: {e}")


def test_sinding_jail_encounter():
    """Test Sinding's jail encounter trigger"""
    print("\n=== Testing Sinding Jail Encounter ===")
    
    campaign_state = {}
    trigger_sinding_jail_encounter(campaign_state)
    
    assert campaign_state.get('ill_met_moonlight_started') is True, "Expected ill_met_moonlight_started flag to be set"
    print("✓ Sinding jail encounter trigger works")
    
    # Test that it doesn't trigger again
    campaign_state_copy = campaign_state.copy()
    trigger_sinding_jail_encounter(campaign_state)
    assert campaign_state == campaign_state_copy, "Encounter should not trigger twice"
    print("✓ Encounter correctly does not trigger twice")


def test_bloated_mans_grotto():
    """Test Bloated Man's Grotto scene"""
    print("\n=== Testing Bloated Man's Grotto Scene ===")
    
    campaign_state = {'ill_met_moonlight_started': True}
    scene_bloated_mans_grotto(campaign_state)
    
    assert campaign_state.get('bloated_mans_grotto_encountered') is True, "Expected grotto encountered flag"
    print("✓ Bloated Man's Grotto scene works")


def test_bloated_mans_grotto_no_start():
    """Test that grotto scene doesn't trigger without quest start"""
    print("\n=== Testing Grotto Scene (No Quest Start) ===")
    
    campaign_state = {}
    scene_bloated_mans_grotto(campaign_state)
    
    assert campaign_state.get('bloated_mans_grotto_encountered') is not True, "Grotto should not trigger without quest start"
    print("✓ Grotto scene correctly doesn't trigger without quest start")


def test_moonlight_kill_sinding():
    """Test killing Sinding outcome"""
    print("\n=== Testing Kill Sinding Outcome ===")
    
    campaign_state = {'ill_met_moonlight_started': True}
    scene_moonlight_kill_sinding(campaign_state)
    
    assert campaign_state.get('ill_met_moonlight_completed') is True, "Expected quest completed flag"
    assert campaign_state.get('ill_met_moonlight_outcome') == 'sinding_killed', "Expected outcome to be sinding_killed"
    assert campaign_state.get('artifact_saviors_hide_obtained') is True, "Expected Savior's Hide obtained flag"
    print("✓ Kill Sinding outcome works and grants Savior's Hide")


def test_moonlight_spare_sinding():
    """Test sparing Sinding outcome"""
    print("\n=== Testing Spare Sinding Outcome ===")
    
    campaign_state = {'ill_met_moonlight_started': True}
    scene_moonlight_spare_sinding(campaign_state)
    
    assert campaign_state.get('ill_met_moonlight_completed') is True, "Expected quest completed flag"
    assert campaign_state.get('ill_met_moonlight_outcome') == 'sinding_spared', "Expected outcome to be sinding_spared"
    assert campaign_state.get('artifact_ring_of_hircine_obtained') is True, "Expected Ring of Hircine obtained flag"
    print("✓ Spare Sinding outcome works and grants Ring of Hircine")


def test_moonlight_outcomes_not_both():
    """Test that both outcomes cannot be achieved simultaneously"""
    print("\n=== Testing Mutually Exclusive Outcomes ===")
    
    campaign_state = {'ill_met_moonlight_started': True}
    
    # Complete with kill outcome
    scene_moonlight_kill_sinding(campaign_state)
    assert campaign_state.get('ill_met_moonlight_completed') is True
    
    # Try to complete with spare outcome (should not work as quest is already completed)
    scene_moonlight_spare_sinding(campaign_state)
    
    # The spare function should not change anything because quest is already completed
    assert campaign_state.get('ill_met_moonlight_outcome') == 'sinding_killed', "Outcome should remain sinding_killed"
    assert campaign_state.get('artifact_ring_of_hircine_obtained') is not True, "Should not get Ring if already completed quest"
    print("✓ Quest outcomes are mutually exclusive")


def test_moonlight_quest_sequence():
    """Test the full quest sequence"""
    print("\n=== Testing Full Moonlight Quest Sequence ===")
    
    campaign_state = {}
    
    # Step 1: Jail encounter
    trigger_sinding_jail_encounter(campaign_state)
    assert campaign_state.get('ill_met_moonlight_started') is True
    print("  ✓ Step 1: Quest started at jail")
    
    # Step 2: Grotto scene
    scene_bloated_mans_grotto(campaign_state)
    assert campaign_state.get('bloated_mans_grotto_encountered') is True
    print("  ✓ Step 2: Grotto encounter triggered")
    
    # Step 3: Resolution (spare path)
    scene_moonlight_spare_sinding(campaign_state)
    assert campaign_state.get('ill_met_moonlight_completed') is True
    assert campaign_state.get('artifact_ring_of_hircine_obtained') is True
    print("  ✓ Step 3: Quest resolved with spare outcome")
    
    print("✓ Full quest sequence works correctly")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Falkreath Triggers Tests")
    print("=" * 60)
    
    tests = [
        test_falkreath_arrival,
        test_graveyard_scene,
        test_siddgeir_bandit_bounty,
        test_dengeir_vampire_hunt,
        test_dark_brotherhood_contact_innocence_lost,
        test_dark_brotherhood_contact_murder,
        test_dark_brotherhood_no_contact,
        test_dark_brotherhood_contact_once,
        test_astrid_abduction,
        test_astrid_abduction_no_contact,
        test_astrid_abduction_already_joined,
        test_sanctuary_discovery,
        test_sanctuary_discovery_once,
        test_sanctuary_entry,
        test_sanctuary_entry_no_member,
        test_scene_functions_with_none_state,
        test_sinding_jail_encounter,
        test_bloated_mans_grotto,
        test_bloated_mans_grotto_no_start,
        test_moonlight_kill_sinding,
        test_moonlight_spare_sinding,
        test_moonlight_outcomes_not_both,
        test_moonlight_quest_sequence,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"✗ {test.__name__} failed: {e}")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} error: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
