#!/usr/bin/env python3
"""
Test suite for Session Zero functionality
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from session_zero import SessionZeroManager


def test_session_zero_initialization():
    """Test SessionZeroManager initialization"""
    print("\n=== Testing Session Zero Initialization ===")
    try:
        # Create temporary directories for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            state_dir = Path(tmpdir) / "state"
            data_dir.mkdir()
            state_dir.mkdir()
            
            manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
            
            assert manager.data_dir == data_dir, "Data directory not set correctly"
            assert manager.state_dir == state_dir, "State directory not set correctly"
            
            print("✓ SessionZeroManager initializes correctly")
            return True
            
    except Exception as e:
        print(f"✗ Initialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_validate_character_data():
    """Test character data validation"""
    print("\n=== Testing Character Data Validation ===")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            state_dir = Path(tmpdir) / "state"
            data_dir.mkdir()
            state_dir.mkdir()
            
            manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
            
            # Test 1: Valid complete character
            valid_character = {
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': 'The Warrior Stone',
                'faction_alignment': 'imperial',
                'aspects': {
                    'high_concept': 'Nord Warrior Seeking Glory',
                    'trouble': 'Haunted by Past Failures',
                    'other_aspects': ['Loyal to Friends', 'Distrusts Magic']
                },
                'skills': {
                    'Great (+4)': ['Fight'],
                    'Good (+3)': ['Athletics', 'Physique'],
                    'Fair (+2)': ['Will', 'Notice', 'Rapport'],
                    'Average (+1)': ['Shoot', 'Stealth', 'Lore', 'Empathy']
                },
                'stunts': [
                    'Whirlwind Attack: Once per scene, attack all enemies',
                    'Battle Fury: +2 to Fight when wounded',
                    'Unbreakable: +2 to defend against physical attacks'
                ]
            }
            assert manager.validate_character_data(valid_character), "Valid complete character should pass validation"
            print("✓ Valid complete character passes validation")
            
            # Test 2: Missing required field
            invalid_character = {
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord'
                # Missing standing_stone and faction_alignment
            }
            assert not manager.validate_character_data(invalid_character), "Invalid character should fail validation"
            print("✓ Missing fields correctly detected")
            
            # Test 3: Invalid faction alignment
            invalid_faction = {
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': 'The Warrior Stone',
                'faction_alignment': 'invalid_faction',
                'aspects': {
                    'high_concept': 'Test Concept',
                    'trouble': 'Test Trouble',
                    'other_aspects': ['Test Aspect']
                },
                'skills': {
                    'Great (+4)': ['Fight'],
                    'Good (+3)': ['Athletics', 'Physique'],
                    'Fair (+2)': ['Will', 'Notice', 'Rapport'],
                    'Average (+1)': ['Shoot', 'Stealth', 'Lore', 'Empathy']
                },
                'stunts': ['Stunt 1', 'Stunt 2', 'Stunt 3']
            }
            assert not manager.validate_character_data(invalid_faction), "Invalid faction should fail validation"
            print("✓ Invalid faction alignment detected")
            
            # Test 4: Empty standing stone
            empty_stone = {
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': '',
                'faction_alignment': 'imperial'
            }
            assert not manager.validate_character_data(empty_stone), "Empty standing stone should fail validation"
            print("✓ Empty standing stone detected")
            
            # Test 5: Missing trouble aspect
            missing_trouble = {
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': 'The Warrior Stone',
                'faction_alignment': 'imperial',
                'aspects': {
                    'high_concept': 'Test Concept',
                    'trouble': '[Player to define - Required]',  # Not filled
                    'other_aspects': ['Test Aspect']
                },
                'skills': {
                    'Great (+4)': ['Fight'],
                    'Good (+3)': ['Athletics', 'Physique'],
                    'Fair (+2)': ['Will', 'Notice', 'Rapport'],
                    'Average (+1)': ['Shoot', 'Stealth', 'Lore', 'Empathy']
                },
                'stunts': ['Stunt 1', 'Stunt 2', 'Stunt 3']
            }
            assert not manager.validate_character_data(missing_trouble), "Missing trouble should fail validation"
            print("✓ Missing trouble aspect detected")
            
            # Test 6: Invalid skill pyramid (wrong count)
            invalid_skills = {
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': 'The Warrior Stone',
                'faction_alignment': 'imperial',
                'aspects': {
                    'high_concept': 'Test Concept',
                    'trouble': 'Test Trouble',
                    'other_aspects': ['Test Aspect']
                },
                'skills': {
                    'Great (+4)': ['Fight', 'Athletics'],  # Should be 1, not 2
                    'Good (+3)': ['Physique'],
                    'Fair (+2)': ['Will', 'Notice', 'Rapport'],
                    'Average (+1)': ['Shoot', 'Stealth', 'Lore', 'Empathy']
                },
                'stunts': ['Stunt 1', 'Stunt 2', 'Stunt 3']
            }
            assert not manager.validate_character_data(invalid_skills), "Invalid skill pyramid should fail validation"
            print("✓ Invalid skill pyramid detected")
            
            # Test 7: Wrong number of stunts
            wrong_stunts = {
                'name': 'Test Character',
                'player': 'Test Player',
                'race': 'Nord',
                'standing_stone': 'The Warrior Stone',
                'faction_alignment': 'imperial',
                'aspects': {
                    'high_concept': 'Test Concept',
                    'trouble': 'Test Trouble',
                    'other_aspects': ['Test Aspect']
                },
                'skills': {
                    'Great (+4)': ['Fight'],
                    'Good (+3)': ['Athletics', 'Physique'],
                    'Fair (+2)': ['Will', 'Notice', 'Rapport'],
                    'Average (+1)': ['Shoot', 'Stealth', 'Lore', 'Empathy']
                },
                'stunts': ['Stunt 1', 'Stunt 2']  # Should be 3, not 2
            }
            assert not manager.validate_character_data(wrong_stunts), "Wrong number of stunts should fail validation"
            print("✓ Wrong number of stunts detected")
            
            print("\n✓ ALL CHARACTER VALIDATION TESTS PASSED")
            return True
            
    except Exception as e:
        print(f"✗ Character validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_update_campaign_state():
    """Test campaign state update functionality"""
    print("\n=== Testing Campaign State Update ===")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir) / "data"
            state_dir = Path(tmpdir) / "state"
            data_dir.mkdir()
            state_dir.mkdir()
            
            manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
            
            # Test character data
            characters = [
                {
                    'id': 'pc_test_char',
                    'name': 'Test Character',
                    'player': 'Test Player',
                    'race': 'Nord',
                    'standing_stone': 'The Warrior Stone',
                    'faction_alignment': 'imperial',
                    'aspects': {
                        'high_concept': 'Nord Warrior',
                        'trouble': 'Hot-Headed',
                        'other_aspects': ['Loyal']
                    }
                }
            ]
            
            # Test 1: Imperial alignment
            campaign_state = manager.update_campaign_state('imperial', characters)
            
            assert campaign_state['starting_location'] == 'Whiterun', "Starting location should be Whiterun"
            assert campaign_state['civil_war_state']['player_alliance'] == 'imperial', "Player alliance should be imperial"
            assert campaign_state['session_zero_completed'] == True, "Session zero should be marked complete"
            assert campaign_state['civil_war_state']['faction_relationship']['imperial_legion'] == 30, "Imperial relationship should be positive"
            assert campaign_state['civil_war_state']['faction_relationship']['stormcloaks'] == -20, "Stormcloak relationship should be negative"
            print("✓ Imperial alignment sets correct state")
            
            # Test 2: Stormcloak alignment
            campaign_state = manager.update_campaign_state('stormcloak', characters)
            assert campaign_state['civil_war_state']['player_alliance'] == 'stormcloak', "Player alliance should be stormcloak"
            assert campaign_state['civil_war_state']['faction_relationship']['imperial_legion'] == -20, "Imperial relationship should be negative"
            assert campaign_state['civil_war_state']['faction_relationship']['stormcloaks'] == 30, "Stormcloak relationship should be positive"
            print("✓ Stormcloak alignment sets correct state")
            
            # Test 3: Neutral alignment
            campaign_state = manager.update_campaign_state('neutral', characters)
            assert campaign_state['civil_war_state']['player_alliance'] == 'neutral', "Player alliance should be neutral"
            assert campaign_state['civil_war_state']['faction_relationship']['imperial_legion'] == 0, "Imperial relationship should be neutral"
            assert campaign_state['civil_war_state']['faction_relationship']['stormcloaks'] == 0, "Stormcloak relationship should be neutral"
            assert 'companions' in campaign_state.get('faction_relationships', {}), "Companions relationship should be set"
            print("✓ Neutral alignment sets correct state")
            
            # Test 4: Starting narratives
            for alignment in ['imperial', 'stormcloak', 'neutral']:
                campaign_state = manager.update_campaign_state(alignment, characters)
                assert 'starting_narrative' in campaign_state, f"Starting narrative should exist for {alignment}"
                assert 'Whiterun' in campaign_state['starting_narrative'], f"Narrative should mention Whiterun for {alignment}"
                assert 'Battle of Whiterun' in campaign_state['starting_narrative'], f"Narrative should mention Battle of Whiterun for {alignment}"
            print("✓ Starting narratives created correctly")
            
            # Test 5: Player characters added
            assert len(campaign_state['player_characters']) == 1, "Player character should be added"
            assert campaign_state['player_characters'][0]['name'] == 'Test Character', "Character name should match"
            print("✓ Player characters added to campaign state")
            
            # Test 6: Verify file is saved
            campaign_state_file = state_dir / "campaign_state.json"
            assert campaign_state_file.exists(), "Campaign state file should be created"
            
            with open(campaign_state_file, 'r') as f:
                saved_state = json.load(f)
            assert saved_state['starting_location'] == 'Whiterun', "Saved state should have correct starting location"
            print("✓ Campaign state file saved correctly")
            
            print("\n✓ ALL CAMPAIGN STATE UPDATE TESTS PASSED")
            return True
            
    except Exception as e:
        print(f"✗ Campaign state update test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_character_template_creation():
    """Test character template creation with faction alignment"""
    print("\n=== Testing Character Template Creation ===")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create data structure with races
            data_dir = Path(tmpdir) / "data"
            state_dir = Path(tmpdir) / "state"
            data_dir.mkdir()
            state_dir.mkdir()
            
            # Create a test races file
            source_dir = data_dir.parent / "source_material" / "converted_pdfs"
            source_dir.mkdir(parents=True)
            
            races_data = {
                "races": [
                    {
                        "name": "Nord",
                        "description": "Test Nord",
                        "starting_aspect": "Child of Skyrim",
                        "racial_ability": {
                            "name": "Resist Frost",
                            "effect": "Resist cold"
                        },
                        "skill_bonuses": ["Fight", "Athletics"]
                    }
                ]
            }
            
            with open(source_dir / "races.json", 'w') as f:
                json.dump(races_data, f)
            
            manager = SessionZeroManager(data_dir=str(data_dir), state_dir=str(state_dir))
            
            # Create character template
            character = manager.create_character_template(
                "Test Player",
                "Test Character",
                "Nord",
                "The Warrior Stone"
            )
            
            assert character is not None, "Character template should be created"
            assert character['name'] == 'Test Character', "Character name should match"
            assert character['player'] == 'Test Player', "Player name should match"
            assert character['race'] == 'Nord', "Race should match"
            assert character['standing_stone'] == 'The Warrior Stone', "Standing stone should match"
            print("✓ Character template created with all required fields")
            
            print("\n✓ ALL CHARACTER TEMPLATE CREATION TESTS PASSED")
            return True
            
    except Exception as e:
        print(f"✗ Character template creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("SESSION ZERO TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Session Zero Initialization", test_session_zero_initialization()))
    results.append(("Character Data Validation", test_validate_character_data()))
    results.append(("Campaign State Update", test_update_campaign_state()))
    results.append(("Character Template Creation", test_character_template_creation()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
