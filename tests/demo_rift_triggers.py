#!/usr/bin/env python3
"""
Demo script showing how to use Riften (The Rift) location triggers

This demonstrates the location triggers, companion commentary, and quest initiation.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.rift_triggers import rift_location_triggers


def demo_scenario_1():
    """Demo: Player enters Riften marketplace (not in Guild)"""
    print("\n" + "="*60)
    print("SCENARIO 1: First Visit to Riften Marketplace")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "player": {
            "thieves_guild_member": False
        }
    }
    
    print("\nPlayer Location: Riften Marketplace")
    print("\nActive Companions: None")
    print("\nGuild Status: Not a member of Thieves Guild")
    print("\nTriggered Events:")
    
    events = rift_location_triggers("riften_marketplace", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event[:100]}{'...' if len(event) > 100 else ''}")


def demo_scenario_2():
    """Demo: Player enters Riften marketplace as Guild member"""
    print("\n" + "="*60)
    print("SCENARIO 2: Returning to Marketplace (Guild Member)")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "player": {
            "thieves_guild_member": True
        }
    }
    
    print("\nPlayer Location: Riften Marketplace")
    print("\nActive Companions: None")
    print("\nGuild Status: Member of Thieves Guild")
    print("\nTriggered Events:")
    
    events = rift_location_triggers("riften_marketplace", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event[:100]}{'...' if len(event) > 100 else ''}")
    
    print("\nNote: Brynjolf doesn't approach - you're already in the Guild!")


def demo_scenario_3():
    """Demo: Player tours Riften districts with Iona"""
    print("\n" + "="*60)
    print("SCENARIO 3: Touring Riften Districts with Iona")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": ["Iona"]
        }
    }
    
    locations = [
        ("Riften Marketplace", "riften_marketplace"),
        ("The Ratway", "riften_ratway"),
        ("Temple of Mara", "riften_temple"),
        ("Mistveil Keep", "riften_mistveil_keep")
    ]
    
    for location_name, location_key in locations:
        print(f"\n--- {location_name} ---")
        events = rift_location_triggers(location_key, campaign_state)
        for event in events:
            # Show first 80 chars for readability
            display = event[:80] + "..." if len(event) > 80 else event
            print(f"  • {display}")


def demo_scenario_4():
    """Demo: Player explores The Rift wilderness"""
    print("\n" + "="*60)
    print("SCENARIO 4: Exploring The Rift Wilderness")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    locations = [
        ("The Rift Forest", "the_rift_forest"),
        ("Lake Honrich", "lake_honrich"),
        ("General Riften Entrance", "riften")
    ]
    
    for location_name, location_key in locations:
        print(f"\n--- {location_name} ---")
        events = rift_location_triggers(location_key, campaign_state)
        if events:
            for event in events:
                display = event[:80] + "..." if len(event) > 80 else event
                print(f"  • {display}")
        else:
            print("  (No events triggered)")


def demo_scenario_5():
    """Demo: Full marketplace experience with Iona, not in Guild"""
    print("\n" + "="*60)
    print("SCENARIO 5: Marketplace with Iona (Not in Guild)")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": [
                {
                    "name": "Iona",
                    "npc_id": "iona",
                    "loyalty": 75
                }
            ]
        },
        "player": {
            "thieves_guild_member": False
        }
    }
    
    print("\nPlayer Location: Riften Marketplace")
    print("\nActive Companions: Iona (Housecarl)")
    print("\nGuild Status: Not a member")
    print("\nTriggered Events:")
    
    events = rift_location_triggers("riften_marketplace", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"\n  {i}. {event}")
    
    print("\nNote: Multiple triggers fire - location description, Brynjolf recruitment, and Iona's commentary!")


def main():
    """Run all demo scenarios"""
    print("\n" + "="*60)
    print("RIFTEN (THE RIFT) LOCATION TRIGGERS - DEMONSTRATION")
    print("Location Events, Companion Commentary & Quest Initiation")
    print("="*60)
    
    demo_scenario_1()
    demo_scenario_2()
    demo_scenario_3()
    demo_scenario_4()
    demo_scenario_5()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print("\nThe Rift location trigger system is fully functional!")
    print("Features include:")
    print("  • Detailed descriptions for all Riften districts")
    print("  • Environmental triggers for The Rift wilderness")
    print("  • Brynjolf recruitment in marketplace (if not in Guild)")
    print("  • Iona companion commentary in Riften locations")
    print("  • Multiple triggers can fire simultaneously")
    print("\nAdditional Riften companions (like Mjoll) can be added")
    print("using the same pattern established for Iona.")
    print()


if __name__ == "__main__":
    main()
