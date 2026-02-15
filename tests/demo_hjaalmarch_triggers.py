#!/usr/bin/env python3
"""
Demo Script for Hjaalmarch (Morthal) Location Triggers

This script demonstrates the various location-based triggers for Morthal and Hjaalmarch Hold.
It showcases district-specific events, quest hooks, companion commentary, and civil war impacts.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.hjaalmarch_triggers import hjaalmarch_location_triggers


def print_events(title, events):
    """Helper to print events with formatting"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)
    for i, event in enumerate(events, 1):
        print(f"\n[Event {i}]")
        print(event)
    print()


def demo_morthal_districts():
    """Demonstrate district-specific triggers in Morthal"""
    print("\n" + "#" * 70)
    print("# MORTHAL DISTRICTS DEMO")
    print("#" * 70)
    
    campaign_state = {
        "companions": {"active_companions": []},
        "time_of_day": "day"
    }
    
    # Highmoon Hall
    events = hjaalmarch_location_triggers("morthal_highmoon_hall", campaign_state)
    print_events("Entering Highmoon Hall (Jarl's Longhouse)", events)
    
    # Moorside Inn
    events = hjaalmarch_location_triggers("morthal_moorside_inn", campaign_state)
    print_events("Entering Moorside Inn", events)
    
    # Swamp Perimeter
    events = hjaalmarch_location_triggers("morthal_swamp_perimeter", campaign_state)
    print_events("Morthal Swamp Perimeter", events)


def demo_laid_to_rest_quest():
    """Demonstrate the Laid to Rest vampire quest triggers"""
    print("\n" + "#" * 70)
    print("# LAID TO REST QUEST DEMO")
    print("#" * 70)
    
    # Day investigation
    campaign_state_day = {
        "companions": {"active_companions": []},
        "time_of_day": "day",
        "quests": {"active": [], "completed": []}
    }
    
    events = hjaalmarch_location_triggers("morthal_burned_house", campaign_state_day)
    print_events("Investigating Burned House (Daytime)", events)
    
    # Night investigation - ghost and vampire encounter
    campaign_state_night = {
        "companions": {"active_companions": []},
        "time_of_day": "night",
        "quests": {"active": [], "completed": []}
    }
    
    events = hjaalmarch_location_triggers("morthal_burned_house", campaign_state_night)
    print_events("Investigating Burned House (Nighttime)", events)
    
    # Entering Movarth's Lair during quest
    campaign_state_quest = {
        "companions": {"active_companions": []},
        "quests": {"active": ["laid_to_rest"], "completed": []}
    }
    
    events = hjaalmarch_location_triggers("movarths_lair", campaign_state_quest)
    print_events("Entering Movarth's Lair (Quest Active)", events)


def demo_falion_ritual():
    """Demonstrate Falion's secret vampirism cure ritual"""
    print("\n" + "#" * 70)
    print("# FALION'S SECRET RITUAL DEMO")
    print("#" * 70)
    
    campaign_state = {
        "companions": {"active_companions": []},
        "time_of_day": "night",
        "quests": {"active": [], "completed": []}
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    print_events("Morthal at Night (Witnessing Falion's Ritual)", events)


def demo_companion_commentary():
    """Demonstrate companion commentary"""
    print("\n" + "#" * 70)
    print("# COMPANION COMMENTARY DEMO")
    print("#" * 70)
    
    # With Benor (Morthal native)
    campaign_state = {
        "companions": {
            "active_companions": [
                {
                    "name": "Benor",
                    "npc_id": "benor",
                    "loyalty": 75
                }
            ]
        }
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    print_events("Entering Morthal with Benor", events)


def demo_civil_war_changes():
    """Demonstrate civil war faction changes"""
    print("\n" + "#" * 70)
    print("# CIVIL WAR FACTION CHANGES DEMO")
    print("#" * 70)
    
    # Stormcloak takeover
    campaign_state_sc = {
        "companions": {"active_companions": []},
        "jarl_hjaalmarch": "sorli"
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state_sc)
    print_events("Morthal After Stormcloak Takeover (Sorli as Jarl)", events)
    
    # Imperial restoration
    campaign_state_imp = {
        "companions": {"active_companions": []},
        "civil_war_phase": "imperial_victory",
        "jarl_hjaalmarch": "sorli"  # Will be restored to Idgrod
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state_imp)
    print_events("Morthal After Imperial Victory (Idgrod Restored)", events)


def demo_general_arrival():
    """Demonstrate general arrival at Morthal"""
    print("\n" + "#" * 70)
    print("# GENERAL MORTHAL ARRIVAL")
    print("#" * 70)
    
    campaign_state = {
        "companions": {"active_companions": []}
    }
    
    events = hjaalmarch_location_triggers("morthal", campaign_state)
    print_events("First Arrival at Morthal", events)


def run_all_demos():
    """Run all demonstration scenarios"""
    print("\n" + "=" * 70)
    print("HJAALMARCH (MORTHAL) LOCATION TRIGGERS - INTERACTIVE DEMO")
    print("=" * 70)
    print("\nThis demo showcases the narrative triggers for Morthal and Hjaalmarch Hold.")
    print("Each scenario demonstrates different atmospheric events, quest hooks,")
    print("companion interactions, and faction changes.\n")
    
    demo_general_arrival()
    demo_morthal_districts()
    demo_laid_to_rest_quest()
    demo_falion_ritual()
    demo_companion_commentary()
    demo_civil_war_changes()
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nThese triggers integrate seamlessly with your campaign to provide")
    print("rich, contextual narration based on location, time, quests, and state.")
    print()


if __name__ == '__main__':
    run_all_demos()
