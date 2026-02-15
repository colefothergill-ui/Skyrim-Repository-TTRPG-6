#!/usr/bin/env python3
"""
Test companion loyalty monitoring functionality
"""

import sys
import os
import json
from pathlib import Path
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def test_companion_loyalty_review():
    """Test the review_companion_loyalty method"""
    print("\n=== Testing Companion Loyalty Review ===")
    
    try:
        from gm_tools import GMTools
        
        # Get absolute path to data directory
        test_dir = Path(__file__).parent
        repo_root = test_dir.parent
        data_dir = repo_root / "data"
        
        # Create test state directory
        test_state_dir = Path('/tmp/test_companion_state')
        test_state_dir.mkdir(exist_ok=True)
        
        # Create test campaign state with various loyalty levels
        campaign_state = {
            'campaign_id': 'test_001',
            'companions': {
                'active_companions': [
                    {
                        'name': 'Hadvar',
                        'npc_id': 'npc_stat_hadvar',
                        'loyalty': 75
                    },
                    {
                        'name': 'Ralof',
                        'npc_id': 'npc_stat_ralof',
                        'loyalty': 85
                    }
                ]
            }
        }
        
        # Save test campaign state
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        
        # Test with companions in party
        print("\nTest 1: Companions with various loyalty levels")
        tools = GMTools(data_dir=str(data_dir), state_dir=str(test_state_dir))
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        tools.review_companion_loyalty()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        
        # Assert expected content appears
        assert "Hadvar – Loyalty 75/100" in output, "Should display Hadvar's loyalty"
        assert "Reliable companion, shares Imperial intelligence" in output, "Should display 60-79 threshold status for Hadvar"
        assert "Ralof – Loyalty 85/100" in output, "Should display Ralof's loyalty"
        assert "Will die for party" in output, "Should display 80+ threshold status for Ralof"
        assert "🤝 High loyalty!" in output, "Should show high loyalty warning for Ralof"
        assert "Quest Unlocked" in output, "Should show unlocked quests"
        assert "Protecting Riverwood" in output, "Should show specific quest name"
        
        print("✓ Successfully reviewed companion loyalty with correct status and quests")
        
        # Test with no active companions
        print("\nTest 2: No active companions")
        campaign_state['companions']['active_companions'] = []
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        tools.review_companion_loyalty()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "No active companions in party" in output, "Should show no companions message"
        
        print("✓ Handled empty companion list correctly")
        
        # Test with low loyalty companion
        print("\nTest 3: Companion with critically low loyalty")
        campaign_state['companions']['active_companions'] = [
            {
                'name': 'Hadvar',
                'npc_id': 'npc_stat_hadvar',
                'loyalty': 15
            }
        ]
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        tools.review_companion_loyalty()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "Hadvar – Loyalty 15/100" in output, "Should display low loyalty value"
        assert "Leaves party" in output or "0-19" in output, "Should display 0-19 threshold status"
        assert "⚠️  Low loyalty!" in output, "Should show low loyalty warning"
        
        print("✓ Correctly warned about low loyalty")
        
        # Test with high loyalty companion
        print("\nTest 4: Companion with very high loyalty")
        campaign_state['companions']['active_companions'] = [
            {
                'name': 'Ralof',
                'npc_id': 'npc_stat_ralof',
                'loyalty': 95
            }
        ]
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        tools.review_companion_loyalty()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "Ralof – Loyalty 95/100" in output, "Should display high loyalty value"
        assert "Will die for party" in output, "Should display 80+ threshold status"
        assert "🤝 High loyalty!" in output, "Should show high loyalty message"
        assert "Quest Unlocked" in output, "Should show unlocked quests"
        
        print("✓ Correctly identified high loyalty with quests")
        
        # Test with companion at quest unlock threshold
        print("\nTest 5: Companion at quest unlock threshold")
        campaign_state['companions']['active_companions'] = [
            {
                'name': 'Hadvar',
                'npc_id': 'npc_stat_hadvar',
                'loyalty': 70
            }
        ]
        with open(test_state_dir / 'campaign_state.json', 'w') as f:
            json.dump(campaign_state, f, indent=2)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        tools.review_companion_loyalty()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "Hadvar – Loyalty 70/100" in output, "Should display loyalty at threshold"
        assert "Reliable companion" in output, "Should display 60-79 threshold status"
        assert "Quest Unlocked" in output, "Should show unlocked quest"
        assert "Protecting Riverwood" in output, "Should show quest that requires loyalty 70"
        
        print("✓ Correctly identified unlocked quests at threshold")
        
        print("\n=== All Companion Loyalty Tests Passed! ===")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_companion_loyalty_review()
    sys.exit(0 if success else 1)
