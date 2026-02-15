#!/usr/bin/env python3
"""
Story Progression Script for Skyrim TTRPG

This script automates story progression by:
- Updating faction clocks
- Advancing time and world state
- Generating story events based on current state
- Managing quest progression
"""

import json
import os
from datetime import datetime
from pathlib import Path


class StoryProgressionManager:
    def __init__(self, data_dir="data"):
        """
        Initialize the StoryProgressionManager.
        
        Args:
            data_dir: Path to the data directory (default: "data")
        """
        self.data_dir = Path(data_dir)
        self.world_state_path = self.data_dir / "world_state" / "current_state.json"
        self.factions_dir = self.data_dir / "factions"
        self.quests_dir = self.data_dir / "quests"
        
        # Ensure directories exist
        (self.data_dir / "world_state").mkdir(parents=True, exist_ok=True)
        self.factions_dir.mkdir(parents=True, exist_ok=True)
        self.quests_dir.mkdir(parents=True, exist_ok=True)
        
    def load_world_state(self):
        """
        Load the current world state.
        
        Returns:
            dict: World state data if successful, None otherwise
        """
        if self.world_state_path.exists():
            try:
                with open(self.world_state_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading world state: {e}")
                return None
        return None
    
    def save_world_state(self, state):
        """
        Save the world state.
        
        Args:
            state: World state dictionary to save
            
        Returns:
            bool: True if save successful, False otherwise
        """
        if not isinstance(state, dict):
            print("Error: state must be a dictionary")
            return False
            
        try:
            with open(self.world_state_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
            return True
        except (IOError, OSError) as e:
            print(f"Error saving world state: {e}")
            return False
    
    def advance_time(self, days=1):
        """
        Advance the in-game time by specified days.
        
        Args:
            days: Number of days to advance (default: 1, must be positive)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not isinstance(days, (int, float)) or days <= 0:
            print(f"Error: days must be a positive number, got {days}")
            return False
            
        state = self.load_world_state()
        if state:
            # Use safe dictionary access with default value
            current_days = state.get('in_game_days_passed', 0)
            state['in_game_days_passed'] = current_days + days
            print(f"Advanced time by {days} day(s). Total days: {state['in_game_days_passed']}")
            return self.save_world_state(state)
        return False
    
    def update_faction_clock(self, faction_id, progress_change):
        """
        Update a faction's clock progress.
        
        Args:
            faction_id: The faction identifier
            progress_change: Amount to change clock progress (can be negative)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not faction_id or not isinstance(faction_id, str):
            print("Error: faction_id must be a non-empty string")
            return False
        if not isinstance(progress_change, (int, float)):
            print("Error: progress_change must be a number")
            return False
            
        faction_path = self.factions_dir / f"{faction_id}.json"
        if faction_path.exists():
            try:
                with open(faction_path, 'r', encoding='utf-8') as f:
                    faction = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading faction file: {e}")
                return False
            
            if 'clock' in faction and isinstance(faction['clock'], dict):
                old_progress = faction['clock'].get('progress', 0)
                segments = faction['clock'].get('segments', 8)
                
                # Clamp progress between 0 and segments
                faction['clock']['progress'] = min(
                    segments,
                    max(0, old_progress + progress_change)
                )
                
                try:
                    with open(faction_path, 'w', encoding='utf-8') as f:
                        json.dump(faction, f, indent=2)
                except (IOError, OSError) as e:
                    print(f"Error writing faction file: {e}")
                    return False
                
                faction_name = faction.get('name', faction_id)
                print(f"Updated {faction_name} clock: {old_progress} -> {faction['clock']['progress']}/{segments}")
                
                if faction['clock']['progress'] >= segments:
                    clock_name = faction['clock'].get('name', 'goal')
                    print(f"WARNING: {faction_name} has completed their clock: {clock_name}")
                
                return True
            else:
                print(f"Faction {faction_id} does not have a valid clock")
        else:
            print(f"Faction {faction_id} not found")
        return False
    
    def generate_story_events(self):
        """
        Generate story events based on world state.
        
        Returns:
            list: List of story event dictionaries
        """
        state = self.load_world_state()
        if not state:
            return []
        
        events = []
        
        # Check post-dragon status (post-Alduin timeline)
        post_dragon = state.get('post_dragon_crisis', {})
        dragon_status = post_dragon.get('status', '')
        
        # Generate events based on current timeline
        # Note: In post-Alduin timeline, dragon crisis is resolved
        # Focus on civil war and Thalmor plots instead
        
        # Check faction standings - safe access
        faction_standings = state.get('faction_standings', {})
        if isinstance(faction_standings, dict):
            for faction_name, data in faction_standings.items():
                if isinstance(data, dict):
                    morale = data.get('morale', 50)
                    if morale < 40:
                        events.append({
                            'type': 'low_morale',
                            'faction': faction_name,
                            'description': f'{faction_name} morale is critically low',
                            'impact': 'Potential desertions or surrenders'
                        })
        
        # Civil war progression - safe access
        political_situation = state.get('political_situation', {})
        if isinstance(political_situation, dict):
            skyrim_status = political_situation.get('skyrim_status', '')
            if skyrim_status == 'Civil War in progress':
                events.append({
                    'type': 'civil_war',
                    'description': 'Skirmishes continue along faction borders',
                    'impact': 'Trade routes disrupted, civilian casualties'
                })
        
        return events
    
    def progress_quests(self, session_data):
        """
        Update quest states based on session data.
        
        Args:
            session_data: Dictionary containing session information with quest updates
        """
        if not isinstance(session_data, dict):
            print("Error: session_data must be a dictionary")
            return
            
        if 'quests_updated' not in session_data:
            return
        
        quests_updated = session_data.get('quests_updated', [])
        if not isinstance(quests_updated, list):
            return
            
        for quest_update in quests_updated:
            if not isinstance(quest_update, dict):
                continue
                
            quest_name = quest_update.get('quest')
            quest_status = quest_update.get('status')
            
            if not quest_name or not quest_status:
                continue
            
            quest_files = list(self.quests_dir.glob("*.json"))
            for quest_file in quest_files:
                try:
                    with open(quest_file, 'r', encoding='utf-8') as f:
                        quest = json.load(f)
                except (IOError, json.JSONDecodeError) as e:
                    print(f"Error reading quest file {quest_file}: {e}")
                    continue
                
                if quest.get('name') == quest_name:
                    quest['status'] = quest_status
                    try:
                        with open(quest_file, 'w', encoding='utf-8') as f:
                            json.dump(quest, f, indent=2)
                        print(f"Updated quest '{quest['name']}' status to: {quest['status']}")
                    except (IOError, OSError) as e:
                        print(f"Error writing quest file {quest_file}: {e}")
    
    def add_major_event(self, event_description):
        """
        Add a major event to the world state.
        
        Args:
            event_description: Description of the major event
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not event_description or not isinstance(event_description, str):
            print("Error: event_description must be a non-empty string")
            return False
            
        state = self.load_world_state()
        if state:
            # Ensure major_events list exists
            if 'major_events' not in state or not isinstance(state['major_events'], list):
                state['major_events'] = []
            
            state['major_events'].append(event_description)
            if self.save_world_state(state):
                print(f"Added major event: {event_description}")
                return True
        return False
    
    def generate_rumors(self):
        """
        Generate new rumors based on current world state.
        
        Returns:
            list: List of rumor strings
        """
        state = self.load_world_state()
        if not state:
            return []
        
        rumors = []
        
        # Post-Alduin timeline - dragons are largely inactive
        # Generate civil war and Thalmor-focused rumors instead
        
        # Civil war rumors - safe access
        political_situation = state.get('political_situation', {})
        if isinstance(political_situation, dict):
            skyrim_status = political_situation.get('skyrim_status', '')
            if skyrim_status == 'Civil War in progress':
                rumors.append("The Stormcloaks are gaining ground in the east.")
                rumors.append("General Tullius is planning a major offensive.")
        
        # Faction-based rumors
        faction_files = list(self.factions_dir.glob("*.json"))
        for faction_file in faction_files:
            try:
                with open(faction_file, 'r', encoding='utf-8') as f:
                    faction = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading faction file {faction_file}: {e}")
                continue
                
            if 'clock' in faction and isinstance(faction['clock'], dict):
                progress = faction['clock'].get('progress', 0)
                segments = faction['clock'].get('segments', 8)
                if progress > segments * 0.5:
                    faction_name = faction.get('name', 'Unknown')
                    rumors.append(f"The {faction_name} are up to something...")
        
        return rumors


def main():
    """Main function to demonstrate story progression capabilities"""
    print("=== Skyrim TTRPG Story Progression Manager ===\n")
    
    manager = StoryProgressionManager()
    
    # Example: Advance time
    print("1. Advancing time...")
    manager.advance_time(1)
    print()
    
    # Example: Update faction clock
    print("2. Updating faction clock...")
    manager.update_faction_clock('whiterun_guard', 1)
    print()
    
    # Example: Generate story events
    print("3. Generating story events...")
    events = manager.generate_story_events()
    for event in events:
        print(f"- [{event['type']}] {event['description']}")
        print(f"  Impact: {event['impact']}")
    print()
    
    # Example: Generate rumors
    print("4. Generating rumors...")
    rumors = manager.generate_rumors()
    for rumor in rumors:
        print(f"- {rumor}")
    print()
    
    print("Story progression complete!")


if __name__ == "__main__":
    main()
