#!/usr/bin/env python3
"""
Query Script for Skyrim TTRPG

This script provides querying capabilities for:
- NPCs (search by name, location, faction)
- Rules (search by keyword)
- Quests (search by status, type, location)
- World state information
- PDF topics (search converted PDF content by topic)
"""

import json
import os
from pathlib import Path
from utils import location_matches


class DataQueryManager:
    def __init__(self, data_dir="data"):
        """
        Initialize the DataQueryManager.
        
        Args:
            data_dir: Path to the data directory (default: "data")
        """
        self.data_dir = Path(data_dir)
        self.npc_stat_sheets_dir = self.data_dir / "npc_stat_sheets"
        
        # Ensure directories exist
        (self.data_dir / "npcs").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "pcs").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "quests").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "factions").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "sessions").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "world_state").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "rules").mkdir(parents=True, exist_ok=True)
        
    def query_npcs(self, name=None, location=None, faction=None):
        """
        Query NPCs based on filters.
        
        Args:
            name: Filter by name (partial match, case-insensitive)
            location: Filter by location (exact match, case-insensitive)
            faction: Filter by faction (exact match, case-insensitive)
            
        Returns:
            list: List of matching NPC dictionaries
        """
        npcs_dir = self.data_dir / "npcs"
        if not npcs_dir.exists():
            return []
            
        results = []
        
        for npc_file in npcs_dir.glob("*.json"):
            try:
                with open(npc_file, 'r', encoding='utf-8') as f:
                    npc = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Warning: Error reading {npc_file.name}: {e}")
                continue
            
            match = True
            if name and isinstance(name, str):
                npc_name = npc.get('name', '')
                if isinstance(npc_name, str) and name.lower() not in npc_name.lower():
                    match = False
            if location and isinstance(location, str):
                npc_location = npc.get('location', '')
                if isinstance(npc_location, str) and location.lower() != npc_location.lower():
                    match = False
            if faction and isinstance(faction, str):
                npc_faction = npc.get('faction', '')
                if isinstance(npc_faction, str) and faction.lower() != npc_faction.lower():
                    match = False
            
            if match:
                results.append(npc)
        
        return results
    
    def query_pcs(self, name=None, player=None):
        """
        Query Player Characters.
        
        Args:
            name: Filter by character name (partial match, case-insensitive)
            player: Filter by player name (partial match, case-insensitive)
            
        Returns:
            list: List of matching PC dictionaries
        """
        pcs_dir = self.data_dir / "pcs"
        if not pcs_dir.exists():
            return []
            
        results = []
        
        for pc_file in pcs_dir.glob("*.json"):
            try:
                with open(pc_file, 'r', encoding='utf-8') as f:
                    pc = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Warning: Error reading {pc_file.name}: {e}")
                continue
            
            match = True
            if name and isinstance(name, str):
                pc_name = pc.get('name', '')
                if isinstance(pc_name, str) and name.lower() not in pc_name.lower():
                    match = False
            if player and isinstance(player, str):
                pc_player = pc.get('player', '')
                if isinstance(pc_player, str) and player.lower() not in pc_player.lower():
                    match = False
            
            if match:
                results.append(pc)
        
        return results
    
    def query_quests(self, status=None, quest_type=None, name=None):
        """
        Query quests based on filters.
        
        Args:
            status: Filter by status (exact match, case-insensitive)
            quest_type: Filter by quest type (exact match, case-insensitive)
            name: Filter by name (partial match, case-insensitive)
            
        Returns:
            list: List of matching quest dictionaries
        """
        quests_dir = self.data_dir / "quests"
        if not quests_dir.exists():
            return []
            
        results = []
        
        for quest_file in quests_dir.glob("*.json"):
            try:
                with open(quest_file, 'r', encoding='utf-8') as f:
                    quest = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Warning: Error reading {quest_file.name}: {e}")
                continue
            
            match = True
            if status and isinstance(status, str):
                quest_status = quest.get('status', '')
                if isinstance(quest_status, str) and quest_status.lower() != status.lower():
                    match = False
            if quest_type and isinstance(quest_type, str):
                quest_quest_type = quest.get('type', '')
                if isinstance(quest_quest_type, str) and quest_quest_type.lower() != quest_type.lower():
                    match = False
            if name and isinstance(name, str):
                quest_name = quest.get('name', '')
                if isinstance(quest_name, str) and name.lower() not in quest_name.lower():
                    match = False
            
            if match:
                results.append(quest)
        
        return results
    
    def query_factions(self, name=None, faction_type=None):
        """
        Query factions.
        
        Args:
            name: Filter by faction name (partial match, case-insensitive)
            faction_type: Filter by faction type (exact match, case-insensitive)
            
        Returns:
            list: List of matching faction dictionaries
        """
        factions_dir = self.data_dir / "factions"
        if not factions_dir.exists():
            return []
            
        results = []
        
        for faction_file in factions_dir.glob("*.json"):
            try:
                with open(faction_file, 'r', encoding='utf-8') as f:
                    faction = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Warning: Error reading {faction_file.name}: {e}")
                continue
            
            match = True
            if name and isinstance(name, str):
                faction_name = faction.get('name', '')
                if isinstance(faction_name, str) and name.lower() not in faction_name.lower():
                    match = False
            if faction_type and isinstance(faction_type, str):
                faction_faction_type = faction.get('type', '')
                if isinstance(faction_faction_type, str) and faction_type.lower() != faction_faction_type.lower():
                    match = False
            
            if match:
                results.append(faction)
        
        return results
    
    def query_faction_quests(self, faction_id=None, quest_id=None, act=None):
        """
        Query faction quests from factions.json.
        
        Args:
            faction_id: Filter by faction (e.g., 'companions', 'thieves_guild')
            quest_id: Filter by specific quest ID
            act: Filter by act context (e.g., 'Act 1', 'Act 2')
        
        Returns:
            dict: Faction quest information, or error dict if file not found
        """
        factions_file = self.data_dir / "factions.json"
        
        if not factions_file.exists():
            return {"error": "Factions file not found"}
        
        try:
            with open(factions_file, 'r', encoding='utf-8') as f:
                factions_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            return {"error": f"Error reading factions file: {e}"}
        
        faction_quests = factions_data.get('faction_quests', {})
        results = {}
        
        for faction, quest_data in faction_quests.items():
            # Filter by faction_id if provided
            if faction_id and faction != faction_id:
                continue
            
            if not isinstance(quest_data, dict):
                continue
                
            filtered_quests = []
            for quest in quest_data.get('quests', []):
                if not isinstance(quest, dict):
                    continue
                    
                # Filter by quest_id if provided
                if quest_id and quest.get('id') != quest_id:
                    continue
                
                # Filter by act if provided
                if act and act not in quest.get('act_context', []):
                    continue
                
                filtered_quests.append(quest)
            
            if filtered_quests or not quest_id:
                results[faction] = {
                    'questline': quest_data.get('questline'),
                    'quests': filtered_quests,
                    'side_quests': quest_data.get('side_quests', [])
                }
        
        return results
    
    def get_trust_mechanics(self):
        """
        Get trust mechanics from factions.json.
        
        Returns:
            dict: Trust mechanics data, or error dict if file not found
        """
        factions_file = self.data_dir / "factions.json"
        
        if not factions_file.exists():
            return {"error": "Factions file not found"}
        
        try:
            with open(factions_file, 'r', encoding='utf-8') as f:
                factions_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            return {"error": f"Error reading factions file: {e}"}
        
        return factions_data.get('trust_mechanics', {})
    
    def get_main_story_integration(self):
        """
        Get main story integration info from factions.json.
        
        Returns:
            dict: Main story integration data, or error dict if file not found
        """
        factions_file = self.data_dir / "factions.json"
        
        if not factions_file.exists():
            return {"error": "Factions file not found"}
        
        try:
            with open(factions_file, 'r', encoding='utf-8') as f:
                factions_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            return {"error": f"Error reading factions file: {e}"}
        
        return factions_data.get('main_story_integration', {})
    
    def get_world_state(self):
        """
        Get the current world state.
        
        Returns:
            dict: World state data if successful, None otherwise
        """
        world_state_file = self.data_dir / "world_state" / "current_state.json"
        if world_state_file.exists():
            try:
                with open(world_state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading world state: {e}")
                return None
        return None
    
    def search_rules(self, keyword):
        """
        Search rules documentation for keyword.
        
        Args:
            keyword: Search term to look for in rules files
            
        Returns:
            list: List of dicts containing file name and matching lines
        """
        if not keyword or not isinstance(keyword, str):
            print("Error: keyword must be a non-empty string")
            return []
            
        rules_dir = self.data_dir / "rules"
        if not rules_dir.exists():
            return []
            
        results = []
        
        for rules_file in rules_dir.glob("*.md"):
            try:
                with open(rules_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except (IOError, UnicodeDecodeError) as e:
                print(f"Warning: Error reading {rules_file.name}: {e}")
                continue
            
            if keyword.lower() in content.lower():
                # Find relevant sections
                lines = content.split('\n')
                relevant_lines = []
                for line_index, line in enumerate(lines):
                    if keyword.lower() in line.lower():
                        # Get context (2 lines before and after)
                        context_start = max(0, line_index - 2)
                        context_end = min(len(lines), line_index + 3)
                        relevant_lines.extend(lines[context_start:context_end])
                
                results.append({
                    'file': rules_file.name,
                    'matches': relevant_lines
                })
        
        return results
    
    def get_session_log(self, session_number=None):
        """
        Get session log(s).
        
        Args:
            session_number: Specific session number to retrieve, or None for all sessions
            
        Returns:
            list: List of session data dictionaries
        """
        sessions_dir = self.data_dir / "sessions"
        if not sessions_dir.exists():
            return []
            
        results = []
        
        if session_number:
            if not isinstance(session_number, int) or session_number <= 0:
                print("Error: session_number must be a positive integer")
                return []
                
            session_file = sessions_dir / f"session_{session_number:03d}.json"
            if session_file.exists():
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        return [json.load(f)]
                except (IOError, json.JSONDecodeError) as e:
                    print(f"Error reading session file: {e}")
                    return []
        else:
            # Return all sessions
            for session_file in sorted(sessions_dir.glob("session_*.json")):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        results.append(json.load(f))
                except (IOError, json.JSONDecodeError) as e:
                    print(f"Warning: Error reading {session_file.name}: {e}")
                    continue
        
        return results
    
    def get_character_relationships(self, character_id):
        """
        Get all relationships for a character (PC or NPC).
        
        Args:
            character_id: The character ID to look up
            
        Returns:
            dict: Relationships dictionary, or empty dict if not found
        """
        if not character_id or not isinstance(character_id, str):
            print("Error: character_id must be a non-empty string")
            return {}
            
        # Check NPCs
        npcs = self.query_npcs()
        pcs = self.query_pcs()
        
        target = None
        for npc in npcs:
            if npc.get('id') == character_id:
                target = npc
                break
        
        if not target:
            for pc in pcs:
                if pc.get('id') == character_id:
                    target = pc
                    break
        
        if target and 'relationships' in target:
            return target['relationships']
        
        return {}
    
    def query_pdf_topics(self, topic):
        """
        Query PDF index for topic and return relevant files.
        
        Args:
            topic: Topic to search for in PDF index
            
        Returns:
            dict: Query results with files and details, or error dict
        """
        if not topic or not isinstance(topic, str):
            return {"error": "Topic must be a non-empty string", "files": [], "details": []}
            
        pdf_index_file = self.data_dir / "pdf_index.json"
        
        if not pdf_index_file.exists():
            return {"error": "PDF index not found", "files": [], "details": []}
        
        try:
            with open(pdf_index_file, 'r', encoding='utf-8') as f:
                pdf_index = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            return {"error": f"Error reading PDF index: {e}", "files": [], "details": []}
        
        # Search query mappings
        query_mappings = pdf_index.get('query_mappings', {})
        topic_lower = topic.lower()
        
        # Find matching files
        matching_files = []
        if topic_lower in query_mappings:
            matching_files = query_mappings[topic_lower]
        
        # Search in topics structure for more detailed info
        results = []
        topics_data = pdf_index.get('topics', {})
        
        if isinstance(topics_data, dict):
            for category, items in topics_data.items():
                if isinstance(items, dict):
                    for item_name, item_data in items.items():
                        if isinstance(item_data, dict):
                            topics_list = item_data.get('topics', [])
                            if isinstance(topics_list, list):
                                if topic_lower in ' '.join(topics_list).lower():
                                    results.append({
                                        'file': item_data.get('file', 'Unknown'),
                                        'format': item_data.get('format', 'Unknown'),
                                        'description': item_data.get('description', ''),
                                        'source_pdf': item_data.get('source_pdf', 'Unknown')
                                    })
        
        return {
            'query': topic,
            'files': matching_files,
            'details': results
        }
    
    def get_pdf_content(self, topic):
        """
        Get actual content from PDF-converted files for a topic.
        
        Args:
            topic: Topic to retrieve content for
            
        Returns:
            dict: Dictionary with query and list of content results
        """
        query_result = self.query_pdf_topics(topic)
        content = []
        
        for detail in query_result.get('details', []):
            file_path = Path(detail.get('file', ''))
            
            # Skip if file path is invalid
            if not file_path or not isinstance(detail, dict):
                continue
            
            # Adjust path if relative
            if not file_path.is_absolute():
                file_path = self.data_dir.parent / file_path
            
            if file_path.exists():
                detail_format = detail.get('format', '')
                try:
                    if detail_format == 'json':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            content.append({
                                'file': str(file_path),
                                'type': 'json',
                                'content': data,
                                'description': detail.get('description', '')
                            })
                    elif detail_format == 'markdown':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text = f.read()
                            content.append({
                                'file': str(file_path),
                                'type': 'markdown',
                                'content': text,
                                'description': detail.get('description', '')
                            })
                except (IOError, json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"Warning: Error reading {file_path}: {e}")
                    continue
        
        return {
            'query': topic,
            'results': content
        }
    
    def query_npc_enemy_stats(self, name=None, entity_type=None, category=None, location=None):
        """
        Query NPC/enemy stat sheets based on filters
        
        Args:
            name: Search by name (partial match)
            entity_type: Filter by type (e.g., 'Ally', 'Enemy', 'Dragon', 'Undead')
            category: Filter by category ('Friendly NPC', 'Hostile NPC', 'Enemy')
            location: Filter by location (partial match, case-insensitive)
        
        Returns:
            List of matching stat sheets
        """
        if not self.npc_stat_sheets_dir.exists():
            return []
        
        results = []
        
        for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
            try:
                with open(stat_file, 'r') as f:
                    stat_sheet = json.load(f)
                
                match = True
                
                # Name filter (partial, case-insensitive)
                if name and name.lower() not in stat_sheet.get('name', '').lower():
                    match = False
                
                # Type filter (exact match, case-insensitive)
                if entity_type and entity_type.lower() != stat_sheet.get('type', '').lower():
                    match = False
                
                # Category filter (exact match, case-insensitive)
                if category and category.lower() != stat_sheet.get('category', '').lower():
                    match = False
                
                # Location filter (partial match in either direction, case-insensitive)
                if location:
                    sheet_location = stat_sheet.get('location', '')
                    if not location_matches(location, sheet_location):
                        match = False
                
                if match:
                    results.append(stat_sheet)
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Error reading {stat_file.name}: {e}")
                continue
        
        return results
    
    def get_npc_enemy_stat_by_id(self, stat_id):
        """Get a specific NPC/enemy stat sheet by ID"""
        if not self.npc_stat_sheets_dir.exists():
            return None
        
        for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
            try:
                with open(stat_file, 'r') as f:
                    stat_sheet = json.load(f)
                
                if stat_sheet.get('id') == stat_id:
                    return stat_sheet
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Error reading {stat_file.name}: {e}")
                continue
        
        return None
    
    def get_enemies_by_location(self, location):
        """Get all enemies that can appear in a specific location"""
        return self.query_npc_enemy_stats(location=location, category="Enemy")
    
    def get_enemies_by_hold(self, hold_name):
        """
        Get enemies that can appear in a specific hold, considering hold_context
        
        Args:
            hold_name: Name of the hold (e.g., 'Eastmarch', 'The Rift', 'Whiterun')
        
        Returns:
            Dict with primary, contested, and rare enemies for the hold
        """
        if not self.npc_stat_sheets_dir.exists():
            return {"primary": [], "contested": [], "rare": []}
        
        results = {
            "primary": [],
            "contested": [],
            "rare": []
        }
        
        for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
            try:
                with open(stat_file, 'r') as f:
                    stat_sheet = json.load(f)
                
                # Only consider enemies
                if stat_sheet.get('category') != 'Enemy':
                    continue
                
                hold_context = stat_sheet.get('hold_context', {})
                
                # Check if hold is in primary list
                if hold_name in hold_context.get('primary', []):
                    results['primary'].append(stat_sheet)
                # Check if hold is in contested list
                elif hold_name in hold_context.get('contested', []):
                    results['contested'].append(stat_sheet)
                # Check if hold is in rare list
                elif hold_name in hold_context.get('rare', []):
                    results['rare'].append(stat_sheet)
                # Also check location field for general matches
                elif location_matches(hold_name, stat_sheet.get('location', '')):
                    # Add to primary if no hold_context specified
                    if not hold_context:
                        results['primary'].append(stat_sheet)
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Error reading {stat_file.name}: {e}")
                continue
        
        return results
    
    def get_enemies_by_act(self, act):
        """
        Get enemies appropriate for a specific act
        
        Args:
            act: Act identifier (e.g., 'Act 1', 'Act 2', 'Act 3')
        
        Returns:
            List of enemy stat sheets appropriate for the act
        """
        if not self.npc_stat_sheets_dir.exists():
            return []
        
        results = []
        
        for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
            try:
                with open(stat_file, 'r') as f:
                    stat_sheet = json.load(f)
                
                # Only consider enemies
                if stat_sheet.get('category') != 'Enemy':
                    continue
                
                # Check if act is in act_context
                if act in stat_sheet.get('act_context', []):
                    results.append(stat_sheet)
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Error reading {stat_file.name}: {e}")
                continue
        
        return results
    
    def get_npcs_for_scene(self, location=None, scene_type=None):
        """
        Get NPCs appropriate for a scene
        
        Args:
            location: Scene location
            scene_type: Type of scene (e.g., 'combat', 'dialogue', 'exploration')
        
        Returns:
            Dict with friendly and hostile NPCs
        """
        result = {
            'friendly': [],
            'hostile': [],
            'enemies': []
        }
        
        if location:
            # Get friendly NPCs at location
            result['friendly'] = self.query_npc_enemy_stats(
                location=location, 
                category="Friendly NPC"
            )
            
            # Get hostile NPCs at location
            result['hostile'] = self.query_npc_enemy_stats(
                location=location, 
                category="Hostile NPC"
            )
            
            # Get enemies at location
            result['enemies'] = self.query_npc_enemy_stats(
                location=location, 
                category="Enemy"
            )
        
        return result
    
    def list_all_stat_sheets(self):
        """List all available NPC/enemy stat sheets"""
        if not self.npc_stat_sheets_dir.exists():
            return []
        
        results = []
        for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
            try:
                with open(stat_file, 'r') as f:
                    stat_sheet = json.load(f)
                    results.append({
                        'id': stat_sheet.get('id'),
                        'name': stat_sheet.get('name'),
                        'type': stat_sheet.get('type'),
                        'category': stat_sheet.get('category'),
                        'location': stat_sheet.get('location')
                    })
            except (json.JSONDecodeError, IOError):
                continue
        
        return results


def display_npc(npc):
    """Display NPC information in a readable format"""
    print(f"\n{'='*50}")
    print(f"Name: {npc['name']}")
    print(f"Type: {npc.get('type', 'Unknown')}")
    print(f"Location: {npc.get('location', 'Unknown')}")
    print(f"Faction: {npc.get('faction', 'None')}")
    print(f"\nHigh Concept: {npc['aspects']['high_concept']}")
    print(f"Trouble: {npc['aspects']['trouble']}")
    print(f"\nNotes: {npc.get('notes', 'None')}")
    print(f"{'='*50}")


def display_quest(quest):
    """Display quest information in a readable format"""
    print(f"\n{'='*50}")
    print(f"Quest: {quest['name']}")
    print(f"Type: {quest['type']}")
    print(f"Status: {quest['status']}")
    print(f"\nDescription: {quest['description']}")
    print(f"\nObjectives:")
    for obj in quest['objectives']:
        status_symbol = "✓" if obj['status'] == 'Completed' else "○"
        print(f"  {status_symbol} {obj['description']}")
    print(f"{'='*50}")


def display_stat_sheet(stat):
    """Display NPC/enemy stat sheet in a readable format"""
    print(f"\n{'='*70}")
    print(f"Name: {stat['name']} ({stat['category']})")
    print(f"Type: {stat['type']}")
    print(f"Location: {stat['location']}")
    print(f"Faction: {stat.get('faction', 'None')}")
    
    print(f"\n--- Aspects ---")
    print(f"High Concept: {stat['aspects']['high_concept']}")
    print(f"Trouble: {stat['aspects']['trouble']}")
    if 'other_aspects' in stat['aspects']:
        for aspect in stat['aspects']['other_aspects']:
            print(f"  • {aspect}")
    
    print(f"\n--- Skills ---")
    for level, skills in stat['skills'].items():
        if isinstance(skills, list):
            print(f"{level}: {', '.join(skills)}")
        else:
            print(f"{level}: {skills}")
    
    print(f"\n--- Stress ---")
    if stat['stress'].get('physical'):
        print(f"Physical: [{len(stat['stress']['physical'])} boxes]")
    if stat['stress'].get('mental'):
        print(f"Mental: [{len(stat['stress']['mental'])} boxes]")
    
    print(f"\n--- Stunts ---")
    for stunt in stat.get('stunts', []):
        print(f"  • {stunt}")
    
    if stat.get('notes'):
        print(f"\nNotes: {stat['notes'][:200]}...")
    
    print(f"{'='*70}")


def main():
    """Main function to demonstrate query capabilities"""
    print("=== Skyrim TTRPG Data Query Manager ===\n")
    
    manager = DataQueryManager("../data")
    
    # Example: Query NPCs
    print("1. Querying NPCs in Whiterun...")
    npcs = manager.query_npcs(location="Whiterun")
    for npc in npcs:
        display_npc(npc)
    
    # Example: Query Active Quests
    print("\n2. Querying Active Quests...")
    quests = manager.query_quests(status="Active")
    for quest in quests:
        display_quest(quest)
    
    # Example: Search Rules
    print("\n3. Searching rules for 'magic'...")
    rule_results = manager.search_rules("magic")
    for result in rule_results:
        print(f"\nFound in {result['file']}:")
        for line in result['matches'][:5]:  # Show first 5 lines
            print(f"  {line}")
    
    # Example: Get World State
    print("\n4. Getting World State...")
    world_state = manager.get_world_state()
    if world_state:
        print(f"Game Date: {world_state.get('game_date', 'Unknown')}")
        print(f"Days Passed: {world_state.get('in_game_days_passed', 0)}")
        
        # Post-Alduin timeline - dragon crisis is resolved
        post_dragon = world_state.get('post_dragon_crisis', {})
        if post_dragon:
            print(f"Dragon Status: {post_dragon.get('status', 'Unknown')}")
            print(f"Timeline Note: {post_dragon.get('timeline_note', 'N/A')}")
        
        # Show Civil War status from political situation
        political_situation = world_state.get('political_situation', {})
        if political_situation:
            print(f"\nCivil War Status: {political_situation.get('skyrim_status', 'Unknown')}")
        
        print("\nActive Threats:")
        for threat in world_state.get('active_threats', []):
            print(f"  - {threat}")
    
    # Example: Query PDF Topics
    print("\n5. Querying PDF topics for 'standing stones'...")
    pdf_results = manager.query_pdf_topics("standing stones")
    if 'error' in pdf_results:
        print(f"  Error: {pdf_results['error']}")
    else:
        print(f"Query: {pdf_results.get('query', 'unknown')}")
        print(f"Matched files: {pdf_results.get('files', [])}")
        for detail in pdf_results.get('details', []):
            print(f"\n  File: {detail['file']}")
            print(f"  Description: {detail['description']}")
            print(f"  Source PDF: {detail['source_pdf']}")
    
    # Example: Query PDF Topics for races
    print("\n6. Querying PDF topics for 'races'...")
    race_results = manager.query_pdf_topics("races")
    if 'error' in race_results:
        print(f"  Error: {race_results['error']}")
    else:
        print(f"Query: {race_results.get('query', 'unknown')}")
        print(f"Matched files: {race_results.get('files', [])}")
    
    # Example: Get PDF content
    print("\n7. Getting PDF content for 'dragonbreak'...")
    content_results = manager.get_pdf_content("dragonbreak")
    for result in content_results.get('results', []):
        print(f"\n  From: {result['file']}")
        print(f"  Description: {result['description']}")
        if result['type'] == 'markdown':
            # Show first 200 characters
            content_preview = result['content'][:200].replace('\n', ' ')
            print(f"  Preview: {content_preview}...")
    
    # NEW: Example: List all NPC/enemy stat sheets
    print("\n8. Listing all NPC/enemy stat sheets...")
    all_stats = manager.list_all_stat_sheets()
    for stat in all_stats:
        print(f"  - {stat['name']} ({stat['category']}) - {stat['location']}")
    
    # NEW: Example: Query enemies by type
    print("\n9. Querying Enemy stat sheets...")
    enemies = manager.query_npc_enemy_stats(category="Enemy")
    print(f"Found {len(enemies)} enemy types:")
    for enemy in enemies[:3]:  # Show first 3
        display_stat_sheet(enemy)
    
    # NEW: Example: Get NPCs for a scene
    print("\n10. Getting NPCs for Whiterun scene...")
    scene_npcs = manager.get_npcs_for_scene(location="Whiterun")
    print(f"Friendly NPCs: {len(scene_npcs['friendly'])}")
    print(f"Hostile NPCs: {len(scene_npcs['hostile'])}")
    print(f"Enemies: {len(scene_npcs['enemies'])}")
    
    # NEW: Example: Query specific enemy
    print("\n11. Querying for Dragons...")
    dragons = manager.query_npc_enemy_stats(name="dragon")
    for dragon in dragons:
        display_stat_sheet(dragon)
    
    # NEW: Example: Query faction quests
    print("\n12. Querying Companions faction quests...")
    companion_quests = manager.query_faction_quests(faction_id="companions")
    for faction, data in companion_quests.items():
        print(f"\n{faction.upper()} - {data['questline']}")
        for quest in data['quests'][:2]:  # Show first 2
            print(f"  [{quest['id']}] {quest['name']}")
            print(f"    Description: {quest['description']}")
    
    # NEW: Example: Get enemies by hold
    print("\n13. Getting enemies for Eastmarch hold...")
    eastmarch_enemies = manager.get_enemies_by_hold("Eastmarch")
    print(f"Primary enemies: {len(eastmarch_enemies['primary'])}")
    for enemy in eastmarch_enemies['primary']:
        print(f"  - {enemy['name']}")
    
    # NEW: Example: Get enemies by act
    print("\n14. Getting enemies for Act 1...")
    act1_enemies = manager.get_enemies_by_act("Act 1")
    print(f"Act 1 enemies: {len(act1_enemies)}")
    for enemy in act1_enemies[:5]:  # Show first 5
        print(f"  - {enemy['name']} ({enemy['location']})")
    
    # NEW: Example: Get trust mechanics
    print("\n15. Getting trust mechanics...")
    trust_mechanics = manager.get_trust_mechanics()
    print("Trust Levels:")
    for level, description in trust_mechanics.get('trust_levels', {}).items():
        print(f"  {level}: {description}")
    
    print("\nQuery complete!")


if __name__ == "__main__":
    main()
