#!/usr/bin/env python3
"""
GM Tools for Skyrim TTRPG

This script provides Game Master tools for:
- Viewing ongoing clocks and their status
- Getting faction hooks and plot suggestions
- Response guidelines for situations
- Campaign overview and insights
- Quick reference to important data
"""

import json
import os
from pathlib import Path
from datetime import datetime
from utils import location_matches


class GMTools:
    def __init__(self, data_dir="../data", state_dir="../state"):
        self.data_dir = Path(data_dir)
        self.state_dir = Path(state_dir)
        self.npc_stat_sheets_dir = self.data_dir / "npc_stat_sheets"
        
    def load_json(self, filepath):
        """Helper to load JSON file"""
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    
    def view_all_clocks(self):
        """Display all active clocks in the campaign"""
        print("\n" + "="*70)
        print("ACTIVE CLOCKS OVERVIEW")
        print("="*70)
        
        # Faction clocks
        factions_data = self.load_json(self.data_dir / "factions.json")
        if factions_data:
            print("\n=== FACTION CLOCKS ===\n")
            
            for faction_id, faction in factions_data.get('major_factions', {}).items():
                if 'clocks' in faction:
                    print(f"{faction['name']}:")
                    for clock in faction['clocks']:
                        progress = clock['progress']
                        segments = clock['segments']
                        bar = '█' * progress + '░' * (segments - progress)
                        percentage = (progress / segments * 100) if segments > 0 else 0
                        
                        print(f"  {clock['name']}: [{bar}] {progress}/{segments} ({percentage:.0f}%)")
                        print(f"    Effect: {clock['effect']}")
                        
                        # Warnings
                        if progress >= segments:
                            print(f"    ⚠️  CLOCK FILLED!")
                        elif progress >= segments * 0.75:
                            print(f"    ⚠️  Almost full - {segments - progress} segments remaining")
                    print()
        
        # Thalmor arcs
        thalmor_data = self.load_json(self.data_dir / "thalmor_arcs.json")
        if thalmor_data:
            print("\n=== THALMOR PLOTS ===\n")
            
            for arc in thalmor_data.get('thalmor_overarching_arc', {}).get('arcs', []):
                print(f"{arc['name']}:")
                for phase in arc.get('phases', []):
                    progress = phase.get('clock_progress', 0)
                    segments = phase.get('clock_max', 10)
                    bar = '█' * progress + '░' * (segments - progress)
                    
                    print(f"  Phase {phase['phase']}: {phase['name']}")
                    print(f"    [{bar}] {progress}/{segments}")
                print()
        
        # Campaign state arcs
        campaign_state = self.load_json(self.state_dir / "campaign_state.json")
        if campaign_state:
            print("\n=== STORY ARCS ===\n")
            
            for arc in campaign_state.get('active_story_arcs', []):
                print(f"{arc['arc_name']}: {arc['status']}")
                print(f"  Progress: {arc['progress']}")
                print(f"  Next: {arc['next_milestone']}")
                print()
    
    def get_faction_hooks(self, faction_id=None):
        """Get plot hooks and current objectives for factions"""
        factions_data = self.load_json(self.data_dir / "factions.json")
        if not factions_data:
            print("Factions data not found")
            return
        
        print("\n" + "="*70)
        print("FACTION PLOT HOOKS")
        print("="*70)
        
        major_factions = factions_data.get('major_factions', {})
        
        if faction_id:
            # Show specific faction
            if faction_id in major_factions:
                faction = major_factions[faction_id]
                self._display_faction_hooks(faction_id, faction)
            else:
                print(f"Faction '{faction_id}' not found")
        else:
            # Show all factions
            for faction_id, faction in major_factions.items():
                self._display_faction_hooks(faction_id, faction)
                print()
    
    def _display_faction_hooks(self, faction_id, faction):
        """Display hooks for a specific faction"""
        print(f"\n{faction['name']} ({faction_id})")
        print("-" * 50)
        
        # Current goals
        print("Current Goals:")
        for goal in faction.get('goals', []):
            print(f"  • {goal}")
        
        # Clock-based hooks
        if 'clocks' in faction:
            print("\nActive Objectives (from clocks):")
            for clock in faction['clocks']:
                progress = clock['progress']
                segments = clock['segments']
                if progress < segments:
                    remaining = segments - progress
                    print(f"  • {clock['name']} ({remaining} segments to completion)")
                    
                    # Generate hook based on clock
                    if progress < segments * 0.3:
                        urgency = "Early stage"
                    elif progress < segments * 0.7:
                        urgency = "Mid-stage, gaining momentum"
                    else:
                        urgency = "⚠️ URGENT - Nearly complete!"
                    print(f"    Status: {urgency}")
        
        # Relationship-based hooks
        if 'relationships' in faction:
            conflicts = []
            allies = []
            
            for other_faction, value in faction['relationships'].items():
                if value <= -50:
                    conflicts.append(other_faction)
                elif value >= 50:
                    allies.append(other_faction)
            
            if conflicts:
                print(f"\nHostile to: {', '.join(conflicts)}")
                print("  Hook: Conflict with these factions could create missions")
            
            if allies:
                print(f"\nAllied with: {', '.join(allies)}")
                print("  Hook: Cooperation missions possible")
    
    def get_campaign_overview(self):
        """Get complete campaign status overview"""
        print("\n" + "="*70)
        print("CAMPAIGN OVERVIEW")
        print("="*70)
        
        campaign_state = self.load_json(self.state_dir / "campaign_state.json")
        if not campaign_state:
            print("Campaign state not found")
            return
        
        # Basic info
        print(f"\nCampaign: {campaign_state.get('campaign_name')}")
        print(f"Started: {campaign_state.get('started_date')}")
        print(f"Sessions: {campaign_state.get('session_count')}")
        print(f"Current Act: {campaign_state.get('current_act')}")
        
        # Civil War status
        civil_war = campaign_state.get('civil_war_state', {})
        print(f"\n--- Civil War ---")
        print(f"Player Alliance: {civil_war.get('player_alliance')}")
        print(f"Battle of Whiterun: {civil_war.get('battle_of_whiterun_status')}")
        print(f"Imperial Victories: {civil_war.get('imperial_victories')}")
        print(f"Stormcloak Victories: {civil_war.get('stormcloak_victories')}")
        
        # Main quest status
        main_quest = campaign_state.get('main_quest_state', {})
        print(f"\n--- Main Quest ---")
        print(f"Civil War Involvement: {main_quest.get('civil_war_involvement', True)}")
        print(f"Major Battles: {main_quest.get('battles_participated', 0)}")
        print(f"Faction Quests Completed: {len(main_quest.get('faction_quests_completed', []))}")
        
        # Thalmor threat
        thalmor = campaign_state.get('thalmor_arc', {})
        print(f"\n--- Thalmor Threat ---")
        print(f"Awareness of Party: {thalmor.get('thalmor_awareness_of_party')}")
        print(f"Embassy Infiltrated: {thalmor.get('embassy_infiltrated')}")
        print(f"Schemes Discovered: {len(thalmor.get('thalmor_schemes_discovered', []))}")
        
        # Active story arcs
        print(f"\n--- Active Story Arcs ---")
        for arc in campaign_state.get('active_story_arcs', []):
            print(f"{arc['arc_name']}: {arc['status']}")
            print(f"  Next: {arc['next_milestone']}")
        
        # Major decisions made
        print(f"\n--- Key Decisions Made ---")
        decisions = campaign_state.get('branching_decisions', {})
        for key, value in decisions.items():
            if value:
                print(f"  • {key}: {value}")
        
        # World consequences
        consequences = campaign_state.get('world_consequences', {})
        if consequences.get('npcs_killed'):
            print(f"\n--- Significant Deaths ---")
            for npc in consequences['npcs_killed']:
                print(f"  • {npc}")
        
        if consequences.get('towns_affected'):
            print(f"\n--- Towns Affected ---")
            for town in consequences['towns_affected']:
                print(f"  • {town}")
    
    def suggest_session_content(self):
        """Suggest content for the next session based on current state"""
        print("\n" + "="*70)
        print("NEXT SESSION SUGGESTIONS")
        print("="*70)
        
        campaign_state = self.load_json(self.state_dir / "campaign_state.json")
        if not campaign_state:
            print("Campaign state not found")
            return
        
        suggestions = []
        
        # Check main quest progression
        main_quest = campaign_state.get('main_quest_state', {})
        # Civil war is central, so always suggest advancing it
        suggestions.append({
            'priority': 'HIGH',
            'category': 'Civil War',
            'suggestion': 'Advance the Civil War storyline with battle preparations or faction missions'
        })
        
        # Check civil war
        civil_war = campaign_state.get('civil_war_state', {})
        if civil_war.get('player_alliance') == 'neutral':
            suggestions.append({
                'priority': 'MEDIUM',
                'category': 'Civil War',
                'suggestion': 'Pressure players to choose a side in the civil war'
            })
        
        if civil_war.get('battle_of_whiterun_status') == 'not_started':
            suggestions.append({
                'priority': 'HIGH',
                'category': 'Civil War',
                'suggestion': 'Battle of Whiterun is a major turning point - prepare for this'
            })
        
        # Check Thalmor threat
        thalmor = campaign_state.get('thalmor_arc', {})
        if not thalmor.get('embassy_infiltrated'):
            suggestions.append({
                'priority': 'MEDIUM',
                'category': 'Thalmor',
                'suggestion': 'Diplomatic Immunity quest - infiltrate Thalmor Embassy'
            })
        
        # Check active story arcs
        for arc in campaign_state.get('active_story_arcs', []):
            if arc['status'] == 'active':
                suggestions.append({
                    'priority': 'MEDIUM',
                    'category': 'Story Arc',
                    'suggestion': f"{arc['arc_name']}: {arc['next_milestone']}"
                })
        
        # Display suggestions
        for priority in ['HIGH', 'MEDIUM', 'LOW']:
            priority_suggestions = [s for s in suggestions if s['priority'] == priority]
            if priority_suggestions:
                print(f"\n{priority} PRIORITY:")
                for sug in priority_suggestions:
                    print(f"  [{sug['category']}] {sug['suggestion']}")
        
        # Additional GM tips
        print("\n--- GM Tips ---")
        print("• Balance combat, social, and exploration encounters")
        print("• Use faction clocks to create time pressure")
        print("• Offer meaningful choices with real consequences")
        print("• Let players drive the narrative")
    
    def quick_reference(self, topic):
        """Quick reference for common GM needs"""
        references = {
            'difficulty': """
FATE CORE DIFFICULTY LADDER:
• Legendary (+8)
• Epic (+7)
• Fantastic (+6)
• Superb (+5)
• Great (+4)
• Good (+3)
• Fair (+2)
• Average (+1)
• Mediocre (0)
• Poor (-1)
• Terrible (-2)
            """,
            'combat': """
COMBAT GUIDELINES:
• Average enemy: +1 to +2
• Tough enemy: +3 to +4
• Boss enemy: +5 to +6
• Legendary enemy: +7+

Stress boxes:
• Mooks: 1 stress, taken out immediately
• Minions: 2 stress boxes
• Standard NPCs: 2-3 stress boxes
• Important NPCs: 3-4 stress boxes + consequences
            """,
            'rewards': """
REWARD GUIDELINES:
Gold:
• Minor quest: 50-100 gold
• Standard quest: 100-250 gold
• Major quest: 250-500 gold
• Epic quest: 500-1000+ gold

Experience/Milestones:
• Minor milestone: Every 1-2 sessions
• Significant milestone: Every 3-4 sessions
• Major milestone: End of story arc (8-12 sessions)
            """,
            'social': """
SOCIAL ENCOUNTER GUIDELINES:
• Use Rapport for building trust
• Use Deceive for lies and misdirection
• Use Provoke for intimidation
• Use Empathy to read people
• Use Notice to spot tells

NPC attitudes:
• Hostile: -2 to social rolls
• Unfriendly: -1 to social rolls
• Neutral: +0
• Friendly: +1 to social rolls
• Allied: +2 to social rolls
            """
        }
        
        if topic.lower() in references:
            print(references[topic.lower()])
        else:
            print("Available topics: difficulty, combat, rewards, social")
    
    def generate_random_encounter(self):
        """Generate a random encounter suggestion"""
        import random
        
        encounters = [
            "Bandit ambush on the road",
            "Dragon sighting in the distance",
            "Thalmor patrol questioning travelers",
            "Merchant caravan under attack",
            "Ancient Nord ruins discovered",
            "Mysterious traveler with information",
            "Wildlife attack (bear, wolves, sabre cat)",
            "Civil war skirmish nearby",
            "Necromancer raising dead",
            "Vampire attack at night",
            "Giant and mammoths blocking path",
            "Forsworn raiders",
            "Haunted barrow with draugr",
            "Daedric cultists performing ritual",
            "Injured adventurer needs help"
        ]
        
        encounter = random.choice(encounters)
        difficulty = random.choice(['Easy (+1)', 'Average (+2)', 'Fair (+3)', 'Tough (+4)'])
        
        print(f"\n=== Random Encounter ===")
        print(f"Encounter: {encounter}")
        print(f"Difficulty: {difficulty}")
        print(f"\nGM Tip: Tie this to ongoing story arcs when possible")
    
    def suggest_npc_stats_for_scene(self, location=None, scene_type=None):
        """
        Suggest appropriate NPC/enemy stat blocks for a scene
        
        Args:
            location: Scene location (e.g., "Whiterun", "Nordic ruins")
            scene_type: Type of scene ("combat", "dialogue", "exploration")
        """
        print("\n" + "="*70)
        print("NPC/ENEMY STAT SUGGESTIONS")
        print("="*70)
        
        if not self.npc_stat_sheets_dir.exists():
            print("No stat sheets directory found")
            return
        
        suggestions = {
            'available': [],
            'recommended': []
        }
        
        # Load all stat sheets
        for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
            try:
                with open(stat_file, 'r') as f:
                    stat_sheet = json.load(f)
                
                # Filter by location if provided (partial match in either direction)
                if location:
                    sheet_location = stat_sheet.get('location', '')
                    if not location_matches(location, sheet_location):
                        continue
                
                suggestions['available'].append(stat_sheet)
                
                # Check scene triggers for recommendations
                scene_triggers = stat_sheet.get('scene_triggers', [])
                if scene_type:
                    for trigger in scene_triggers:
                        if scene_type.lower() in trigger.lower():
                            suggestions['recommended'].append(stat_sheet)
                            break
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Error reading {stat_file.name}: {e}")
                continue
        
        # Display results
        print(f"\nLocation: {location or 'Any'}")
        print(f"Scene Type: {scene_type or 'Any'}")
        
        if suggestions['recommended']:
            print(f"\n--- Recommended for This Scene ({len(suggestions['recommended'])}) ---")
            for stat in suggestions['recommended']:
                print(f"\n• {stat['name']} ({stat['category']})")
                print(f"  Type: {stat['type']}")
                print(f"  High Concept: {stat['aspects']['high_concept']}")
                if 'combat_tactics' in stat:
                    print(f"  Tactics: {stat['combat_tactics'][:100]}...")
        
        if suggestions['available']:
            print(f"\n--- All Available ({len(suggestions['available'])}) ---")
            for stat in suggestions['available']:
                category_symbol = "☺" if stat['category'] == "Friendly NPC" else "☠"
                print(f"  {category_symbol} {stat['name']} - {stat['type']}")
        
        if not suggestions['available']:
            print("\nNo stat sheets match the criteria")
            print("Consider using generic enemies or creating custom NPCs")
    
    def inject_npc_stats_to_combat(self, enemy_types, difficulty="average"):
        """
        Inject NPC/enemy stats into a combat encounter
        
        Args:
            enemy_types: List of enemy types (e.g., ["bandit", "draugr"])
            difficulty: Encounter difficulty ("easy", "average", "hard", "deadly")
        """
        print("\n" + "="*70)
        print("COMBAT ENCOUNTER SETUP")
        print("="*70)
        
        if not self.npc_stat_sheets_dir.exists():
            print("No stat sheets directory found")
            return
        
        print(f"\nDifficulty: {difficulty.upper()}")
        print(f"Enemy Types: {', '.join(enemy_types)}")
        
        # Determine number of enemies based on difficulty
        enemy_counts = {
            'easy': 1,
            'average': 2,
            'hard': 3,
            'deadly': 4
        }
        count = enemy_counts.get(difficulty.lower(), 2)
        
        print(f"\n--- Suggested Enemy Composition ---")
        print(f"Number of enemies: {count}")
        
        # Find matching stat sheets (avoid duplicates)
        encounter_enemies = []
        seen_ids = set()
        
        for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
            try:
                with open(stat_file, 'r') as f:
                    stat_sheet = json.load(f)
                
                stat_id = stat_sheet.get('id')
                
                # Check if enemy type matches and not already added
                if stat_id not in seen_ids:
                    for enemy_type in enemy_types:
                        if (enemy_type.lower() in stat_sheet.get('name', '').lower() or
                            enemy_type.lower() in stat_sheet.get('type', '').lower()):
                            encounter_enemies.append(stat_sheet)
                            seen_ids.add(stat_id)
                            break
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Error reading {stat_file.name}: {e}")
                continue
        
        # Display encounter
        if encounter_enemies:
            print("\n--- Enemy Stat Blocks ---")
            for i, enemy in enumerate(encounter_enemies[:count], 1):
                print(f"\n{i}. {enemy['name']}")
                print(f"   Type: {enemy['type']}")
                print(f"   High Concept: {enemy['aspects']['high_concept']}")
                
                # Display key stats
                print(f"\n   Skills:")
                for level, skills in enemy['skills'].items():
                    if isinstance(skills, list):
                        print(f"     {level}: {', '.join(skills)}")
                
                print(f"\n   Stress: Physical [{len(enemy['stress'].get('physical', []))}]", end="")
                if enemy['stress'].get('mental'):
                    print(f", Mental [{len(enemy['stress']['mental'])}]")
                else:
                    print()
                
                print(f"\n   Key Stunts:")
                for stunt in enemy.get('stunts', [])[:2]:
                    print(f"     • {stunt}")
                
                if 'combat_tactics' in enemy:
                    print(f"\n   Tactics: {enemy['combat_tactics'][:150]}...")
        else:
            print("\nNo matching enemies found in stat sheets")
        
        # GM tips
        print("\n--- GM Tips ---")
        print("• Use zones for tactical positioning")
        print("• Create environmental aspects")
        print("• Track stress and consequences carefully")
        print("• Apply combat consequences to world state after encounter")
    
    def get_npc_relationship_advice(self, npc_name):
        """Get advice on managing NPC relationships"""
        print("\n" + "="*70)
        print(f"RELATIONSHIP MANAGEMENT: {npc_name}")
        print("="*70)
        
        # Try to find NPC in stat sheets
        npc_data = None
        if self.npc_stat_sheets_dir.exists():
            for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
                try:
                    with open(stat_file, 'r') as f:
                        stat_sheet = json.load(f)
                    
                    if npc_name.lower() in stat_sheet.get('name', '').lower():
                        npc_data = stat_sheet
                        break
                except (json.JSONDecodeError, IOError):
                    continue
        
        if npc_data:
            print(f"\nNPC: {npc_data['name']}")
            print(f"Type: {npc_data['type']}")
            
            if 'trust_clock' in npc_data and npc_data['trust_clock'].get('enabled'):
                trust = npc_data['trust_clock']
                print(f"\nTrust Clock: {trust['current']}/{trust['max']}")
                print(f"Description: {trust['description']}")
            
            if 'relationships' in npc_data:
                print("\nKnown Relationships:")
                for entity, relationship in npc_data['relationships'].items():
                    print(f"  • {entity}: {relationship}")
            
            if 'personality_notes' in npc_data:
                notes = npc_data['personality_notes']
                print("\nPersonality:")
                print(f"  Speaking Style: {notes.get('speaking_style', 'N/A')}")
                if 'motivations' in notes:
                    print(f"  Motivations: {', '.join(notes['motivations'][:3])}")
                if 'fears' in notes:
                    print(f"  Fears: {', '.join(notes['fears'][:3])}")
            
            print("\n--- Relationship Advice ---")
            if npc_data.get('category') == 'Friendly NPC':
                print("• Build trust through helpful actions")
                print("• Respect their faction and beliefs")
                print("• Use their trust clock to track relationship")
            elif npc_data.get('category') == 'Hostile NPC':
                print("• Hostility can sometimes be overcome with diplomacy")
                print("• Actions against their faction will worsen relations")
                print("• Consider long-term consequences of conflicts")
        else:
            print(f"\nNPC '{npc_name}' not found in stat sheets")
            print("\n--- General Relationship Advice ---")
            print("• Track relationships in character sheets")
            print("• Use aspects to reflect relationship status")
            print("• Create relationship clocks for ongoing developments")
            print("• Make relationship changes feel earned through roleplay")
    
    def tri_check_result(self, successes):
        """
        Determine outcome narrative for a Tri-Check (3-roll challenge) based on successes.
        
        Args:
            successes (int): Number of successful checks out of 3 (0-3).
        """
        print("\n" + "="*70)
        print("TRI-CHECK OUTCOME")
        print("="*70)
        if successes >= 3:
            # All three checks succeeded – overwhelming success
            print("★ **Full Success (3/3)**: You accomplish your goal brilliantly. Everything goes in the party's favor with added benefits.")
            print("Narrative: The plan not only works, it exceeds expectations. No complications – maybe even a bonus reward or advantage.")
        elif successes == 2:
            # Two successes – success with a minor cost
            print("✓ **Major Success (2/3)**: You succeed, but with a small cost or complication.")
            print("Narrative: The party achieves the goal, but perhaps they expend extra resources or suffer a minor consequence in the process.")
        elif successes == 1:
            # One success – success at a significant cost, or a mixed outcome
            print("≈ **Partial Success (1/3)**: You only partly succeed, or succeed but with a serious cost.")
            print("Narrative: The goal is achieved *barely*. Expect a major complication or harm – success comes at a price that changes the situation.")
        else:
            # 0 successes – failure that still moves the story forward
            print("✘ **Failure (0/3)**: You do not succeed, but the story moves forward with consequences.")
            print("Narrative: The attempt fails or causes a serious setback. The party must deal with fallout, but the GM should ensure this propels the story (not a dead end).")
    
    def review_companion_loyalty(self):
        """
        Review active companions' loyalty and suggest narrative consequences or unlocks.
        """
        campaign_state = self.load_json(self.state_dir / "campaign_state.json")
        if not campaign_state or "companions" not in campaign_state:
            print("No companions data found in campaign state.")
            return
        active_comps = campaign_state["companions"].get("active_companions", [])
        if not active_comps:
            print("No active companions in party.")
            return

        print("\n" + "="*70)
        print("COMPANION LOYALTY REVIEW")
        print("="*70)
        for comp in active_comps:
            name = comp.get("name", "Unknown")
            loyalty = comp.get("loyalty", 0)
            npc_id = comp.get("npc_id")
            
            # Skip companions with missing npc_id
            if not npc_id:
                print(f"\n{name} – Loyalty {loyalty}/100.")
                print("⚠️  Warning: No NPC ID found for this companion. Cannot load detailed information.")
                continue
            
            # Load companion's full stat sheet for thresholds and quests
            # Try both npc_id.json and search by ID in files
            stat = self.load_json(self.npc_stat_sheets_dir / f"{npc_id}.json")
            if not stat and self.npc_stat_sheets_dir.exists():
                # If file not found by npc_id, search all stat sheets for matching ID
                for stat_file in self.npc_stat_sheets_dir.glob("*.json"):
                    try:
                        with open(stat_file, 'r') as f:
                            stat_sheet = json.load(f)
                        if stat_sheet.get('id') == npc_id:
                            stat = stat_sheet
                            break
                    except (json.JSONDecodeError, IOError):
                        continue
            
            threshold_desc = None
            if stat and "companion_mechanics" in stat:
                thresholds = stat["companion_mechanics"].get("loyalty_thresholds", {})
                # Determine which threshold bracket the loyalty falls into
                if loyalty >= 80 and "80+" in thresholds:
                    threshold_desc = thresholds["80+"]
                elif loyalty >= 60 and "60-79" in thresholds:
                    threshold_desc = thresholds["60-79"]
                elif loyalty >= 40 and "40-59" in thresholds:
                    threshold_desc = thresholds["40-59"]
                elif loyalty >= 20 and "20-39" in thresholds:
                    threshold_desc = thresholds["20-39"]
                elif "0-19" in thresholds:
                    threshold_desc = thresholds["0-19"]
            
            # Print status
            status_line = f"{name} – Loyalty {loyalty}/100."
            if threshold_desc:
                status_line += f" Status: {threshold_desc}"
            print("\n" + status_line)
            
            # Warn if stat sheet not found
            if not stat:
                print(f"⚠️  Warning: Stat sheet not found for {name} ({npc_id}). Detailed information unavailable.")
            
            # Warnings or events based on loyalty
            if loyalty <= 20:
                print("⚠️  Low loyalty! This companion may refuse orders or leave the party soon.")
            elif loyalty >= 80:
                print("🤝 High loyalty! This companion is deeply bonded and may even sacrifice themselves for the party.")
            # Check for companion-specific quests unlocked by loyalty
            if stat and "companion_mechanics" in stat:
                for quest in stat["companion_mechanics"].get("companion_quests", []):
                    req = quest.get("loyalty_required", 0)
                    if loyalty >= req:
                        print(f"📜 Quest Unlocked: **{quest['name']}** – {quest['description']} (Reward: {quest.get('reward', 'N/A')})")


def main():
    """Main function"""
    tools = GMTools()
    
    print("Skyrim GM Tools")
    print("===============\n")
    
    print("1. View All Clocks")
    print("2. Get Faction Hooks")
    print("3. Campaign Overview")
    print("4. Suggest Session Content")
    print("5. Quick Reference")
    print("6. Generate Random Encounter")
    print("7. Suggest NPC Stats for Scene")
    print("8. Inject NPC Stats to Combat")
    print("9. Get NPC Relationship Advice")
    print("10. Tri-Check System Resolution")
    print("11. Review Companion Loyalty")
    print("12. Exit")
    
    while True:
        choice = input("\nEnter choice (1-12): ").strip()
        
        if choice == "1":
            tools.view_all_clocks()
        
        elif choice == "2":
            faction_id = input("Faction ID (or blank for all): ").strip()
            tools.get_faction_hooks(faction_id if faction_id else None)
        
        elif choice == "3":
            tools.get_campaign_overview()
        
        elif choice == "4":
            tools.suggest_session_content()
        
        elif choice == "5":
            topic = input("Topic (difficulty/combat/rewards/social): ").strip()
            tools.quick_reference(topic)
        
        elif choice == "6":
            tools.generate_random_encounter()
        
        elif choice == "7":
            location = input("Scene location (or blank for any): ").strip()
            scene_type = input("Scene type (combat/dialogue/exploration, or blank): ").strip()
            tools.suggest_npc_stats_for_scene(
                location if location else None,
                scene_type if scene_type else None
            )
        
        elif choice == "8":
            enemy_types_input = input("Enemy types (comma-separated, e.g., 'bandit,draugr'): ").strip()
            enemy_types = [e.strip() for e in enemy_types_input.split(',')]
            difficulty = input("Difficulty (easy/average/hard/deadly): ").strip()
            tools.inject_npc_stats_to_combat(enemy_types, difficulty)
        
        elif choice == "9":
            npc_name = input("NPC name: ").strip()
            tools.get_npc_relationship_advice(npc_name)
        
        elif choice == "10":
            successes_input = input("Number of successes (0-3): ").strip()
            try:
                successes = int(successes_input)
                if 0 <= successes <= 3:
                    tools.tri_check_result(successes)
                else:
                    print("Please enter a number between 0 and 3")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 3")
        
        elif choice == "11":
            tools.review_companion_loyalty()
        
        elif choice == "12":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1-12.")


if __name__ == "__main__":
    main()
