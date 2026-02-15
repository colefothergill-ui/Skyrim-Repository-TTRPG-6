#!/usr/bin/env python3
"""
NPC Manager for Skyrim TTRPG

This script manages:
- NPC stats and abilities
- NPC loyalty and relationships
- NPC progression
- Companion management
"""

import json
import os
from pathlib import Path
from datetime import datetime

from first_impression import auto_first_impression


class NPCManager:
    def __init__(self, data_dir="../data", state_dir="../state"):
        self.data_dir = Path(data_dir)
        self.state_dir = Path(state_dir)
        self.npcs_dir = self.data_dir / "npcs"
        self.relationships_path = self.data_dir / "npc_relationships.json"
        self.campaign_state_path = self.state_dir / "campaign_state.json"
        self.faction_clocks_path = self.data_dir / "civil_war_clocks.json"
        
    def load_npc(self, npc_id):
        """Load an NPC file"""
        npc_file = self.npcs_dir / f"{npc_id}.json"
        if npc_file.exists():
            with open(npc_file, 'r') as f:
                return json.load(f)
        return None
    
    def save_npc(self, npc_data):
        """Save NPC data"""
        npc_id = npc_data.get('id')
        if not npc_id:
            print("Error: NPC must have an 'id' field")
            return False
        
        self.npcs_dir.mkdir(exist_ok=True)
        npc_file = self.npcs_dir / f"{npc_id}.json"
        
        with open(npc_file, 'w') as f:
            json.dump(npc_data, f, indent=2)
        
        print(f"Saved NPC: {npc_data.get('name', npc_id)}")
        return True
    
    def load_relationships(self):
        """Load NPC relationships data"""
        if self.relationships_path.exists():
            with open(self.relationships_path, 'r') as f:
                return json.load(f)
        return None
    
    def save_relationships(self, data):
        """Save relationships data"""
        with open(self.relationships_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def update_loyalty(self, npc_id, change, reason=""):
        """
        Update an NPC's loyalty to the party
        
        Args:
            npc_id: ID of the NPC
            change: Amount to change loyalty (+/-)
            reason: Why loyalty changed
        """
        npc = self.load_npc(npc_id)
        if not npc:
            print(f"NPC '{npc_id}' not found")
            return False
        
        # Initialize loyalty if not present
        if 'loyalty' not in npc:
            npc['loyalty'] = 50
        
        old_loyalty = npc['loyalty']
        npc['loyalty'] = max(0, min(100, npc['loyalty'] + change))
        
        print(f"\n{npc['name']} - Loyalty Update")
        print(f"Loyalty: {old_loyalty} -> {npc['loyalty']}")
        if reason:
            print(f"Reason: {reason}")
        
        # Check loyalty thresholds
        if npc['loyalty'] >= 80:
            status = "Deeply loyal - will sacrifice for party"
        elif npc['loyalty'] >= 60:
            status = "Loyal companion"
        elif npc['loyalty'] >= 40:
            status = "Questioning loyalty"
        elif npc['loyalty'] >= 20:
            status = "May refuse dangerous orders"
        else:
            status = "⚠️ At risk of leaving!"
        
        print(f"Status: {status}")
        
        # Record the change
        if 'loyalty_history' not in npc:
            npc['loyalty_history'] = []
        
        npc['loyalty_history'].append({
            'change': change,
            'reason': reason,
            'new_loyalty': npc['loyalty'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.save_npc(npc)
        return True
    
    def update_relationship(self, npc1_id, npc2_id, change, reason=""):
        """
        Update relationship between two NPCs
        
        Args:
            npc1_id: ID of first NPC
            npc2_id: ID of second NPC
            change: Amount to change relationship
            reason: Why it changed
        """
        relationships = self.load_relationships()
        if not relationships:
            print("Relationships data not found")
            return False
        
        # Find or create relationship entry
        # This is simplified - real implementation would be more complex
        print(f"\nRelationship Update: {npc1_id} <-> {npc2_id}")
        print(f"Change: {change:+d}")
        if reason:
            print(f"Reason: {reason}")
        
        # Would update the relationships.json here
        return True
    
    def check_companion_status(self, npc_id):
        """
        Check companion's current status and loyalty
        """
        npc = self.load_npc(npc_id)
        if not npc:
            return None
        
        print(f"\n{'='*60}")
        print(f"COMPANION: {npc['name']}")
        print(f"{'='*60}")
        
        # Basic info
        print(f"Role: {npc.get('type', npc.get('role', 'Unknown'))}")
        print(f"Faction: {npc.get('faction', 'None')}")
        
        # Loyalty
        loyalty = npc.get('loyalty', 50)
        print(f"\nLoyalty: {loyalty}/100")
        
        loyalty_bar = '█' * (loyalty // 5) + '░' * (20 - (loyalty // 5))
        print(f"[{loyalty_bar}]")
        
        # Stats
        if 'skills' in npc:
            print(f"\n--- Skills ---")
            for skill, value in npc['skills'].items():
                print(f"{skill}: {value}")
        
        # Equipment
        if 'equipment' in npc:
            print(f"\n--- Equipment ---")
            for item_type, items in npc['equipment'].items():
                if items:
                    print(f"{item_type}: {', '.join(items) if isinstance(items, list) else items}")
        
        # Special abilities
        if 'special_abilities' in npc:
            print(f"\n--- Special Abilities ---")
            for ability in npc['special_abilities']:
                print(f"- {ability}")
        
        # Recent loyalty changes
        if 'loyalty_history' in npc and npc['loyalty_history']:
            print(f"\n--- Recent Loyalty Changes ---")
            for entry in npc['loyalty_history'][-5:]:  # Last 5
                print(f"[{entry['timestamp']}] {entry['change']:+d}: {entry['reason']}")
        
        return npc
    
    def create_npc_template(self, name, role, faction=None):
        """
        Create a basic NPC template
        
        Args:
            name: NPC name
            role: NPC role (companion, quest_giver, vendor, etc.)
            faction: Associated faction
        """
        import re
        
        # Create ID from name
        npc_id = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
        npc_id = re.sub(r'_+', '_', npc_id).strip('_')
        
        npc = {
            "id": npc_id,
            "name": name,
            "role": role,
            "faction": faction,
            "level": 1,
            "race": "Nord",
            "class": "Warrior",
            "aspects": {
                "high_concept": f"{role}",
                "trouble": "[To be defined]",
                "aspect_3": "[To be defined]"
            },
            "skills": {
                "Great (+4)": [],
                "Good (+3)": [],
                "Fair (+2)": [],
                "Average (+1)": []
            },
            "stress": {
                "physical": [False, False],
                "mental": [False, False]
            },
            "consequences": {
                "mild": None,
                "moderate": None,
                "severe": None
            },
            "equipment": {
                "weapons": [],
                "armor": [],
                "items": []
            },
            "personality": "[To be defined]",
            "goals": [],
            "relationships": {},
            "loyalty": 50,
            "notes": f"Created: {datetime.now().strftime('%Y-%m-%d')}"
        }
        
        self.save_npc(npc)
        print(f"Created NPC template: {name} ({npc_id})")
        return npc
    
    def list_npcs(self):
        """List all NPCs in the system"""
        if not self.npcs_dir.exists():
            print("No NPCs directory found")
            return []
        
        npc_files = list(self.npcs_dir.glob("*.json"))
        
        print(f"\n=== NPCs ({len(npc_files)}) ===\n")
        
        npcs = []
        for npc_file in sorted(npc_files):
            with open(npc_file, 'r') as f:
                npc = json.load(f)
                print(f"{npc['id']}: {npc['name']}")
                print(f"  Role: {npc.get('role', 'Unknown')}")
                if 'loyalty' in npc:
                    print(f"  Loyalty: {npc['loyalty']}/100")
                print()
                npcs.append((npc['id'], npc['name']))
        
        return npcs
    
    def companion_loyalty_check(self, npc_id, situation):
        """
        Check if companion will follow through in a difficult situation
        
        Args:
            npc_id: ID of the companion
            situation: Description of the situation
        
        Returns:
            Boolean indicating if companion will comply
        """
        npc = self.load_npc(npc_id)
        if not npc:
            return False
        
        loyalty = npc.get('loyalty', 50)
        
        print(f"\n{npc['name']} - Loyalty Check")
        print(f"Situation: {situation}")
        print(f"Current Loyalty: {loyalty}/100")
        
        # Simple threshold check
        if loyalty >= 80:
            result = "Will follow without question"
            will_comply = True
        elif loyalty >= 60:
            result = "Will follow orders"
            will_comply = True
        elif loyalty >= 40:
            result = "May hesitate or question"
            will_comply = True
        elif loyalty >= 20:
            result = "Likely to refuse dangerous/immoral orders"
            will_comply = False
        else:
            result = "Will refuse and may leave"
            will_comply = False
        
        print(f"Result: {result}")
        return will_comply
    
    def load_campaign_state(self):
        """Load campaign state data"""
        if self.campaign_state_path.exists():
            with open(self.campaign_state_path, 'r') as f:
                return json.load(f)
        return None
    
    def save_campaign_state(self, state):
        """Save campaign state data"""
        self.state_dir.mkdir(exist_ok=True)
        with open(self.campaign_state_path, 'w') as f:
            json.dump(state, f, indent=2)
        return True
    
    def get_active_companions(self):
        """Get list of currently active companions"""
        state = self.load_campaign_state()
        if state and 'companions' in state:
            return state['companions'].get('active_companions', [])
        return []
    
    def get_available_companions(self):
        """Get list of available companions that can be recruited"""
        state = self.load_campaign_state()
        if state and 'companions' in state:
            return state['companions'].get('available_companions', [])
        return []
    
    def recruit_companion(self, npc_id):
        """
        Recruit a companion to the active party
        
        Args:
            npc_id: ID of the NPC to recruit
            
        Returns:
            Boolean indicating success
        """
        state = self.load_campaign_state()
        if not state:
            print("Could not load campaign state")
            return False
        
        if 'companions' not in state:
            state['companions'] = {
                'active_companions': [],
                'available_companions': [],
                'dismissed_companions': [],
                'companion_relationships': {}
            }
        
        companions = state['companions']
        
        # Find companion in available list
        companion = None
        for i, comp in enumerate(companions['available_companions']):
            if comp['npc_id'] == npc_id:
                companion = comp
                companions['available_companions'].pop(i)
                break
        
        if not companion:
            print(f"Companion {npc_id} not found in available companions")
            return False
        
        # Check recruitment conditions
        if companion.get('status') == 'unavailable':
            print(f"Cannot recruit {companion['name']}: {companion.get('recruitment_condition', 'Requirements not met')}")
            return False
        
        # Check if already active
        if any(c['npc_id'] == npc_id for c in companions['active_companions']):
            print(f"{companion['name']} is already in the active party")
            return False
        
        # Move to active companions
        companion['status'] = 'active'
        companions['active_companions'].append(companion)
        
        state['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_campaign_state(state)
        
        print(f"\n✓ {companion['name']} has joined the party!")
        print(f"Loyalty: {companion.get('loyalty', 50)}/100")
        
        return True
    
    def dismiss_companion(self, npc_id):
        """
        Dismiss a companion from active party
        
        Args:
            npc_id: ID of the companion to dismiss
            
        Returns:
            Boolean indicating success
        """
        state = self.load_campaign_state()
        if not state or 'companions' not in state:
            return False
        
        companions = state['companions']
        
        # Find and remove from active companions
        companion = None
        for i, comp in enumerate(companions['active_companions']):
            if comp['npc_id'] == npc_id:
                companion = comp
                companions['active_companions'].pop(i)
                break
        
        if not companion:
            print(f"Companion {npc_id} not found in active companions")
            return False
        
        # Move to dismissed companions
        companion['status'] = 'dismissed'
        companions['dismissed_companions'].append(companion)
        
        state['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_campaign_state(state)
        
        print(f"\n{companion['name']} has been dismissed and returned to {companion.get('location', 'their home')}")
        
        return True
    
    def check_faction_alignment(self, npc_id, faction):
        """
        Check NPC's alignment with a specific faction
        
        Args:
            npc_id: ID of the NPC
            faction: Faction name to check
            
        Returns:
            String: 'allied', 'neutral', 'hostile', or 'unknown'
        """
        npc = self.load_npc(npc_id)
        if not npc:
            return 'unknown'
        
        npc_faction = npc.get('faction', '').lower()
        faction = faction.lower()
        
        # Check direct faction membership
        if npc_faction == faction:
            return 'allied'
        
        # Check relationships
        relationships = npc.get('relationships', {})
        for entity, relation in relationships.items():
            if entity.lower() == faction or faction in entity.lower():
                relation_lower = relation.lower()
                if any(word in relation_lower for word in ['ally', 'friend', 'loyal', 'trust']):
                    return 'allied'
                elif any(word in relation_lower for word in ['enemy', 'hostile', 'hate', 'rival']):
                    return 'hostile'
        
        # Check faction affinity for companions
        if 'companion_status' in npc:
            faction_affinity = npc.get('companion_status', {}).get('faction_affinity', '')
            if faction_affinity.lower() == faction:
                return 'allied'
        
        return 'unknown'
    
    def process_decision_point(self, npc_id, decision_key, chosen_option):
        """
        Process an NPC decision point based on player choice.
        
        This method handles branching narrative decisions for NPCs, applying consequences
        such as loyalty changes, relationship modifications, quest triggers, and unlocking
        new story paths. Decision points are defined in the NPC's JSON data under the
        'decision_points' key.
        
        Args:
            npc_id: ID of the NPC (e.g., 'general_tullius', 'ulfric_stormcloak')
            decision_key: Key identifying the decision point (e.g., 'civil_war_choice')
            chosen_option: Option chosen by player (e.g., 'imperial', 'stormcloak')
            
        Returns:
            Dict containing:
                - success: Boolean indicating if decision was processed
                - npc_name: Name of the NPC
                - decision: The decision key processed
                - option: The option chosen
                - consequences: Dict of consequences applied
                - loyalty_change: Loyalty change amount (if any)
                - new_relationship: Updated relationship status (if any)
                - unlocked: New content unlocked (if any)
                
        Example:
            result = manager.process_decision_point(
                'general_tullius', 'civil_war_choice', 'imperial'
            )
            print(f"Loyalty changed by: {result.get('loyalty_change', 0)}")
        """
        npc = self.load_npc(npc_id)
        if not npc:
            return {'success': False, 'message': 'NPC not found'}
        
        decision_points = npc.get('decision_points', {})
        if decision_key not in decision_points:
            return {'success': False, 'message': 'Decision point not found'}
        
        decision = decision_points[decision_key]
        
        # Check if condition is met (simplified - would need more complex logic)
        if 'condition' in decision:
            print(f"Decision condition: {decision['condition']}")
        
        # Get consequences for chosen option
        consequences = decision.get('consequences', {}).get(chosen_option, {})
        if not consequences and chosen_option in decision.get('options', []):
            # Option exists but no consequences defined
            consequences = {'message': f"Chose {chosen_option}"}
        
        result = {
            'success': True,
            'npc_name': npc['name'],
            'decision': decision_key,
            'option': chosen_option,
            'consequences': consequences
        }
        
        # Apply loyalty changes
        loyalty_change = consequences.get('loyalty_change', 0)
        if loyalty_change != 0:
            self.update_loyalty(npc_id, loyalty_change, f"Decision: {decision_key} - {chosen_option}")
            result['loyalty_change'] = loyalty_change
        
        # Handle relationship changes
        if 'relationship_change' in consequences:
            new_relationship = consequences['relationship_change']
            print(f"\nRelationship with {npc['name']} changed to: {new_relationship}")
            result['new_relationship'] = new_relationship
        
        # Handle quest triggers
        if 'unlocks' in consequences:
            print(f"\nUnlocked: {consequences['unlocks']}")
            result['unlocked'] = consequences['unlocks']
        
        # Print result
        print(f"\n{'='*60}")
        print(f"DECISION POINT: {decision_key}")
        print(f"NPC: {npc['name']}")
        print(f"Chosen: {chosen_option}")
        if 'note' in consequences:
            print(f"Note: {consequences['note']}")
        print(f"{'='*60}")
        
        return result
    
    def handle_dialogue_interaction(self, npc_id, dialogue_key, response_option=None):
        """
        Handle a dialogue tree interaction with an NPC.
        
        This method manages branching dialogue conversations with NPCs. On the first call
        (without response_option), it displays the dialogue text and available responses.
        On the second call (with response_option), it processes the player's choice,
        applies consequences (loyalty changes, quest triggers), and follows to the next
        dialogue node if specified.
        
        Dialogue trees are defined in the NPC's JSON data under 'dialogue_trees' key.
        
        Args:
            npc_id: ID of the NPC (e.g., 'ulfric_stormcloak', 'lydia')
            dialogue_key: Key identifying the dialogue node (e.g., 'initial_meeting', 'greeting')
            response_option: (Optional) Player's response choice - can be:
                - int: Zero-based index of response (e.g., 0 for first option)
                - str: Exact text of response option
                - None: Display dialogue and available responses without processing
            
        Returns:
            Dict containing:
                - success: Boolean indicating if dialogue was processed
                - npc_name: Name of the NPC
                - dialogue_key: The dialogue node accessed
                - dialogue_text: The NPC's dialogue text
                - responses: List of available response options (if response_option is None)
                - loyalty_change: Loyalty change from response (if any)
                - quest_triggered: Quest ID activated (if any)
                - relationship_change: Updated relationship (if any)
                - companion_status: Updated companion status (if any)
                - next_dialogue: Key of next dialogue node (if response leads to another)
                - next_dialogue_text: Text of next dialogue node (if applicable)
                
        Example:
            # Get dialogue and responses
            result = manager.handle_dialogue_interaction('ulfric_stormcloak', 'initial_meeting')
            for i, response in enumerate(result['responses']):
                print(f"{i}. {response['option']}")
            
            # Choose response
            result = manager.handle_dialogue_interaction('ulfric_stormcloak', 'initial_meeting', 0)
            if 'quest_triggered' in result:
                print(f"Quest started: {result['quest_triggered']}")
        """
        npc = self.load_npc(npc_id)
        if not npc:
            return {'success': False, 'message': 'NPC not found'}

        # Subtle first-impression trigger (prints once per NPC unless forced)
        try:
            repo_root = Path(__file__).resolve().parent.parent
            auto_first_impression(repo_root, npc_id=npc_id, trigger="First Impression", force=False, quiet=False)
        except Exception:
            pass
        
        dialogue_trees = npc.get('dialogue_trees', {})
        if dialogue_key not in dialogue_trees:
            return {'success': False, 'message': 'Dialogue not found'}
        
        dialogue = dialogue_trees[dialogue_key]
        
        print(f"\n{npc['name']}: {dialogue.get('greeting', dialogue.get('dialogue', ''))}")
        
        result = {
            'success': True,
            'npc_name': npc['name'],
            'dialogue_key': dialogue_key,
            'dialogue_text': dialogue.get('greeting', dialogue.get('dialogue', ''))
        }
        
        # If this dialogue has a condition, check it
        if 'condition' in dialogue:
            result['condition'] = dialogue['condition']
            print(f"[Condition: {dialogue['condition']}]")
        
        # Handle responses
        if 'responses' in dialogue and response_option is None:
            print("\nAvailable responses:")
            for i, response in enumerate(dialogue['responses'], 1):
                print(f"{i}. {response['option']}")
            result['responses'] = dialogue['responses']
            return result
        
        # Process chosen response
        if response_option is not None and 'responses' in dialogue:
            chosen_response = None
            
            # Find the response by option text or index
            if isinstance(response_option, int):
                if 0 <= response_option < len(dialogue['responses']):
                    chosen_response = dialogue['responses'][response_option]
            else:
                for response in dialogue['responses']:
                    if response['option'] == response_option:
                        chosen_response = response
                        break
            
            if not chosen_response:
                return {'success': False, 'message': f'Invalid response option: {response_option}'}
            
            if chosen_response:
                print(f"\nYou: {chosen_response['option']}")
                
                # Apply loyalty changes
                if 'loyalty_change' in chosen_response:
                    loyalty_change = chosen_response['loyalty_change']
                    self.update_loyalty(npc_id, loyalty_change, f"Dialogue: {chosen_response['option']}")
                    result['loyalty_change'] = loyalty_change
                
                # Handle quest triggers
                if 'quest_trigger' in chosen_response:
                    print(f"\n[Quest triggered: {chosen_response['quest_trigger']}]")
                    result['quest_triggered'] = chosen_response['quest_trigger']
                
                # Handle relationship changes
                if 'relationship_change' in chosen_response:
                    print(f"\n[Relationship changed: {chosen_response['relationship_change']}]")
                    result['relationship_change'] = chosen_response['relationship_change']
                
                # Handle companion status changes
                if 'companion_status' in chosen_response:
                    result['companion_status'] = chosen_response['companion_status']
                
                # Follow to next dialogue
                if 'leads_to' in chosen_response:
                    next_dialogue_key = chosen_response['leads_to']
                    result['next_dialogue'] = next_dialogue_key
                    
                    if next_dialogue_key in dialogue_trees:
                        next_dialogue = dialogue_trees[next_dialogue_key]
                        print(f"\n{npc['name']}: {next_dialogue.get('dialogue', '')}")
                        result['next_dialogue_text'] = next_dialogue.get('dialogue', '')
        
        # Handle quest activation
        if 'quest_activated' in dialogue:
            print(f"\n[Quest activated: {dialogue['quest_activated']}]")
            result['quest_activated'] = dialogue['quest_activated']
        
        # Handle faction alignment
        if 'faction_alignment' in dialogue:
            print(f"\n[Faction alignment: {dialogue['faction_alignment']}]")
            result['faction_alignment'] = dialogue['faction_alignment']
        
        return result
    
    def update_companion_based_on_faction_clock(self, faction, clock_value):
        """
        Update companion availability and loyalty based on faction clock progress.
        
        This method provides runtime integration between the faction clock system
        and companion loyalty. As factions gain or lose power (represented by clock
        values 0-10), companions aligned with or opposed to those factions will have
        their loyalty adjusted accordingly.
        
        Companions with 'allied' alignment to the faction gain loyalty when the faction
        is doing well (clock_value >= 7). Companions with 'hostile' alignment lose
        loyalty when enemy factions succeed.
        
        This creates dynamic, reactive relationships where companions care about the
        success or failure of their affiliated factions, adding depth to companion
        interactions during the civil war.
        
        Args:
            faction: Faction name (e.g., 'imperial_legion', 'stormcloaks', 'thalmor')
            clock_value: Current faction clock value on 0-10 scale, where:
                - 0-3: Faction struggling/losing
                - 4-6: Faction holding steady
                - 7-10: Faction succeeding/winning
            
        Returns:
            List of affected companions, each as dict containing:
                - npc_id: Companion's NPC ID
                - name: Companion's name
                - change: Loyalty change amount (+/-)
                - reason: Explanation of why loyalty changed
                
        Example:
            # Imperial Legion wins major battle, clock advances to 8
            affected = manager.update_companion_based_on_faction_clock('imperial_legion', 8)
            for comp in affected:
                print(f"{comp['name']}: {comp['change']:+d} loyalty")
                # Output: "Lydia: +2 loyalty" (if Lydia is Imperial-aligned)
        
        Notes:
            - Only affects companions at high clock values (7+)
            - Allied companions: +2 loyalty when faction succeeds
            - Hostile companions: -3 loyalty when enemy faction succeeds
            - Neutral companions: No change
            - Checks all companions (active, available, and dismissed)
        """
        state = self.load_campaign_state()
        if not state or 'companions' not in state:
            return []
        
        affected = []
        companions_data = state['companions']
        
        # Check all companions (active, available, dismissed)
        all_companions = (
            companions_data.get('active_companions', []) +
            companions_data.get('available_companions', []) +
            companions_data.get('dismissed_companions', [])
        )
        
        for companion in all_companions:
            npc_id = companion['npc_id']
            
            # Check faction alignment
            alignment = self.check_faction_alignment(npc_id, faction)
            
            # Adjust loyalty based on faction clock and alignment
            if alignment == 'allied':
                # Faction doing well = companion happier
                if clock_value >= 7:
                    loyalty_change = 2
                    reason = f"{faction} faction is succeeding"
                    self.update_loyalty(npc_id, loyalty_change, reason)
                    affected.append({
                        'npc_id': npc_id,
                        'name': companion['name'],
                        'change': loyalty_change,
                        'reason': reason
                    })
            elif alignment == 'hostile':
                # Faction doing well = companion unhappy
                if clock_value >= 7:
                    loyalty_change = -3
                    reason = f"Enemy faction {faction} is succeeding"
                    self.update_loyalty(npc_id, loyalty_change, reason)
                    affected.append({
                        'npc_id': npc_id,
                        'name': companion['name'],
                        'change': loyalty_change,
                        'reason': reason
                    })
        
        if affected:
            print(f"\n{'='*60}")
            print(f"FACTION CLOCK UPDATE: {faction} at {clock_value}/10")
            print(f"Affected companions:")
            for comp in affected:
                print(f"  - {comp['name']}: {comp['change']:+d} ({comp['reason']})")
            print(f"{'='*60}")
        
        return affected
    
    def load_faction_leader_npc(self, faction):
        """
        Load the stat sheet for a neutral faction leader
        
        Args:
            faction: Faction name ('companions', 'thieves_guild', 'college', etc.)
        
        Returns:
            NPC data dict or None
        """
        npc_mapping = {
            "companions": "kodlak_whitemane",
            "thieves_guild": "brynjolf",
            "college": "tolfdir",
            "college_of_winterhold": "savos_aren",
            "dark_brotherhood": "astrid",
            "blades": "delphine",
            "whiterun_contact": "olfrid_battle-born",
            "court_wizard": "farengar_secret-fire"
        }
        
        npc_id = npc_mapping.get(faction)
        if not npc_id:
            return None
        
        # Try loading from npc_stat_sheets directory
        stat_sheet_path = self.data_dir / "npc_stat_sheets" / f"{npc_id}.json"
        if stat_sheet_path.exists():
            with open(stat_sheet_path, 'r') as f:
                return json.load(f)
        
        # Fallback to npcs directory
        return self.load_npc(npc_id)
    
    def add_companion_to_party(self, npc_id, loyalty=60, recruitment_context=""):
        """
        Add a companion to the active party
        
        Args:
            npc_id: NPC ID to add
            loyalty: Starting loyalty (default 60)
            recruitment_context: Why/how they were recruited
        
        Returns:
            Success boolean
        """
        npc = self.load_npc(npc_id)
        if not npc:
            # Try loading from stat sheets
            stat_sheet_path = self.data_dir / "npc_stat_sheets" / f"{npc_id}.json"
            if stat_sheet_path.exists():
                with open(stat_sheet_path, 'r') as f:
                    npc = json.load(f)
            else:
                print(f"Error: NPC {npc_id} not found")
                return False
        
        state = self.load_campaign_state()
        if not state:
            print("Error: No campaign state found")
            return False
        
        if "companions" not in state:
            state["companions"] = {
                "active_companions": [],
                "available_companions": [],
                "dismissed_companions": []
            }
        
        # Check if already active
        for comp in state["companions"]["active_companions"]:
            if comp.get("npc_id") == npc_id:
                print(f"{npc['name']} is already an active companion")
                return False
        
        # Create companion entry
        companion = {
            "npc_id": npc_id,
            "name": npc["name"],
            "status": "active",
            "loyalty": loyalty,
            "location": "With party",
            "recruitment_trigger": recruitment_context,
            "faction_affinity": npc.get("faction", "").lower().replace(" ", "_")
        }
        
        # Remove from available if present
        state["companions"]["available_companions"] = [
            c for c in state["companions"].get("available_companions", [])
            if c.get("npc_id") != npc_id
        ]
        
        # Add to active
        state["companions"]["active_companions"].append(companion)
        
        # Update companion relationships
        if "companion_relationships" not in state["companions"]:
            state["companions"]["companion_relationships"] = {}
        state["companions"]["companion_relationships"][npc["name"].lower()] = loyalty
        
        self.save_campaign_state(state)
        print(f"\n✓ {npc['name']} has joined the party as an active companion!")
        print(f"  Starting loyalty: {loyalty}")
        print(f"  Recruitment: {recruitment_context}")
        
        return True
    
    def switch_companion_allegiance(self, npc_id, new_faction, reason=""):
        """
        Handle a companion switching faction allegiance (e.g., Hadvar/Ralof in neutral start)
        
        Args:
            npc_id: NPC ID
            new_faction: New faction allegiance
            reason: Why they're switching
        
        Returns:
            Result dict with loyalty changes and consequences
        """
        npc = self.load_npc(npc_id)
        if not npc:
            # Try loading from stat sheets
            stat_sheet_path = self.data_dir / "npc_stat_sheets" / f"{npc_id}.json"
            if stat_sheet_path.exists():
                with open(stat_sheet_path, 'r') as f:
                    npc = json.load(f)
            else:
                return {"success": False, "error": "NPC not found"}
        
        state = self.load_campaign_state()
        if not state or "companions" not in state:
            return {"success": False, "error": "No campaign state"}
        
        # Find companion in active list
        companion = None
        for comp in state["companions"]["active_companions"]:
            if comp.get("npc_id") == npc_id:
                companion = comp
                break
        
        if not companion:
            return {"success": False, "error": "NPC is not an active companion"}
        
        old_faction = companion.get("faction_affinity", "unknown")
        
        # Calculate loyalty impact
        loyalty_change = 0
        if new_faction == old_faction:
            # No change needed
            return {"success": True, "message": "Already aligned with this faction", "loyalty_change": 0}
        else:
            # Switching away from original faction causes loyalty loss
            loyalty_change = -10
            reason_text = reason if reason else f"Switched allegiance from {old_faction} to {new_faction}"
            self.update_loyalty(npc_id, loyalty_change, reason_text)
        
        # Update companion data
        companion["faction_affinity"] = new_faction
        companion["notes"] = companion.get("notes", "") + f" [Switched to {new_faction}: {reason}]"
        
        self.save_campaign_state(state)
        
        result = {
            "success": True,
            "npc_name": npc["name"],
            "old_faction": old_faction,
            "new_faction": new_faction,
            "loyalty_change": loyalty_change,
            "current_loyalty": companion["loyalty"],
            "reason": reason
        }
        
        print(f"\n⚠️  FACTION ALLEGIANCE CHANGE")
        print(f"  {npc['name']}: {old_faction} → {new_faction}")
        print(f"  Loyalty impact: {loyalty_change}")
        print(f"  Reason: {reason}")
        print(f"  Current loyalty: {companion['loyalty']}")
        
        return result


def main():
    """Main function for testing"""
    manager = NPCManager()
    
    print("Skyrim NPC Manager")
    print("==================\n")
    
    print("1. List All NPCs")
    print("2. Check NPC/Companion Status")
    print("3. Update Loyalty")
    print("4. Create NPC Template")
    print("5. Loyalty Check for Situation")
    print("6. Recruit Companion")
    print("7. Dismiss Companion")
    print("8. Check Active Companions")
    print("9. Process Decision Point")
    print("10. Handle Dialogue Interaction")
    print("11. Check Faction Alignment")
    print("12. Exit")
    
    while True:
        choice = input("\nEnter choice (1-12): ").strip()
        
        if choice == "1":
            manager.list_npcs()
        
        elif choice == "2":
            npc_id = input("NPC ID: ").strip()
            manager.check_companion_status(npc_id)
        
        elif choice == "3":
            npc_id = input("NPC ID: ").strip()
            change = input("Loyalty change (+/-): ").strip()
            reason = input("Reason: ").strip()
            manager.update_loyalty(npc_id, int(change), reason)
        
        elif choice == "4":
            name = input("NPC Name: ").strip()
            role = input("Role: ").strip()
            faction = input("Faction (or blank): ").strip()
            manager.create_npc_template(name, role, faction if faction else None)
        
        elif choice == "5":
            npc_id = input("NPC ID: ").strip()
            situation = input("Situation description: ").strip()
            manager.companion_loyalty_check(npc_id, situation)
        
        elif choice == "6":
            npc_id = input("NPC ID to recruit: ").strip()
            manager.recruit_companion(npc_id)
        
        elif choice == "7":
            npc_id = input("NPC ID to dismiss: ").strip()
            manager.dismiss_companion(npc_id)
        
        elif choice == "8":
            companions = manager.get_active_companions()
            print(f"\nActive Companions ({len(companions)}):")
            for comp in companions:
                print(f"  - {comp['name']} (Loyalty: {comp.get('loyalty', 50)}/100)")
        
        elif choice == "9":
            npc_id = input("NPC ID: ").strip()
            decision_key = input("Decision key (e.g., civil_war_choice): ").strip()
            option = input("Chosen option: ").strip()
            result = manager.process_decision_point(npc_id, decision_key, option)
            print(f"\nResult: {result}")
        
        elif choice == "10":
            npc_id = input("NPC ID: ").strip()
            dialogue_key = input("Dialogue key (e.g., initial_meeting): ").strip()
            result = manager.handle_dialogue_interaction(npc_id, dialogue_key)
            if result.get('responses'):
                response_idx = input("\nChoose response (0-based index): ").strip()
                if response_idx.isdigit():
                    result = manager.handle_dialogue_interaction(npc_id, dialogue_key, int(response_idx))
            print(f"\nResult: {result}")
        
        elif choice == "11":
            npc_id = input("NPC ID: ").strip()
            faction = input("Faction name: ").strip()
            alignment = manager.check_faction_alignment(npc_id, faction)
            print(f"\n{npc_id} alignment with {faction}: {alignment}")
        
        elif choice == "12":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-12.")


if __name__ == "__main__":
    main()
