#!/usr/bin/env python3
"""
Demo script for The Pale (Dawnstar) Triggers

This demonstrates the location-based scenes and quest triggers
for The Pale hold and Dawnstar, showcasing how they might be
used in a narrative campaign session.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.pale_triggers import (
    scene_dawnstar_arrival,
    scene_windpeak_inn_commotion,
    trigger_erandur_waking_nightmare,
    trigger_skald_giant_bounty,
    trigger_wayfinder_void_salts,
    trigger_pale_blizzard,
    trigger_erandur_intersect,
    pale_get_next_scene
)


def demo_dawnstar_campaign():
    """Demonstrate a typical campaign flow through Dawnstar"""
    
    # Initialize campaign and party state
    campaign_state = {}
    party_state = {}
    
    print("=" * 70)
    print("THE PALE HOLD - DAWNSTAR CAMPAIGN DEMO")
    print("=" * 70)
    print("\nThis demo shows how The Pale triggers might be used in a campaign.\n")
    
    # --- Scene 1: Arrival at Dawnstar ---
    print("\n" + "─" * 70)
    print("SCENE 1: ARRIVAL AT DAWNSTAR")
    print("─" * 70)
    print("\nThe party approaches Dawnstar for the first time...\n")
    scene_dawnstar_arrival(party_state)
    
    input("\n[Press Enter to continue...]")
    
    # --- Scene 2: Exploring the Town ---
    print("\n" + "─" * 70)
    print("SCENE 2: THE WINDPEAK INN")
    print("─" * 70)
    print("\nSeeking rest and information, the party enters the Windpeak Inn...\n")
    scene_windpeak_inn_commotion(party_state)
    
    input("\n[Press Enter to continue...]")
    
    # --- Scene 3: Erandur's Quest ---
    print("\n" + "─" * 70)
    print("SCENE 3: ERANDUR'S PLEA")
    print("─" * 70)
    print("\nThe Dunmer priest approaches the party...\n")
    trigger_erandur_waking_nightmare(campaign_state)
    
    input("\n[Press Enter to continue...]")
    
    # --- Scene 4: Meeting the Jarl ---
    print("\n" + "─" * 70)
    print("SCENE 4: AUDIENCE WITH JARL SKALD")
    print("─" * 70)
    print("\nAfter helping with the nightmare crisis, the party is summoned to the longhouse...\n")
    trigger_skald_giant_bounty(campaign_state)
    
    input("\n[Press Enter to continue...]")
    
    # --- Scene 5: The Docks ---
    print("\n" + "─" * 70)
    print("SCENE 5: AT THE DOCKS")
    print("─" * 70)
    print("\nWhile exploring the harbor, the party meets a young sea captain...\n")
    trigger_wayfinder_void_salts(campaign_state)
    
    input("\n[Press Enter to continue...]")
    
    # --- Scene 6: Travel Hazard ---
    print("\n" + "─" * 70)
    print("SCENE 6: WILDERNESS TRAVEL")
    print("─" * 70)
    print("\nLater, while traveling through The Pale's frozen wilderness...\n")
    trigger_pale_blizzard(campaign_state)
    
    print("\n" + "─" * 70)
    print("END OF DEMO")
    print("─" * 70)
    
    # Show final state
    print("\n=== Campaign State Summary ===")
    print(f"Party has visited Dawnstar: {party_state.get('seen_dawnstar_intro', False)}")
    print(f"Party heard about nightmares: {party_state.get('heard_nightmare_rumors', False)}")
    print(f"Waking Nightmare quest offered: {campaign_state.get('waking_nightmare_quest_given', False)}")
    print(f"Giant bounty quest offered: {campaign_state.get('skald_giant_quest_given', False)}")
    print(f"Void salts quest offered: {campaign_state.get('wayfinder_void_salts_quest_given', False)}")
    print(f"Blizzard encountered: {campaign_state.get('blizzard_active', False)}")
    
    print("\n" + "=" * 70)


def demo_quest_idempotence():
    """Demonstrate that quest triggers only fire once"""
    
    print("\n" + "=" * 70)
    print("QUEST TRIGGER IDEMPOTENCE DEMO")
    print("=" * 70)
    print("\nThis demonstrates that quest triggers only fire once.\n")
    
    campaign_state = {}
    
    print("─" * 70)
    print("First attempt to trigger Erandur's quest:")
    print("─" * 70)
    trigger_erandur_waking_nightmare(campaign_state)
    
    print("\n" + "─" * 70)
    print("Second attempt (should NOT print quest dialogue):")
    print("─" * 70)
    trigger_erandur_waking_nightmare(campaign_state)
    print("(No dialogue printed - quest already given)")
    
    print("\n" + "=" * 70)


def demo_erandur_intersect():
    """Demonstrate the Erandur intersect trigger"""
    
    print("\n" + "=" * 70)
    print("ERANDUR INTERSECT TRIGGER DEMO")
    print("=" * 70)
    print("\nThis demonstrates the new Erandur intersect trigger.\n")
    
    print("─" * 70)
    print("Scenario: PC approaches Nightcaller Temple directly via Clairvoyance")
    print("─" * 70)
    
    campaign_state = {
        "scene_flags": {
            "session04_nightcaller_temple_targeted": True
        }
    }
    
    print("\nCalling pale_get_next_scene()...\n")
    result = pale_get_next_scene(campaign_state)
    
    if result:
        print("Scene triggered!")
        print(f"  Scene ID: {result['scene_id']}")
        print(f"  Title: {result['title']}")
        print(f"  Type: {result['type']}")
        print(f"  Location: {result['location']}")
        print(f"  Tags: {', '.join(result['tags'])}")
        print(f"\nScene flags updated:")
        print(f"  erandur_introduced: {campaign_state['scene_flags']['erandur_introduced']}")
        print(f"  erandur_intersection_method: {campaign_state['scene_flags']['erandur_intersection_method']}")
    else:
        print("No scene triggered.")
    
    print("\n" + "─" * 70)
    print("Calling pale_get_next_scene() again (should not trigger)...")
    print("─" * 70)
    result = pale_get_next_scene(campaign_state)
    
    if result:
        print("Scene triggered!")
    else:
        print("No scene triggered. (Correct - trigger is idempotent)")
    
    print("\n" + "=" * 70)


def main():
    """Main demo function"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "THE PALE HOLD TRIGGERS DEMONSTRATION" + " " * 16 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\nThis demo shows the location triggers for Dawnstar and The Pale.")
    print("Choose a demo to run:")
    print("\n1. Full Dawnstar Campaign Flow")
    print("2. Quest Idempotence Demo")
    print("3. Erandur Intersect Trigger Demo")
    print("4. Run All")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        demo_dawnstar_campaign()
    elif choice == "2":
        demo_quest_idempotence()
    elif choice == "3":
        demo_erandur_intersect()
    elif choice == "4":
        demo_dawnstar_campaign()
        input("\n[Press Enter to continue to next demo...]")
        demo_quest_idempotence()
        input("\n[Press Enter to continue to next demo...]")
        demo_erandur_intersect()
    elif choice == "5":
        print("\nExiting demo. Talos guide you!")
        return
    else:
        print("\nInvalid choice. Exiting.")
        return
    
    print("\n\nDemo complete! These triggers integrate with the GPT narrative engine")
    print("to provide dynamic, context-aware storytelling for The Pale hold.\n")


if __name__ == '__main__':
    main()
