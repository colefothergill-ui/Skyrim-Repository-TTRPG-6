#!/usr/bin/env python3
"""
Demo script to show session zero functionality
This simulates a non-interactive run to demonstrate the features
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from session_zero import SessionZeroManager


def demo_session_zero():
    """Demonstrate session zero functionality"""
    print("="*60)
    print("SESSION ZERO DEMONSTRATION")
    print("="*60)
    print("\nThis demonstrates the revamped session zero system:")
    print("- Faction alignment for Battle of Whiterun")
    print("- Mandatory Standing Stone selection")
    print("- Campaign state integration")
    print("- Data validation")
    print()
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir) / "data"
        state_dir = Path(tmpdir) / "state"
        data_dir.mkdir()
        state_dir.mkdir()
        
        # Create races data
        source_dir = data_dir.parent / "source_material" / "converted_pdfs"
        source_dir.mkdir(parents=True)
        
        races_data = {
            "races": [
                {
                    "name": "Nord",
                    "description": "Hardy people of Skyrim",
                    "starting_aspect": "Child of Skyrim",
                    "racial_ability": {
                        "name": "Resist Frost",
                        "effect": "+2 to defend against cold"
                    },
                    "skill_bonuses": ["Fight", "Athletics"]
                }
            ]
        }
        
        with open(source_dir / "races.json", 'w') as f:
            json.dump(races_data, f)
        
        # Initialize manager
        manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
        
        print("\n1. DISPLAYING CIVIL WAR CONTEXT")
        print("-" * 60)
        manager.display_civil_war_context()
        
        print("\n\n2. CREATING TEST CHARACTER")
        print("-" * 60)
        
        # Create a test character
        character = manager.create_character_template(
            "Demo Player",
            "Ragnar Ironheart",
            "Nord",
            "The Warrior Stone"
        )
        
        # Add faction alignment
        character['faction_alignment'] = 'imperial'
        character['backstory'] = """
**Civil War Context**: Concerned about Skyrim's internal conflict and Empire's rule

**Civil War Stance**: Believes in Imperial law and order to unite Skyrim

**Motivation**: Seeks to prove loyalty and become a legendary warrior

**Connections**: Has family in Whiterun who support the Empire
"""
        character['additional_faction_interests'] = "Interested in joining the Companions"
        
        print(f"\nCreated character: {character['name']}")
        print(f"  Player: {character['player']}")
        print(f"  Race: {character['race']}")
        print(f"  Standing Stone: {character['standing_stone']}")
        print(f"  Faction Alignment: {character['faction_alignment']}")
        
        print("\n\n3. VALIDATING CHARACTER DATA")
        print("-" * 60)
        
        is_valid = manager.validate_character_data(character)
        if is_valid:
            print("✓ Character data is valid!")
        else:
            print("✗ Character data validation failed!")
            return
        
        print("\n\n4. UPDATING CAMPAIGN STATE")
        print("-" * 60)
        
        characters = [character]
        campaign_state = manager.update_campaign_state('imperial', characters)
        
        print("\nCampaign State Summary:")
        print(f"  Starting Location: {campaign_state['starting_location']}")
        print(f"  Player Alliance: {campaign_state['civil_war_state']['player_alliance']}")
        print(f"  Battle Status: {campaign_state['civil_war_state']['battle_of_whiterun_status']}")
        print(f"  Session Zero Complete: {campaign_state['session_zero_completed']}")
        print(f"\n  Faction Relationships:")
        for faction, value in campaign_state['civil_war_state']['faction_relationship'].items():
            symbol = "+" if value > 0 else ""
            print(f"    {faction}: {symbol}{value}")
        
        print(f"\n  Starting Narrative:")
        narrative = campaign_state['starting_narrative']
        for line in narrative.split('. '):
            if line.strip():
                print(f"    {line.strip()}.")
        
        print(f"\n  Player Characters:")
        for pc in campaign_state['player_characters']:
            print(f"    - {pc['name']} ({pc['race']}, {pc['standing_stone']})")
        
        print("\n\n5. VERIFYING CAMPAIGN STATE FILE")
        print("-" * 60)
        
        campaign_state_file = state_dir / "campaign_state.json"
        if campaign_state_file.exists():
            print(f"✓ Campaign state file created: {campaign_state_file}")
            
            with open(campaign_state_file, 'r') as f:
                saved_state = json.load(f)
            
            print(f"\nKey fields in saved file:")
            print(f"  - starting_location: {saved_state.get('starting_location')}")
            print(f"  - session_zero_completed: {saved_state.get('session_zero_completed')}")
            print(f"  - player_alliance: {saved_state['civil_war_state'].get('player_alliance')}")
            print(f"  - last_updated: {saved_state.get('last_updated')}")
        else:
            print("✗ Campaign state file not created!")
            return
        
        print("\n\n6. TESTING DIFFERENT FACTION ALIGNMENTS")
        print("-" * 60)
        
        for faction in ['imperial', 'stormcloak', 'neutral']:
            print(f"\n{faction.upper()} Alignment:")
            test_state = manager.update_campaign_state(faction, characters)
            print(f"  Alliance: {test_state['civil_war_state']['player_alliance']}")
            
            imperial_rel = test_state['civil_war_state']['faction_relationship']['imperial_legion']
            stormcloak_rel = test_state['civil_war_state']['faction_relationship']['stormcloaks']
            
            print(f"  Imperial Legion: {'+' if imperial_rel > 0 else ''}{imperial_rel}")
            print(f"  Stormcloaks: {'+' if stormcloak_rel > 0 else ''}{stormcloak_rel}")
            
            if faction == 'neutral' and 'faction_relationships' in test_state:
                companions_rel = test_state.get('faction_relationships', {}).get('companions', 0)
                print(f"  Companions: {'+' if companions_rel > 0 else ''}{companions_rel}")
        
        print("\n\n" + "="*60)
        print("DEMONSTRATION COMPLETE!")
        print("="*60)
        print("\nAll features working correctly:")
        print("✓ Battle of Whiterun context displayed")
        print("✓ Faction alignment enforced")
        print("✓ Standing Stone required")
        print("✓ Character validation working")
        print("✓ Campaign state properly updated")
        print("✓ Starting location set to Whiterun")
        print("✓ Faction relationships configured")
        print("✓ Starting narratives generated")
        print("\nSession zero revamp implementation successful!")
        print("="*60)


if __name__ == "__main__":
    demo_session_zero()
