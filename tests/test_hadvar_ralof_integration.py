#!/usr/bin/env python3
"""
Test suite for Hadvar and Ralof NPC integration
Tests companion assignment, loyalty tracking, and story integration
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


def test_npc_stat_sheets_exist():
    """Test that Hadvar and Ralof stat sheets exist and are properly formatted"""
    print("\n=== Testing NPC Stat Sheets ===")
    
    try:
        repo_root = Path(__file__).parent.parent
        hadvar_path = repo_root / "data" / "npc_stat_sheets" / "hadvar.json"
        ralof_path = repo_root / "data" / "npc_stat_sheets" / "ralof.json"
        
        # Test Hadvar exists
        assert hadvar_path.exists(), "Hadvar stat sheet not found"
        with open(hadvar_path, 'r') as f:
            hadvar = json.load(f)
        
        # Validate Hadvar structure
        assert hadvar['name'] == "Hadvar", "Hadvar name incorrect"
        assert hadvar['id'] == "npc_stat_hadvar", "Hadvar ID incorrect"
        assert hadvar['faction'] == "Imperial Legion", "Hadvar faction incorrect"
        assert 'aspects' in hadvar, "Hadvar missing aspects"
        assert 'skills' in hadvar, "Hadvar missing skills"
        assert 'stunts' in hadvar, "Hadvar missing stunts"
        assert 'companion_mechanics' in hadvar, "Hadvar missing companion mechanics"
        assert 'starting_loyalty' in hadvar['companion_mechanics'], "Hadvar missing starting loyalty"
        print("✓ Hadvar stat sheet valid")
        
        # Test Ralof exists
        assert ralof_path.exists(), "Ralof stat sheet not found"
        with open(ralof_path, 'r') as f:
            ralof = json.load(f)
        
        # Validate Ralof structure
        assert ralof['name'] == "Ralof", "Ralof name incorrect"
        assert ralof['id'] == "npc_stat_ralof", "Ralof ID incorrect"
        assert ralof['faction'] == "Stormcloaks", "Ralof faction incorrect"
        assert 'aspects' in ralof, "Ralof missing aspects"
        assert 'skills' in ralof, "Ralof missing skills"
        assert 'stunts' in ralof, "Ralof missing stunts"
        assert 'companion_mechanics' in ralof, "Ralof missing companion mechanics"
        assert 'starting_loyalty' in ralof['companion_mechanics'], "Ralof missing starting loyalty"
        print("✓ Ralof stat sheet valid")
        
        # Test that loyalty mechanics are defined
        assert 'loyalty_increases' in hadvar['companion_mechanics'], "Hadvar missing loyalty increase triggers"
        assert 'loyalty_decreases' in hadvar['companion_mechanics'], "Hadvar missing loyalty decrease triggers"
        assert 'loyalty_increases' in ralof['companion_mechanics'], "Ralof missing loyalty increase triggers"
        assert 'loyalty_decreases' in ralof['companion_mechanics'], "Ralof missing loyalty decrease triggers"
        print("✓ Loyalty mechanics defined for both NPCs")
        
        # Test companion quests exist
        assert 'companion_quests' in hadvar['companion_mechanics'], "Hadvar missing companion quests"
        assert 'companion_quests' in ralof['companion_mechanics'], "Ralof missing companion quests"
        print("✓ Companion quests defined")
        
        return True
        
    except Exception as e:
        print(f"✗ NPC stat sheet test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_imperial_companion_assignment():
    """Test that Hadvar is assigned when Imperial alignment is chosen"""
    print("\n=== Testing Imperial Companion Assignment ===")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            state_dir = Path(tmpdir) / "state"
            data_dir.mkdir()
            state_dir.mkdir()
            
            # Create character data
            characters = [{
                'id': 'pc_test',
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': 'The Warrior Stone',
                'faction_alignment': 'imperial'
            }]
            
            manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
            campaign_state = manager.update_campaign_state('imperial', characters)
            
            # Verify Hadvar is assigned
            assert 'companions' in campaign_state, "Companions section missing"
            assert 'active_companions' in campaign_state['companions'], "Active companions list missing"
            assert len(campaign_state['companions']['active_companions']) == 1, "Should have exactly 1 active companion"
            
            companion = campaign_state['companions']['active_companions'][0]
            assert companion['name'] == 'Hadvar', "Imperial alignment should assign Hadvar"
            assert companion['npc_id'] == 'npc_stat_hadvar', "Hadvar NPC ID incorrect"
            assert companion['loyalty'] == 60, "Starting loyalty should be 60"
            assert companion['faction_affinity'] == 'imperial_legion', "Hadvar faction affinity incorrect"
            print("✓ Hadvar correctly assigned for Imperial alignment")
            
            # Verify branching decision recorded
            assert 'branching_decisions' in campaign_state, "Branching decisions missing"
            assert campaign_state['branching_decisions']['civil_war_entry_contact'] == 'Hadvar', "Civil War entry contact decision not recorded"
            print("✓ Civil War entry contact decision recorded")
            
            # Verify narrative mentions Hadvar
            assert 'Hadvar' in campaign_state['starting_narrative'], "Starting narrative should mention Hadvar"
            print("✓ Starting narrative includes Hadvar")
            
            return True
            
    except Exception as e:
        print(f"✗ Imperial companion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_stormcloak_companion_assignment():
    """Test that Ralof is assigned when Stormcloak alignment is chosen"""
    print("\n=== Testing Stormcloak Companion Assignment ===")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            state_dir = Path(tmpdir) / "state"
            data_dir.mkdir()
            state_dir.mkdir()
            
            # Create character data
            characters = [{
                'id': 'pc_test',
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': 'The Warrior Stone',
                'faction_alignment': 'stormcloak'
            }]
            
            manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
            campaign_state = manager.update_campaign_state('stormcloak', characters)
            
            # Verify Ralof is assigned
            assert 'companions' in campaign_state, "Companions section missing"
            assert 'active_companions' in campaign_state['companions'], "Active companions list missing"
            assert len(campaign_state['companions']['active_companions']) == 1, "Should have exactly 1 active companion"
            
            companion = campaign_state['companions']['active_companions'][0]
            assert companion['name'] == 'Ralof', "Stormcloak alignment should assign Ralof"
            assert companion['npc_id'] == 'npc_stat_ralof', "Ralof NPC ID incorrect"
            assert companion['loyalty'] == 60, "Starting loyalty should be 60"
            assert companion['faction_affinity'] == 'stormcloaks', "Ralof faction affinity incorrect"
            print("✓ Ralof correctly assigned for Stormcloak alignment")
            
            # Verify branching decision recorded
            assert 'branching_decisions' in campaign_state, "Branching decisions missing"
            assert campaign_state['branching_decisions']['civil_war_entry_contact'] == 'Ralof', "Civil War entry contact decision not recorded"
            print("✓ Civil War entry contact decision recorded")
            
            # Verify narrative mentions Ralof
            assert 'Ralof' in campaign_state['starting_narrative'], "Starting narrative should mention Ralof"
            print("✓ Starting narrative includes Ralof")
            
            return True
            
    except Exception as e:
        print(f"✗ Stormcloak companion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_neutral_companion_availability():
    """Test that both companions are available when neutral alignment is chosen"""
    print("\n=== Testing Neutral Companion Availability ===")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            state_dir = Path(tmpdir) / "state"
            data_dir.mkdir()
            state_dir.mkdir()
            
            # Create character data
            characters = [{
                'id': 'pc_test',
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': 'The Warrior Stone',
                'faction_alignment': 'neutral'
            }]
            
            manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
            campaign_state = manager.update_campaign_state('neutral', characters)
            
            # Verify no active companions
            assert 'companions' in campaign_state, "Companions section missing"
            assert 'active_companions' in campaign_state['companions'], "Active companions list missing"
            assert len(campaign_state['companions']['active_companions']) == 0, "Neutral should have 0 active companions initially"
            print("✓ No active companions for neutral alignment")
            
            # Verify both are available
            assert 'available_companions' in campaign_state['companions'], "Available companions list missing"
            assert len(campaign_state['companions']['available_companions']) == 2, "Should have both companions available"
            
            available_names = [c['name'] for c in campaign_state['companions']['available_companions']]
            assert 'Hadvar' in available_names, "Hadvar should be available"
            assert 'Ralof' in available_names, "Ralof should be available"
            print("✓ Both Hadvar and Ralof available for neutral alignment")
            
            # Verify branching decision is undecided
            assert 'branching_decisions' in campaign_state, "Branching decisions missing"
            assert campaign_state['branching_decisions']['civil_war_entry_contact'] == 'undecided', "Civil War entry contact should be undecided"
            print("✓ Civil War entry contact marked as undecided")
            
            # Verify narrative mentions both
            assert 'Hadvar' in campaign_state['starting_narrative'], "Starting narrative should mention Hadvar"
            assert 'Ralof' in campaign_state['starting_narrative'], "Starting narrative should mention Ralof"
            print("✓ Starting narrative mentions both companions")
            
            return True
            
    except Exception as e:
        print(f"✗ Neutral companion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_story_manager_companion_methods():
    """Test StoryManager methods for companion integration"""
    print("\n=== Testing Story Manager Companion Methods ===")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            state_dir = Path(tmpdir) / "state"
            data_dir.mkdir()
            state_dir.mkdir()
            
            # Create campaign state with Hadvar
            campaign_state = {
                "campaign_id": "test",
                "branching_decisions": {
                    "civil_war_entry_contact": "Hadvar"
                },
                "companions": {
                    "active_companions": [{
                        "npc_id": "npc_stat_hadvar",
                        "name": "Hadvar",
                        "status": "active",
                        "loyalty": 60
                    }]
                }
            }
            
            state_file = state_dir / "campaign_state.json"
            with open(state_file, 'w') as f:
                json.dump(campaign_state, f)
            
            # Test get_starting_companion
            story_manager = StoryManager(data_dir=str(data_dir), state_dir=str(state_dir))
            companion = story_manager.get_starting_companion()
            
            assert companion is not None, "Should return companion"
            assert companion['name'] == 'Hadvar', "Should return Hadvar"
            print("✓ get_starting_companion works correctly")
            
            # Test get_companion_dialogue_hooks for Whiterun
            dialogue_hooks = story_manager.get_companion_dialogue_hooks("Whiterun", "arrival")
            
            assert 'companions' in dialogue_hooks, "Should have companions section"
            assert len(dialogue_hooks['companions']) > 0, "Should have companion dialogue hooks"
            
            hadvar_hooks = dialogue_hooks['companions'][0]
            assert hadvar_hooks['name'] == 'Hadvar', "Should have Hadvar hooks"
            assert len(hadvar_hooks['hooks']) > 0, "Should have dialogue hooks for Hadvar"
            print("✓ get_companion_dialogue_hooks works correctly")
            
            return True
            
    except Exception as e:
        print(f"✗ Story manager companion methods test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_civil_war_quest_integration():
    """Test that civil war quests reference companions"""
    print("\n=== Testing Civil War Quest Integration ===")
    
    try:
        repo_root = Path(__file__).parent.parent
        civil_war_path = repo_root / "data" / "quests" / "civil_war_quests.json"
        
        assert civil_war_path.exists(), "Civil war quests file not found"
        
        with open(civil_war_path, 'r') as f:
            civil_war_data = json.load(f)
        
        # Test Imperial version has Hadvar support
        imperial_battle = civil_war_data['civil_war_questline']['quests']['battle_of_whiterun']['imperial_version']
        assert 'companion_support' in imperial_battle, "Imperial battle missing companion support"
        assert 'hadvar' in imperial_battle['companion_support'], "Imperial battle missing Hadvar support"
        
        hadvar_support = imperial_battle['companion_support']['hadvar']
        assert 'bonuses' in hadvar_support, "Hadvar support missing bonuses"
        assert 'dialogue' in hadvar_support, "Hadvar support missing dialogue"
        print("✓ Imperial Battle of Whiterun includes Hadvar support")
        
        # Test Stormcloak version has Ralof support
        stormcloak_battle = civil_war_data['civil_war_questline']['quests']['battle_of_whiterun']['stormcloak_version']
        assert 'companion_support' in stormcloak_battle, "Stormcloak battle missing companion support"
        assert 'ralof' in stormcloak_battle['companion_support'], "Stormcloak battle missing Ralof support"
        
        ralof_support = stormcloak_battle['companion_support']['ralof']
        assert 'bonuses' in ralof_support, "Ralof support missing bonuses"
        assert 'dialogue' in ralof_support, "Ralof support missing dialogue"
        print("✓ Stormcloak Battle of Whiterun includes Ralof support")
        
        # Test rewards mention loyalty
        assert 'hadvar_loyalty' in imperial_battle['rewards'], "Imperial battle should reward Hadvar loyalty"
        assert 'ralof_loyalty' in stormcloak_battle['rewards'], "Stormcloak battle should reward Ralof loyalty"
        print("✓ Battle rewards include companion loyalty bonuses")
        
        return True
        
    except Exception as e:
        print(f"✗ Civil war quest integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("HADVAR AND RALOF INTEGRATION TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("NPC Stat Sheets", test_npc_stat_sheets_exist()))
    results.append(("Imperial Companion Assignment", test_imperial_companion_assignment()))
    results.append(("Stormcloak Companion Assignment", test_stormcloak_companion_assignment()))
    results.append(("Neutral Companion Availability", test_neutral_companion_availability()))
    results.append(("Story Manager Companion Methods", test_story_manager_companion_methods()))
    results.append(("Civil War Quest Integration", test_civil_war_quest_integration()))
    
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
