#!/usr/bin/env python3
"""
Tests for NPC Manager enhancements
Including companion system, decision points, and dialogue trees
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from npc_manager import NPCManager


def setup_test_environment():
    """Create temporary test environment"""
    test_dir = tempfile.mkdtemp()
    data_dir = Path(test_dir) / "data"
    state_dir = Path(test_dir) / "state"
    
    data_dir.mkdir()
    state_dir.mkdir()
    (data_dir / "npcs").mkdir()
    
    # Create test campaign state
    campaign_state = {
        "campaign_id": "test_001",
        "companions": {
            "active_companions": [],
            "available_companions": [
                {
                    "npc_id": "test_companion",
                    "name": "Test Companion",
                    "status": "available",
                    "loyalty": 60,
                    "location": "Test Location",
                    "recruitment_condition": "None",
                    "faction_affinity": "test_faction"
                }
            ],
            "dismissed_companions": [],
            "companion_relationships": {}
        },
        "last_updated": "2026-01-27"
    }
    
    with open(state_dir / "campaign_state.json", 'w') as f:
        json.dump(campaign_state, f, indent=2)
    
    # Create test NPC
    test_npc = {
        "name": "Test Companion",
        "id": "test_companion",
        "faction": "test_faction",
        "loyalty": 60,
        "decision_points": {
            "test_decision": {
                "condition": "test_condition",
                "options": ["option_a", "option_b"],
                "consequences": {
                    "option_a": {
                        "loyalty_change": 5,
                        "note": "Good choice"
                    },
                    "option_b": {
                        "loyalty_change": -5,
                        "note": "Bad choice"
                    }
                }
            }
        },
        "dialogue_trees": {
            "greeting": {
                "greeting": "Hello, adventurer!",
                "responses": [
                    {
                        "option": "Join me",
                        "leads_to": "accept",
                        "loyalty_change": 5
                    },
                    {
                        "option": "Go away",
                        "loyalty_change": -5
                    }
                ]
            },
            "accept": {
                "dialogue": "I'll join you!",
                "quest_activated": "test_quest"
            }
        },
        "relationships": {
            "test_faction": "Loyal member"
        }
    }
    
    with open(data_dir / "npcs" / "test_companion.json", 'w') as f:
        json.dump(test_npc, f, indent=2)
    
    return test_dir, data_dir, state_dir


def teardown_test_environment(test_dir):
    """Clean up test environment"""
    shutil.rmtree(test_dir)


def test_companion_recruitment():
    """Test recruiting a companion"""
    print("\n=== Testing Companion Recruitment ===")
    test_dir, data_dir, state_dir = setup_test_environment()
    
    try:
        manager = NPCManager(data_dir=str(data_dir), state_dir=str(state_dir))
        
        # Test getting available companions
        available = manager.get_available_companions()
        assert len(available) == 1, "Should have 1 available companion"
        assert available[0]['npc_id'] == 'test_companion', "Should be test_companion"
        print("✓ Get available companions works")
        
        # Test recruitment
        success = manager.recruit_companion('test_companion')
        assert success, "Recruitment should succeed"
        print("✓ Companion recruitment works")
        
        # Verify companion is now active
        active = manager.get_active_companions()
        assert len(active) == 1, "Should have 1 active companion"
        assert active[0]['npc_id'] == 'test_companion', "Should be test_companion"
        print("✓ Active companion tracking works")
        
        # Verify companion removed from available
        available = manager.get_available_companions()
        assert len(available) == 0, "Should have 0 available companions after recruitment"
        print("✓ Companion removed from available list")
        
        # Test duplicate recruitment prevention
        success = manager.recruit_companion('test_companion')
        assert not success, "Should not be able to recruit already active companion"
        print("✓ Duplicate recruitment prevention works")
        
        print("\n✓ ALL COMPANION RECRUITMENT TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Companion recruitment test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        teardown_test_environment(test_dir)


def test_companion_dismissal():
    """Test dismissing a companion"""
    print("\n=== Testing Companion Dismissal ===")
    test_dir, data_dir, state_dir = setup_test_environment()
    
    try:
        manager = NPCManager(data_dir=str(data_dir), state_dir=str(state_dir))
        
        # First recruit the companion
        manager.recruit_companion('test_companion')
        
        # Test dismissal
        success = manager.dismiss_companion('test_companion')
        assert success, "Dismissal should succeed"
        print("✓ Companion dismissal works")
        
        # Verify companion is no longer active
        active = manager.get_active_companions()
        assert len(active) == 0, "Should have 0 active companions after dismissal"
        print("✓ Companion removed from active list")
        
        # Verify companion is in dismissed list
        state = manager.load_campaign_state()
        dismissed = state['companions']['dismissed_companions']
        assert len(dismissed) == 1, "Should have 1 dismissed companion"
        print("✓ Companion added to dismissed list")
        
        print("\n✓ ALL COMPANION DISMISSAL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Companion dismissal test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        teardown_test_environment(test_dir)


def test_faction_alignment():
    """Test faction alignment checking"""
    print("\n=== Testing Faction Alignment ===")
    test_dir, data_dir, state_dir = setup_test_environment()
    
    try:
        manager = NPCManager(data_dir=str(data_dir), state_dir=str(state_dir))
        
        # Test alignment with NPC's own faction
        alignment = manager.check_faction_alignment('test_companion', 'test_faction')
        assert alignment == 'allied', f"Should be allied to own faction, got {alignment}"
        print("✓ Own faction alignment works")
        
        # Test alignment with unrelated faction
        alignment = manager.check_faction_alignment('test_companion', 'other_faction')
        assert alignment in ['neutral', 'unknown'], f"Should be neutral/unknown to other faction, got {alignment}"
        print("✓ Other faction alignment works")
        
        print("\n✓ ALL FACTION ALIGNMENT TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Faction alignment test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        teardown_test_environment(test_dir)


def test_decision_points():
    """Test NPC decision point processing"""
    print("\n=== Testing Decision Points ===")
    test_dir, data_dir, state_dir = setup_test_environment()
    
    try:
        manager = NPCManager(data_dir=str(data_dir), state_dir=str(state_dir))
        
        # Load initial loyalty
        npc = manager.load_npc('test_companion')
        initial_loyalty = npc['loyalty']
        
        # Test decision point with positive outcome
        result = manager.process_decision_point('test_companion', 'test_decision', 'option_a')
        assert result['success'], "Decision processing should succeed"
        assert result['option'] == 'option_a', "Should record chosen option"
        print("✓ Decision point processing works")
        
        # Verify loyalty changed
        npc = manager.load_npc('test_companion')
        new_loyalty = npc['loyalty']
        assert new_loyalty > initial_loyalty, f"Loyalty should increase, was {initial_loyalty}, now {new_loyalty}"
        print(f"✓ Loyalty changed correctly: {initial_loyalty} -> {new_loyalty}")
        
        print("\n✓ ALL DECISION POINT TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Decision point test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        teardown_test_environment(test_dir)


def test_dialogue_trees():
    """Test dialogue tree interactions"""
    print("\n=== Testing Dialogue Trees ===")
    test_dir, data_dir, state_dir = setup_test_environment()
    
    try:
        manager = NPCManager(data_dir=str(data_dir), state_dir=str(state_dir))
        
        # Test getting initial dialogue
        result = manager.handle_dialogue_interaction('test_companion', 'greeting')
        assert result['success'], "Dialogue should succeed"
        assert 'responses' in result, "Should return available responses"
        assert len(result['responses']) == 2, "Should have 2 response options"
        print("✓ Initial dialogue retrieval works")
        
        # Test choosing a response
        npc = manager.load_npc('test_companion')
        initial_loyalty = npc['loyalty']
        
        result = manager.handle_dialogue_interaction('test_companion', 'greeting', 0)
        assert result['success'], "Response handling should succeed"
        print("✓ Response selection works")
        
        # Verify loyalty changed
        npc = manager.load_npc('test_companion')
        new_loyalty = npc['loyalty']
        assert new_loyalty != initial_loyalty, "Loyalty should change after response"
        print(f"✓ Dialogue loyalty change works: {initial_loyalty} -> {new_loyalty}")
        
        # Verify next dialogue
        if 'next_dialogue' in result:
            assert result['next_dialogue'] == 'accept', "Should lead to 'accept' dialogue"
            print("✓ Dialogue branching works")
        
        print("\n✓ ALL DIALOGUE TREE TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Dialogue tree test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        teardown_test_environment(test_dir)


def test_npc_json_schemas():
    """Test that all new NPC JSON files are valid"""
    print("\n=== Testing NPC JSON Schemas ===")
    
    try:
        repo_root = Path(__file__).parent.parent
        npcs_dir = repo_root / "data" / "npcs"
        
        required_npcs = [
            "general_tullius.json",
            "ulfric_stormcloak.json",
            "lydia.json",
            "aela_the_huntress.json"
        ]
        
        required_fields = ["name", "id", "type", "faction", "aspects", "skills"]
        
        for npc_file in required_npcs:
            npc_path = npcs_dir / npc_file
            assert npc_path.exists(), f"NPC file {npc_file} should exist"
            
            with open(npc_path, 'r') as f:
                npc_data = json.load(f)
            
            # Check required fields
            for field in required_fields:
                assert field in npc_data, f"{npc_file} missing required field: {field}"
            
            # Check Fate Core aspects structure
            assert 'high_concept' in npc_data['aspects'], f"{npc_file} missing high_concept"
            assert 'trouble' in npc_data['aspects'], f"{npc_file} missing trouble"
            
            # Check skills structure
            skill_levels = ['Great', 'Good', 'Fair', 'Average']
            for level in skill_levels:
                assert level in npc_data['skills'], f"{npc_file} missing skill level: {level}"
            
            print(f"✓ {npc_file} schema valid")
        
        print("\n✓ ALL NPC JSON SCHEMA TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ NPC JSON schema test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_campaign_state_companions():
    """Test that campaign state has companions structure"""
    print("\n=== Testing Campaign State Companions Structure ===")
    
    try:
        repo_root = Path(__file__).parent.parent
        state_path = repo_root / "state" / "campaign_state.json"
        
        assert state_path.exists(), "Campaign state file should exist"
        
        with open(state_path, 'r') as f:
            state = json.load(f)
        
        # Check companions key exists
        assert 'companions' in state, "Campaign state missing 'companions' key"
        
        companions = state['companions']
        
        # Check required subkeys
        required_keys = ['active_companions', 'available_companions', 'dismissed_companions']
        for key in required_keys:
            assert key in companions, f"Companions missing required key: {key}"
        
        # Verify structure
        assert isinstance(companions['active_companions'], list), "active_companions should be a list"
        assert isinstance(companions['available_companions'], list), "available_companions should be a list"
        
        # Check available companions have required fields
        for companion in companions['available_companions']:
            assert 'npc_id' in companion, "Companion missing npc_id"
            assert 'name' in companion, "Companion missing name"
            assert 'loyalty' in companion, "Companion missing loyalty"
            assert 'status' in companion, "Companion missing status"
        
        print("✓ Campaign state companions structure valid")
        print(f"✓ Found {len(companions['available_companions'])} available companions")
        
        print("\n✓ ALL CAMPAIGN STATE TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Campaign state test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all NPC enhancement tests"""
    print("="*60)
    print("NPC ENHANCEMENT TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Companion Recruitment", test_companion_recruitment()))
    results.append(("Companion Dismissal", test_companion_dismissal()))
    results.append(("Faction Alignment", test_faction_alignment()))
    results.append(("Decision Points", test_decision_points()))
    results.append(("Dialogue Trees", test_dialogue_trees()))
    results.append(("NPC JSON Schemas", test_npc_json_schemas()))
    results.append(("Campaign State Companions", test_campaign_state_companions()))
    
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
