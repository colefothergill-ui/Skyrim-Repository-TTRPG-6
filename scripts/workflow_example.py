#!/usr/bin/env python3
"""
Example Workflow Script for Skyrim TTRPG

This script demonstrates a complete workflow:
1. Query data
2. Create a new session
3. Progress the story
4. Export for ChatGPT
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from query_data import DataQueryManager
from session_manager import SessionContextManager
from story_progression import StoryProgressionManager
from export_repo import RepositoryExporter


def main():
    print("=" * 70)
    print("SKYRIM TTRPG - COMPLETE WORKFLOW EXAMPLE")
    print("=" * 70)
    print()
    
    # Initialize managers
    query_manager = DataQueryManager("../data")
    session_manager = SessionContextManager("../data")
    story_manager = StoryProgressionManager("../data")
    exporter = RepositoryExporter("..")
    
    # Step 1: Query current campaign state
    print("STEP 1: Querying Campaign State")
    print("-" * 70)
    
    world_state = query_manager.get_world_state()
    if world_state:
        print(f"Campaign Date: {world_state.get('game_date', 'Unknown')}")
        print(f"Days Passed: {world_state.get('in_game_days_passed', 0)}")
        
        # Post-Alduin timeline - show dragon status
        post_dragon = world_state.get('post_dragon_crisis', {})
        dragon_status = post_dragon.get('status', 'Unknown')
        print(f"Dragon Status: {dragon_status}")
    else:
        print("No world state found. Run story_progression.py first.")
    print()
    
    active_quests = query_manager.query_quests(status="Active")
    print(f"Active Quests: {len(active_quests)}")
    for quest in active_quests:
        print(f"  - {quest['name']} ({quest['type']})")
    print()
    
    # Step 2: Review previous session
    print("STEP 2: Reviewing Previous Session")
    print("-" * 70)
    
    latest_session = session_manager.get_latest_session()
    if latest_session:
        print(f"Last Session: #{latest_session['session_number']} - {latest_session['title']}")
        print(f"Date: {latest_session['date']}")
        print(f"Key Events:")
        for event in latest_session['key_events'][:3]:
            print(f"  - {event}")
    print()
    
    # Step 3: Generate story events
    print("STEP 3: Generating Story Events")
    print("-" * 70)
    
    events = story_manager.generate_story_events()
    print(f"Generated {len(events)} potential events:")
    for event in events[:3]:
        print(f"  [{event['type']}] {event['description']}")
    print()
    
    # Step 4: Generate rumors
    print("STEP 4: Generating Rumors")
    print("-" * 70)
    
    rumors = story_manager.generate_rumors()
    print("Current rumors in Skyrim:")
    for rumor in rumors[:4]:
        print(f"  - \"{rumor}\"")
    print()
    
    # Step 5: Quick reference for GM
    print("STEP 5: Quick Reference")
    print("-" * 70)
    
    quick_ref = exporter.create_quick_reference()
    print(quick_ref[:400] + "...\n")
    
    # Step 6: Campaign statistics
    print("STEP 6: Campaign Statistics")
    print("-" * 70)
    
    stats = exporter.collect_statistics()
    print("Current Campaign Size:")
    for key, value in stats.items():
        print(f"  {key.upper()}: {value}")
    print()
    
    # Summary
    print("=" * 70)
    print("WORKFLOW COMPLETE")
    print("=" * 70)
    print()
    print("Ready for next session! Use these commands:")
    print("  - python3 query_data.py          # Search data")
    print("  - python3 session_manager.py     # Manage sessions")
    print("  - python3 story_progression.py   # Progress story")
    print("  - python3 export_repo.py         # Export for ChatGPT")
    print()
    print("Upload skyrim_ttrpg_export.zip to ChatGPT 5.2 for AI assistance!")
    print()


if __name__ == "__main__":
    main()
