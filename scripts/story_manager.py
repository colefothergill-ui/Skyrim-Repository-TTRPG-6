#!/usr/bin/env python3
"""
Story Manager for Skyrim TTRPG

This script manages:
- Dynamic branching quest logic
- Campaign state transitions
- Story progression based on player choices
- Integration between main quest, civil war, and Thalmor arcs
- Scene-based NPC/enemy stat application
- Dragonbreak support for parallel timeline events
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from utils import location_matches
from query_data import DataQueryManager
from first_impression import maybe_first_impression

# Import DragonbreakManager if available
try:
    from dragonbreak_manager import DragonbreakManager
    DRAGONBREAK_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    DRAGONBREAK_AVAILABLE = False
    # Optionally log the import failure for debugging
    # import sys
    # print(f"Warning: DragonbreakManager not available: {e}", file=sys.stderr)


class StoryManager:
    def __init__(self, data_dir="../data", state_dir="../state"):
        self.data_dir = Path(data_dir)
        self.state_dir = Path(state_dir)
        self.campaign_state_path = self.state_dir / "campaign_state.json"
        self.main_quests_path = self.data_dir / "quests" / "main_quests.json"
        self.civil_war_path = self.data_dir / "quests" / "civil_war_quests.json"
        self.thalmor_path = self.data_dir / "thalmor_arcs.json"
        self.npc_stat_sheets_dir = self.data_dir / "npc_stat_sheets"
        self.query_manager = DataQueryManager(str(self.data_dir))
        
        # Initialize Dragonbreak Manager if available
        if DRAGONBREAK_AVAILABLE:
            self.dragonbreak_manager = DragonbreakManager(str(self.data_dir), str(self.state_dir))
        else:
            self.dragonbreak_manager = None
        
    def load_campaign_state(self):
        """Load current campaign state"""
        if self.campaign_state_path.exists():
            with open(self.campaign_state_path, 'r') as f:
                return json.load(f)
        return None
    
    def save_campaign_state(self, state):
        """Save campaign state"""
        self.state_dir.mkdir(exist_ok=True)
        state['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.campaign_state_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_main_quests(self):
        """Load main quest data"""
        if self.main_quests_path.exists():
            with open(self.main_quests_path, 'r') as f:
                return json.load(f)
        return None
    
    def load_civil_war_quests(self):
        """Load civil war quest data"""
        if self.civil_war_path.exists():
            with open(self.civil_war_path, 'r') as f:
                return json.load(f)
        return None
    
    def record_branching_decision(self, decision_key, choice):
        """
        Record a major branching decision
        
        Args:
            decision_key: Key from branching_decisions (e.g., 'civil_war_entry_contact')
            choice: The choice made (e.g., 'Ralof' or 'Hadvar')
        """
        state = self.load_campaign_state()
        if state and 'branching_decisions' in state:
            state['branching_decisions'][decision_key] = choice
            
            # Add to world consequences
            consequence = f"Decision: {decision_key} = {choice}"
            if 'world_consequences' in state:
                state['world_consequences']['major_choices'].append({
                    'decision': decision_key,
                    'choice': choice,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            self.save_campaign_state(state)
            print(f"Recorded decision: {decision_key} = {choice}")
            return True
        return False
    
    def update_civil_war_state(self, alliance=None, battle_result=None):
        """
        Update civil war state
        
        Args:
            alliance: 'imperial', 'stormcloak', or None
            battle_result: Dict with battle outcome
        """
        state = self.load_campaign_state()
        if not state:
            return False
        
        if alliance:
            state['civil_war_state']['player_alliance'] = alliance
            print(f"Player alliance set to: {alliance}")
        
        if battle_result:
            battle_name = battle_result.get('battle_name')
            winner = battle_result.get('winner')
            
            if winner == 'imperial':
                state['civil_war_state']['imperial_victories'] += 1
            elif winner == 'stormcloak':
                state['civil_war_state']['stormcloak_victories'] += 1
            
            state['civil_war_state']['key_battles_completed'].append(battle_name)
            
            # Update Battle of Whiterun specifically
            if 'whiterun' in battle_name.lower():
                state['civil_war_state']['battle_of_whiterun_status'] = 'completed'
                print(f"Battle of Whiterun completed - Winner: {winner}")
        
        self.save_campaign_state(state)
        return True
    
    def update_main_quest_state(self, **kwargs):
        """
        Update main quest progression
        
        Kwargs can include:
            civil_war_involvement: bool
            dragons_knowledge: str
            blades_contacted: bool
            greybeards_training: str
            alduin_threat_level: int
            dragon_souls_absorbed: int
            shouts_learned: list
        """
        state = self.load_campaign_state()
        if not state or 'main_quest_state' not in state:
            return False
        
        for key, value in kwargs.items():
            if key in state['main_quest_state']:
                if key == 'shouts_learned' and isinstance(value, list):
                    # Append to list
                    for shout in value:
                        if shout not in state['main_quest_state']['shouts_learned']:
                            state['main_quest_state']['shouts_learned'].append(shout)
                elif key == 'dragon_souls_absorbed':
                    # Increment
                    state['main_quest_state'][key] += value
                else:
                    state['main_quest_state'][key] = value
                
                print(f"Updated main quest: {key} = {value}")
        
        self.save_campaign_state(state)
        return True
    
    def update_thalmor_arc(self, plot_id, progress_change=0, discovery=None):
        """
        Update Thalmor arc progression
        
        Args:
            plot_id: ID of the Thalmor plot
            progress_change: Amount to change progress clock
            discovery: Discovery made by players (string)
        """
        state = self.load_campaign_state()
        if not state or 'thalmor_arc' not in state:
            return False
        
        # Update active plots
        for plot in state['thalmor_arc']['active_plots']:
            if plot['plot_id'] == plot_id:
                plot['progress'] = max(0, min(plot['clock_segments'], 
                                             plot['progress'] + progress_change))
                print(f"Thalmor plot '{plot_id}' progress: {plot['progress']}/{plot['clock_segments']}")
        
        # Record discovery
        if discovery:
            state['thalmor_arc']['thalmor_schemes_discovered'].append({
                'discovery': discovery,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"Thalmor scheme discovered: {discovery}")
        
        self.save_campaign_state(state)
        return True
    
    def get_available_quests(self):
        """
        Get list of currently available quests based on state
        """
        state = self.load_campaign_state()
        main_quests_data = self.load_main_quests()
        
        if not state or not main_quests_data:
            return []
        
        available = []
        
        # Check main questline
        for quest in main_quests_data['main_questline']['quests']:
            if quest['status'] == 'available':
                available.append({
                    'type': 'main',
                    'quest': quest
                })
        
        return available
    
    def advance_quest(self, quest_id, new_status):
        """
        Advance a quest to a new status
        
        Args:
            quest_id: ID of the quest
            new_status: New status ('available', 'active', 'completed', 'failed')
        """
        main_quests_data = self.load_main_quests()
        if not main_quests_data:
            return False
        
        # Find and update quest
        for quest in main_quests_data['main_questline']['quests']:
            if quest['id'] == quest_id:
                old_status = quest['status']
                quest['status'] = new_status
                
                # If completing a quest, unlock next quest
                if new_status == 'completed' and 'next_quest' in quest:
                    next_quest_id = quest['next_quest']
                    for next_quest in main_quests_data['main_questline']['quests']:
                        if next_quest['id'] == next_quest_id:
                            next_quest['status'] = 'available'
                            print(f"Unlocked quest: {next_quest['name']}")
                
                # Save updated data
                with open(self.main_quests_path, 'w') as f:
                    json.dump(main_quests_data, f, indent=2)
                
                print(f"Quest '{quest['name']}' status: {old_status} -> {new_status}")
                return True
        
        return False
    
    def check_story_arcs(self):
        """
        Check and update active story arcs
        """
        state = self.load_campaign_state()
        if not state or 'active_story_arcs' not in state:
            return None
        
        print("\n=== Active Story Arcs ===")
        for arc in state['active_story_arcs']:
            print(f"\n{arc['arc_name']} - Status: {arc['status']}")
            print(f"  Progress: {arc['progress']}")
            print(f"  Next: {arc['next_milestone']}")
        
        return state['active_story_arcs']
    
    def add_world_consequence(self, consequence_type, data):
        """
        Add a world consequence
        
        Args:
            consequence_type: 'towns_affected', 'npcs_killed', 'npcs_befriended'
            data: The data to add
        """
        state = self.load_campaign_state()
        if not state or 'world_consequences' not in state:
            return False
        
        if consequence_type in state['world_consequences']:
            if data not in state['world_consequences'][consequence_type]:
                state['world_consequences'][consequence_type].append(data)
                self.save_campaign_state(state)
                print(f"World consequence recorded: {consequence_type} - {data}")
                return True
        
        return False
    
    def generate_story_summary(self):
        """
        Generate a summary of the current story state
        """
        state = self.load_campaign_state()
        if not state:
            return "No campaign state found."
        
        summary = f"""
=== Campaign Summary ===
Campaign: {state['campaign_name']}
Date: {state['started_date']} (Session {state['session_count']})
Act: {state['current_act']}

=== Civil War ===
Alliance: {state['civil_war_state']['player_alliance']}
Battle of Whiterun: {state['civil_war_state']['battle_of_whiterun_status']}
Imperial Victories: {state['civil_war_state']['imperial_victories']}
Stormcloak Victories: {state['civil_war_state']['stormcloak_victories']}

=== Main Quest ===
Civil War Active: {state['main_quest_state'].get('civil_war_involvement', True)}
Dragon Souls: {state['main_quest_state']['dragon_souls_absorbed']}
Shouts Known: {len(state['main_quest_state']['shouts_learned'])}
Greybeards Training: {state['main_quest_state']['greybeards_training']}

=== Thalmor Threat ===
Awareness Level: {state['thalmor_arc']['thalmor_awareness_of_party']}
Embassy Infiltrated: {state['thalmor_arc']['embassy_infiltrated']}
Schemes Discovered: {len(state['thalmor_arc']['thalmor_schemes_discovered'])}

=== Major Decisions ===
"""
        for key, value in state['branching_decisions'].items():
            if value:
                summary += f"- {key}: {value}\n"
        
        return summary
    
    def get_scene_npcs(self, location, scene_type="general"):
        """
        Get appropriate NPCs/enemies for a scene based on location and type
        
        Args:
            location: Scene location (e.g., "Whiterun", "Nordic ruins", "Roads")
            scene_type: Type of scene (e.g., "combat", "dialogue", "exploration")
        
        Returns:
            Dict with suggested NPCs and enemies for the scene
        """
        result = {
            'friendly': [],
            'hostile': [],
            'enemies': [],
            'suggestions': []
        }
        
        if not self.npc_stat_sheets_dir.exists():
            return result
        
        # Load all stat sheets and filter by location
        for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
            try:
                with open(stat_file, 'r') as f:
                    stat_sheet = json.load(f)
                
                # Check if location matches (case-insensitive partial match)
                sheet_location = stat_sheet.get('location', '')
                
                if location_matches(location, sheet_location):
                    category = stat_sheet.get('category', '')
                    
                    if category == "Friendly NPC":
                        result['friendly'].append(stat_sheet)
                    elif category == "Hostile NPC":
                        result['hostile'].append(stat_sheet)
                    elif category == "Enemy":
                        result['enemies'].append(stat_sheet)
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Error reading {stat_file.name}: {e}")
                continue
        
        # Add scene-specific suggestions
        if scene_type == "combat":
            result['suggestions'].append("Consider using enemies appropriate to location")
            result['suggestions'].append("Mix enemy types for varied combat")
        elif scene_type == "dialogue":
            result['suggestions'].append("Use friendly NPCs for information gathering")
            result['suggestions'].append("Hostile NPCs can create tension")
        
        return result
    
    def apply_combat_consequences(self, enemy_type, outcome):
        """
        Apply consequences from combat encounters to world state
        
        Args:
            enemy_type: Type of enemy defeated (e.g., "dragon", "bandit", "thalmor")
            outcome: Combat outcome ("victory", "defeat", "fled")
        
        Returns:
            Dict with applied consequences
        """
        state = self.load_campaign_state()
        if not state:
            return {"error": "No campaign state found"}
        
        consequences = {
            'faction_changes': [],
            'world_updates': [],
            'quest_triggers': []
        }
        
        # Dragon encounters
        if "dragon" in enemy_type.lower():
            if outcome == "victory":
                # Update main quest state
                if 'main_quest_state' in state:
                    state['main_quest_state']['dragon_souls_absorbed'] += 1
                    consequences['world_updates'].append("Dragon soul absorbed")
                    consequences['quest_triggers'].append("Dragon Rising progression")
        
        # Thalmor encounters
        if "thalmor" in enemy_type.lower():
            if outcome == "victory" and 'thalmor_arc' in state:
                state['thalmor_arc']['thalmor_awareness_of_party'] = min(10, 
                    state['thalmor_arc']['thalmor_awareness_of_party'] + 1)
                consequences['faction_changes'].append("Thalmor awareness increased")
        
        # Bandit encounters
        if "bandit" in enemy_type.lower():
            if outcome == "victory":
                consequences['world_updates'].append("Area safer for travelers")
        
        self.save_campaign_state(state)
        return consequences
    
    def _load_active_pc(self):
        """Load the active PC file from campaign state (if available)."""
        state = self.load_campaign_state() or {}
        pc_id = state.get("active_pc_id") or state.get("active_pc")

        if isinstance(pc_id, str) and pc_id:
            # Normalize common forms
            if not pc_id.startswith("pc_"):
                pc_id = f"pc_{pc_id}"
            pc_path = self.data_dir / "pcs" / f"{pc_id}.json"
            if pc_path.exists():
                with open(pc_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        return None

    def _get_pc_compel_hooks(self, max_items=5):
        """
        Return structured compel hooks (usually Trouble-based) for GM prompts.
        
        Returns:
            List of dict, each containing keys like 'id', 'title', 'when', 
            'compel_hit', 'suggested_scene_aspect', 'tags', and optionally 
            'exception_tags'. Returns empty list if no hooks are found.
        """
        pc = self._load_active_pc()
        if not isinstance(pc, dict):
            return []

        aspects = pc.get("aspects", {})
        if not isinstance(aspects, dict):
            return []

        lib = aspects.get("compel_library", {})
        if isinstance(lib, dict):
            ideas = lib.get("ideas", [])
            if isinstance(ideas, list) and ideas:
                return ideas[:max_items]
        return []
    
    def trigger_scene_event(self, scene_data):
        """
        Trigger a scene event and apply appropriate NPCs/enemies
        
        Args:
            scene_data: Dict with scene information
                - location: str
                - type: str (combat/dialogue/exploration)
                - triggers: list of trigger conditions
        
        Returns:
            Complete scene setup with NPCs/enemies
        """
        location = scene_data.get('location', 'Unknown')
        scene_type = scene_data.get('type', 'general')
        
        # Get NPCs for scene
        scene_npcs = self.get_scene_npcs(location, scene_type)
        
        # Add first impression hook for NPCs
        # Dynamically determine PC appearance path based on active PC
        state_path = str(self.campaign_state_path)
        appearance_path = None
        
        # Try to determine PC ID from campaign state
        try:
            with open(self.campaign_state_path, 'r') as f:
                state = json.load(f)
                pc_id = state.get("active_pc_id") or state.get("active_pc")
                if not pc_id and state.get("player_characters"):
                    # Fallback to first PC in player_characters list
                    pc_id = state["player_characters"][0].get("id")
                
                if pc_id:
                    # Convert pc_id to appearance file slug
                    slug = pc_id.replace("pc_", "")
                    appearance_path = str(self.data_dir / "pcs" / "appearances" / f"{slug}_appearance.json")
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass  # No state or invalid state, skip first impressions
        
        # Only attempt first impressions if appearance file exists
        if appearance_path and Path(appearance_path).exists():
            # scene_npcs is a dict of buckets -> list[dict]
            for bucket_name, bucket_disposition in (
                ("friendly", "positive"),
                ("hostile", "negative"),
                ("enemies", "neutral"),
            ):
                for npc in (scene_npcs.get(bucket_name, []) or []):
                    if not isinstance(npc, dict):
                        # Log data quality issue for debugging
                        print(f"Warning: Non-dict item found in {bucket_name} bucket: {type(npc).__name__}", file=sys.stderr)
                        continue
                    npc_id = npc.get("id") or npc.get("npc_id")
                    if not npc_id:
                        continue

                    # Normalize stat-sheet ids (e.g., 'npc_stat_mallus_maccius' -> 'mallus_maccius')
                    if isinstance(npc_id, str) and npc_id.startswith("npc_stat_"):
                        npc_id = npc_id.replace("npc_stat_", "", 1)

                    try:
                        line = maybe_first_impression(
                            state_path,
                            appearance_path,
                            npc_id,
                            disposition=bucket_disposition
                        )
                        if line:
                            npc.setdefault("gm_barks", [])
                            npc["gm_barks"].append(line)
                    except Exception as e:
                        # Log full error for debugging, show simple message to users
                        print(f"First impression error for {npc_id} in {bucket_name}: {e}", file=sys.stderr)
                        npc.setdefault("gm_barks", [])
                        npc["gm_barks"].append("(First impression unavailable)")
        
        # Build scene response
        scene_setup = {
            'location': location,
            'type': scene_type,
            'npcs': scene_npcs,
            'description': self._generate_scene_description(location, scene_type),
            'mechanical_notes': self._get_mechanical_notes(scene_type)
        }
        
        pc_compels = self._get_pc_compel_hooks(max_items=5)
        if pc_compels:
            scene_setup["pc_compel_hooks"] = pc_compels
        
        return scene_setup
    
    def _generate_scene_description(self, location, scene_type):
        """Generate a description for the scene"""
        descriptions = {
            'combat': f"A dangerous confrontation unfolds in {location}",
            'dialogue': f"An opportunity for conversation arises in {location}",
            'exploration': f"The party explores {location}, discovering its secrets"
        }
        return descriptions.get(scene_type, f"The party finds themselves in {location}")
    
    def _get_mechanical_notes(self, scene_type):
        """Get mechanical notes for scene type"""
        notes = {
            'combat': [
                "Use zones for tactical positioning",
                "Track stress and consequences",
                "Apply combat consequences to world state after"
            ],
            'dialogue': [
                "Use Rapport, Deceive, or Provoke as appropriate",
                "Update relationship clocks based on outcome",
                "Compel aspects for dramatic tension"
            ],
            'exploration': [
                "Use Notice, Investigate, or Lore",
                "Create aspects from discoveries",
                "Set up future encounters"
            ]
        }
        return notes.get(scene_type, [])
    
    def track_faction_quest_progress(self, faction_id, quest_id, status='started', trust_change=0):
        """
        Track faction quest progress and update trust
        
        Args:
            faction_id: ID of the faction (e.g., 'companions', 'thieves_guild')
            quest_id: ID of the quest
            status: Quest status ('started', 'in_progress', 'completed', 'failed')
            trust_change: Change in trust level (positive or negative)
        
        Returns:
            Updated state or error
        """
        state = self.load_campaign_state()
        if not state:
            return {"error": "No campaign state found"}
        
        # Initialize faction quest tracking if not exists
        if 'faction_quests' not in state:
            state['faction_quests'] = {}
        
        if faction_id not in state['faction_quests']:
            state['faction_quests'][faction_id] = {
                'trust_level': 0,
                'completed_quests': [],
                'active_quests': [],
                'failed_quests': []
            }
        
        faction_data = state['faction_quests'][faction_id]
        
        # Update quest status
        if status == 'started':
            if quest_id not in faction_data['active_quests']:
                faction_data['active_quests'].append(quest_id)
        elif status == 'completed':
            if quest_id in faction_data['active_quests']:
                faction_data['active_quests'].remove(quest_id)
            if quest_id not in faction_data['completed_quests']:
                faction_data['completed_quests'].append(quest_id)
        elif status == 'failed':
            if quest_id in faction_data['active_quests']:
                faction_data['active_quests'].remove(quest_id)
            if quest_id not in faction_data['failed_quests']:
                faction_data['failed_quests'].append(quest_id)
        
        # Update trust level
        if trust_change != 0:
            faction_data['trust_level'] = max(0, min(10, 
                faction_data['trust_level'] + trust_change))
            print(f"{faction_id} trust level: {faction_data['trust_level']}/10")
        
        self.save_campaign_state(state)
        print(f"Faction quest updated: {faction_id} - {quest_id} ({status})")
        
        return {
            'faction_id': faction_id,
            'quest_id': quest_id,
            'status': status,
            'trust_level': faction_data['trust_level'],
            'completed_quests': faction_data['completed_quests']
        }
    
    def get_faction_status(self, faction_id=None):
        """
        Get current status with one or all factions
        
        Args:
            faction_id: Specific faction to query, or None for all
        
        Returns:
            Faction status information
        """
        state = self.load_campaign_state()
        if not state or 'faction_quests' not in state:
            return {"error": "No faction data found"}
        
        if faction_id:
            return state['faction_quests'].get(faction_id, 
                {"error": f"No data for faction {faction_id}"})
        
        return state['faction_quests']
    
    def get_starting_companion(self):
        """
        Get the starting companion (Hadvar or Ralof) based on civil war entry contact
        
        Returns:
            Dict with companion info or None
        """
        state = self.load_campaign_state()
        if not state:
            return None
        
        # Check branching decision for civil war entry contact
        entry_companion = state.get('branching_decisions', {}).get('civil_war_entry_contact')
        
        if not entry_companion or entry_companion == 'undecided':
            return None
        
        # Find companion in active companions
        if 'companions' in state:
            for companion in state['companions'].get('active_companions', []):
                if companion['name'] == entry_companion:
                    return companion
        
        return None
    
    def get_companion_dialogue_hooks(self, location, situation="general"):
        """
        Get dialogue hooks for active companions based on location and situation
        
        Args:
            location: Current location (e.g., "Whiterun", "Riverwood")
            situation: Current situation type (e.g., "arrival", "combat", "civil_war")
        
        Returns:
            Dict with companion dialogue suggestions
        """
        state = self.load_campaign_state()
        if not state or 'companions' not in state:
            return {"companions": [], "suggestions": []}
        
        active_companions = state['companions'].get('active_companions', [])
        entry_companion = state.get('branching_decisions', {}).get('civil_war_entry_contact')
        
        result = {
            'companions': [],
            'dialogue_hooks': []
        }
        
        # Add Hadvar dialogue hooks
        if entry_companion == "Hadvar":
            hadvar_hooks = {
                'name': 'Hadvar',
                'location': location,
                'situation': situation,
                'hooks': []
            }
            
            if location.lower() == "riverwood":
                hadvar_hooks['hooks'].append({
                    'trigger': 'Arrival',
                    'dialogue': "We should visit my uncle Alvor's forge. He'll help us, no questions asked. Family is family."
                })
                hadvar_hooks['hooks'].append({
                    'trigger': 'At Alvor\'s forge',
                    'dialogue': "Uncle! It's good to see you. These are my companions from the civil war efforts. Can you help us?"
                })
            
            if location.lower() == "whiterun":
                hadvar_hooks['hooks'].append({
                    'trigger': 'Approaching gates',
                    'dialogue': "Whiterun. The heart of Skyrim. We need to inform the Jarl about the war situation. My Imperial credentials should get us an audience."
                })
                if situation == "civil_war":
                    hadvar_hooks['hooks'].append({
                        'trigger': 'Civil war discussion',
                        'dialogue': "The Battle of Whiterun is coming. I believe the Empire is necessary to keep Skyrim strong against the Thalmor, but... I hope we can end this with minimal bloodshed."
                    })
            
            if situation == "combat" and "imperial" in location.lower():
                hadvar_hooks['hooks'].append({
                    'trigger': 'Fighting alongside Imperials',
                    'dialogue': "Shield wall! Protect your brothers! For the Empire!"
                })
            
            result['companions'].append(hadvar_hooks)
        
        # Add Ralof dialogue hooks
        elif entry_companion == "Ralof":
            ralof_hooks = {
                'name': 'Ralof',
                'location': location,
                'situation': situation,
                'hooks': []
            }
            
            if location.lower() == "riverwood":
                ralof_hooks['hooks'].append({
                    'trigger': 'Arrival',
                    'dialogue': "My sister Gerdur runs the lumber mill here. She and her husband will shelter us. We Nords look after our own."
                })
                ralof_hooks['hooks'].append({
                    'trigger': 'At the lumber mill',
                    'dialogue': "Gerdur! By Talos, it's good to see you alive. These are friends - we're fighting together for Skyrim's freedom."
                })
            
            if location.lower() == "whiterun":
                ralof_hooks['hooks'].append({
                    'trigger': 'Approaching gates',
                    'dialogue': "Whiterun. For now, Balgruuf sits the fence, but he's already made his choice - the Empire's lap dog. We need to be careful here."
                })
                if situation == "civil_war":
                    ralof_hooks['hooks'].append({
                        'trigger': 'Civil war discussion',
                        'dialogue': "The Battle of Whiterun will decide Skyrim's future. We fight for our freedom, our right to worship Talos, and our children's future. That's worth any price."
                    })
            
            if situation == "combat" and "stormcloak" in location.lower():
                ralof_hooks['hooks'].append({
                    'trigger': 'Fighting alongside Stormcloaks',
                    'dialogue': "For Skyrim! For Talos! Show them the fury of true Nords!"
                })
            
            result['companions'].append(ralof_hooks)
        
        # Add general suggestions
        if active_companions:
            result['dialogue_hooks'].append("Companions may comment on party decisions, especially those related to their faction")
            result['dialogue_hooks'].append("Ask companions for their perspective on local NPCs or situations")
            result['dialogue_hooks'].append("Companions may warn about dangers or suggest alternate approaches based on their knowledge")
        
        return result
    
    def trigger_battle_of_whiterun_encounter(self, neutral_subfaction=None):
        """
        Trigger the Battle of Whiterun encounter where neutral players meet Hadvar and Ralof
        
        Args:
            neutral_subfaction: The specific neutral faction the player is aligned with
        
        Returns:
            Encounter data with Hadvar/Ralof meeting setup
        """
        state = self.load_campaign_state()
        
        encounter = {
            "encounter_type": "battle_of_whiterun_choice",
            "location": "Whiterun - Battlements or Main Gate",
            "participants": ["Hadvar", "Ralof"],
            "context": "The Battle of Whiterun has erupted. Stormcloak forces assault the city while Imperial defenders rally.",
            "choice_required": True
        }
        
        # Add faction-specific context
        if neutral_subfaction == "companions":
            encounter["arrival_context"] = (
                "You arrive at Whiterun on Kodlak's orders to help defend the city. "
                "The Companions focus on honor, not politics, but the battle forces you to choose."
            )
        elif neutral_subfaction == "thieves_guild":
            encounter["arrival_context"] = (
                "You came to deliver Brynjolf's message to Olfrid Battle-Born, but the battle has begun. "
                "The guild's neutrality won't protect you in this chaos."
            )
        elif neutral_subfaction == "college":
            encounter["arrival_context"] = (
                "You arrived to assist Farengar with dragon research, but the battle interrupts everything. "
                "The College's scholarly pursuits must wait."
            )
        elif neutral_subfaction == "dark_brotherhood":
            encounter["arrival_context"] = (
                "You came to assassinate Jarl Balgruuf, but the battle creates both opportunity and complication. "
                "Chaos reigns, and you must decide your approach."
            )
        elif neutral_subfaction == "blades":
            encounter["arrival_context"] = (
                "You escorted Delphine to meet Farengar, but the battle erupts. "
                "Delphine's old Imperial loyalty conflicts with the immediate danger."
            )
        elif neutral_subfaction == "greybeards":
            encounter["arrival_context"] = (
                "You came hoping to broker peace or protect innocents, but the battle has begun. "
                "The Way of the Voice teaches restraint, but action is required."
            )
        else:
            encounter["arrival_context"] = (
                "You arrive in Whiterun as a neutral party, but the Battle of Whiterun forces you to take a side."
            )
        
        # The encounter itself
        encounter["encounter_description"] = (
            "Amidst the chaos of battle, you encounter two familiar faces: Hadvar, the Imperial soldier, "
            "and Ralof, the Stormcloak warrior. Both recognize you and call out for aid. "
            "Hadvar shouts: 'The city needs defenders! Stand with us!' "
            "Ralof counters: 'Help us free Whiterun from Imperial occupation!' "
            "You must choose whom to assist."
        )
        
        encounter["choices"] = {
            "assist_hadvar": {
                "description": "Fight alongside Hadvar and the Imperial defenders",
                "consequences": [
                    "Hadvar becomes available as companion with loyalty 60",
                    "Ralof becomes unavailable",
                    "Imperial Legion relationship +30",
                    "Stormcloaks relationship -20",
                    "Civil war entry contact set to 'Hadvar'"
                ],
                "narrative": "You choose to stand with Hadvar and defend Whiterun alongside Imperial forces."
            },
            "assist_ralof": {
                "description": "Fight alongside Ralof and the Stormcloak attackers",
                "consequences": [
                    "Ralof becomes available as companion with loyalty 60",
                    "Hadvar becomes unavailable",
                    "Stormcloaks relationship +30",
                    "Imperial Legion relationship -20",
                    "Civil war entry contact set to 'Ralof'"
                ],
                "narrative": "You choose to stand with Ralof and assault Whiterun with the Stormcloaks."
            }
        }
        
        # Add Dark Brotherhood specific choice
        # Note: This choice is mutually exclusive with Hadvar/Ralof choices
        # Attempting assassination makes both civil war factions hostile
        if neutral_subfaction == "dark_brotherhood":
            encounter["choices"]["complete_contract"] = {
                "description": "Attempt to assassinate Jarl Balgruuf during the chaos (WARNING: This prevents choosing Hadvar or Ralof as companions)",
                "consequences": [
                    "Dark Brotherhood contract completed if successful",
                    "Both Hadvar and Ralof become hostile if discovered",
                    "Cannot recruit either Hadvar or Ralof as companion",
                    "Whiterun guards become hostile",
                    "Massive gold reward from Astrid (1000+ gold)",
                    "Must flee Whiterun after assassination",
                    "Civil war continues without your involvement"
                ],
                "narrative": "You use the battle as cover to complete Astrid's contract on the Jarl. This choice means forgoing any alliance with Hadvar or Ralof.",
                "mutually_exclusive": True,
                "warning": "Choosing assassination prevents companion recruitment and makes both civil war factions hostile"
            }
        
        return encounter
    
    def get_neutral_faction_quest_hooks(self, faction, act=1):
        """
        Get quest hooks that lead neutral faction members to Battle of Whiterun
        
        Args:
            faction: The neutral faction ('companions', 'thieves_guild', 'college', etc.)
            act: Current act (default 1 for Battle of Whiterun)
        
        Returns:
            Quest hooks dictionary
        """
        hooks = {
            "companions": {
                "quest_name": "Defending Whiterun",
                "quest_giver": "Kodlak Whitemane",
                "objective": "Assess threats to Whiterun and help defend the city",
                "starting_dialogue": (
                    "Kodlak: 'Jarl Balgruuf has requested aid. Whiterun faces danger. "
                    "I'm sending you - not to choose sides in politics, but to protect innocents. "
                    "Go to Whiterun, see what threatens the city, and defend those who cannot defend themselves.'"
                ),
                "complications": "Battle of Whiterun erupts, forcing faction choice",
                "rewards": "Companions reputation, Kodlak's respect, chosen companion"
            },
            "thieves_guild": {
                "quest_name": "Riften's Business in Whiterun",
                "quest_giver": "Brynjolf",
                "objective": "Deliver message to Olfrid Battle-Born and secure guild operations",
                "starting_dialogue": (
                    "Brynjolf: 'I need you to head to Whiterun. Find Olfrid Battle-Born - "
                    "discreet fellow, Battle-Born clan. Deliver this message. The civil war's "
                    "heating up, and we need our operations there secured. Stay sharp.'"
                ),
                "complications": "Arrive during Battle of Whiterun, must survive and choose side",
                "rewards": "Thieves Guild advancement, Olfrid's contacts, chosen companion"
            },
            "college": {
                "quest_name": "Dragon Research Mission",
                "quest_giver": "Tolfdir / Savos Aren",
                "objective": "Assist Farengar Secret-Fire with dragon investigation",
                "starting_dialogue": (
                    "Savos Aren: 'Dragons returning is no coincidence. This threatens all of Skyrim. "
                    "Go to Whiterun - Farengar Secret-Fire, a former student, is researching the phenomenon. "
                    "Assist him, learn what he's discovered, and report back.'"
                ),
                "complications": "Battle interrupts research, must fight to survive and protect knowledge",
                "rewards": "College favor, access to dragon research, chosen companion"
            },
            "dark_brotherhood": {
                "quest_name": "The Whiterun Contract",
                "quest_giver": "Astrid",
                "objective": "Assassinate Jarl Balgruuf during battle chaos",
                "starting_dialogue": (
                    "Astrid: 'I have a contract for you. Jarl Balgruuf of Whiterun. "
                    "Anonymous client, excellent payment. The city's preparing for battle - "
                    "perfect cover. His death will look like war casualty. In, kill, out. "
                    "Think you can handle it?'"
                ),
                "complications": "Must choose: complete contract, delay it, or refuse and fight in battle",
                "rewards": "Dark Brotherhood gold and advancement, or betrayal of the family"
            },
            "blades": {
                "quest_name": "Dragon Investigation Escort",
                "quest_giver": "Delphine",
                "objective": "Escort Delphine to Whiterun to investigate dragon research",
                "starting_dialogue": (
                    "Delphine: 'I need to get to Whiterun and see what Farengar's discovered "
                    "about the dragons. My research says there's something critical in his data. "
                    "Will you escort me? I can't risk the Thalmor catching me on the road alone.'"
                ),
                "complications": "Battle erupts upon arrival, must protect Delphine and choose side",
                "rewards": "Blades trust, dragon knowledge, chosen companion"
            },
            "greybeards": {
                "quest_name": "Peace Keeper's Burden",
                "quest_giver": "Personal calling / Master Arngeir",
                "objective": "Attempt to broker peace or at least protect civilians",
                "starting_dialogue": (
                    "Your own conscience drives you to Whiterun. Master Arngeir's words echo: "
                    "'True strength lies in restraint and wisdom, not violence.' You hope to "
                    "prevent bloodshed or at least protect innocents from the civil war."
                ),
                "complications": "Battle begins despite peaceful intentions, must choose side to survive",
                "rewards": "Moral clarity, respect for trying peace, chosen companion"
            }
        }
        
        return hooks.get(faction, None)
    
    def resolve_hadvar_ralof_choice(self, choice):
        """
        Resolve the player's choice between Hadvar and Ralof
        
        Args:
            choice: 'hadvar' or 'ralof'
        
        Returns:
            Updated campaign state with companion added
        """
        state = self.load_campaign_state()
        
        if choice == "hadvar":
            # Add Hadvar as active companion
            hadvar_companion = {
                "npc_id": "npc_stat_hadvar",
                "name": "Hadvar",
                "status": "active",
                "loyalty": 60,
                "location": "With party",
                "recruitment_trigger": "Fought together at Battle of Whiterun",
                "faction_affinity": "imperial_legion",
                "notes": "Rallied to defend Whiterun together. Pragmatic Imperial soldier."
            }
            
            if "companions" not in state:
                state["companions"] = {
                    "active_companions": [],
                    "available_companions": [],
                    "dismissed_companions": []
                }
            
            # Remove from available if present
            state["companions"]["available_companions"] = [
                c for c in state["companions"].get("available_companions", [])
                if c.get("name") != "Hadvar"
            ]
            
            # Add to active
            state["companions"]["active_companions"].append(hadvar_companion)
            
            # Update faction relationships
            if "civil_war_state" in state:
                state["civil_war_state"]["player_alliance"] = "imperial"
                state["civil_war_state"]["faction_relationship"]["imperial_legion"] += 30
                state["civil_war_state"]["faction_relationship"]["stormcloaks"] -= 20
            
            # Record decision
            state["branching_decisions"]["civil_war_entry_contact"] = "Hadvar"
            state["branching_decisions"]["battle_of_whiterun_choice"] = "fought_with_imperials"
            
            print("\n✓ Hadvar joins the party as an active companion!")
            print("  Imperial Legion relationship increased")
            print("  Stormcloaks view you with suspicion")
            
        elif choice == "ralof":
            # Add Ralof as active companion
            ralof_companion = {
                "npc_id": "npc_stat_ralof",
                "name": "Ralof",
                "status": "active",
                "loyalty": 60,
                "location": "With party",
                "recruitment_trigger": "Fought together at Battle of Whiterun",
                "faction_affinity": "stormcloaks",
                "notes": "Rallied to assault Whiterun together. Passionate Stormcloak warrior."
            }
            
            if "companions" not in state:
                state["companions"] = {
                    "active_companions": [],
                    "available_companions": [],
                    "dismissed_companions": []
                }
            
            # Remove from available if present
            state["companions"]["available_companions"] = [
                c for c in state["companions"].get("available_companions", [])
                if c.get("name") != "Ralof"
            ]
            
            # Add to active
            state["companions"]["active_companions"].append(ralof_companion)
            
            # Update faction relationships
            if "civil_war_state" in state:
                state["civil_war_state"]["player_alliance"] = "stormcloak"
                state["civil_war_state"]["faction_relationship"]["stormcloaks"] += 30
                state["civil_war_state"]["faction_relationship"]["imperial_legion"] -= 20
            
            # Record decision
            state["branching_decisions"]["civil_war_entry_contact"] = "Ralof"
            state["branching_decisions"]["battle_of_whiterun_choice"] = "fought_with_stormcloaks"
            
            print("\n✓ Ralof joins the party as an active companion!")
            print("  Stormcloaks relationship increased")
            print("  Imperial Legion views you with suspicion")
        
        # Save updated state
        self.save_campaign_state(state)
        return state
    
    def generate_wilderness_encounter(self, hold_name, act="Act 1", difficulty="moderate"):
        """
        Generate a wilderness encounter based on hold and act
        
        Args:
            hold_name: Name of the hold (e.g., 'Eastmarch', 'The Rift')
            act: Current act of the campaign
            difficulty: Encounter difficulty ('easy', 'moderate', 'hard', 'boss')
        
        Returns:
            Complete encounter with enemies and setup
        """
        import random
        
        # Get enemies appropriate for this hold
        hold_enemies = self.query_manager.get_enemies_by_hold(hold_name)
        
        # Get enemies appropriate for this act
        act_enemies = self.query_manager.get_enemies_by_act(act)
        
        # Find overlap (enemies that fit both hold and act)
        suitable_enemies = []
        act_enemy_ids = [e.get('id') for e in act_enemies]
        
        for enemy in hold_enemies.get('primary', []):
            if enemy.get('id') in act_enemy_ids:
                suitable_enemies.append({'enemy': enemy, 'rarity': 'common'})
        
        for enemy in hold_enemies.get('contested', []):
            if enemy.get('id') in act_enemy_ids:
                suitable_enemies.append({'enemy': enemy, 'rarity': 'uncommon'})
        
        for enemy in hold_enemies.get('rare', []):
            if enemy.get('id') in act_enemy_ids:
                suitable_enemies.append({'enemy': enemy, 'rarity': 'rare'})
        
        if not suitable_enemies:
            return {"error": f"No suitable enemies found for {hold_name} in {act}"}
        
        # Select enemies based on difficulty
        encounter_enemies = []
        if difficulty == "easy":
            # 1-2 common enemies
            count = random.randint(1, 2)
            common = [e for e in suitable_enemies if e['rarity'] == 'common']
            if common:
                encounter_enemies = random.sample(common, min(count, len(common)))
        elif difficulty == "moderate":
            # 2-4 enemies, mix of common and uncommon
            count = random.randint(2, 4)
            non_rare = [e for e in suitable_enemies if e['rarity'] != 'rare']
            if non_rare:
                encounter_enemies = random.sample(non_rare, min(count, len(non_rare)))
        elif difficulty == "hard":
            # 3-5 enemies including uncommon/rare
            count = random.randint(3, 5)
            encounter_enemies = random.sample(suitable_enemies, min(count, len(suitable_enemies)))
        elif difficulty == "boss":
            # 1 boss-level enemy or rare enemy with minions
            rare_enemies = [e for e in suitable_enemies if e['rarity'] == 'rare' or 
                           'boss' in e['enemy'].get('id', '').lower()]
            if rare_enemies:
                encounter_enemies = [random.choice(rare_enemies)]
                # Add some minions
                common = [e for e in suitable_enemies if e['rarity'] == 'common']
                if common:
                    minion_count = random.randint(1, 2)
                    encounter_enemies.extend(random.sample(common, min(minion_count, len(common))))
        
        # Build encounter description
        encounter = {
            'hold': hold_name,
            'act': act,
            'difficulty': difficulty,
            'enemies': [e['enemy'] for e in encounter_enemies],
            'rarity_levels': [e['rarity'] for e in encounter_enemies],
            'setup': self._generate_encounter_setup(hold_name, encounter_enemies),
            'mechanical_notes': [
                f"Encounter difficulty: {difficulty}",
                "Use appropriate terrain aspects for the hold",
                "Consider weather and time of day",
                "Enemies may flee if outmatched or call for reinforcements"
            ]
        }
        
        return encounter
    
    def _generate_encounter_setup(self, hold_name, enemy_data):
        """Generate narrative setup for wilderness encounter"""
        if not enemy_data:
            return "A quiet wilderness area..."
        
        # Safely extract enemy names
        enemy_types = []
        for e in enemy_data:
            if isinstance(e, dict) and 'enemy' in e:
                enemy_types.append(e['enemy'].get('name', 'Unknown Enemy'))
            else:
                enemy_types.append('Unknown Enemy')
        
        setups = {
            'Eastmarch': f"In the cold tundra of Eastmarch, the party encounters {', '.join(enemy_types)}",
            'The Rift': f"Among the autumn forests of The Rift, {', '.join(enemy_types)} appear",
            'Whiterun': f"On the open plains near Whiterun, {', '.join(enemy_types)} emerge",
            'Falkreath': f"Deep in Falkreath's dark woods, {', '.join(enemy_types)} lurk",
            'The Reach': f"In the mountainous Reach, {', '.join(enemy_types)} ambush the party"
        }
        
        return setups.get(hold_name, 
            f"In the wilderness of {hold_name}, the party encounters {', '.join(enemy_types)}")
    
    def get_available_faction_quests(self, faction_id, act=None):
        """
        Get available faction quests based on current progress
        
        Args:
            faction_id: ID of the faction
            act: Optional act filter
        
        Returns:
            List of available quests
        """
        # Get faction quest status
        faction_status = self.get_faction_status(faction_id)
        if 'error' in faction_status:
            # No quests started yet, return first quest
            faction_status = {'completed_quests': [], 'active_quests': []}
        
        completed = faction_status.get('completed_quests', [])
        active = faction_status.get('active_quests', [])
        
        # Query all faction quests
        all_quests = self.query_manager.query_faction_quests(faction_id=faction_id, act=act)
        
        if not all_quests or faction_id not in all_quests:
            return []
        
        available = []
        quests = all_quests[faction_id].get('quests', [])
        
        for i, quest in enumerate(quests):
            quest_id = quest['id']
            
            # Skip if already completed or active
            if quest_id in completed or quest_id in active:
                continue
            
            # First quest is always available
            if i == 0:
                available.append(quest)
            # Other quests require previous quest to be completed
            elif i > 0 and quests[i-1]['id'] in completed:
                available.append(quest)
        
        return available
    
    def get_current_act_number(self):
        """Get current Act as integer (1, 2, or 3)"""
        state = self.load_campaign_state()
        if not state:
            return 1
        return state.get('current_act', 1)
    
    def advance_to_next_act(self, act_number):
        """
        Advance campaign to specified Act
        
        Args:
            act_number: 1, 2, or 3
        """
        state = self.load_campaign_state()
        if not state:
            return False
        
        state['current_act'] = act_number
        print(f"\n{'='*50}")
        print(f"Campaign advanced to Act {act_number}")
        print(f"{'='*50}\n")
        
        # Add act transition to story arcs
        if 'active_story_arcs' in state:
            for arc in state['active_story_arcs']:
                arc['progress'] = max(arc['progress'], (act_number - 1) * 3)
        
        self.save_campaign_state(state)
        return True
    
    def get_act_appropriate_quests(self, act=None):
        """
        Get quests appropriate for the current or specified Act
        
        Args:
            act: "Act I", "Act II", or "Act III" (or None for current)
        """
        if act is None:
            act_number = self.get_current_act_number()
            act = f"Act {['I', 'II', 'III'][act_number - 1]}"
        
        main_quests_data = self.load_main_quests()
        if not main_quests_data:
            return []
        
        quests = main_quests_data.get('main_questline', {}).get('quests', [])
        act_quests = [q for q in quests if q.get('act') == act]
        
        return act_quests
    
    def load_clocks(self, clock_type="all"):
        """
        Load clock data from clock JSON files
        
        Args:
            clock_type: "civil_war", "thalmor", "faction_trust", or "all"
        """
        clocks_dir = self.data_dir / "clocks"
        clocks = {}
        
        if clock_type in ["civil_war", "all"]:
            civil_war_path = clocks_dir / "civil_war_clocks.json"
            if civil_war_path.exists():
                with open(civil_war_path, 'r') as f:
                    clocks['civil_war'] = json.load(f)
        
        if clock_type in ["thalmor", "all"]:
            thalmor_path = clocks_dir / "thalmor_influence_clocks.json"
            if thalmor_path.exists():
                with open(thalmor_path, 'r') as f:
                    clocks['thalmor'] = json.load(f)
        
        if clock_type in ["faction_trust", "all"]:
            trust_path = clocks_dir / "faction_trust_clocks.json"
            if trust_path.exists():
                with open(trust_path, 'r') as f:
                    clocks['faction_trust'] = json.load(f)
        
        return clocks
    
    def advance_clock(self, clock_category, clock_name, segments=1):
        """
        Advance a specific clock by given segments
        
        Args:
            clock_category: "civil_war", "thalmor", or "faction_trust"
            clock_name: Name of the specific clock
            segments: Number of segments to advance (can be negative for setbacks)
        """
        clocks_dir = self.data_dir / "clocks"
        
        # Map category to file
        file_map = {
            "civil_war": "civil_war_clocks.json",
            "thalmor": "thalmor_influence_clocks.json",
            "faction_trust": "faction_trust_clocks.json"
        }
        
        if clock_category not in file_map:
            print(f"Error: Unknown clock category: {clock_category}")
            return False
        
        file_path = clocks_dir / file_map[clock_category]
        if not file_path.exists():
            print(f"Error: Clock file not found: {file_path}")
            return False
        
        # Load clocks
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Find and update the clock
        if clock_category == "civil_war":
            clocks = data.get('civil_war_clocks', {}).get('clocks', {})
        elif clock_category == "thalmor":
            clocks = data.get('thalmor_influence_clocks', {}).get('clocks', {})
        elif clock_category == "faction_trust":
            clocks = data.get('faction_trust_clocks', {}).get('clocks', {})
        
        if clock_name not in clocks:
            print(f"Error: Clock not found: {clock_name}")
            print(f"Available clocks: {', '.join(clocks.keys())}")
            return False
        
        clock = clocks[clock_name]
        old_progress = clock['current_progress'] if 'current_progress' in clock else clock.get('current_trust', 0)
        max_value = clock['total_segments'] if 'total_segments' in clock else clock.get('max_trust', 10)
        
        # Update progress
        if 'current_progress' in clock:
            clock['current_progress'] = max(0, min(max_value, clock['current_progress'] + segments))
            new_progress = clock['current_progress']
        elif 'current_trust' in clock:
            clock['current_trust'] = max(0, min(max_value, clock['current_trust'] + segments))
            new_progress = clock['current_trust']
        
        # Update last_updated timestamp
        if clock_category in ["civil_war", "thalmor"]:
            data[f'{clock_category}_clocks']['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save updated clocks
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n{'='*50}")
        print(f"Clock Updated: {clock_name}")
        print(f"Progress: {old_progress} -> {new_progress} / {max_value}")
        if new_progress >= max_value:
            print(f"⚠️  CLOCK FILLED! Effect: {clock.get('completion_effect', 'See clock data')}")
        print(f"{'='*50}\n")
        
        return True
    
    def advance_whiterun_jobs_clock(self, clock_name, segments=1):
        """
        Advance a Whiterun jobs clock with gating support
        
        Args:
            clock_name: Name of the specific clock (e.g., 'guild_foothold_whiterun')
            segments: Number of segments to advance
        """
        clocks_dir = self.data_dir / "clocks"
        file_path = clocks_dir / "whiterun_jobs.json"
        
        if not file_path.exists():
            print(f"Error: whiterun_jobs.json not found at {file_path}")
            return False
        
        # Load clocks
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        clocks = data.get('whiterun_jobs', {}).get('clocks', {})
        
        if clock_name not in clocks:
            print(f"Error: Clock not found: {clock_name}")
            return False
        
        clock = clocks[clock_name]
        old_progress = clock.get('current', 0)
        max_value = clock.get('max', 10)
        new_progress = old_progress + segments
        
        # Check for gating
        if 'gate' in clock:
            gate = clock['gate']
            cap = gate.get('cap_until_condition_met', max_value)
            
            if new_progress >= cap:
                # Load campaign state to check condition
                campaign_state = self.load_campaign_state()
                condition = gate.get('condition', '')
                
                # Simple condition evaluation for whiterun control or imperial alliance
                condition_met = False
                if campaign_state:
                    civil_war = campaign_state.get('civil_war_state', {})
                    whiterun_control = civil_war.get('whiterun_control', None)
                    player_alliance = civil_war.get('player_alliance', 'neutral')
                    
                    # Check if condition mentions imperial control or alliance
                    if 'imperial' in condition.lower():
                        if whiterun_control == 'imperial' or player_alliance == 'imperial':
                            condition_met = True
                
                if not condition_met:
                    print(f"\n{'='*50}")
                    print(f"⚠️  Foothold stalled: requires Imperial control or Imperial alliance.")
                    print(f"Clock: {clock_name}")
                    print(f"Progress capped at: {cap}/{max_value}")
                    print(f"Gate note: {gate.get('note', 'N/A')}")
                    print(f"{'='*50}\n")
                    # Don't advance beyond cap
                    new_progress = min(new_progress, cap)
        
        # Update progress
        clock['current'] = max(0, min(max_value, new_progress))
        
        # Update timestamp
        data['whiterun_jobs']['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save updated clocks
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n{'='*50}")
        print(f"Clock Updated: {clock_name}")
        print(f"Progress: {old_progress} -> {clock['current']} / {max_value}")
        if clock['current'] >= max_value:
            print(f"⚠️  CLOCK FILLED! Effect: {clock.get('completion_effect', 'See clock data')}")
        print(f"{'='*50}\n")
        
        return True
    
    def get_story_hooks_for_quest(self, quest_id):
        """Get story hooks and GM notes for a specific quest"""
        main_quests_data = self.load_main_quests()
        if not main_quests_data:
            return None
        
        quests = main_quests_data.get('main_questline', {}).get('quests', [])
        for quest in quests:
            if quest.get('id') == quest_id:
                return {
                    'quest_name': quest.get('name'),
                    'act': quest.get('act'),
                    'story_hooks': quest.get('story_hooks', []),
                    'gm_notes': quest.get('gm_notes', ''),
                    'faction_dynamics': quest.get('faction_dynamics', {}),
                    'act_transition': quest.get('act_transition')
                }
        
        return None
    
    def integrate_quest_with_clocks(self, quest_id):
        """
        Show how a quest integrates with current clock states
        Provides GM with context on clock advancement opportunities
        """
        quest_info = self.get_story_hooks_for_quest(quest_id)
        if not quest_info:
            print(f"Quest not found: {quest_id}")
            return None
        
        print(f"\n{'='*60}")
        print(f"Quest: {quest_info['quest_name']} ({quest_info['act']})")
        print(f"{'='*60}\n")
        
        print("Story Hooks:")
        for hook in quest_info['story_hooks']:
            print(f"  • {hook}")
        
        if quest_info['gm_notes']:
            print(f"\nGM Notes: {quest_info['gm_notes']}")
        
        if quest_info['faction_dynamics']:
            print("\nFaction Dynamics:")
            for faction, dynamic in quest_info['faction_dynamics'].items():
                print(f"  • {faction}: {dynamic}")
        
        # Show relevant clocks
        clocks = self.load_clocks("all")
        
        print("\n" + "="*60)
        print("Relevant Clock Advancement Opportunities:")
        print("="*60)
        
        # Civil war clocks if quest involves civil war
        if 'whiterun' in quest_id or 'civil' in quest_info['quest_name'].lower():
            if 'civil_war' in clocks:
                cw_clocks = clocks['civil_war'].get('civil_war_clocks', {}).get('clocks', {})
                print("\nCivil War Clocks:")
                for clock_name, clock_data in cw_clocks.items():
                    progress = clock_data.get('current_progress', 0)
                    total = clock_data.get('total_segments', 10)
                    print(f"  • {clock_name}: {progress}/{total}")
        
        # Thalmor clocks if quest involves Thalmor
        if 'thalmor' in quest_id or 'diplomatic' in quest_id or 'embassy' in quest_info['quest_name'].lower():
            if 'thalmor' in clocks:
                th_clocks = clocks['thalmor'].get('thalmor_influence_clocks', {}).get('clocks', {})
                print("\nThalmor Influence Clocks:")
                for clock_name, clock_data in th_clocks.items():
                    progress = clock_data.get('current_progress', 0)
                    total = clock_data.get('total_segments', 10)
                    print(f"  • {clock_name}: {progress}/{total}")
        
        # Faction trust
        if quest_info['faction_dynamics']:
            if 'faction_trust' in clocks:
                ft_clocks = clocks['faction_trust'].get('faction_trust_clocks', {}).get('clocks', {})
                print("\nFaction Trust (affected by this quest):")
                for faction in quest_info['faction_dynamics'].keys():
                    for clock_name, clock_data in ft_clocks.items():
                        if faction.lower() in clock_name.lower():
                            trust = clock_data.get('current_trust', 0)
                            max_trust = clock_data.get('max_trust', 10)
                            print(f"  • {clock_name}: {trust}/{max_trust}")
        
        print("\n" + "="*60 + "\n")
        
        return quest_info
    
    def initiate_dragonbreak(self, fracture_name, description, trigger_event):
        """
        Initiate a timeline fracture (Dragonbreak) for parallel story paths
        
        Args:
            fracture_name: Name of the timeline fracture
            description: Description of what caused the fracture
            trigger_event: The event that triggered this fracture
        
        Returns:
            The ID of the new timeline branch, or None if Dragonbreak is unavailable
        """
        if not self.dragonbreak_manager:
            print("Warning: Dragonbreak Manager not available")
            return None
        
        branch_id = self.dragonbreak_manager.create_timeline_fracture(
            fracture_name, description, trigger_event
        )
        
        # Record this in campaign state
        state = self.load_campaign_state()
        if state:
            if 'dragonbreak_events' not in state:
                state['dragonbreak_events'] = []
            
            state['dragonbreak_events'].append({
                'branch_id': branch_id,
                'name': fracture_name,
                'trigger': trigger_event,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.save_campaign_state(state)
        
        return branch_id
    
    def track_parallel_event(self, event_type, event_data, branch_mapping):
        """
        Track an event that has different outcomes across timeline branches
        
        Args:
            event_type: Type of event ('npc', 'faction', 'quest', 'world_state')
            event_data: Core data about the event (id, name)
            branch_mapping: Dict mapping branch_id to outcome in that branch
        """
        if not self.dragonbreak_manager:
            print("Warning: Dragonbreak Manager not available")
            return False
        
        if event_type == 'npc':
            self.dragonbreak_manager.track_npc_across_branches(
                event_data['id'], event_data['name'], branch_mapping
            )
        elif event_type == 'faction':
            self.dragonbreak_manager.track_faction_across_branches(
                event_data['id'], event_data['name'], branch_mapping
            )
        elif event_type == 'quest':
            self.dragonbreak_manager.track_quest_across_branches(
                event_data['id'], event_data['name'], branch_mapping
            )
        
        return True
    
    def handle_branching_decision_with_dragonbreak(self, decision_key, choices_dict):
        """
        Handle a major branching decision by creating parallel timelines
        
        Args:
            decision_key: Key for the decision (e.g., 'civil_war_alliance')
            choices_dict: Dict of choice -> outcome mapping
                         e.g., {'imperial': {...}, 'stormcloak': {...}}
        
        Returns:
            Dict mapping choice to timeline branch
        """
        if not self.dragonbreak_manager:
            print("Warning: Dragonbreak Manager not available, using standard branching")
            return {}
        
        branches = {}
        
        # Create a timeline branch for each choice
        for choice, outcome in choices_dict.items():
            branch_id = self.dragonbreak_manager.create_timeline_fracture(
                f"{decision_key}_{choice}",
                f"Timeline where player chose: {choice}",
                decision_key
            )
            branches[choice] = branch_id
            
            # Define consequences for this branch
            if 'consequences' in outcome:
                for cons_type, cons_data in outcome['consequences'].items():
                    self.dragonbreak_manager.define_branch_consequence(
                        branch_id, cons_type, cons_data
                    )
        
        return branches
    
    def get_active_timeline_state(self):
        """
        Get the state of the currently active timeline branch
        
        Returns:
            Timeline state dict or None
        """
        if not self.dragonbreak_manager:
            return None
        
        return self.dragonbreak_manager.get_timeline_state()


def main():
    """Main function for testing"""
    manager = StoryManager()
    
    print("Skyrim Story Manager")
    print("====================\n")
    
    # Display menu
    print("1. View Campaign Summary")
    print("2. Record Branching Decision")
    print("3. Update Civil War State")
    print("4. Update Main Quest State")
    print("5. Update Thalmor Arc")
    print("6. Check Available Quests")
    print("7. Advance Quest")
    print("8. Check Story Arcs")
    print("9. Get Scene NPCs")
    print("10. Trigger Scene Event")
    print("11. Apply Combat Consequences")
    print("12. Track Faction Quest Progress")
    print("13. Generate Wilderness Encounter")
    print("14. Get Available Faction Quests")
    print("15. Exit")
    
    while True:
        choice = input("\nEnter choice (1-15): ").strip()
        
        if choice == "1":
            print(manager.generate_story_summary())
        
        elif choice == "2":
            decision_key = input("Decision key (e.g., 'civil_war_entry_contact'): ").strip()
            decision_value = input("Choice made: ").strip()
            manager.record_branching_decision(decision_key, decision_value)
        
        elif choice == "3":
            alliance = input("Alliance (imperial/stormcloak/neutral): ").strip()
            manager.update_civil_war_state(alliance=alliance if alliance != 'neutral' else None)
        
        elif choice == "4":
            print("Update main quest (enter key=value, e.g., 'civil_war_involvement=true')")
            update = input("Update: ").strip()
            if '=' in update:
                key, value = update.split('=', 1)
                # Parse value
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
                manager.update_main_quest_state(**{key: value})
        
        elif choice == "5":
            plot_id = input("Thalmor plot ID: ").strip()
            progress = input("Progress change (+/-): ").strip()
            discovery = input("Discovery (or blank): ").strip()
            manager.update_thalmor_arc(
                plot_id, 
                int(progress) if progress else 0,
                discovery if discovery else None
            )
        
        elif choice == "6":
            quests = manager.get_available_quests()
            print(f"\nAvailable Quests: {len(quests)}")
            for q in quests:
                print(f"- [{q['type']}] {q['quest']['name']}")
        
        elif choice == "7":
            quest_id = input("Quest ID: ").strip()
            status = input("New status (available/active/completed/failed): ").strip()
            manager.advance_quest(quest_id, status)
        
        elif choice == "8":
            manager.check_story_arcs()
        
        elif choice == "9":
            location = input("Location: ").strip()
            scene_type = input("Scene type (combat/dialogue/exploration): ").strip()
            npcs = manager.get_scene_npcs(location, scene_type)
            print(f"\nScene NPCs for {location}:")
            print(f"Friendly NPCs: {len(npcs['friendly'])}")
            for npc in npcs['friendly']:
                print(f"  - {npc['name']}")
            print(f"Hostile NPCs: {len(npcs['hostile'])}")
            for npc in npcs['hostile']:
                print(f"  - {npc['name']}")
            print(f"Enemies: {len(npcs['enemies'])}")
            for enemy in npcs['enemies']:
                print(f"  - {enemy['name']}")
            if npcs['suggestions']:
                print("Suggestions:")
                for suggestion in npcs['suggestions']:
                    print(f"  - {suggestion}")
        
        elif choice == "10":
            location = input("Scene location: ").strip()
            scene_type = input("Scene type (combat/dialogue/exploration): ").strip()
            scene_data = {
                'location': location,
                'type': scene_type
            }
            scene_setup = manager.trigger_scene_event(scene_data)
            print(f"\n=== Scene Setup ===")
            print(f"Location: {scene_setup['location']}")
            print(f"Type: {scene_setup['type']}")
            print(f"Description: {scene_setup['description']}")
            print(f"\nAvailable NPCs:")
            print(f"  Friendly: {len(scene_setup['npcs']['friendly'])}")
            print(f"  Hostile: {len(scene_setup['npcs']['hostile'])}")
            print(f"  Enemies: {len(scene_setup['npcs']['enemies'])}")
            if scene_setup['mechanical_notes']:
                print("\nMechanical Notes:")
                for note in scene_setup['mechanical_notes']:
                    print(f"  - {note}")
            if scene_setup.get("pc_compel_hooks"):
                print("\nPC Compel Hooks:")
                for c in scene_setup["pc_compel_hooks"]:
                    if isinstance(c, dict):
                        title = c.get("title", c.get("id", "Compel"))
                        when = c.get("when", "")
                        print(f"  - {title}: {when}")
        
        elif choice == "11":
            enemy_type = input("Enemy type (dragon/thalmor/bandit/etc): ").strip()
            outcome = input("Outcome (victory/defeat/fled): ").strip()
            consequences = manager.apply_combat_consequences(enemy_type, outcome)
            print(f"\n=== Combat Consequences ===")
            if consequences.get('faction_changes'):
                print("Faction Changes:")
                for change in consequences['faction_changes']:
                    print(f"  - {change}")
            if consequences.get('world_updates'):
                print("World Updates:")
                for update in consequences['world_updates']:
                    print(f"  - {update}")
            if consequences.get('quest_triggers'):
                print("Quest Triggers:")
                for trigger in consequences['quest_triggers']:
                    print(f"  - {trigger}")
        
        elif choice == "12":
            faction_id = input("Faction ID (companions/thieves_guild/etc): ").strip()
            quest_id = input("Quest ID: ").strip()
            status = input("Status (started/completed/failed): ").strip()
            trust = input("Trust change (+/-): ").strip()
            result = manager.track_faction_quest_progress(
                faction_id, quest_id, status, 
                int(trust) if trust else 0
            )
            print(f"Result: {result}")
        
        elif choice == "13":
            hold = input("Hold name (e.g., Eastmarch, The Rift): ").strip()
            act = input("Act (Act 1/Act 2/Act 3): ").strip()
            difficulty = input("Difficulty (easy/moderate/hard/boss): ").strip()
            encounter = manager.generate_wilderness_encounter(hold, act, difficulty)
            if 'error' in encounter:
                print(f"Error: {encounter['error']}")
            else:
                print(f"\n=== Wilderness Encounter ===")
                print(f"Hold: {encounter['hold']}")
                print(f"Difficulty: {encounter['difficulty']}")
                print(f"Setup: {encounter['setup']}")
                print(f"\nEnemies:")
                for i, enemy in enumerate(encounter['enemies']):
                    rarity = encounter['rarity_levels'][i]
                    print(f"  [{rarity}] {enemy['name']} - {enemy['type']}")
        
        elif choice == "14":
            faction_id = input("Faction ID: ").strip()
            act = input("Act filter (optional): ").strip()
            available = manager.get_available_faction_quests(
                faction_id, act if act else None
            )
            print(f"\nAvailable quests for {faction_id}:")
            for quest in available:
                print(f"  [{quest['id']}] {quest['name']}")
                print(f"    {quest['description']}")
        
        elif choice == "15":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-15.")


if __name__ == "__main__":
    main()
