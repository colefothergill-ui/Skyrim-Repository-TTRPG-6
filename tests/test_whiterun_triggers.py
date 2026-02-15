#!/usr/bin/env python3
"""
Tests for Whiterun Location Triggers

This module tests the whiterun_location_triggers function to ensure
proper event generation based on location and campaign state.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.whiterun_triggers import whiterun_location_triggers


def test_plains_district_trigger():
    """Test that Plains District triggers appropriate events"""
    print("\n=== Testing Plains District Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = whiterun_location_triggers("whiterun_plains_district", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Plains District"
    assert any("Plains District" in event for event in events), "Expected Plains District description"
    print(f"✓ Plains District trigger works: {events}")


def test_wind_district_trigger():
    """Test that Wind District triggers appropriate events"""
    print("\n=== Testing Wind District Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = whiterun_location_triggers("whiterun_wind_district", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Wind District"
    assert any("Wind District" in event for event in events), "Expected Wind District description"
    assert any("Gildergreen" in event or "Jorrvaskr" in event for event in events), "Expected district landmarks"
    print(f"✓ Wind District trigger works: {events}")


def test_cloud_district_trigger():
    """Test that Cloud District triggers appropriate events"""
    print("\n=== Testing Cloud District Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = whiterun_location_triggers("whiterun_cloud_district", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Cloud District"
    assert any("Cloud District" in event for event in events), "Expected Cloud District description"
    assert any("Dragonsreach" in event for event in events), "Expected Dragonsreach mention"
    print(f"✓ Cloud District trigger works: {events}")


def test_general_whiterun_trigger():
    """Test general Whiterun entrance trigger"""
    print("\n=== Testing General Whiterun Trigger ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = whiterun_location_triggers("whiterun", campaign_state)
    
    assert len(events) > 0, "Expected at least one event for Whiterun"
    assert any("gates" in event.lower() or "whiterun" in event.lower() for event in events), "Expected Whiterun entrance description"
    print(f"✓ General Whiterun trigger works: {events}")


def test_lydia_companion_commentary():
    """Test that Lydia provides commentary when in Whiterun"""
    print("\n=== Testing Lydia Companion Commentary ===")
    
    # Test with Lydia as active companion
    campaign_state = {
        "companions": {
            "active_companions": ["Lydia", "Hadvar"]
        }
    }
    
    events = whiterun_location_triggers("whiterun", campaign_state)
    
    assert len(events) > 0, "Expected events when Lydia is present"
    lydia_event = [e for e in events if "Lydia" in e and "Thane" in e]
    assert len(lydia_event) > 0, "Expected Lydia to comment about being in Whiterun"
    print(f"✓ Lydia commentary works: {lydia_event[0]}")


def test_lydia_commentary_case_insensitive():
    """Test that Lydia detection is case-insensitive"""
    print("\n=== Testing Lydia Commentary (Case Insensitive) ===")
    
    # Test with lowercase lydia
    campaign_state = {
        "companions": {
            "active_companions": ["lydia"]
        }
    }
    
    events = whiterun_location_triggers("Whiterun", campaign_state)
    
    lydia_event = [e for e in events if "Lydia" in e]
    assert len(lydia_event) > 0, "Expected Lydia commentary with lowercase companion name"
    print(f"✓ Case-insensitive Lydia detection works")


def test_lydia_commentary_in_district():
    """Test that Lydia comments in Whiterun districts"""
    print("\n=== Testing Lydia Commentary in Districts ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Lydia"]
        }
    }
    
    # Test in Plains District
    events = whiterun_location_triggers("whiterun_plains_district", campaign_state)
    lydia_event = [e for e in events if "Lydia" in e]
    assert len(lydia_event) > 0, "Expected Lydia to comment in Plains District"
    
    # Test in Wind District
    events = whiterun_location_triggers("whiterun_wind_district", campaign_state)
    lydia_event = [e for e in events if "Lydia" in e]
    assert len(lydia_event) > 0, "Expected Lydia to comment in Wind District"
    
    print(f"✓ Lydia comments in all Whiterun districts")


def test_no_lydia_commentary_outside_whiterun():
    """Test that Lydia doesn't comment when outside Whiterun"""
    print("\n=== Testing No Lydia Commentary Outside Whiterun ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Lydia"]
        }
    }
    
    # Test in a non-Whiterun location
    events = whiterun_location_triggers("riverwood", campaign_state)
    lydia_event = [e for e in events if "Lydia" in e and "Thane" in e]
    
    # Lydia should not comment in non-Whiterun locations
    assert len(lydia_event) == 0, "Lydia should not comment outside Whiterun"
    print(f"✓ Lydia correctly silent outside Whiterun")


def test_no_companion_commentary_without_lydia():
    """Test that no Lydia commentary appears without her as companion"""
    print("\n=== Testing No Commentary Without Lydia ===")
    
    campaign_state = {
        "companions": {
            "active_companions": ["Hadvar", "Ralof"]
        }
    }
    
    events = whiterun_location_triggers("whiterun", campaign_state)
    lydia_event = [e for e in events if "Lydia" in e]
    
    assert len(lydia_event) == 0, "Expected no Lydia commentary without her in party"
    print(f"✓ No Lydia commentary when she's not a companion")


def test_empty_companions_list():
    """Test handling of empty companions list"""
    print("\n=== Testing Empty Companions List ===")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = whiterun_location_triggers("whiterun", campaign_state)
    
    assert len(events) > 0, "Expected events even with no companions"
    lydia_event = [e for e in events if "Lydia" in e]
    assert len(lydia_event) == 0, "Expected no Lydia commentary with empty companions"
    print(f"✓ Handles empty companions list correctly")


def test_missing_companions_key():
    """Test handling of missing companions key in campaign state"""
    print("\n=== Testing Missing Companions Key ===")
    
    campaign_state = {}
    
    events = whiterun_location_triggers("whiterun", campaign_state)
    
    # Should not crash, just return location events without companion commentary
    assert len(events) > 0, "Expected events even without companions key"
    print(f"✓ Handles missing companions key gracefully")


def test_complex_companion_objects():
    """Test with companion as dictionary objects (more realistic)"""
    print("\n=== Testing Complex Companion Objects ===")
    
    # More realistic campaign state with companion objects
    campaign_state = {
        "companions": {
            "active_companions": [
                {
                    "name": "Lydia",
                    "npc_id": "lydia",
                    "loyalty": 70
                },
                {
                    "name": "Hadvar",
                    "npc_id": "hadvar",
                    "loyalty": 65
                }
            ]
        }
    }
    
    events = whiterun_location_triggers("whiterun", campaign_state)
    
    # The function should properly detect Lydia from dictionary companions
    assert len(events) > 0, "Expected events when Lydia dict is present"
    lydia_event = [e for e in events if "Lydia" in e and "Thane" in e]
    assert len(lydia_event) > 0, "Expected Lydia commentary with dictionary companion"
    print(f"✓ Function handles complex companion objects correctly")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Whiterun Triggers Tests")
    print("=" * 60)
    
    tests = [
        test_plains_district_trigger,
        test_wind_district_trigger,
        test_cloud_district_trigger,
        test_general_whiterun_trigger,
        test_lydia_companion_commentary,
        test_lydia_commentary_case_insensitive,
        test_lydia_commentary_in_district,
        test_no_lydia_commentary_outside_whiterun,
        test_no_companion_commentary_without_lydia,
        test_empty_companions_list,
        test_missing_companions_key,
        test_complex_companion_objects,
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
