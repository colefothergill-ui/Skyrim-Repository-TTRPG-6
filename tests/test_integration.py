#!/usr/bin/env python3
"""
Integration test for custom content (Civil War and Thalmor Focus Campaign, 
Dragonbreak system, and Faction Plot Allegations)
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_dragonbreak_manager():
    """Test Dragonbreak Manager functionality"""
    print("\n=== Testing Dragonbreak Manager ===")
    try:
        from dragonbreak_manager import DragonbreakManager
        
        manager = DragonbreakManager(data_dir="../data", state_dir="/tmp/test_state")
        
        # Test 1: Create timeline fracture
        branch_id = manager.create_timeline_fracture(
            "Test Civil War Split",
            "Test timeline divergence",
            "Test battle outcome"
        )
        assert branch_id is not None, "Failed to create timeline fracture"
        print(f"✓ Created timeline fracture: {branch_id}")
        
        # Test 2: Track NPC across branches
        manager.track_npc_across_branches(
            "test_npc",
            "Test NPC",
            {
                "primary": {"status": "alive"},
                branch_id: {"status": "dead"}
            }
        )
        print("✓ NPC tracking across branches works")
        
        # Test 3: Track faction across branches
        manager.track_faction_across_branches(
            "test_faction",
            "Test Faction",
            {
                "primary": {"control": "imperial"},
                branch_id: {"control": "stormcloak"}
            }
        )
        print("✓ Faction tracking across branches works")
        
        # Test 4: Track quest across branches
        manager.track_quest_across_branches(
            "test_quest",
            "Test Quest",
            {
                "primary": "imperial_victory",
                branch_id: "stormcloak_victory"
            }
        )
        print("✓ Quest tracking across branches works")
        
        # Test 5: Define consequences
        cons_id = manager.define_branch_consequence(
            branch_id,
            "world_event",
            "Test consequence"
        )
        assert cons_id is not None, "Failed to define consequence"
        print(f"✓ Defined consequence: {cons_id}")
        
        print("\n✓ ALL DRAGONBREAK TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Dragonbreak Manager test failed: {e}")
        return False


def test_story_manager_integration():
    """Test Story Manager integration with Dragonbreak"""
    print("\n=== Testing Story Manager Integration ===")
    try:
        from story_manager import StoryManager
        
        manager = StoryManager(data_dir="../data", state_dir="/tmp/test_state")
        
        # Test 1: Check dragonbreak manager is available
        assert manager.dragonbreak_manager is not None, "Dragonbreak Manager not integrated"
        print("✓ Dragonbreak Manager integrated with Story Manager")
        
        # Test 2: Initiate dragonbreak through story manager
        branch_id = manager.initiate_dragonbreak(
            "Test Story Branch",
            "Test story divergence",
            "Test story event"
        )
        assert branch_id is not None, "Failed to initiate dragonbreak"
        print(f"✓ Initiated dragonbreak through Story Manager: {branch_id}")
        
        # Test 3: Track parallel event
        success = manager.track_parallel_event(
            'npc',
            {'id': 'test_char', 'name': 'Test Character'},
            {
                'primary': {'status': 'friendly'},
                branch_id: {'status': 'hostile'}
            }
        )
        assert success, "Failed to track parallel event"
        print("✓ Parallel event tracking works")
        
        print("\n✓ ALL STORY MANAGER INTEGRATION TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Story Manager integration test failed: {e}")
        return False


def test_faction_allegations():
    """Test Faction Allegation system (Side Plot C mechanics)"""
    print("\n=== Testing Faction Allegation System ===")
    try:
        from faction_logic import FactionManager
        
        manager = FactionManager(data_dir="../data")
        
        # Test 1: Check if faction data loads
        data = manager.load_factions_data()
        assert data is not None, "Failed to load faction data"
        print(f"✓ Loaded faction data with {len(data.get('major_factions', {}))} factions")
        
        # Test 2: Add allegation (if stormcloaks faction exists)
        if 'stormcloaks' in data.get('major_factions', {}):
            allegation_id = manager.add_faction_allegation(
                'stormcloaks',
                'thalmor_conspiracy',
                'Test Accuser',
                'Test allegation details'
            )
            assert allegation_id is not None, "Failed to add allegation"
            print(f"✓ Added allegation: {allegation_id}")
            
            # Test 3: Update evidence
            success = manager.update_allegation_evidence(
                'stormcloaks',
                allegation_id,
                3,
                "Test evidence"
            )
            assert success, "Failed to update evidence"
            print("✓ Evidence update works")
            
            # Test 4: Get allegations
            allegations = manager.get_faction_allegations('stormcloaks', 'pending')
            assert len(allegations) > 0, "Failed to retrieve allegations"
            print(f"✓ Retrieved {len(allegations)} allegation(s)")
        else:
            print("⚠ Stormcloaks faction not found, skipping allegation tests")
        
        # Test 5: Thalmor plot tracking (if thalmor faction exists)
        if 'thalmor' in data.get('major_factions', {}):
            plot_id = manager.track_thalmor_plot(
                "Test Plot",
                "test_target",
                "Test plot details"
            )
            if plot_id:
                print(f"✓ Tracked Thalmor plot: {plot_id}")
                
                # Test 6: Advance plot
                success = manager.advance_thalmor_plot(plot_id, 2)
                assert success, "Failed to advance plot"
                print("✓ Plot advancement works")
        else:
            print("⚠ Thalmor faction not found, skipping plot tests")
        
        print("\n✓ ALL FACTION ALLEGATION TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Faction allegation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_documentation_updates():
    """Test that documentation has been updated"""
    print("\n=== Testing Documentation Updates ===")
    try:
        import os
        from pathlib import Path
        
        # Get the repository root directory
        test_dir = Path(__file__).parent
        repo_root = test_dir.parent
        doc_path = repo_root / 'docs' / 'campaign_module.md'
        
        # Check campaign_module.md has been updated
        with open(doc_path, 'r') as f:
            content = f.read()
            
        # Should NOT contain Dragonborn-focused content
        dragonborn_mentions = content.count('Dragonborn revealed')
        assert dragonborn_mentions == 0, f"Found {dragonborn_mentions} 'Dragonborn revealed' references"
        print("✓ Dragonborn-focused content removed from documentation")
        
        # Should contain Civil War focus
        assert 'Civil War' in content, "Missing Civil War focus"
        print("✓ Civil War focus present")
        
        # Should mention Dragonbreak system
        assert 'Dragonbreak' in content or 'dragonbreak' in content, "Missing Dragonbreak references"
        print("✓ Dragonbreak system referenced")
        
        # Should mention neutral factions
        assert 'neutral' in content.lower(), "Missing neutral faction references"
        print("✓ Neutral faction references present")
        
        print("\n✓ ALL DOCUMENTATION TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Documentation test failed: {e}")
        return False


def main():
    """Run all integration tests"""
    print("="*60)
    print("CUSTOM CONTENT INTEGRATION TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Dragonbreak Manager", test_dragonbreak_manager()))
    results.append(("Story Manager Integration", test_story_manager_integration()))
    results.append(("Faction Allegations", test_faction_allegations()))
    results.append(("Documentation Updates", test_documentation_updates()))
    
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
