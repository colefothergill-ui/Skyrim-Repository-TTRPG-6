#!/usr/bin/env python3
"""
Demo script showing how to use Markarth and The Reach location triggers

This demonstrates the location-based events, quest hooks, and companion commentary functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.markarth_triggers import markarth_location_triggers


def demo_scenario_1():
    """Demo: Player first enters Markarth"""
    print("\n" + "="*60)
    print("SCENARIO 1: First Arrival in Markarth")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "daedric_princes": {}
    }
    
    print("\nPlayer Location: Markarth")
    print("\nActive Companions: None")
    print("\nTriggered Events:")
    
    events = markarth_location_triggers("markarth", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event}")


def demo_scenario_2():
    """Demo: Player explores Markarth districts"""
    print("\n" + "="*60)
    print("SCENARIO 2: Exploring Markarth Districts")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    districts = [
        ("Understone Keep", "markarth_understone_keep"),
        ("Temple of Dibella", "markarth_temple_dibella"),
        ("The Warrens", "markarth_warrens"),
        ("Treasury House", "markarth_treasury_house"),
        ("Silver-Blood Inn", "markarth_silver-blood_inn")
    ]
    
    for district_name, district_key in districts:
        print(f"\n--- {district_name} ---")
        events = markarth_location_triggers(district_key, campaign_state)
        for event in events:
            print(f"  • {event[:150]}..." if len(event) > 150 else f"  • {event}")


def demo_scenario_3():
    """Demo: Player encounters quest hooks in Markarth"""
    print("\n" + "="*60)
    print("SCENARIO 3: Quest Hooks in Markarth")
    print("="*60)
    
    quest_locations = [
        ("Abandoned House (House of Horrors)", "markarth_abandoned_house"),
        ("Nepos's House (Forsworn Conspiracy)", "nepos_house"),
        ("Cidhna Mine (No One Escapes)", "markarth_cidhna_mine")
    ]
    
    for quest_name, location_key in quest_locations:
        print(f"\n--- {quest_name} ---")
        
        campaign_state = {
            "companions": {
                "active_companions": []
            },
            "daedric_princes": {}
        }
        
        events = markarth_location_triggers(location_key, campaign_state)
        for event in events:
            print(f"  • {event[:150]}..." if len(event) > 150 else f"  • {event}")


def demo_scenario_4():
    """Demo: Player explores The Reach wilderness"""
    print("\n" + "="*60)
    print("SCENARIO 4: Exploring The Reach Wilderness")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    wilderness_locations = [
        ("Karthspire", "karthspire"),
        ("Hag Rock Redoubt", "hag_rock_redoubt"),
        ("Druadach Redoubt", "druadach_redoubt"),
        ("Lost Valley Redoubt", "lost_valley_redoubt"),
        ("Nchuand-Zel (Dwemer Ruins)", "nchuand-zel")
    ]
    
    for location_name, location_key in wilderness_locations:
        print(f"\n--- {location_name} ---")
        events = markarth_location_triggers(location_key, campaign_state)
        for event in events:
            print(f"  • {event[:150]}..." if len(event) > 150 else f"  • {event}")


def demo_scenario_5():
    """Demo: Player returns to Markarth with Reach-native companion"""
    print("\n" + "="*60)
    print("SCENARIO 5: Returning to Markarth with Reach-Native Companion")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": ["Illisif"]  # Placeholder Reach-native companion
        }
    }
    
    print("\nPlayer Location: Markarth")
    print("\nActive Companions: Illisif (Reach Native)")
    print("\nTriggered Events:")
    
    events = markarth_location_triggers("markarth", campaign_state)
    for i, event in enumerate(events, 1):
        print(f"  {i}. {event[:150]}..." if len(event) > 150 else f"  {i}. {event}")
    
    print("\nNote: Illisif is a placeholder companion name used in the implementation.")


def demo_scenario_6():
    """Demo: Quest already completed - Abandoned House"""
    print("\n" + "="*60)
    print("SCENARIO 6: Abandoned House After Quest Completion")
    print("="*60)
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "daedric_princes": {
            "molag": "completed"
        }
    }
    
    print("\nPlayer Location: Abandoned House")
    print("\nQuest Status: House of Horrors (Molag Bal) - Completed")
    print("\nTriggered Events:")
    
    events = markarth_location_triggers("markarth_abandoned_house", campaign_state)
    if events:
        for i, event in enumerate(events, 1):
            print(f"  {i}. {event}")
    else:
        print("  (No special events - quest already completed)")
    
    print("\nNote: Quest-specific triggers respect quest completion status.")


def main():
    """Run all demo scenarios"""
    print("\n" + "="*60)
    print("MARKARTH & THE REACH LOCATION TRIGGERS - DEMONSTRATION")
    print("Showing District Events, Quest Hooks, and Companion Commentary")
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
    print("\nThe Markarth location trigger system includes:")
    print("  • City district descriptions (5 districts)")
    print("  • Wilderness locations (5 major sites)")
    print("  • Quest hooks (3 major quests)")
    print("  • Companion commentary support")
    print("  • Quest state awareness")
    print("\nAll triggers follow the established pattern from other holds.")
    print()


if __name__ == "__main__":
    main()
