#!/usr/bin/env python3
"""
Demo script showing how to use Windhelm location triggers

This demonstrates quest hooks, companion commentary, and location-based events
for the Eastmarch side quests.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.windhelm_triggers import windhelm_location_triggers


def demo_scenario_1():
    """Demo: Player enters Windhelm graveyard at night (Blood on the Ice hook)"""
    print("\n" + "="*60)
    print("SCENARIO 1: Windhelm Graveyard at Night (Quest Hook)")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "time_of_day": "night",
        "quests": {
            "active": [],
            "completed": []
        }
    }
    
    print("\nPlayer Location: Windhelm Graveyard")
    print("Time of Day: Night")
    print("Active Companions: None")
    print("Quest Status: Blood on the Ice not started")
    print("\nTriggered Events:")
    
    events = windhelm_location_triggers("windhelm_graveyard", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event}")
    
    print("\n💡 This triggers the start of the 'Blood on the Ice' quest!")


def demo_scenario_2():
    """Demo: Player enters marketplace (White Phial hook)"""
    print("\n" + "="*60)
    print("SCENARIO 2: Windhelm Market (Quest Hook)")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "quests": {
            "active": [],
            "completed": []
        }
    }
    
    print("\nPlayer Location: Windhelm Market")
    print("Active Companions: None")
    print("Quest Status: The White Phial not started")
    print("\nTriggered Events:")
    
    events = windhelm_location_triggers("windhelm_market", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event}")
    
    print("\n💡 This hints at the 'The White Phial' quest from Nurelion!")


def demo_scenario_3():
    """Demo: Player enters Windhelm with Stenvar"""
    print("\n" + "="*60)
    print("SCENARIO 3: Entering Windhelm with Stenvar")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": ["Stenvar"]
        }
    }
    
    print("\nPlayer Location: Windhelm")
    print("Active Companions: Stenvar")
    print("\nTriggered Events:")
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event}")


def demo_scenario_4():
    """Demo: Player tours Windhelm districts"""
    print("\n" + "="*60)
    print("SCENARIO 4: Touring Windhelm Districts")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": [{"name": "Uthgerd the Unbroken", "npc_id": "uthgerd"}]
        }
    }
    
    locations = [
        ("Gray Quarter", "windhelm_gray_quarter"),
        ("Palace of the Kings", "windhelm_palace_of_the_kings"),
        ("Candlehearth Hall", "windhelm_candlehearth_hall")
    ]
    
    print("\nActive Companions: Uthgerd the Unbroken")
    
    for location_name, location_key in locations:
        print(f"\n--- {location_name} ---")
        events = windhelm_location_triggers(location_key, campaign_state)
        for event in events:
            print(f"  • {event}")


def demo_scenario_5():
    """Demo: Quest already active - no hook triggered"""
    print("\n" + "="*60)
    print("SCENARIO 5: Quest Already Active (No Hook)")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "time_of_day": "night",
        "quests": {
            "active": ["blood_on_the_ice"],
            "completed": []
        }
    }
    
    print("\nPlayer Location: Windhelm Graveyard")
    print("Time of Day: Night")
    print("Quest Status: Blood on the Ice already active")
    print("\nTriggered Events:")
    
    events = windhelm_location_triggers("windhelm_graveyard", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event}")
    
    print("\n💡 Notice: The quest discovery event does NOT trigger since the quest is already active!")


def demo_scenario_6():
    """Demo: Graveyard during the day (subtle hint)"""
    print("\n" + "="*60)
    print("SCENARIO 6: Graveyard During Day (Subtle Hint)")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "time_of_day": "day",
        "quests": {
            "active": [],
            "completed": []
        }
    }
    
    print("\nPlayer Location: Windhelm Graveyard")
    print("Time of Day: Day")
    print("Quest Status: Blood on the Ice not started")
    print("\nTriggered Events:")
    
    events = windhelm_location_triggers("windhelm_graveyard", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event}")
    
    print("\n💡 During the day, players get subtle hints about the murders rather than the full discovery scene!")


def main():
    """Run all demo scenarios"""
    print("\n" + "="*60)
    print("WINDHELM LOCATION TRIGGERS - DEMONSTRATION")
    print("Eastmarch Side Quests: Blood on the Ice & The White Phial")
    print("="*60)
    
    demo_scenario_1()
    demo_scenario_2()
    demo_scenario_3()
    demo_scenario_4()
    demo_scenario_5()
    demo_scenario_6()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print("\n📜 Quest Data:")
    print("   - Quest definitions available in: data/quests/eastmarch_side_quests.json")
    print("   - Blood on the Ice: Murder mystery investigation in Windhelm")
    print("   - The White Phial: Retrieve a legendary alchemical artifact")
    print("\n🎮 Integration:")
    print("   - Triggers automatically activate based on location and time")
    print("   - Quest hooks only appear when quests are not yet active/completed")
    print("   - Companion commentary enhances immersion")
    print()


if __name__ == "__main__":
    main()
