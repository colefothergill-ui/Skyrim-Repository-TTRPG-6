#!/usr/bin/env python3
"""
Test suite for neutral faction integration
Tests neutral faction starts, NPC stat sheets, and story triggers
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from session_zero import SessionZeroManager
from story_manager import StoryManager
from npc_manager import NPCManager


def test_neutral_faction_npc_stat_sheets():
    """Test that all neutral faction leader NPC stat sheets exist and are valid"""
    print("\n=== Testing Neutral Faction NPC Stat Sheets ===")
    
    try:
        repo_root = Path(__file__).parent.parent
        data_dir = repo_root / "data"
        
        required_npcs = {
            "brynjolf": "Thieves Guild",
            "olfrid_battle-born": "Whiterun Contact",
            "tolfdir": "College of Winterhold Instructor",
            "savos_aren": "Arch-Mage",
            "farengar_secret-fire": "Court Wizard",
            "astrid": "Dark Brotherhood",
            "delphine": "Blades",
            "kodlak_whitemane": "Companions"
        }
        
        for npc_id, role in required_npcs.items():
            stat_path = data_dir / "npc_stat_sheets" / f"{npc_id}.json"
            assert stat_path.exists(), f"{role} stat sheet ({npc_id}) not found"
            
            with open(stat_path, 'r') as f:
                npc_data = json.load(f)
            
            # Validate structure
            assert 'name' in npc_data, f"{npc_id} missing name"
            assert 'id' in npc_data, f"{npc_id} missing id"
            assert 'faction' in npc_data, f"{npc_id} missing faction"
            assert 'aspects' in npc_data, f"{npc_id} missing aspects"
            assert 'skills' in npc_data, f"{npc_id} missing skills"
            
            # Check neutral faction integration fields
            if npc_id != "olfrid_battle-born" and npc_id != "farengar_secret-fire":
                assert 'neutral_faction_integration' in npc_data, f"{npc_id} missing neutral_faction_integration"
            
            print(f"✓ {npc_data['name']} ({role}) stat sheet valid")
        
        return True
        
    except Exception as e:
        print(f"✗ Neutral faction NPC test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_session_zero_neutral_narratives():
    """Test that session zero can generate neutral faction narratives"""
    print("\n=== Testing Session Zero Neutral Faction Narratives ===")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(__file__).parent.parent / "data"
            state_dir = Path(tmpdir) / "state"
            state_dir.mkdir()
            
            manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
            
            # Test each neutral faction narrative
            factions = ["companions", "thieves_guild", "college", "dark_brotherhood", "blades", "greybeards"]
            
            for faction in factions:
                narrative_info = manager.get_neutral_faction_narrative(faction)
                
                assert narrative_info is not None, f"Narrative for {faction} not found"
                assert 'narrative' in narrative_info, f"{faction} missing narrative text"
                assert 'starting_faction' in narrative_info, f"{faction} missing starting_faction"
                assert 'key_npc' in narrative_info, f"{faction} missing key_npc"
                assert len(narrative_info['narrative']) > 100, f"{faction} narrative too short"
                
                print(f"✓ {faction.replace('_', ' ').title()} narrative valid")
            
            return True
            
    except Exception as e:
        print(f"✗ Neutral faction narrative test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_campaign_state_with_neutral_subfaction():
    """Test campaign state creation with specific neutral subfaction"""
    print("\n=== Testing Campaign State with Neutral Subfaction ===")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(__file__).parent.parent / "data"
            state_dir = Path(tmpdir) / "state"
            state_dir.mkdir()
            
            manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
            
            # Create test character
            characters = [{
                'id': 'pc_test_companions',
                'name': 'Test Companion Member',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': 'The Warrior Stone',
                'faction_alignment': 'neutral'
            }]
            
            # Test Companions start
            campaign_state = manager.update_campaign_state('neutral', characters, neutral_subfaction='companions')
            
            assert 'starting_narrative' in campaign_state, "Missing starting narrative"
            assert 'Kodlak' in campaign_state['starting_narrative'], "Companions narrative should mention Kodlak"
            assert 'neutral_subfaction' in campaign_state, "Missing neutral_subfaction field"
            assert campaign_state['neutral_subfaction'] == 'companions', "Neutral subfaction not set correctly"
            assert 'starting_npc_contact' in campaign_state, "Missing starting NPC contact"
            assert campaign_state['starting_npc_contact'] == 'kodlak_whitemane', "Wrong NPC contact"
            
            print("✓ Companions subfaction campaign state valid")
            
            # Test Thieves Guild start
            state_dir_tg = Path(tmpdir) / "state_tg"
            state_dir_tg.mkdir()
            manager_tg = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir_tg))
            
            characters_tg = [{
                'id': 'pc_test_thieves',
                'name': 'Test Thief',
                'player': 'Test Player',
                'race': 'Khajiit',
                'standing_stone': 'The Thief Stone',
                'faction_alignment': 'neutral'
            }]
            
            campaign_state_tg = manager_tg.update_campaign_state('neutral', characters_tg, neutral_subfaction='thieves_guild')
            
            assert 'Brynjolf' in campaign_state_tg['starting_narrative'], "Thieves Guild narrative should mention Brynjolf"
            assert campaign_state_tg['neutral_subfaction'] == 'thieves_guild', "Thieves Guild subfaction not set"
            
            print("✓ Thieves Guild subfaction campaign state valid")
            
            return True
            
    except Exception as e:
        print(f"✗ Neutral subfaction campaign state test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_story_manager_neutral_quest_hooks():
    """Test story manager neutral faction quest hooks"""
    print("\n=== Testing Story Manager Neutral Quest Hooks ===")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(__file__).parent.parent / "data"
            state_dir = Path(tmpdir) / "state"
            state_dir.mkdir()
            
            story_manager = StoryManager(data_dir=str(data_dir), state_dir=str(state_dir))
            
            # Test quest hooks for each faction
            factions = ["companions", "thieves_guild", "college", "dark_brotherhood", "blades", "greybeards"]
            
            for faction in factions:
                hooks = story_manager.get_neutral_faction_quest_hooks(faction)
                
                assert hooks is not None, f"Quest hooks for {faction} not found"
                assert 'quest_name' in hooks, f"{faction} missing quest_name"
                assert 'quest_giver' in hooks, f"{faction} missing quest_giver"
                assert 'objective' in hooks, f"{faction} missing objective"
                assert 'starting_dialogue' in hooks, f"{faction} missing starting_dialogue"
                assert 'complications' in hooks, f"{faction} missing complications"
                
                print(f"✓ {faction.replace('_', ' ').title()} quest hooks valid")
                print(f"  Quest: {hooks['quest_name']}")
                print(f"  Giver: {hooks['quest_giver']}")
            
            return True
            
    except Exception as e:
        print(f"✗ Story manager quest hooks test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_battle_of_whiterun_encounter():
    """Test Battle of Whiterun encounter generation"""
    print("\n=== Testing Battle of Whiterun Encounter ===")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(__file__).parent.parent / "data"
            state_dir = Path(tmpdir) / "state"
            state_dir.mkdir()
            
            story_manager = StoryManager(data_dir=str(data_dir), state_dir=str(state_dir))
            
            # Test basic encounter
            encounter = story_manager.trigger_battle_of_whiterun_encounter()
            
            assert 'encounter_type' in encounter, "Missing encounter type"
            assert encounter['encounter_type'] == 'battle_of_whiterun_choice', "Wrong encounter type"
            assert 'participants' in encounter, "Missing participants"
            assert 'Hadvar' in encounter['participants'], "Hadvar not in participants"
            assert 'Ralof' in encounter['participants'], "Ralof not in participants"
            assert 'choices' in encounter, "Missing choices"
            assert 'assist_hadvar' in encounter['choices'], "Missing Hadvar choice"
            assert 'assist_ralof' in encounter['choices'], "Missing Ralof choice"
            
            print("✓ Basic Battle of Whiterun encounter valid")
            
            # Test Companions-specific encounter
            encounter_comp = story_manager.trigger_battle_of_whiterun_encounter(neutral_subfaction='companions')
            
            assert 'arrival_context' in encounter_comp, "Missing arrival context for Companions"
            assert 'Kodlak' in encounter_comp['arrival_context'], "Companions context should mention Kodlak"
            
            print("✓ Companions-specific encounter valid")
            
            # Test Dark Brotherhood-specific encounter (has extra choice)
            encounter_db = story_manager.trigger_battle_of_whiterun_encounter(neutral_subfaction='dark_brotherhood')
            
            assert 'complete_contract' in encounter_db['choices'], "Dark Brotherhood should have assassination choice"
            
            print("✓ Dark Brotherhood-specific encounter valid (includes assassination option)")
            
            return True
            
    except Exception as e:
        print(f"✗ Battle of Whiterun encounter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_npc_manager_faction_leaders():
    """Test NPC manager can load faction leaders"""
    print("\n=== Testing NPC Manager Faction Leader Loading ===")
    
    try:
        data_dir = Path(__file__).parent.parent / "data"
        state_dir = Path(__file__).parent.parent / "state"
        
        npc_manager = NPCManager(data_dir=str(data_dir), state_dir=str(state_dir))
        
        # Test loading faction leaders
        factions = {
            "companions": "Kodlak Whitemane",
            "thieves_guild": "Brynjolf",
            "college": "Tolfdir",
            "dark_brotherhood": "Astrid",
            "blades": "Delphine"
        }
        
        for faction, expected_name in factions.items():
            npc_data = npc_manager.load_faction_leader_npc(faction)
            
            assert npc_data is not None, f"Failed to load {faction} leader"
            assert npc_data['name'] == expected_name, f"Wrong name for {faction} leader"
            
            print(f"✓ {expected_name} ({faction}) loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ NPC manager faction leader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("NEUTRAL FACTION INTEGRATION TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Neutral Faction NPC Stat Sheets", test_neutral_faction_npc_stat_sheets()))
    results.append(("Session Zero Neutral Narratives", test_session_zero_neutral_narratives()))
    results.append(("Campaign State with Neutral Subfaction", test_campaign_state_with_neutral_subfaction()))
    results.append(("Story Manager Neutral Quest Hooks", test_story_manager_neutral_quest_hooks()))
    results.append(("Battle of Whiterun Encounter", test_battle_of_whiterun_encounter()))
    results.append(("NPC Manager Faction Leaders", test_npc_manager_faction_leaders()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
