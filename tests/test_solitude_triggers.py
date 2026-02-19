#!/usr/bin/env python3
"""
Tests for Solitude Location Triggers

This module tests the solitude_location_triggers function to ensure
proper event generation based on location and campaign state, including
site-specific triggers and companion commentary.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.solitude_triggers import solitude_location_triggers


def test_blue_palace_trigger():
    """Test that Blue Palace triggers appropriate events"""
    print("\n=== Testing Blue Palace Trigger ===")

    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }

    events = solitude_location_triggers("blue palace", campaign_state)

    assert len(events) > 0, "Expected at least one event for the Blue Palace"
    assert any("Blue Palace" in event for event in events), "Expected Blue Palace description"
    assert any("Elisif" in event for event in events), "Expected mention of Elisif the Fair"
    print(f"✓ Blue Palace trigger works: {events}")


def test_castle_dour_trigger():
    """Test that Castle Dour triggers appropriate events"""
    print("\n=== Testing Castle Dour Trigger ===")

    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }

    events = solitude_location_triggers("castle dour", campaign_state)

    assert len(events) > 0, "Expected at least one event for Castle Dour"
    assert any("Castle Dour" in event for event in events), "Expected Castle Dour description"
    assert any("Imperial" in event or "Legion" in event for event in events), "Expected Imperial/Legion mention"
    print(f"✓ Castle Dour trigger works: {events}")


def test_winking_skeever_trigger():
    """Test that Winking Skeever triggers appropriate events"""
    print("\n=== Testing Winking Skeever Trigger ===")

    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }

    events = solitude_location_triggers("winking skeever", campaign_state)

    assert len(events) > 0, "Expected at least one event for the Winking Skeever"
    assert any("Winking Skeever" in event or "inn" in event.lower() or "hearth" in event.lower() for event in events), "Expected inn description"
    assert any("Dervorin" in event for event in events), "Expected mention of Dervorin"
    print(f"✓ Winking Skeever trigger works: {events}")


def test_companion_marcurio_commentary():
    """Test that Marcurio provides commentary when entering Solitude"""
    print("\n=== Testing Marcurio Companion Commentary ===")

    campaign_state = {
        "companions": {
            "active_companions": ["Marcurio"]
        }
    }

    events = solitude_location_triggers("solitude", campaign_state)

    assert len(events) > 0, "Expected at least one event"
    assert any("Marcurio" in event for event in events), "Expected Marcurio commentary"
    print(f"✓ Marcurio commentary trigger works: {events}")


def test_companion_marcurio_dict_format():
    """Test that Marcurio in dict format provides commentary"""
    print("\n=== Testing Marcurio Companion (Dict Format) ===")

    campaign_state = {
        "companions": {
            "active_companions": [
                {"name": "Marcurio", "npc_id": "marcurio"}
            ]
        }
    }

    events = solitude_location_triggers("solitude", campaign_state)

    assert len(events) > 0, "Expected at least one event"
    assert any("Marcurio" in event for event in events), "Expected Marcurio commentary (dict format)"
    print(f"✓ Marcurio (dict format) commentary trigger works: {events}")


def test_marcurio_only_in_solitude():
    """Test that Marcurio commentary only fires when 'solitude' is in the location"""
    print("\n=== Testing Marcurio Only Fires in Solitude ===")

    campaign_state = {
        "companions": {
            "active_companions": ["Marcurio"]
        }
    }

    # Blue Palace doesn't contain 'solitude' in the string itself
    events = solitude_location_triggers("blue palace", campaign_state)

    assert not any("Marcurio" in event for event in events), "Marcurio should not trigger at blue palace location string"
    print(f"✓ Marcurio commentary does not fire outside Solitude: {events}")


def test_no_events_for_unrelated_location():
    """Test that unrelated locations produce no events"""
    print("\n=== Testing No Events for Unrelated Location ===")

    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }

    events = solitude_location_triggers("whiterun", campaign_state)

    assert len(events) == 0, "Expected no events for unrelated location"
    print(f"✓ No events for unrelated location: {events}")


def test_empty_companions():
    """Test that triggers work with no companions"""
    print("\n=== Testing Empty Companions ===")

    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }

    events = solitude_location_triggers("solitude blue palace", campaign_state)

    # Should still generate Blue Palace event even with no companions
    assert any("Blue Palace" in event for event in events), "Expected Blue Palace event with no companions"
    print(f"✓ Triggers work with empty companions: {events}")


def test_missing_campaign_state():
    """Test that triggers handle missing/empty campaign state gracefully"""
    print("\n=== Testing Missing Campaign State ===")

    campaign_state = {}

    events = solitude_location_triggers("blue palace", campaign_state)

    assert len(events) > 0, "Expected at least one event even with empty campaign state"
    assert any("Blue Palace" in event for event in events), "Expected Blue Palace description"
    print(f"✓ Triggers handle missing campaign state gracefully: {events}")


def test_multiple_triggers_same_location():
    """Test that multiple triggers can fire for a location matching several patterns"""
    print("\n=== Testing Multiple Triggers for Combined Location ===")

    campaign_state = {
        "companions": {
            "active_companions": ["Marcurio"]
        }
    }

    # 'solitude blue palace' matches both blue_palace and the marcurio+solitude check
    events = solitude_location_triggers("solitude blue palace", campaign_state)

    assert any("Blue Palace" in event for event in events), "Expected Blue Palace event"
    assert any("Marcurio" in event for event in events), "Expected Marcurio commentary"
    print(f"✓ Multiple triggers fire for combined location: {events}")


def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("Running Solitude Location Trigger Tests")
    print("=" * 60)

    test_functions = [
        test_blue_palace_trigger,
        test_castle_dour_trigger,
        test_winking_skeever_trigger,
        test_companion_marcurio_commentary,
        test_companion_marcurio_dict_format,
        test_marcurio_only_in_solitude,
        test_no_events_for_unrelated_location,
        test_empty_companions,
        test_missing_campaign_state,
        test_multiple_triggers_same_location,
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
