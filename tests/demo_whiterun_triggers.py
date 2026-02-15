#!/usr/bin/env python3
"""
Demo script showing how to use Whiterun location triggers

This demonstrates the companion commentary placeholder functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.whiterun_triggers import whiterun_location_triggers


def demo_scenario_1():
    """Demo: Player enters Whiterun without Lydia"""
    print("\n" + "="*60)
    print("SCENARIO 1: Entering Whiterun (No Companions)")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    print("\nPlayer Location: Whiterun")
    print("\nActive Companions: None")
    print("\nTriggered Events:")
    
    events = whiterun_location_triggers("whiterun", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event}")


def demo_scenario_2():
    """Demo: Player enters Whiterun with Lydia"""
    print("\n" + "="*60)
    print("SCENARIO 2: Returning to Whiterun with Lydia")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": ["Lydia", "Hadvar"]
        }
    }
    
    print("\nPlayer Location: Whiterun")
    print("\nActive Companions: Lydia, Hadvar")
    print("\nTriggered Events:")
    
    events = whiterun_location_triggers("whiterun", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event}")


def demo_scenario_3():
    """Demo: Player tours Whiterun districts with Lydia"""
    print("\n" + "="*60)
    print("SCENARIO 3: Touring Whiterun Districts with Lydia")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": ["Lydia"]
        }
    }
    
    locations = [
        ("Whiterun Plains District", "whiterun_plains_district"),
        ("Whiterun Wind District", "whiterun_wind_district"),
        ("Whiterun Cloud District", "whiterun_cloud_district")
    ]
    
    for location_name, location_key in locations:
        print(f"\n--- {location_name} ---")
        events = whiterun_location_triggers(location_key, campaign_state)
        for event in events:
            print(f"  • {event}")


def demo_scenario_4():
    """Demo: Player in Riverwood with Lydia (no commentary)"""
    print("\n" + "="*60)
    print("SCENARIO 4: Lydia Outside Whiterun (No Commentary)")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": ["Lydia"]
        }
    }
    
    print("\nPlayer Location: Riverwood")
    print("\nActive Companions: Lydia")
    print("\nTriggered Events:")
    
    events = whiterun_location_triggers("riverwood", campaign_state)
    if events:
        for i, event in enumerate(events, 1):
            print(f"  {i}. {event}")
    else:
        print("  (No events triggered - Riverwood triggers would be in a separate module)")
    
    print("\nNote: Lydia's commentary only triggers in Whiterun locations.")


def main():
    """Run all demo scenarios"""
    print("\n" + "="*60)
    print("WHITERUN LOCATION TRIGGERS - DEMONSTRATION")
    print("Companion Commentary Placeholder System")
    print("="*60)
    
    demo_scenario_1()
    demo_scenario_2()
    demo_scenario_3()
    demo_scenario_4()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print("\nThe companion commentary system is ready for future expansion.")
    print("Additional companions (Aela, Farkas, etc.) can be added using")
    print("the same pattern established for Lydia.")
    print()


if __name__ == "__main__":
    main()
