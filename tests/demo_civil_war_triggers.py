#!/usr/bin/env python3
"""
Demo: Civil War Triggers for Windhelm

This demo script showcases the new Civil War tie-ins for Windhelm,
demonstrating how the city's atmosphere changes based on the state
of the civil war.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.windhelm_triggers import windhelm_location_triggers


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_scenario_1():
    """Scenario 1: Stormcloak Victory at Whiterun"""
    print_section("SCENARIO 1: Stormcloak Victory at Whiterun")
    print("\nContext: The Stormcloaks have successfully captured Whiterun.")
    print("         Jarl Balgruuf has been exiled and Vignar Gray-Mane is now Jarl.")
    print("\nThe party enters Windhelm for the first time since the battle...")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "whiterun_control": "stormcloak"
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    print("\n[NARRATIVE]")
    for event in events:
        print(f"  • {event}\n")
    
    print("[SYSTEM] Flag 'windhelm_heard_whiterun_win' set to True")
    print("         This event will not repeat on future visits.")


def demo_scenario_2():
    """Scenario 2: Imperial Victory at Whiterun"""
    print_section("SCENARIO 2: Imperial Victory at Whiterun")
    print("\nContext: The Stormcloak assault on Whiterun has failed.")
    print("         Jarl Balgruuf remains loyal to the Empire.")
    print("\nThe party enters Windhelm...")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "whiterun_control": "imperial"
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    print("\n[NARRATIVE]")
    for event in events:
        print(f"  • {event}\n")
    
    print("[SYSTEM] Flag 'windhelm_heard_whiterun_loss' set to True")
    print("         This event will not repeat on future visits.")


def demo_scenario_3():
    """Scenario 3: Battle for Windhelm Begins"""
    print_section("SCENARIO 3: Imperial Assault on Windhelm")
    print("\nContext: The Imperial Legion has launched their final assault.")
    print("         The Battle for Windhelm has begun.")
    print("\nThe party enters Windhelm during the siege...")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "battle_for_windhelm_started": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    print("\n[NARRATIVE]")
    for event in events:
        print(f"  • {event}\n")
    
    print("[SYSTEM] Flag 'windhelm_siege_alert' set to True")
    print("         The city is now in battle mode.")


def demo_scenario_4():
    """Scenario 4: Season Unending Truce"""
    print_section("SCENARIO 4: Season Unending Truce")
    print("\nContext: The Greybeards have brokered a temporary truce.")
    print("         Both sides must honor the ceasefire.")
    print("\nThe party enters Windhelm during the truce...")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "truce_active": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    print("\n[NARRATIVE]")
    for event in events:
        print(f"  • {event}\n")
    
    print("[SYSTEM] Flag 'windhelm_truce_noticed' set to True")
    print("         The party has witnessed the tense peace.")


def demo_scenario_5():
    """Scenario 5: Multiple Events"""
    print_section("SCENARIO 5: Complex Civil War State")
    print("\nContext: Multiple civil war events have occurred:")
    print("         - Stormcloaks won Whiterun")
    print("         - A truce has been called")
    print("\nThe party enters Windhelm...")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        },
        "whiterun_control": "stormcloak",
        "truce_active": True
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    print("\n[NARRATIVE]")
    for event in events:
        print(f"  • {event}\n")
    
    print("[SYSTEM] Multiple flags set")
    print("         Both events can fire simultaneously if appropriate.")


def demo_scenario_6():
    """Scenario 6: No Civil War State"""
    print_section("SCENARIO 6: No Active Civil War Events")
    print("\nContext: The party has not engaged with the civil war yet.")
    print("         No battle outcomes or special events have occurred.")
    print("\nThe party enters Windhelm...")
    
    campaign_state = {
        "companions": {
            "active_companions": []
        }
    }
    
    events = windhelm_location_triggers("windhelm", campaign_state)
    
    print("\n[NARRATIVE]")
    for event in events:
        print(f"  • {event}\n")
    
    print("[SYSTEM] Only basic location description shown")
    print("         Civil war triggers remain inactive until flags are set.")


def main():
    """Run all demonstration scenarios"""
    print("\n" + "=" * 70)
    print("  CIVIL WAR TRIGGERS FOR WINDHELM - DEMONSTRATION")
    print("=" * 70)
    print("\nThis demo showcases how Windhelm's atmosphere dynamically responds")
    print("to the state of the Civil War questline.")
    
    demo_scenario_1()
    demo_scenario_2()
    demo_scenario_3()
    demo_scenario_4()
    demo_scenario_5()
    demo_scenario_6()
    
    print("\n" + "=" * 70)
    print("  DEMO COMPLETE")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Dynamic narrative based on civil war state")
    print("  ✓ Safe flag checking (no errors if flags missing)")
    print("  ✓ One-time triggers (events don't repeat)")
    print("  ✓ Multiple events can fire together")
    print("  ✓ Seamless integration with existing triggers")
    print()


if __name__ == "__main__":
    main()
