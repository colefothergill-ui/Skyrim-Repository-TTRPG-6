#!/usr/bin/env python3
"""
Faction Logic Manager for Skyrim TTRPG

This script manages:
- Faction trust clocks
- Faction progression and ranks
- Faction relationships
- Faction rewards and consequences
"""

import json
import os
from pathlib import Path
from datetime import datetime


class FactionManager:
    def __init__(self, data_dir="../data"):
        self.data_dir = Path(data_dir)
        self.factions_path = self.data_dir / "factions.json"
        self.factions_dir = self.data_dir / "factions"
        
    def load_factions_data(self):
        """Load comprehensive factions data"""
        if self.factions_path.exists():
            with open(self.factions_path, 'r') as f:
                return json.load(f)
        return None
    
    def save_factions_data(self, data):
        """Save factions data"""
        with open(self.factions_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_individual_faction(self, faction_id):
        """Load individual faction file if it exists"""
        faction_file = self.factions_dir / f"{faction_id}.json"
        if faction_file.exists():
            with open(faction_file, 'r') as f:
                return json.load(f)
        return None
    
    def update_faction_clock(self, faction_id, clock_name, progress_change):
        """
        Update a faction's clock
        
        Args:
            faction_id: ID of the faction
            clock_name: Name of the clock to update
            progress_change: Amount to change (+/-)
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        # Find faction
        faction = None
        if faction_id in data.get('major_factions', {}):
            faction = data['major_factions'][faction_id]
        
        if not faction or 'clocks' not in faction:
            print(f"Faction '{faction_id}' or its clocks not found")
            return False
        
        # Update the clock
        for clock in faction['clocks']:
            if clock['name'] == clock_name:
                old_progress = clock['progress']
                clock['progress'] = max(0, min(clock['segments'], 
                                              clock['progress'] + progress_change))
                
                print(f"\n{faction['name']} - {clock_name}")
                print(f"Progress: {old_progress} -> {clock['progress']}/{clock['segments']}")
                
                # Check if clock is filled
                if clock['progress'] >= clock['segments']:
                    print(f"⚠️  Clock filled! Effect: {clock['effect']}")
                
                self.save_factions_data(data)
                return True
        
        print(f"Clock '{clock_name}' not found in faction '{faction_id}'")
        return False
    
    def update_faction_relationship(self, faction_id, other_faction, change):
        """
        Update relationship between factions
        
        Args:
            faction_id: ID of the faction
            other_faction: ID of the other faction
            change: Amount to change relationship (+/-)
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        if faction_id in data.get('major_factions', {}):
            faction = data['major_factions'][faction_id]
            
            if 'relationships' in faction:
                old_value = faction['relationships'].get(other_faction, 0)
                new_value = max(-100, min(100, old_value + change))
                faction['relationships'][other_faction] = new_value
                
                print(f"\n{faction['name']} <-> {other_faction}")
                print(f"Relationship: {old_value} -> {new_value}")
                
                self.save_factions_data(data)
                return True
        
        return False
    
    def update_faction_resources(self, faction_id, resource_type, change):
        """
        Update faction resources
        
        Args:
            faction_id: ID of the faction
            resource_type: Type of resource (military_strength, gold, etc.)
            change: Amount to change (+/-)
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        if faction_id in data.get('major_factions', {}):
            faction = data['major_factions'][faction_id]
            
            if 'resources' in faction and resource_type in faction['resources']:
                old_value = faction['resources'][resource_type]
                
                # Handle numeric vs string values
                if isinstance(old_value, (int, float)):
                    new_value = max(0, old_value + change)
                    faction['resources'][resource_type] = new_value
                    print(f"\n{faction['name']} - {resource_type}")
                    print(f"{old_value} -> {new_value}")
                else:
                    print(f"Resource '{resource_type}' is not numeric (value: {old_value})")
                    return False
                
                self.save_factions_data(data)
                return True
        
        return False
    
    def check_faction_status(self, faction_id):
        """
        Display comprehensive faction status
        """
        data = self.load_factions_data()
        if not data:
            return None
        
        faction = None
        if faction_id in data.get('major_factions', {}):
            faction = data['major_factions'][faction_id]
        
        if not faction:
            print(f"Faction '{faction_id}' not found")
            return None
        
        print(f"\n{'='*60}")
        print(f"FACTION: {faction['name']}")
        print(f"{'='*60}")
        print(f"Description: {faction['description']}")
        print(f"Headquarters: {faction['headquarters']}")
        print(f"Leader: {faction['leader']['name']} ({faction['leader']['role']})")
        print(f"Alignment: {faction['alignment']}")
        
        print(f"\n--- Goals ---")
        for i, goal in enumerate(faction['goals'], 1):
            print(f"{i}. {goal}")
        
        print(f"\n--- Clocks ---")
        for clock in faction.get('clocks', []):
            progress_bar = '█' * clock['progress'] + '░' * (clock['segments'] - clock['progress'])
            print(f"{clock['name']}: [{progress_bar}] {clock['progress']}/{clock['segments']}")
            print(f"  Effect: {clock['effect']}")
        
        print(f"\n--- Resources ---")
        for resource, value in faction.get('resources', {}).items():
            print(f"{resource}: {value}")
        
        print(f"\n--- Relationships ---")
        for other_faction, value in faction.get('relationships', {}).items():
            if value >= 50:
                status = "Allied"
            elif value >= 20:
                status = "Friendly"
            elif value >= -20:
                status = "Neutral"
            elif value >= -50:
                status = "Unfriendly"
            else:
                status = "Hostile"
            print(f"{other_faction}: {value} ({status})")
        
        if faction.get('joinable'):
            print(f"\n--- Ranks ---")
            for i, rank in enumerate(faction.get('ranks', []), 1):
                print(f"{i}. {rank}")
        
        return faction
    
    def list_all_factions(self):
        """
        List all major factions
        """
        data = self.load_factions_data()
        if not data:
            return []
        
        print("\n=== Major Factions ===\n")
        factions = []
        
        for faction_id, faction in data.get('major_factions', {}).items():
            print(f"{faction_id}: {faction['name']}")
            print(f"  {faction['description']}")
            print(f"  Leader: {faction['leader']['name']}")
            print()
            factions.append((faction_id, faction['name']))
        
        return factions
    
    def track_player_faction_standing(self, faction_id, player_reputation):
        """
        Track a player's standing with a faction
        
        Args:
            faction_id: ID of the faction
            player_reputation: Reputation score (0-100)
        """
        # This would integrate with PC files
        print(f"Player reputation with {faction_id}: {player_reputation}")
        
        # Determine rank eligibility
        if player_reputation >= 80:
            rank_level = "Highest rank eligible"
        elif player_reputation >= 60:
            rank_level = "High rank eligible"
        elif player_reputation >= 40:
            rank_level = "Mid rank eligible"
        elif player_reputation >= 20:
            rank_level = "Entry rank eligible"
        else:
            rank_level = "Not yet eligible"
        
        print(f"Rank status: {rank_level}")
        return rank_level
    
    def simulate_faction_turn(self, faction_id):
        """
        Simulate a faction's actions in the background
        Advances clocks based on faction's active goals
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        if faction_id not in data.get('major_factions', {}):
            return False
        
        faction = data['major_factions'][faction_id]
        print(f"\n=== {faction['name']} Turn ===")
        
        # Advance clocks by default amount (1 per turn unless interfered with)
        changes_made = False
        for clock in faction.get('clocks', []):
            if clock['progress'] < clock['segments']:
                old_progress = clock['progress']
                clock['progress'] = min(clock['segments'], clock['progress'] + 1)
                print(f"{clock['name']}: {old_progress} -> {clock['progress']}/{clock['segments']}")
                changes_made = True
                
                if clock['progress'] >= clock['segments']:
                    print(f"⚠️  {clock['name']} completed! {clock['effect']}")
        
        if changes_made:
            self.save_factions_data(data)
        else:
            print("No clock changes this turn")
        
        return changes_made
    
    def faction_conflict_resolution(self, faction1_id, faction2_id):
        """
        Resolve conflict between two factions
        """
        data = self.load_factions_data()
        if not data:
            return None
        
        f1 = data['major_factions'].get(faction1_id)
        f2 = data['major_factions'].get(faction2_id)
        
        if not f1 or not f2:
            return None
        
        print(f"\n=== Faction Conflict: {f1['name']} vs {f2['name']} ===")
        
        # Compare military strength
        str1 = f1['resources'].get('military_strength', 50)
        str2 = f2['resources'].get('military_strength', 50)
        
        print(f"{f1['name']} strength: {str1}")
        print(f"{f2['name']} strength: {str2}")
        
        # Determine outcome
        if str1 > str2:
            winner = f1['name']
            margin = str1 - str2
        elif str2 > str1:
            winner = f2['name']
            margin = str2 - str1
        else:
            winner = "Stalemate"
            margin = 0
        
        print(f"\nOutcome: {winner} (margin: {margin})")
        
        return {
            'winner': winner,
            'margin': margin,
            'f1_strength': str1,
            'f2_strength': str2
        }
    
    def add_faction_allegation(self, faction_id, allegation_type, accuser, details):
        """
        Add a faction allegation (Side Plot C mechanics - Thalmor plots, Civil War strategies)
        
        Args:
            faction_id: ID of the faction being accused
            allegation_type: Type of allegation ('thalmor_conspiracy', 'war_crime', 
                           'betrayal', 'corruption', 'espionage')
            accuser: Who is making the allegation
            details: Details of the allegation
        
        Returns:
            Allegation ID
        """
        data = self.load_factions_data()
        if not data:
            return None
        
        if faction_id not in data.get('major_factions', {}):
            print(f"Faction '{faction_id}' not found")
            return None
        
        faction = data['major_factions'][faction_id]
        
        # Initialize allegations list if needed
        if 'allegations' not in faction:
            faction['allegations'] = []
        
        # Create allegation
        allegation = {
            'id': f"allegation_{len(faction['allegations']) + 1}",
            'type': allegation_type,
            'accuser': accuser,
            'details': details,
            'status': 'pending',  # pending, proven, disproven, ignored
            'evidence_level': 0,  # 0-10 scale
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'consequences': []
        }
        
        faction['allegations'].append(allegation)
        self.save_factions_data(data)
        
        print(f"\n⚠️  NEW ALLEGATION against {faction['name']} ⚠️")
        print(f"Type: {allegation_type}")
        print(f"Accuser: {accuser}")
        print(f"Details: {details}")
        print(f"Allegation ID: {allegation['id']}")
        
        return allegation['id']
    
    def update_allegation_evidence(self, faction_id, allegation_id, evidence_change, evidence_description=None):
        """
        Update evidence level for a faction allegation
        
        Args:
            faction_id: ID of the faction
            allegation_id: ID of the allegation
            evidence_change: Amount to change evidence level (+/-)
            evidence_description: Optional description of new evidence
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        if faction_id not in data.get('major_factions', {}):
            return False
        
        faction = data['major_factions'][faction_id]
        
        for allegation in faction.get('allegations', []):
            if allegation['id'] == allegation_id:
                old_evidence = allegation['evidence_level']
                allegation['evidence_level'] = max(0, min(10, old_evidence + evidence_change))
                
                print(f"\n{faction['name']} - {allegation['type']}")
                print(f"Evidence: {old_evidence}/10 -> {allegation['evidence_level']}/10")
                
                if evidence_description:
                    if 'evidence_trail' not in allegation:
                        allegation['evidence_trail'] = []
                    allegation['evidence_trail'].append({
                        'description': evidence_description,
                        'change': evidence_change,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                
                # Auto-update status based on evidence
                if allegation['evidence_level'] >= 8:
                    allegation['status'] = 'proven'
                    print("⚖️  Status: PROVEN")
                elif allegation['evidence_level'] <= 2 and allegation['status'] == 'pending':
                    allegation['status'] = 'disproven'
                    print("⚖️  Status: DISPROVEN")
                
                self.save_factions_data(data)
                return True
        
        print(f"Allegation '{allegation_id}' not found")
        return False
    
    def resolve_allegation(self, faction_id, allegation_id, resolution, consequences=None):
        """
        Resolve a faction allegation with consequences
        
        Args:
            faction_id: ID of the faction
            allegation_id: ID of the allegation
            resolution: Resolution status ('proven', 'disproven', 'ignored')
            consequences: List of consequence strings
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        if faction_id not in data.get('major_factions', {}):
            return False
        
        faction = data['major_factions'][faction_id]
        
        for allegation in faction.get('allegations', []):
            if allegation['id'] == allegation_id:
                allegation['status'] = resolution
                allegation['resolved_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if consequences:
                    allegation['consequences'] = consequences
                
                print(f"\n⚖️  ALLEGATION RESOLVED ⚖️")
                print(f"Faction: {faction['name']}")
                print(f"Allegation: {allegation['type']}")
                print(f"Resolution: {resolution}")
                
                if consequences:
                    print("Consequences:")
                    for cons in consequences:
                        print(f"  - {cons}")
                
                # Apply faction relationship impacts
                if resolution == 'proven':
                    # Negative impact on faction reputation
                    if 'reputation' not in faction:
                        faction['reputation'] = 50
                    faction['reputation'] = max(0, faction['reputation'] - 10)
                    print(f"\nFaction reputation decreased to: {faction['reputation']}")
                
                self.save_factions_data(data)
                return True
        
        print(f"Allegation '{allegation_id}' not found")
        return False
    
    def get_faction_allegations(self, faction_id, status_filter=None):
        """
        Get all allegations for a faction
        
        Args:
            faction_id: ID of the faction
            status_filter: Optional filter by status ('pending', 'proven', 'disproven', 'ignored')
        """
        data = self.load_factions_data()
        if not data:
            return []
        
        if faction_id not in data.get('major_factions', {}):
            return []
        
        faction = data['major_factions'][faction_id]
        allegations = faction.get('allegations', [])
        
        if status_filter:
            allegations = [a for a in allegations if a['status'] == status_filter]
        
        if allegations:
            print(f"\n=== Allegations against {faction['name']} ===")
            for allegation in allegations:
                print(f"\n{allegation['id']}: {allegation['type']}")
                print(f"  Accuser: {allegation['accuser']}")
                print(f"  Status: {allegation['status']}")
                print(f"  Evidence: {allegation['evidence_level']}/10")
                print(f"  Details: {allegation['details']}")
                if allegation.get('consequences'):
                    print(f"  Consequences: {', '.join(allegation['consequences'])}")
        else:
            print(f"No allegations found for {faction_id}")
        
        return allegations
    
    def track_thalmor_plot(self, plot_name, target_faction, plot_details, clock_segments=8):
        """
        Track a Thalmor plot as part of Side Plot C mechanics
        
        Args:
            plot_name: Name of the Thalmor plot
            target_faction: Faction being targeted
            plot_details: Details of the plot
            clock_segments: Number of segments for the plot clock
        """
        data = self.load_factions_data()
        if not data:
            return None
        
        # Find or create Thalmor faction
        thalmor = data['major_factions'].get('thalmor_dominion')
        if not thalmor:
            print("Warning: Thalmor faction not found")
            return None
        
        # Initialize plots list if needed
        if 'active_plots' not in thalmor:
            thalmor['active_plots'] = []
        
        # Create plot clock
        plot = {
            'id': f"thalmor_plot_{len(thalmor['active_plots']) + 1}",
            'name': plot_name,
            'target': target_faction,
            'details': plot_details,
            'clock': {
                'progress': 0,
                'segments': clock_segments
            },
            'status': 'active',  # active, exposed, thwarted, succeeded
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'discoveries': []
        }
        
        thalmor['active_plots'].append(plot)
        self.save_factions_data(data)
        
        print(f"\n🕵️  NEW THALMOR PLOT INITIATED 🕵️")
        print(f"Plot: {plot_name}")
        print(f"Target: {target_faction}")
        print(f"Plot ID: {plot['id']}")
        
        return plot['id']
    
    def advance_thalmor_plot(self, plot_id, progress_change, discovery=None):
        """
        Advance a Thalmor plot clock
        
        Args:
            plot_id: ID of the plot
            progress_change: Amount to advance (+/-) 
            discovery: Optional discovery made by players
        """
        data = self.load_factions_data()
        if not data:
            return False
        
        thalmor = data['major_factions'].get('thalmor_dominion')
        if not thalmor:
            return False
        
        for plot in thalmor.get('active_plots', []):
            if plot['id'] == plot_id:
                old_progress = plot['clock']['progress']
                plot['clock']['progress'] = max(0, min(plot['clock']['segments'], 
                                                       old_progress + progress_change))
                
                print(f"\n🕵️  Thalmor Plot: {plot['name']}")
                print(f"Progress: {old_progress}/{plot['clock']['segments']} -> {plot['clock']['progress']}/{plot['clock']['segments']}")
                
                if discovery:
                    plot['discoveries'].append({
                        'discovery': discovery,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    print(f"Discovery: {discovery}")
                
                # Check if plot completed
                if plot['clock']['progress'] >= plot['clock']['segments']:
                    plot['status'] = 'succeeded'
                    print("⚠️  THALMOR PLOT SUCCEEDED!")
                
                self.save_factions_data(data)
                return True
        
        print(f"Plot '{plot_id}' not found")
        return False


def main():
    """Main function for testing"""
    manager = FactionManager()
    
    print("Skyrim Faction Logic Manager")
    print("============================\n")
    
    print("1. List All Factions")
    print("2. Check Faction Status")
    print("3. Update Faction Clock")
    print("4. Update Faction Relationship")
    print("5. Update Faction Resources")
    print("6. Simulate Faction Turn")
    print("7. Faction Conflict Resolution")
    print("8. Exit")
    
    while True:
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == "1":
            manager.list_all_factions()
        
        elif choice == "2":
            faction_id = input("Faction ID: ").strip()
            manager.check_faction_status(faction_id)
        
        elif choice == "3":
            faction_id = input("Faction ID: ").strip()
            clock_name = input("Clock name: ").strip()
            change = input("Progress change (+/-): ").strip()
            manager.update_faction_clock(faction_id, clock_name, int(change))
        
        elif choice == "4":
            faction_id = input("Faction ID: ").strip()
            other_faction = input("Other faction ID: ").strip()
            change = input("Relationship change (+/-): ").strip()
            manager.update_faction_relationship(faction_id, other_faction, int(change))
        
        elif choice == "5":
            faction_id = input("Faction ID: ").strip()
            resource_type = input("Resource type: ").strip()
            change = input("Change amount (+/-): ").strip()
            manager.update_faction_resources(faction_id, resource_type, int(change))
        
        elif choice == "6":
            faction_id = input("Faction ID: ").strip()
            manager.simulate_faction_turn(faction_id)
        
        elif choice == "7":
            faction1 = input("Faction 1 ID: ").strip()
            faction2 = input("Faction 2 ID: ").strip()
            manager.faction_conflict_resolution(faction1, faction2)
        
        elif choice == "8":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()
