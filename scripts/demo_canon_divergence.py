#!/usr/bin/env python3
"""
Demonstration of the check_major_canon_divergence method

This script shows how the GM can use the canon divergence checker
during gameplay to ensure major lore-breaking events are handled
appropriately via the Dragonbreak protocol.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from gm_tools import GMTools

def main():
    """Demonstrate canon divergence checking"""
    tools = GMTools()
    
    print("="*70)
    print("CANON DIVERGENCE CHECKER DEMONSTRATION")
    print("="*70)
    print("\nThis tool helps GMs detect when player actions contradict")
    print("immutable Elder Scrolls canon, triggering the Dragonbreak protocol.")
    print()
    
    # Example scenarios
    scenarios = [
        {
            "name": "Scenario 1: Normal Quest Completion",
            "description": "The party completed a quest to clear bandits from Bleak Falls Barrow",
            "expected": "No divergence - normal gameplay"
        },
        {
            "name": "Scenario 2: Essential Character Death",
            "description": "Ulfric Stormcloak was assassinated during a diplomatic meeting",
            "expected": "DIVERGENCE DETECTED - Dragonbreak needed"
        },
        {
            "name": "Scenario 3: City Visit",
            "description": "The party arrived in Solitude and met with the Jarl",
            "expected": "No divergence - normal gameplay"
        },
        {
            "name": "Scenario 4: Major City Destruction",
            "description": "Whiterun was destroyed in a devastating dragon attack",
            "expected": "DIVERGENCE DETECTED - Dragonbreak needed"
        },
        {
            "name": "Scenario 5: Political Change",
            "description": "General Tullius was killed in the Battle of Solitude",
            "expected": "DIVERGENCE DETECTED - Dragonbreak needed"
        }
    ]
    
    for scenario in scenarios:
        print("\n" + "-"*70)
        print(f"{scenario['name']}")
        print(f"Event: {scenario['description']}")
        print(f"Expected: {scenario['expected']}")
        print("-"*70)
        
        result = tools.check_major_canon_divergence(scenario['description'])
        
        if result:
            print("\n➜ GM Action: Invoke Dragonbreak protocol")
            print("  1. Log event in dragonbreak_log.md")
            print("  2. Create timeline branch in world_state.json")
            print("  3. NPCs may have conflicting memories")
        else:
            print("\n➜ GM Action: Continue normal gameplay")
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nThe canon divergence checker helps maintain Elder Scrolls lore")
    print("while accommodating player agency through the Dragonbreak system.")

if __name__ == "__main__":
    main()
