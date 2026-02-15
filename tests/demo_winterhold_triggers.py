#!/usr/bin/env python3
"""
Demo script for Winterhold & College of Winterhold Location Triggers

This script demonstrates the winterhold_location_triggers function with
various scenarios and campaign states.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.winterhold_triggers import winterhold_location_triggers


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_events(events, indent=2):
    """Print events with formatting"""
    if not events:
        print(" " * indent + "(No events triggered)")
        return
    
    for i, event in enumerate(events, 1):
        print(f"{' ' * indent}{i}. {event}")


def demo_winterhold_journey():
    """Demonstrate a journey through Winterhold and the College"""
    
    print_section("WINTERHOLD & COLLEGE OF WINTERHOLD - LOCATION TRIGGERS DEMO")
    print("\nScenario: An Adept of the College returns to Winterhold")
    print("carrying the legendary Staff of Cinders...")
    
    # Initial campaign state
    campaign_state = {
        "scene_flags": {},
        "player": {
            "college_member": True,
            "college_rank": "Adept",
            "has_staff_of_cinders": True,
            "artifacts": ["staff_of_cinders"]
        },
        "civil_war_state": {
            "player_alliance": "neutral"
        }
    }
    
    # 1. Arriving in Winterhold Town
    print_section("1. ARRIVING IN WINTERHOLD TOWN")
    print("Location: winterhold")
    events = winterhold_location_triggers("winterhold", campaign_state)
    print_events(events)
    
    # 2. Entering the Frozen Hearth
    print_section("2. THE FROZEN HEARTH INN")
    print("Location: winterhold_frozen_hearth")
    events = winterhold_location_triggers("winterhold_frozen_hearth", campaign_state)
    print_events(events)
    
    # 3. Visiting the Jarl's Longhouse
    print_section("3. JARL KORIR'S LONGHOUSE")
    print("Location: winterhold_jarls_longhouse")
    print("(As a College member, tension is expected...)")
    events = winterhold_location_triggers("winterhold_jarls_longhouse", campaign_state)
    print_events(events)
    
    # 4. Crossing the College Bridge
    print_section("4. THE COLLEGE BRIDGE")
    print("Location: winterhold_college_bridge")
    events = winterhold_location_triggers("winterhold_college_bridge", campaign_state)
    print_events(events)
    
    # 5. College Courtyard
    print_section("5. COLLEGE COURTYARD")
    print("Location: college_courtyard")
    events = winterhold_location_triggers("college_courtyard", campaign_state)
    print_events(events)
    
    # 6. Hall of the Elements
    print_section("6. HALL OF THE ELEMENTS")
    print("Location: college_hall_of_elements")
    events = winterhold_location_triggers("college_hall_of_elements", campaign_state)
    print_events(events)
    
    # 7. The Arcanaeum
    print_section("7. THE ARCANAEUM")
    print("Location: college_arcanaeum")
    events = winterhold_location_triggers("college_arcanaeum", campaign_state)
    print_events(events)
    
    # 8. The Midden
    print_section("8. THE MIDDEN")
    print("Location: college_midden")
    events = winterhold_location_triggers("college_midden", campaign_state)
    print_events(events)
    
    # 9. Saarthal Expedition
    print_section("9. SAARTHAL EXCAVATION SITE")
    print("Location: saarthal_excavation")
    events = winterhold_location_triggers("saarthal_excavation", campaign_state)
    print_events(events)


def demo_non_member_admission():
    """Demonstrate non-member attempting to enter College"""
    
    print_section("NON-MEMBER ADMISSION SCENARIO")
    print("\nScenario: A traveler approaches the College for the first time")
    
    campaign_state = {
        "scene_flags": {},
        "player": {
            "college_member": False
        },
        "civil_war_state": {}
    }
    
    print("\nLocation: winterhold_college_bridge")
    print("(Player is not a College member)")
    events = winterhold_location_triggers("winterhold_college_bridge", campaign_state)
    print_events(events)
    
    print("\n[After passing the test, returning as member...]")
    campaign_state["scene_flags"] = {}  # Reset flags
    campaign_state["player"]["college_member"] = True
    campaign_state["player"]["college_rank"] = "Apprentice"
    
    events = winterhold_location_triggers("winterhold_college_bridge", campaign_state)
    print_events(events)


def demo_imperial_tension():
    """Demonstrate Imperial-aligned character in Stormcloak Winterhold"""
    
    print_section("IMPERIAL ALLIANCE TENSION")
    print("\nScenario: An Imperial-aligned character arrives in Winterhold")
    
    campaign_state = {
        "scene_flags": {},
        "player": {},
        "civil_war_state": {
            "player_alliance": "Imperial"
        }
    }
    
    print("\nLocation: winterhold")
    events = winterhold_location_triggers("winterhold", campaign_state)
    print_events(events)


def demo_staff_reactions():
    """Demonstrate Staff of Cinders recognition"""
    
    print_section("STAFF OF CINDERS RECOGNITION")
    print("\nScenario: Wielding the legendary Staff of Cinders")
    
    campaign_state = {
        "scene_flags": {},
        "player": {
            "has_staff_of_cinders": True,
            "college_member": False
        },
        "civil_war_state": {}
    }
    
    print("\n1. In Winterhold town:")
    events = winterhold_location_triggers("winterhold", campaign_state)
    staff_events = [e for e in events if "Cindershroud" in e or "staff" in e.lower()]
    print_events(staff_events if staff_events else events)
    
    campaign_state["scene_flags"] = {}  # Reset
    print("\n2. At the Frozen Hearth:")
    events = winterhold_location_triggers("winterhold_frozen_hearth", campaign_state)
    staff_events = [e for e in events if "staff" in e.lower() or "heirloom" in e.lower()]
    print_events(staff_events if staff_events else events)
    
    campaign_state["scene_flags"] = {}  # Reset
    campaign_state["player"]["college_member"] = True
    print("\n3. At the College bridge:")
    events = winterhold_location_triggers("college_bridge", campaign_state)
    staff_events = [e for e in events if "runes" in e.lower() or "enchantment" in e.lower()]
    print_events(staff_events if staff_events else events)


def demo_location_variety():
    """Show variety of College locations"""
    
    print_section("COLLEGE INTERIOR LOCATIONS")
    print("\nA tour of the College's various chambers...")
    
    campaign_state = {
        "scene_flags": {},
        "player": {
            "college_member": True
        },
        "civil_war_state": {}
    }
    
    locations = [
        ("Hall of Attainment", "college_hall_of_attainment"),
        ("Arch-Mage's Quarters", "college_arch_mage_quarters"),
        ("The Midden", "midden")
    ]
    
    for name, loc_key in locations:
        print(f"\n{name} ({loc_key}):")
        events = winterhold_location_triggers(loc_key, campaign_state)
        print_events(events, indent=4)


def main():
    """Run all demo scenarios"""
    try:
        demo_winterhold_journey()
        demo_non_member_admission()
        demo_imperial_tension()
        demo_staff_reactions()
        demo_location_variety()
        
        print_section("DEMO COMPLETE")
        print("\nAll scenarios demonstrated successfully!")
        print("\nNote: Scene flags persist across calls in the same campaign_state.")
        print("Reset scene_flags to see first-time events again.")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
