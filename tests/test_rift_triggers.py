#!/usr/bin/env python3
"""
Tests for Riften (The Rift) Location Triggers

This module tests the rift_location_triggers function to ensure
proper event generation based on location and campaign state.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.rift_triggers import rift_location_triggers


def test_marketplace_trigger():
    """Test that Riften Marketplace triggers appropriate events"""
    print("\n=== Testing Riften Marketplace Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "player": {
            "thieves_guild_member": False
        }
    }
    
    events = rift_location_triggers("riften_marketplace", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Riften Marketplace"
    assert any("marketplace" in event.lower() for event in events), "Expected marketplace description"
    assert any("Black-Briar" in event or "Lake Honrich" in event for event in events), "Expected marketplace details"
    print(f"✓ Marketplace trigger works: Found {len(events)} events")


def test_ratway_trigger():
    """Test that The Ratway triggers appropriate events"""
    print("\n=== Testing The Ratway Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = rift_location_triggers("riften_ratway", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for The Ratway"
    assert any("Ratway" in event for event in events), "Expected Ratway description"
    assert any("Ragged Flagon" in event or "underground" in event.lower() for event in events), "Expected Ratway details"
    print(f"✓ Ratway trigger works: {events[0][:80]}...")


def test_temple_of_mara_trigger():
    """Test that Temple of Mara triggers appropriate events"""
    print("\n=== Testing Temple of Mara Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = rift_location_triggers("riften_temple_of_mara", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Temple of Mara"
    assert any("Temple of Mara" in event or "Mara" in event for event in events), "Expected temple description"
    assert any("love" in event.lower() or "compassion" in event.lower() for event in events), "Expected temple themes"
    print(f"✓ Temple of Mara trigger works")


def test_mistveil_keep_trigger():
    """Test that Mistveil Keep triggers appropriate events"""
    print("\n=== Testing Mistveil Keep Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = rift_location_triggers("riften_mistveil_keep", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Mistveil Keep"
    assert any("Mistveil" in event for event in events), "Expected Mistveil Keep description"
    assert any("Laila Law-Giver" in event or "Maven" in event for event in events), "Expected political figures"
    print(f"✓ Mistveil Keep trigger works")


def test_general_riften_trigger():
    """Test general Riften entrance trigger"""
    print("\n=== Testing General Riften Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = rift_location_triggers("riften", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Riften"
    assert any("riften" in event.lower() for event in events), "Expected Riften entrance description"
    assert any("wooden" in event.lower() or "canal" in event.lower() for event in events), "Expected city details"
    print(f"✓ General Riften trigger works")


def test_rift_forest_trigger():
    """Test The Rift wilderness forest trigger"""
    print("\n=== Testing The Rift Forest Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = rift_location_triggers("the_rift_forest", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Rift forest"
    assert any("autumn" in event.lower() or "golden" in event.lower() for event in events), "Expected autumn forest description"
    print(f"✓ Rift forest trigger works")


def test_lake_honrich_trigger():
    """Test Lake Honrich trigger"""
    print("\n=== Testing Lake Honrich Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = rift_location_triggers("lake_honrich", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Lake Honrich"
    assert any("Honrich" in event or "lake" in event.lower() for event in events), "Expected lake description"
    print(f"✓ Lake Honrich trigger works")


def test_brynjolf_recruitment_trigger():
    """Test Brynjolf recruitment trigger in marketplace"""
    print("\n=== Testing Brynjolf Recruitment Trigger ===")
    
    # Not yet a member of Thieves Guild
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "player": {
            "thieves_guild_member": False
        }
    }
    
    events = rift_location_triggers("riften_marketplace", campaign_state)
    
    # Should get both marketplace description AND Brynjolf approach
    assert len(events) >= 2, "Expected marketplace description plus Brynjolf approach"
    brynjolf_event = [e for e in events if "Brynjolf" in e]
    assert len(brynjolf_event) > 0, "Expected Brynjolf recruitment trigger"
    assert any("honest day's work" in e for e in brynjolf_event), "Expected Brynjolf's signature line"
    print(f"✓ Brynjolf recruitment trigger works")


def test_no_brynjolf_if_guild_member():
    """Test that Brynjolf doesn't approach if already a guild member"""
    print("\n=== Testing No Brynjolf for Guild Members ===")
    
    # Already a member of Thieves Guild
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "player": {
            "thieves_guild_member": True
        }
    }
    
    events = rift_location_triggers("riften_marketplace", campaign_state)
    
    # Should get marketplace description but NOT Brynjolf approach
    brynjolf_event = [e for e in events if "Brynjolf" in e and "honest day's work" in e]
    assert len(brynjolf_event) == 0, "Brynjolf should not approach guild members"
    print(f"✓ No Brynjolf approach for guild members")


def test_iona_companion_commentary():
    """Test that Iona provides commentary when in Riften"""
    print("\n=== Testing Iona Companion Commentary ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Iona"]
        }
    }
    
    events = rift_location_triggers("riften", campaign_state)
    
    assert len(events) > 0, "Expected events when Iona is present"
    iona_event = [e for e in events if "Iona" in e]
    assert len(iona_event) > 0, "Expected Iona to comment about being in Riften"
    assert any("housecarl" in e.lower() or "Thane" in e for e in iona_event), "Expected Iona's role mentioned"
    print(f"✓ Iona commentary works: {iona_event[0][:80]}...")


def test_iona_commentary_case_insensitive():
    """Test that Iona detection is case-insensitive"""
    print("\n=== Testing Iona Commentary (Case Insensitive) ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["iona"]
        }
    }
    
    events = rift_location_triggers("Riften", campaign_state)
    
    iona_event = [e for e in events if "Iona" in e]
    assert len(iona_event) > 0, "Expected Iona commentary with lowercase companion name"
    print(f"✓ Case-insensitive Iona detection works")


def test_iona_commentary_in_districts():
    """Test that Iona comments in Riften districts"""
    print("\n=== Testing Iona Commentary in Districts ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Iona"]
        }
    }
    
    # Test in marketplace
    events = rift_location_triggers("riften_marketplace", campaign_state)
    iona_event = [e for e in events if "Iona" in e]
    assert len(iona_event) > 0, "Expected Iona to comment in marketplace"
    
    # Test in Mistveil Keep
    events = rift_location_triggers("riften_mistveil_keep", campaign_state)
    iona_event = [e for e in events if "Iona" in e]
    assert len(iona_event) > 0, "Expected Iona to comment in Mistveil Keep"
    
    print(f"✓ Iona comments in all Riften districts")


def test_no_iona_commentary_outside_riften():
    """Test that Iona doesn't comment when outside Riften"""
    print("\n=== Testing No Iona Commentary Outside Riften ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Iona"]
        }
    }
    
    # Test in a non-Riften location
    events = rift_location_triggers("whiterun", campaign_state)
    iona_event = [e for e in events if "Iona" in e]
    
    assert len(iona_event) == 0, "Iona should not comment outside Riften"
    print(f"✓ Iona correctly silent outside Riften")


def test_complex_companion_objects():
    """Test with companion as dictionary objects"""
    print("\n=== Testing Complex Companion Objects ===")
    
    campaign_state = {
        "companions": {
            "active_companions": [
                {
                    "name": "Iona",
                    "npc_id": "iona",
                    "loyalty": 75
                }
            ]
        }
    }
    
    events = rift_location_triggers("riften", campaign_state)
    
    assert len(events) > 0, "Expected events when Iona dict is present"
    iona_event = [e for e in events if "Iona" in e]
    assert len(iona_event) > 0, "Expected Iona commentary with dictionary companion"
    print(f"✓ Function handles complex companion objects correctly")


def test_multiple_triggers_same_location():
    """Test that multiple triggers can fire for the same location"""
    print("\n=== Testing Multiple Triggers ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Iona"]
        },
        "player": {
            "thieves_guild_member": False
        }
    }
    
    # In marketplace with Iona, not yet in guild
    events = rift_location_triggers("riften_marketplace", campaign_state)
    
    # Should get: marketplace description, Brynjolf approach, AND Iona commentary
    assert len(events) >= 3, f"Expected at least 3 events (marketplace, Brynjolf, Iona), got {len(events)}"
    assert any("marketplace" in e.lower() for e in events), "Expected marketplace description"
    assert any("Brynjolf" in e for e in events), "Expected Brynjolf trigger"
    assert any("Iona" in e for e in events), "Expected Iona commentary"
    print(f"✓ Multiple triggers work correctly: {len(events)} events total")


def test_empty_companions_list():
    """Test handling of empty companions list"""
    print("\n=== Testing Empty Companions List ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = rift_location_triggers("riften", campaign_state)
    
    assert len(events) > 0, "Expected events even with no companions"
    iona_event = [e for e in events if "Iona" in e]
    assert len(iona_event) == 0, "Expected no Iona commentary with empty companions"
    print(f"✓ Handles empty companions list correctly")


def test_missing_campaign_state_keys():
    """Test handling of missing keys in campaign state"""
    print("\n=== Testing Missing Campaign State Keys ===")
    
    # No companions key at all
    campaign_state = {}
    events = rift_location_triggers("riften", campaign_state)
    assert len(events) > 0, "Expected events even without companions key"
    
    # No player key
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    events = rift_location_triggers("riften_marketplace", campaign_state)
    # Should still trigger Brynjolf since thieves_guild_member defaults to False
    assert len(events) > 0, "Expected events even without player key"
    
    print(f"✓ Handles missing campaign state keys gracefully")


def test_ragged_flagon_variant():
    """Test that 'ragged flagon' location also triggers Ratway event"""
    print("\n=== Testing Ragged Flagon Variant ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = rift_location_triggers("riften_ragged_flagon", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Ragged Flagon"
    assert any("Ratway" in event or "Ragged Flagon" in event for event in events), "Expected underground description"
    print(f"✓ Ragged Flagon variant works")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Riften (The Rift) Triggers Tests")
    print("=" * 60)
    
    tests = [
        test_marketplace_trigger,
        test_ratway_trigger,
        test_temple_of_mara_trigger,
        test_mistveil_keep_trigger,
        test_general_riften_trigger,
        test_rift_forest_trigger,
        test_lake_honrich_trigger,
        test_brynjolf_recruitment_trigger,
        test_no_brynjolf_if_guild_member,
        test_iona_companion_commentary,
        test_iona_commentary_case_insensitive,
        test_iona_commentary_in_districts,
        test_no_iona_commentary_outside_riften,
        test_complex_companion_objects,
        test_multiple_triggers_same_location,
        test_empty_companions_list,
        test_missing_campaign_state_keys,
        test_ragged_flagon_variant,
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
