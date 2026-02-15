#!/usr/bin/env python3
"""
Test the canon divergence checking functionality
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_canon_divergence_detection():
    """Test that canon divergence detection works correctly"""
    print("\n=== Testing Canon Divergence Detection ===")
    try:
        from gm_tools import GMTools
        
        tools = GMTools()
        
        # Test 1: Canon divergence - Ulfric killed
        print("\n--- Test 1: Ulfric Stormcloak assassination ---")
        result = tools.check_major_canon_divergence("Ulfric Stormcloak is assassinated in Windhelm")
        assert result == True, "Expected canon divergence detection for Ulfric assassination"
        
        # Test 2: Canon divergence - General Tullius killed
        print("\n--- Test 2: General Tullius death ---")
        result = tools.check_major_canon_divergence("General Tullius killed in battle")
        assert result == True, "Expected canon divergence detection for General Tullius death"
        
        # Test 3: Canon divergence - Jarl Elisif killed
        print("\n--- Test 3: Jarl Elisif assassination ---")
        result = tools.check_major_canon_divergence("Jarl Elisif is dead")
        assert result == True, "Expected canon divergence detection for Jarl Elisif death"
        
        # Test 4: Canon divergence - Whiterun destroyed
        print("\n--- Test 4: Whiterun destruction ---")
        result = tools.check_major_canon_divergence("Whiterun destroyed by dragon attack")
        assert result == True, "Expected canon divergence detection for Whiterun destruction"
        
        # Test 5: Canon divergence - Solitude destroyed
        print("\n--- Test 5: Solitude destruction ---")
        result = tools.check_major_canon_divergence("Solitude destroyed in the civil war")
        assert result == True, "Expected canon divergence detection for Solitude destruction"
        
        # Test 6: No canon divergence - normal event
        print("\n--- Test 6: Normal event (no divergence) ---")
        result = tools.check_major_canon_divergence("The party cleared a bandit camp")
        assert result == False, "Expected no canon divergence for normal event"
        
        # Test 7: No canon divergence - character mentioned but not killed
        print("\n--- Test 7: Character mentioned but alive ---")
        result = tools.check_major_canon_divergence("Ulfric Stormcloak gave a speech in Windhelm")
        assert result == False, "Expected no canon divergence when character is mentioned but alive"
        
        # Test 8: No canon divergence - unrelated death
        print("\n--- Test 8: Unrelated death event ---")
        result = tools.check_major_canon_divergence("A bandit was killed in the wilderness")
        assert result == False, "Expected no canon divergence for unrelated death"
        
        # Test 9: No false positive - city mentioned but not destroyed
        print("\n--- Test 9: City mentioned but not destroyed ---")
        result = tools.check_major_canon_divergence("The party defeated bandits near Whiterun")
        assert result == False, "Expected no false positive when city is mentioned but not destroyed"
        
        # Test 10: Canon divergence - Whiterun burned down
        print("\n--- Test 10: Whiterun burned down ---")
        result = tools.check_major_canon_divergence("Whiterun burned down in the battle")
        assert result == True, "Expected canon divergence detection for Whiterun being burned down"
        
        print("\n✓ All canon divergence tests completed successfully")
        return True
        
    except AssertionError as e:
        print(f"\n✗ Canon divergence test assertion failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Canon divergence test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_canon_divergence_detection()
    sys.exit(0 if success else 1)
