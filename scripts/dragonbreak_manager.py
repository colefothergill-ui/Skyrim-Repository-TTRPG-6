#!/usr/bin/env python3
"""
Dragonbreak Manager for Skyrim TTRPG

This script manages:
- Timeline fractures ("Dragonbreaks") where multiple realities exist
- NPC tracking across different timeline branches
- Faction states across timeline branches
- Quest outcomes across timeline branches
- Consequences for different in-game paths triggered dynamically
"""

import json
import os
from pathlib import Path
from datetime import datetime


class DragonbreakManager:
    def __init__(self, data_dir="../data", state_dir="../state"):
        self.data_dir = Path(data_dir)
        self.state_dir = Path(state_dir)
        self.dragonbreak_state_path = self.state_dir / "dragonbreak_state.json"
        self.dragonbreak_log_path = Path("../logs") / "dragonbreak_log.md"
        
    def load_dragonbreak_state(self):
        """Load current dragonbreak state"""
        if self.dragonbreak_state_path.exists():
            with open(self.dragonbreak_state_path, 'r') as f:
                return json.load(f)
        return self._initialize_dragonbreak_state()
    
    def _initialize_dragonbreak_state(self):
        """Initialize a new dragonbreak state"""
        return {
            "active_dragonbreaks": [],
            "timeline_branches": {
                "primary": {
                    "id": "primary",
                    "name": "Primary Timeline",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "npcs": {},
                    "factions": {},
                    "quests": {},
                    "world_state": {}
                }
            },
            "current_timeline": "primary",
            "fracture_points": [],
            "consequences": []
        }
    
    def save_dragonbreak_state(self, state):
        """Save dragonbreak state"""
        self.state_dir.mkdir(exist_ok=True)
        state['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.dragonbreak_state_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def create_timeline_fracture(self, fracture_name, description, trigger_event):
        """
        Create a new timeline fracture (Dragonbreak event)
        
        Args:
            fracture_name: Name of the fracture event
            description: Description of what caused the fracture
            trigger_event: The event that triggered this fracture
        
        Returns:
            The ID of the new timeline branch
        """
        state = self.load_dragonbreak_state()
        
        # Create new timeline branch
        branch_id = f"branch_{len(state['timeline_branches'])}"
        current_timeline = state['timeline_branches'][state['current_timeline']]
        
        # Copy current timeline state to new branch
        new_branch = {
            "id": branch_id,
            "name": fracture_name,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parent_timeline": state['current_timeline'],
            "description": description,
            "trigger_event": trigger_event,
            "npcs": dict(current_timeline['npcs']),
            "factions": dict(current_timeline['factions']),
            "quests": dict(current_timeline['quests']),
            "world_state": dict(current_timeline['world_state'])
        }
        
        state['timeline_branches'][branch_id] = new_branch
        
        # Record the fracture point
        fracture_point = {
            "fracture_id": branch_id,
            "name": fracture_name,
            "description": description,
            "trigger_event": trigger_event,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parent_timeline": state['current_timeline']
        }
        state['fracture_points'].append(fracture_point)
        
        # Add to active dragonbreaks
        dragonbreak = {
            "id": f"dragonbreak_{len(state['active_dragonbreaks']) + 1}",
            "name": fracture_name,
            "branch_ids": [state['current_timeline'], branch_id],
            "status": "active",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        state['active_dragonbreaks'].append(dragonbreak)
        
        self.save_dragonbreak_state(state)
        self._log_dragonbreak_event(fracture_name, description, trigger_event, branch_id)
        
        print(f"\n⚠️  DRAGONBREAK INITIATED ⚠️")
        print(f"Fracture: {fracture_name}")
        print(f"New Timeline Branch: {branch_id}")
        print(f"Description: {description}")
        
        return branch_id
    
    def track_npc_across_branches(self, npc_id, npc_name, branch_states):
        """
        Track an NPC's state across different timeline branches
        
        Args:
            npc_id: Unique identifier for the NPC
            npc_name: Name of the NPC
            branch_states: Dict mapping branch_id to NPC state in that branch
                          e.g., {"primary": {"alive": True, "location": "Whiterun"},
                                 "branch_1": {"alive": False, "location": "Sovngarde"}}
        """
        state = self.load_dragonbreak_state()
        
        for branch_id, npc_state in branch_states.items():
            if branch_id in state['timeline_branches']:
                state['timeline_branches'][branch_id]['npcs'][npc_id] = {
                    "name": npc_name,
                    "state": npc_state,
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        
        self.save_dragonbreak_state(state)
        print(f"NPC '{npc_name}' tracked across {len(branch_states)} timeline branches")
    
    def track_faction_across_branches(self, faction_id, faction_name, branch_states):
        """
        Track a faction's state across different timeline branches
        
        Args:
            faction_id: Unique identifier for the faction
            faction_name: Name of the faction
            branch_states: Dict mapping branch_id to faction state in that branch
        """
        state = self.load_dragonbreak_state()
        
        for branch_id, faction_state in branch_states.items():
            if branch_id in state['timeline_branches']:
                state['timeline_branches'][branch_id]['factions'][faction_id] = {
                    "name": faction_name,
                    "state": faction_state,
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        
        self.save_dragonbreak_state(state)
        print(f"Faction '{faction_name}' tracked across {len(branch_states)} timeline branches")
    
    def track_quest_across_branches(self, quest_id, quest_name, branch_outcomes):
        """
        Track a quest's outcomes across different timeline branches
        
        Args:
            quest_id: Unique identifier for the quest
            quest_name: Name of the quest
            branch_outcomes: Dict mapping branch_id to quest outcome in that branch
        """
        state = self.load_dragonbreak_state()
        
        for branch_id, outcome in branch_outcomes.items():
            if branch_id in state['timeline_branches']:
                state['timeline_branches'][branch_id]['quests'][quest_id] = {
                    "name": quest_name,
                    "outcome": outcome,
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        
        self.save_dragonbreak_state(state)
        print(f"Quest '{quest_name}' tracked across {len(branch_outcomes)} timeline branches")
    
    def define_branch_consequence(self, branch_id, consequence_type, consequence_data):
        """
        Define consequences for a specific timeline branch
        
        Args:
            branch_id: The timeline branch to apply consequences to
            consequence_type: Type of consequence ('npc_behavior', 'faction_relations', 
                            'world_event', 'quest_availability')
            consequence_data: Data describing the consequence
        """
        state = self.load_dragonbreak_state()
        
        consequence = {
            "id": f"consequence_{len(state['consequences']) + 1}",
            "branch_id": branch_id,
            "type": consequence_type,
            "data": consequence_data,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "triggered": False
        }
        
        state['consequences'].append(consequence)
        self.save_dragonbreak_state(state)
        
        print(f"Consequence defined for branch '{branch_id}': {consequence_type}")
        return consequence['id']
    
    def trigger_consequences_for_branch(self, branch_id):
        """
        Trigger all pending consequences for a specific timeline branch
        
        Args:
            branch_id: The timeline branch to trigger consequences for
        
        Returns:
            List of triggered consequences
        """
        state = self.load_dragonbreak_state()
        triggered = []
        
        for consequence in state['consequences']:
            if (consequence['branch_id'] == branch_id and 
                not consequence['triggered']):
                consequence['triggered'] = True
                consequence['triggered_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                triggered.append(consequence)
        
        self.save_dragonbreak_state(state)
        
        if triggered:
            print(f"\n⚡ Triggered {len(triggered)} consequences for branch '{branch_id}':")
            for cons in triggered:
                print(f"  - {cons['type']}: {cons['data']}")
        
        return triggered
    
    def switch_timeline(self, branch_id):
        """
        Switch the active timeline to a different branch
        
        Args:
            branch_id: The timeline branch to switch to
        """
        state = self.load_dragonbreak_state()
        
        if branch_id not in state['timeline_branches']:
            print(f"Error: Timeline branch '{branch_id}' does not exist")
            return False
        
        old_timeline = state['current_timeline']
        state['current_timeline'] = branch_id
        self.save_dragonbreak_state(state)
        
        print(f"Switched timeline: {old_timeline} -> {branch_id}")
        
        # Trigger consequences for the new timeline
        self.trigger_consequences_for_branch(branch_id)
        
        return True
    
    def resolve_dragonbreak(self, dragonbreak_id, resolution_type="merge", primary_branch=None):
        """
        Resolve a dragonbreak, bringing timelines back together
        
        Args:
            dragonbreak_id: ID of the dragonbreak to resolve
            resolution_type: How to resolve ('merge', 'collapse_to_one', 'remain_separate')
            primary_branch: If collapsing, which branch becomes canon
        """
        state = self.load_dragonbreak_state()
        
        for dragonbreak in state['active_dragonbreaks']:
            if dragonbreak['id'] == dragonbreak_id:
                dragonbreak['status'] = 'resolved'
                dragonbreak['resolved_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dragonbreak['resolution_type'] = resolution_type
                
                if resolution_type == "collapse_to_one" and primary_branch:
                    dragonbreak['canonical_branch'] = primary_branch
                    state['current_timeline'] = primary_branch
                
                self.save_dragonbreak_state(state)
                
                print(f"\n✨ DRAGONBREAK RESOLVED ✨")
                print(f"Dragonbreak: {dragonbreak['name']}")
                print(f"Resolution: {resolution_type}")
                if primary_branch:
                    print(f"Canonical Branch: {primary_branch}")
                
                return True
        
        print(f"Error: Dragonbreak '{dragonbreak_id}' not found")
        return False
    
    def get_timeline_state(self, branch_id=None):
        """
        Get the complete state of a timeline branch
        
        Args:
            branch_id: The timeline branch to query (defaults to current)
        """
        state = self.load_dragonbreak_state()
        
        if branch_id is None:
            branch_id = state['current_timeline']
        
        if branch_id not in state['timeline_branches']:
            return None
        
        branch = state['timeline_branches'][branch_id]
        
        print(f"\n=== Timeline: {branch['name']} ({branch_id}) ===")
        print(f"Created: {branch['created']}")
        if 'parent_timeline' in branch:
            print(f"Parent Timeline: {branch['parent_timeline']}")
        
        print(f"\nNPCs tracked: {len(branch['npcs'])}")
        for npc_id, npc_data in branch['npcs'].items():
            print(f"  - {npc_data['name']}: {npc_data['state']}")
        
        print(f"\nFactions tracked: {len(branch['factions'])}")
        for faction_id, faction_data in branch['factions'].items():
            print(f"  - {faction_data['name']}: {faction_data['state']}")
        
        print(f"\nQuests tracked: {len(branch['quests'])}")
        for quest_id, quest_data in branch['quests'].items():
            print(f"  - {quest_data['name']}: {quest_data['outcome']}")
        
        return branch
    
    def list_active_dragonbreaks(self):
        """List all active dragonbreaks"""
        state = self.load_dragonbreak_state()
        
        active = [db for db in state['active_dragonbreaks'] if db['status'] == 'active']
        
        if not active:
            print("No active dragonbreaks")
            return []
        
        print(f"\n=== Active Dragonbreaks ({len(active)}) ===")
        for db in active:
            print(f"\n{db['id']}: {db['name']}")
            print(f"  Branches: {', '.join(db['branch_ids'])}")
            print(f"  Created: {db['created']}")
        
        return active
    
    def list_all_timelines(self):
        """List all timeline branches"""
        state = self.load_dragonbreak_state()
        
        print(f"\n=== Timeline Branches ({len(state['timeline_branches'])}) ===")
        print(f"Current Timeline: {state['current_timeline']}\n")
        
        for branch_id, branch in state['timeline_branches'].items():
            marker = "→ " if branch_id == state['current_timeline'] else "  "
            print(f"{marker}{branch_id}: {branch['name']}")
            print(f"   Created: {branch['created']}")
            print(f"   NPCs: {len(branch['npcs'])}, Factions: {len(branch['factions'])}, Quests: {len(branch['quests'])}")
        
        return state['timeline_branches']
    
    def _log_dragonbreak_event(self, name, description, trigger, branch_id):
        """Log a dragonbreak event to the markdown log file"""
        log_dir = Path("../logs")
        log_dir.mkdir(exist_ok=True)
        
        log_entry = f"""
## Dragonbreak: {name}

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Timeline Branch**: {branch_id}  
**Trigger Event**: {trigger}

**Description**: {description}

---
"""
        
        # Check if file exists and needs header before opening
        file_exists = self.dragonbreak_log_path.exists()
        file_is_empty = not file_exists or self.dragonbreak_log_path.stat().st_size == 0
        
        # Append to log file
        with open(self.dragonbreak_log_path, 'a') as f:
            if file_is_empty:
                f.write("# Dragonbreak Event Log\n\n")
                f.write("This log tracks all timeline fractures (Dragonbreaks) in the campaign.\n\n")
                f.write("---\n")
            f.write(log_entry)


def main():
    """Main function for testing"""
    manager = DragonbreakManager()
    
    print("Skyrim Dragonbreak Manager")
    print("==========================\n")
    
    print("1. Create Timeline Fracture")
    print("2. Track NPC Across Branches")
    print("3. Track Faction Across Branches")
    print("4. Track Quest Across Branches")
    print("5. Define Branch Consequence")
    print("6. Switch Timeline")
    print("7. Get Timeline State")
    print("8. List Active Dragonbreaks")
    print("9. List All Timelines")
    print("10. Resolve Dragonbreak")
    print("11. Exit")
    
    while True:
        choice = input("\nEnter choice (1-11): ").strip()
        
        if choice == "1":
            name = input("Fracture name: ").strip()
            description = input("Description: ").strip()
            trigger = input("Trigger event: ").strip()
            manager.create_timeline_fracture(name, description, trigger)
        
        elif choice == "2":
            npc_id = input("NPC ID: ").strip()
            npc_name = input("NPC name: ").strip()
            # Simplified: track in primary and branch_1
            primary_state = input("State in primary timeline: ").strip()
            branch_state = input("State in branch_1 (or N/A): ").strip()
            states = {"primary": {"status": primary_state}}
            if branch_state.lower() != "n/a":
                states["branch_1"] = {"status": branch_state}
            manager.track_npc_across_branches(npc_id, npc_name, states)
        
        elif choice == "3":
            faction_id = input("Faction ID: ").strip()
            faction_name = input("Faction name: ").strip()
            primary_state = input("State in primary timeline: ").strip()
            branch_state = input("State in branch_1 (or N/A): ").strip()
            states = {"primary": {"status": primary_state}}
            if branch_state.lower() != "n/a":
                states["branch_1"] = {"status": branch_state}
            manager.track_faction_across_branches(faction_id, faction_name, states)
        
        elif choice == "4":
            quest_id = input("Quest ID: ").strip()
            quest_name = input("Quest name: ").strip()
            primary_outcome = input("Outcome in primary timeline: ").strip()
            branch_outcome = input("Outcome in branch_1 (or N/A): ").strip()
            outcomes = {"primary": primary_outcome}
            if branch_outcome.lower() != "n/a":
                outcomes["branch_1"] = branch_outcome
            manager.track_quest_across_branches(quest_id, quest_name, outcomes)
        
        elif choice == "5":
            branch_id = input("Branch ID: ").strip()
            cons_type = input("Consequence type: ").strip()
            cons_data = input("Consequence data: ").strip()
            manager.define_branch_consequence(branch_id, cons_type, cons_data)
        
        elif choice == "6":
            branch_id = input("Switch to branch ID: ").strip()
            manager.switch_timeline(branch_id)
        
        elif choice == "7":
            branch_id = input("Branch ID (or Enter for current): ").strip()
            manager.get_timeline_state(branch_id if branch_id else None)
        
        elif choice == "8":
            manager.list_active_dragonbreaks()
        
        elif choice == "9":
            manager.list_all_timelines()
        
        elif choice == "10":
            db_id = input("Dragonbreak ID: ").strip()
            res_type = input("Resolution type (merge/collapse_to_one/remain_separate): ").strip()
            primary = input("Primary branch (if collapsing): ").strip()
            manager.resolve_dragonbreak(db_id, res_type, primary if primary else None)
        
        elif choice == "11":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-11.")


if __name__ == "__main__":
    main()
