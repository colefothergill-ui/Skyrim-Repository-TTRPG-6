#!/usr/bin/env python3
"""
Tests for Markarth and The Reach Location Triggers

This module tests the markarth_location_triggers function to ensure
proper event generation based on location and campaign state.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.markarth_triggers import markarth_location_triggers


def test_understone_keep_trigger():
    """Test that Understone Keep triggers appropriate events"""
    print("\n=== Testing Understone Keep Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("markarth_understone_keep", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Understone Keep"
    assert any("Understone Keep" in event for event in events), "Expected Understone Keep description"
    assert any("Dwemer" in event for event in events), "Expected Dwemer mention"
    assert any("Igmund" in event for event in events), "Expected Jarl Igmund mention"
    print(f"✓ Understone Keep trigger works: {events[0][:100]}...")


def test_temple_dibella_trigger():
    """Test that Temple of Dibella triggers appropriate events"""
    print("\n=== Testing Temple of Dibella Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("markarth_temple_dibella", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Temple of Dibella"
    assert any("Dibella" in event for event in events), "Expected Dibella mention"
    assert any("temple" in event.lower() for event in events), "Expected temple description"
    print(f"✓ Temple of Dibella trigger works: {events[0][:100]}...")


def test_warrens_trigger():
    """Test that The Warrens triggers appropriate events"""
    print("\n=== Testing The Warrens Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("markarth_warrens", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for The Warrens"
    assert any("Warrens" in event for event in events), "Expected Warrens description"
    assert any("tunnel" in event.lower() or "dimly" in event.lower() for event in events), "Expected slum atmosphere"
    print(f"✓ The Warrens trigger works: {events[0][:100]}...")


def test_treasury_house_trigger():
    """Test that Treasury House triggers appropriate events"""
    print("\n=== Testing Treasury House Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("markarth_treasury_house", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Treasury House"
    assert any("Treasury House" in event or "Silver-Blood" in event for event in events), "Expected Treasury House/Silver-Blood mention"
    print(f"✓ Treasury House trigger works: {events[0][:100]}...")


def test_silver_blood_inn_trigger():
    """Test that Silver-Blood Inn triggers appropriate events"""
    print("\n=== Testing Silver-Blood Inn Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("markarth_silver-blood_inn", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Silver-Blood Inn"
    assert any("inn" in event.lower() or "Silver-Blood" in event for event in events), "Expected inn description"
    print(f"✓ Silver-Blood Inn trigger works: {events[0][:100]}...")


def test_general_markarth_trigger():
    """Test general Markarth entrance trigger"""
    print("\n=== Testing General Markarth Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("markarth", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Markarth"
    assert any("gates" in event.lower() or "markarth" in event.lower() for event in events), "Expected Markarth entrance description"
    print(f"✓ General Markarth trigger works: {events[0][:100]}...")


def test_karthspire_trigger():
    """Test Karthspire wilderness location trigger"""
    print("\n=== Testing Karthspire Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("karthspire", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Karthspire"
    assert any("Karthspire" in event for event in events), "Expected Karthspire description"
    assert any("Forsworn" in event for event in events), "Expected Forsworn mention"
    print(f"✓ Karthspire trigger works: {events[0][:100]}...")


def test_hag_rock_redoubt_trigger():
    """Test Hag Rock Redoubt location trigger"""
    print("\n=== Testing Hag Rock Redoubt Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("hag_rock_redoubt", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Hag Rock Redoubt"
    assert any("Hag Rock" in event for event in events), "Expected Hag Rock description"
    assert any("Forsworn" in event or "Briarheart" in event for event in events), "Expected Forsworn/Briarheart mention"
    print(f"✓ Hag Rock Redoubt trigger works: {events[0][:100]}...")


def test_druadach_redoubt_trigger():
    """Test Druadach Redoubt location trigger"""
    print("\n=== Testing Druadach Redoubt Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("druadach_redoubt", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Druadach Redoubt"
    assert any("Druadach" in event for event in events), "Expected Druadach description"
    print(f"✓ Druadach Redoubt trigger works: {events[0][:100]}...")


def test_lost_valley_redoubt_trigger():
    """Test Lost Valley Redoubt location trigger"""
    print("\n=== Testing Lost Valley Redoubt Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("lost_valley_redoubt", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Lost Valley Redoubt"
    assert any("Lost Valley" in event for event in events), "Expected Lost Valley description"
    assert any("Hagraven" in event or "waterfall" in event.lower() for event in events), "Expected Hagraven or waterfall mention"
    print(f"✓ Lost Valley Redoubt trigger works: {events[0][:100]}...")


def test_nchuand_zel_trigger():
    """Test Nchuand-Zel Dwemer ruin trigger"""
    print("\n=== Testing Nchuand-Zel Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("nchuand-zel", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Nchuand-Zel"
    assert any("Nchuand-Zel" in event or "Dwemer" in event for event in events), "Expected Nchuand-Zel/Dwemer description"
    print(f"✓ Nchuand-Zel trigger works: {events[0][:100]}...")


def test_abandoned_house_quest_hook():
    """Test Abandoned House (House of Horrors) quest hook"""
    print("\n=== Testing Abandoned House Quest Hook ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "daedric_princes": {}  # No Molag Bal quest yet
    }
    
    events = markarth_location_triggers("markarth_abandoned_house", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Abandoned House"
    assert any("abandoned house" in event.lower() or "molag" in event.lower() or "malevolent" in event.lower() for event in events), "Expected House of Horrors quest hook"
    print(f"✓ Abandoned House quest hook works")


def test_abandoned_house_no_trigger_when_quest_done():
    """Test that Abandoned House doesn't trigger if Molag Bal quest is done"""
    print("\n=== Testing Abandoned House No Trigger When Quest Done ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "daedric_princes": {
            "molag": "completed"
        }
    }
    
    events = markarth_location_triggers("markarth_abandoned_house", campaign_state)
    
    # Should not have the special Molag Bal trigger
    molag_events = [e for e in events if "malevolent" in e.lower() or "molag" in e.lower()]
    assert len(molag_events) == 0, "Expected no Molag Bal quest hook when quest is done"
    print(f"✓ Abandoned House correctly doesn't trigger when quest done")


def test_nepos_house_quest_hook():
    """Test Nepos's House (Forsworn Conspiracy) quest hook"""
    print("\n=== Testing Nepos's House Quest Hook ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("nepos_house", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Nepos's House"
    assert any("Nepos" in event for event in events), "Expected Nepos mention"
    print(f"✓ Nepos's House quest hook works: {events[0][:100]}...")


def test_cidhna_mine_quest_hook():
    """Test Cidhna Mine (No One Escapes Cidhna Mine) quest hook"""
    print("\n=== Testing Cidhna Mine Quest Hook ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("markarth_cidhna_mine", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Cidhna Mine"
    assert any("Cidhna Mine" in event or "prison" in event.lower() for event in events), "Expected Cidhna Mine description"
    assert any("King in Rags" in event or "escape" in event.lower() for event in events), "Expected quest hook"
    print(f"✓ Cidhna Mine quest hook works: {events[0][:100]}...")


def test_companion_commentary():
    """Test companion commentary for Reach-native follower"""
    print("\n=== Testing Companion Commentary ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Illisif"]
        }
    }
    
    events = markarth_location_triggers("markarth", campaign_state)
    
    # Should have both general Markarth trigger and Illisif commentary
    assert len(events) >= 2, "Expected at least location event and companion commentary"
    illisif_event = [e for e in events if "Illisif" in e]
    assert len(illisif_event) > 0, "Expected Illisif to comment about Markarth"
    print(f"✓ Companion commentary works")


def test_no_companion_commentary_without_companion():
    """Test that no companion commentary appears without specific companion"""
    print("\n=== Testing No Companion Commentary ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Lydia", "Hadvar"]
        }
    }
    
    events = markarth_location_triggers("markarth", campaign_state)
    
    illisif_event = [e for e in events if "Illisif" in e]
    assert len(illisif_event) == 0, "Expected no Illisif commentary without her in party"
    print(f"✓ No companion commentary when companion not present")


def test_empty_companions_list():
    """Test handling of empty companions list"""
    print("\n=== Testing Empty Companions List ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = markarth_location_triggers("markarth", campaign_state)
    
    assert len(events) > 0, "Expected events even with no companions"
    print(f"✓ Handles empty companions list correctly")


def test_missing_companions_key():
    """Test handling of missing companions key in campaign state"""
    print("\n=== Testing Missing Companions Key ===")
    
    campaign_state = {}
    
    events = markarth_location_triggers("markarth", campaign_state)
    
    # Should not crash, just return location events without companion commentary
    assert len(events) > 0, "Expected events even without companions key"
    print(f"✓ Handles missing companions key gracefully")


def test_case_insensitive_location():
    """Test that location matching is case-insensitive"""
    print("\n=== Testing Case-Insensitive Location Matching ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    # Test with different cases
    events_lower = markarth_location_triggers("markarth", campaign_state)
    events_upper = markarth_location_triggers("MARKARTH", campaign_state)
    events_mixed = markarth_location_triggers("Markarth", campaign_state)
    
    assert len(events_lower) > 0, "Expected events with lowercase location"
    assert len(events_upper) > 0, "Expected events with uppercase location"
    assert len(events_mixed) > 0, "Expected events with mixed case location"
    print(f"✓ Case-insensitive location matching works")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Markarth and The Reach Triggers Tests")
    print("=" * 60)
    
    tests = [
        test_understone_keep_trigger,
        test_temple_dibella_trigger,
        test_warrens_trigger,
        test_treasury_house_trigger,
        test_silver_blood_inn_trigger,
        test_general_markarth_trigger,
        test_karthspire_trigger,
        test_hag_rock_redoubt_trigger,
        test_druadach_redoubt_trigger,
        test_lost_valley_redoubt_trigger,
        test_nchuand_zel_trigger,
        test_abandoned_house_quest_hook,
        test_abandoned_house_no_trigger_when_quest_done,
        test_nepos_house_quest_hook,
        test_cidhna_mine_quest_hook,
        test_companion_commentary,
        test_no_companion_commentary_without_companion,
        test_empty_companions_list,
        test_missing_companions_key,
        test_case_insensitive_location,
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
