#!/usr/bin/env python3
"""
Demo script for Falkreath Hold triggers and data.

This script demonstrates the Falkreath Hold functionality,
including scene triggers, quest hooks, and Dark Brotherhood integration.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from triggers.falkreath_triggers import (
    scene_falkreath_arrival,
    scene_falkreath_graveyard,
    trigger_siddgeir_bandit_bounty,
    trigger_dengeir_vampire_hunt,
    trigger_dark_brotherhood_contact,
    scene_astrid_abduction,
    trigger_sanctuary_discovery,
    trigger_sanctuary_entry,
    trigger_sinding_jail_encounter,
    scene_bloated_mans_grotto,
    scene_moonlight_kill_sinding,
    scene_moonlight_spare_sinding
)


def load_json_file(filepath):
    """Load and display a JSON file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def demo_falkreath_data():
    """Demonstrate Falkreath Hold data structure"""
    print("\n" + "=" * 70)
    print("FALKREATH HOLD DATA DEMO")
    print("=" * 70)
    
    hold_data = load_json_file('../data/holds/falkreath.json')
    if hold_data:
        print(f"\nHold: {hold_data['hold']}")
        print(f"Capital: {hold_data['capital']}")
        print(f"Jarl: {hold_data['jarl']}")
        print(f"Steward: {hold_data['steward']}")
        print(f"\nDescription: {hold_data['description'][:200]}...")
        
        print(f"\n--- Major Locations ({len(hold_data['major_locations'])}) ---")
        for loc in hold_data['major_locations']:
            hidden = " [HIDDEN]" if loc.get('hidden') else ""
            print(f"  • {loc['name']} ({loc['type']}){hidden}")
        
        print(f"\n--- City Districts ({len(hold_data['districts'])}) ---")
        for district in hold_data['districts']:
            print(f"  • {district['name']}")
        
        print(f"\n--- Local Quest Hooks ({len(hold_data['local_quest_hooks'])}) ---")
        for quest in hold_data['local_quest_hooks']:
            print(f"  • {quest['quest']} (from {quest['giver']})")


def demo_npc_stat_sheets():
    """Demonstrate NPC stat sheets"""
    print("\n" + "=" * 70)
    print("NPC STAT SHEETS DEMO")
    print("=" * 70)
    
    npcs = [
        ('Jarl Siddgeir', '../data/npc_stat_sheets/siddgeir.json'),
        ('Dengeir of Stuhn', '../data/npc_stat_sheets/dengeir_of_stuhn.json'),
        ('Nenya', '../data/npc_stat_sheets/nenya.json')
    ]
    
    for name, filepath in npcs:
        npc_data = load_json_file(filepath)
        if npc_data:
            print(f"\n--- {name} ---")
            print(f"Type: {npc_data['type']}")
            print(f"Faction: {npc_data['faction']}")
            print(f"High Concept: {npc_data['aspects']['high_concept']}")
            print(f"Trouble: {npc_data['aspects']['trouble']}")
            
            # Show top skills
            skills = npc_data['skills']
            if 'Great' in skills or 'Superb' in skills:
                top_skill_level = 'Superb' if 'Superb' in skills else 'Great'
                print(f"Top Skills ({top_skill_level}): {', '.join(skills.get(top_skill_level, []))}")
            
            # Show stunts
            if npc_data.get('stunts'):
                print(f"Stunts: {len(npc_data['stunts'])}")
                for stunt in npc_data['stunts']:
                    stunt_name = stunt.split(':')[0]
                    print(f"  • {stunt_name}")


def demo_scene_triggers():
    """Demonstrate scene triggers"""
    print("\n" + "=" * 70)
    print("SCENE TRIGGERS DEMO")
    print("=" * 70)
    
    party_state = {}
    
    print("\n--- Arriving in Falkreath ---")
    scene_falkreath_arrival(party_state)
    print(f"State updated: seen_falkreath_intro = {party_state.get('seen_falkreath_intro')}")
    
    print("\n--- Visiting the Graveyard ---")
    scene_falkreath_graveyard(party_state)
    print(f"State updated: witnessed_graveyard_scene = {party_state.get('witnessed_graveyard_scene')}")


def demo_quest_triggers():
    """Demonstrate quest triggers"""
    print("\n" + "=" * 70)
    print("QUEST TRIGGERS DEMO")
    print("=" * 70)
    
    campaign_state = {}
    
    print("\n--- Jarl Siddgeir's Bandit Bounty ---")
    trigger_siddgeir_bandit_bounty(campaign_state)
    print(f"Quest given: {campaign_state.get('falkreath_bandit_quest_given')}")
    
    print("\n--- Dengeir's Vampire Hunt ---")
    trigger_dengeir_vampire_hunt(campaign_state)
    print(f"Quest given: {campaign_state.get('dengeir_vampire_quest_given')}")


def demo_dark_brotherhood_sequence():
    """Demonstrate Dark Brotherhood event sequence"""
    print("\n" + "=" * 70)
    print("DARK BROTHERHOOD EVENT SEQUENCE DEMO")
    print("=" * 70)
    
    party_actions = {'murder_committed': True}
    campaign_state = {}
    
    print("\n--- Step 1: Dark Brotherhood Contact ---")
    trigger_dark_brotherhood_contact(party_actions, campaign_state)
    print(f"Contacted: {campaign_state.get('dark_brotherhood_contacted')}")
    
    print("\n--- Step 2: Astrid's Abduction (after sleeping) ---")
    scene_astrid_abduction(campaign_state)
    print(f"Abduction scene shown: {campaign_state.get('astrid_abduction_scene')}")
    
    print("\n--- Step 3: Discovering the Sanctuary ---")
    trigger_sanctuary_discovery("Near Dark Brotherhood Sanctuary", campaign_state)
    print(f"Sanctuary discovered: {campaign_state.get('dark_brotherhood_sanctuary_discovered')}")
    
    print("\n--- Step 4: Entering the Sanctuary (as a member) ---")
    campaign_state['dark_brotherhood_member'] = True
    trigger_sanctuary_entry(campaign_state)
    print(f"Entered Sanctuary: {campaign_state.get('dark_brotherhood_sanctuary_entered')}")


def demo_ill_met_by_moonlight():
    """Demonstrate Ill Met by Moonlight quest sequence"""
    print("\n" + "=" * 70)
    print("ILL MET BY MOONLIGHT (HIRCINE'S QUEST) DEMO")
    print("=" * 70)
    
    campaign_state = {}
    
    print("\n--- Step 1: Meeting Sinding in Falkreath Jail ---")
    trigger_sinding_jail_encounter(campaign_state)
    print(f"Quest started: {campaign_state.get('ill_met_moonlight_started')}")
    
    print("\n--- Step 2: Confrontation at Bloated Man's Grotto ---")
    scene_bloated_mans_grotto(campaign_state)
    print(f"Grotto encountered: {campaign_state.get('bloated_mans_grotto_encountered')}")
    
    print("\n--- Branching Path A: Spare Sinding ---")
    campaign_state_spare = campaign_state.copy()
    scene_moonlight_spare_sinding(campaign_state_spare)
    print(f"Quest completed (spare): {campaign_state_spare.get('ill_met_moonlight_completed')}")
    print(f"Ring of Hircine obtained: {campaign_state_spare.get('artifact_ring_of_hircine_obtained')}")
    
    print("\n--- Branching Path B: Kill Sinding ---")
    campaign_state_kill = campaign_state.copy()
    scene_moonlight_kill_sinding(campaign_state_kill)
    print(f"Quest completed (kill): {campaign_state_kill.get('ill_met_moonlight_completed')}")
    print(f"Savior's Hide obtained: {campaign_state_kill.get('artifact_saviors_hide_obtained')}")


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("FALKREATH HOLD IMPLEMENTATION DEMONSTRATION")
    print("=" * 70)
    
    # Change to the tests directory for relative paths to work
    os.chdir(os.path.join(os.path.dirname(__file__)))
    
    demo_falkreath_data()
    demo_npc_stat_sheets()
    demo_scene_triggers()
    demo_quest_triggers()
    demo_dark_brotherhood_sequence()
    demo_ill_met_by_moonlight()
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
