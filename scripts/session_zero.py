#!/usr/bin/env python3
"""
Session Zero Script for Skyrim TTRPG

This script guides players through:
- Character creation
- Race selection
- Standing Stone choice
- Faction alignment
- Backstory development
- Campaign setup
"""

import json
import os
from pathlib import Path
from datetime import datetime


# Faction name mapping for consistency
FACTION_NAME_MAPPING = {
    "college": "college_of_winterhold",
    "college_of_winterhold": "college_of_winterhold",
    "companions": "companions",
    "thieves_guild": "thieves_guild",
    "dark_brotherhood": "dark_brotherhood",
    "blades": "blades",
    "greybeards": "greybeards"
}

# Fate Core skill list for Skyrim
SKYRIM_SKILLS = [
    "Fight",
    "Shoot",
    "Athletics",
    "Physique",
    "Notice",
    "Stealth",
    "Lore",
    "Will",
    "Rapport",
    "Deceive",
    "Empathy",
    "Crafts",
    "Survival"
]

# Fate Core skill pyramid structure
SKILL_PYRAMID = {
    "Great (+4)": 1,
    "Good (+3)": 2,
    "Fair (+2)": 3,
    "Average (+1)": 4
}

# Validation constants
MIN_STUNT_LENGTH = 10  # Minimum characters for a meaningful stunt description


class SessionZeroManager:
    def __init__(self, data_dir="../data", state_dir="../state"):
        self.data_dir = Path(data_dir)
        self.state_dir = Path(state_dir)
        self.source_material_dir = self.data_dir.parent / "source_material" / "converted_pdfs"
        
    def load_races(self):
        """Load race data from converted PDFs"""
        races_file = self.source_material_dir / "races.json"
        if races_file.exists():
            with open(races_file, 'r') as f:
                data = json.load(f)
                return data.get('races', [])
        return []
    
    def load_standing_stones(self):
        """Load standing stone data from converted PDFs"""
        stones_file = self.source_material_dir / "standing_stones.md"
        if stones_file.exists():
            with open(stones_file, 'r') as f:
                content = f.read()
                return content
        return ""
    
    def display_races(self):
        """Display available races"""
        print("\n" + "="*60)
        print("PLAYABLE RACES IN SKYRIM")
        print("="*60)
        
        races = self.load_races()
        for i, race in enumerate(races, 1):
            print(f"\n{i}. {race['name']}")
            print(f"   {race['description']}")
            print(f"   Racial Ability: {race['racial_ability']['name']}")
            print(f"   - {race['racial_ability']['effect']}")
            if 'power' in race:
                print(f"   Racial Power: {race['power']['name']}")
                print(f"   - {race['power']['effect']}")
            print(f"   Skill Bonuses: {', '.join(race['skill_bonuses'])}")
        
        print("\n" + "="*60)
    
    def display_standing_stones(self):
        """Display standing stones information"""
        print("\n" + "="*60)
        print("STANDING STONES OF SKYRIM")
        print("="*60)
        
        # Display summary of main stones
        stones_summary = [
            {
                "name": "The Warrior Stone",
                "effect": "Once per session, +2 to Fight, Shoot, or Athletics in combat",
                "for": "Warriors, Berserkers, Soldiers"
            },
            {
                "name": "The Mage Stone",
                "effect": "Once per session, +2 to Lore for magic or spellcasting",
                "for": "Wizards, Healers, Scholars"
            },
            {
                "name": "The Thief Stone",
                "effect": "Once per session, +2 to Stealth, Deceive, or Notice",
                "for": "Thieves, Assassins, Scouts"
            },
            {
                "name": "The Ritual Stone",
                "effect": "Once per session, reanimate dead to fight for you",
                "for": "Necromancers, Dark mages"
            },
            {
                "name": "The Serpent Stone",
                "effect": "Once per session, paralyze an enemy",
                "for": "Assassins, Control specialists"
            },
            {
                "name": "The Shadow Stone",
                "effect": "Once per session, become invisible",
                "for": "Thieves, Spies"
            },
            {
                "name": "The Steed Stone",
                "effect": "+1 Athletics, ignore armor stealth penalties",
                "for": "Mobile fighters, Scouts"
            },
            {
                "name": "The Lord Stone",
                "effect": "+1 Defend vs physical, +1 Will vs magic",
                "for": "Tanks, Defenders"
            },
            {
                "name": "The Lady Stone",
                "effect": "Recover 1 extra physical stress per scene",
                "for": "Sustained fighters"
            },
            {
                "name": "The Lover Stone",
                "effect": "Bonus milestone progress",
                "for": "Versatile characters"
            },
            {
                "name": "The Atronach Stone",
                "effect": "+2 Lore for magic, but magicka doesn't regenerate naturally",
                "for": "Power mages willing to trade"
            },
            {
                "name": "The Tower Stone",
                "effect": "Once per session, auto-open Average lock",
                "for": "Thieves, Explorers"
            }
        ]
        
        for stone in stones_summary:
            print(f"\n{stone['name']}")
            print(f"  Effect: {stone['effect']}")
            print(f"  Best for: {stone['for']}")
        
        print("\n" + "="*60)
        print("Note: You can change your Standing Stone during play by visiting it in-game")
        print("="*60)
    
    def display_factions(self):
        """Display major factions for alignment"""
        print("\n" + "="*60)
        print("MAJOR FACTIONS IN SKYRIM")
        print("="*60)
        
        factions = [
            {
                "name": "Imperial Legion",
                "description": "The military force of the Empire, fighting to keep Skyrim united",
                "alignment": "Lawful, Order-focused",
                "leader": "General Tullius"
            },
            {
                "name": "Stormcloaks",
                "description": "Rebel faction fighting for Skyrim's independence from the Empire",
                "alignment": "Freedom fighters, Nord-focused",
                "leader": "Ulfric Stormcloak"
            },
            {
                "name": "The Companions",
                "description": "Ancient warrior guild based in Whiterun, honor-bound fighters",
                "alignment": "Neutral, Honor-focused",
                "leader": "Kodlak Whitemane"
            },
            {
                "name": "Thieves Guild",
                "description": "Criminal organization based in Riften, dedicated to stealth and thievery",
                "alignment": "Chaotic Neutral, Profit-focused",
                "leader": "Mercer Frey"
            },
            {
                "name": "Dark Brotherhood",
                "description": "Assassins guild devoted to Sithis and the Night Mother",
                "alignment": "Chaotic Evil, Murder-for-hire",
                "leader": "Astrid (Sanctuary leader)"
            },
            {
                "name": "College of Winterhold",
                "description": "Mages guild dedicated to magical study and research",
                "alignment": "Neutral, Knowledge-focused",
                "leader": "Arch-Mage Savos Aren"
            },
            {
                "name": "The Greybeards",
                "description": "Monks who study the Way of the Voice atop High Hrothgar",
                "alignment": "Lawful Neutral, Peace-focused",
                "leader": "Master Arngeir"
            }
        ]
        
        for faction in factions:
            print(f"\n{faction['name']}")
            print(f"  Description: {faction['description']}")
            print(f"  Alignment: {faction['alignment']}")
            print(f"  Leader: {faction['leader']}")
        
        print("\n" + "="*60)
        print("Note: You can join multiple factions during play")
        print("Some factions conflict with each other (Imperial vs Stormcloak)")
        print("="*60)
    
    def display_civil_war_context(self):
        """Display the Battle of Whiterun context and faction choices"""
        print("\n" + "="*60)
        print("THE BATTLE OF WHITERUN - FACTION ALIGNMENT")
        print("="*60)
        print("\nSkyrim is torn by civil war. The Imperial Legion and the Stormcloak")
        print("Rebellion both seek to control Whiterun, the heart of Skyrim.")
        print("\nJarl Balgruuf the Greater has tried to remain neutral, but the")
        print("Battle of Whiterun approaches. Every adventurer must choose where")
        print("they stand in this conflict.")
        print("\n" + "="*60)
        print("FACTION CHOICES")
        print("="*60)
        
        factions = [
            {
                "name": "Imperial Legion",
                "stance": "Support the Empire and defend Whiterun alongside Imperial forces",
                "alignment": "imperial",
                "pros": [
                    "Part of a larger, organized military",
                    "Access to Imperial resources and gold",
                    "Maintain law and order",
                    "Defend against Stormcloak aggression"
                ],
                "cons": [
                    "Forced alliance with the Thalmor",
                    "Seen as foreign occupiers by some Nords",
                    "May need to compromise Nord traditions"
                ]
            },
            {
                "name": "Stormcloak Rebellion",
                "stance": "Fight for Skyrim's independence and assault Whiterun for the rebellion",
                "alignment": "stormcloak",
                "pros": [
                    "Fight for Nord sovereignty and freedom",
                    "Restore Talos worship openly",
                    "Expel the Thalmor from Skyrim",
                    "Return to traditional Nord values"
                ],
                "cons": [
                    "Seen as rebels and traitors by the Empire",
                    "Limited resources and supply lines",
                    "Risk fracturing Skyrim's unity",
                    "May face racial prejudice concerns"
                ]
            },
            {
                "name": "Neutral Factions",
                "stance": "Align with neutral groups like the Companions, focusing on honor over politics",
                "alignment": "neutral",
                "pros": [
                    "Maintain independence from both sides",
                    "Focus on honor, skill, or magical study",
                    "Flexibility to help either side on your terms",
                    "Avoid being pulled into factional conflicts"
                ],
                "cons": [
                    "Both sides may distrust you",
                    "Limited access to faction-specific resources",
                    "May be caught in the crossfire",
                    "Harder to influence the war's outcome"
                ],
                "examples": "The Companions, College of Winterhold, Thieves Guild"
            }
        ]
        
        for faction in factions:
            print(f"\n{faction['name']}")
            print(f"  Stance: {faction['stance']}")
            print(f"  Pros:")
            for pro in faction['pros']:
                print(f"    + {pro}")
            print(f"  Cons:")
            for con in faction['cons']:
                print(f"    - {con}")
            if 'examples' in faction:
                print(f"  Examples: {faction['examples']}")
        
        print("\n" + "="*60)
        print("Your choice will shape your starting narrative and relationships.")
        print("This choice matters for the Battle of Whiterun and beyond!")
        print("="*60)
    
    def create_character_template(self, player_name, character_name, race, standing_stone):
        """Create a character template JSON"""
        races = self.load_races()
        selected_race = None
        
        for r in races:
            if r['name'].lower() == race.lower():
                selected_race = r
                break
        
        if not selected_race:
            print(f"Warning: Race '{race}' not found in data")
            return None
        
        # Sanitize character name for ID generation
        import re
        sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', character_name.lower())
        sanitized_name = re.sub(r'_+', '_', sanitized_name).strip('_')
        
        character = {
            "name": character_name,
            "id": f"pc_{sanitized_name}",
            "player": player_name,
            "race": selected_race['name'],
            "standing_stone": standing_stone,
            "level": 1,
            "aspects": {
                "high_concept": f"{selected_race['starting_aspect']}",
                "trouble": "[Player to define - Required]",
                "other_aspects": []  # Will be filled during interactive session
            },
            "skills": {
                "Great (+4)": [],
                "Good (+3)": [],
                "Fair (+2)": [],
                "Average (+1)": []
            },
            "racial_bonuses": {
                "ability": selected_race['racial_ability'],
                "power": selected_race.get('power', {}),
                "skill_bonuses": selected_race['skill_bonuses']
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
            "stunts": [],  # Will be filled during interactive session (3 stunts required)
            "refresh": 3,
            "fate_points": 3,
            "equipment": {
                "weapons": [],
                "armor": [],
                "items": []
            },
            "gold": 100,
            "experience": 0,
            "backstory": "[Player to define during Session Zero]",
            "relationships": {},
            "quests": [],
            "session_history": [],
            "notes": "Created during Session Zero"
        }
        
        return character
    
    def save_character(self, character):
        """Save character to data/pcs/ directory"""
        pcs_dir = self.data_dir / "pcs"
        pcs_dir.mkdir(exist_ok=True)
        
        filename = f"{character['id']}.json"
        filepath = pcs_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(character, f, indent=2)
        
        print(f"\nCharacter saved to: {filepath}")
        return filepath
    
    def prompt_for_aspects(self, character):
        """Prompt player to define High Concept, Trouble, and additional aspects"""
        print("\n" + "="*60)
        print("ASPECTS - Define Your Character")
        print("="*60)
        print("\nAspects are phrases that describe who your character is.")
        print("They can be invoked for bonuses or compelled for fate points.")
        
        # High Concept
        print("\n--- HIGH CONCEPT ---")
        print("Your High Concept is the core of your character.")
        print(f"Current: {character['aspects']['high_concept']}")
        print("You can keep this or create your own.")
        print("Examples: 'Nord Warrior Seeking Redemption', 'Cunning Thief with a Heart of Gold'")
        
        high_concept = input("\nHigh Concept (press Enter to keep current): ").strip()
        if high_concept:
            character['aspects']['high_concept'] = high_concept
        
        # Trouble
        print("\n--- TROUBLE ---")
        print("Your Trouble is a complication that makes life interesting.")
        print("Examples: 'Haunted by Past Mistakes', 'Wanted by the Thalmor', 'Can't Resist a Challenge'")
        
        trouble = ""
        while not trouble:
            trouble = input("\nTrouble (required): ").strip()
            if not trouble:
                print("⚠️  Trouble is required! It's what makes your character interesting.")
        character['aspects']['trouble'] = trouble
        
        # Additional Aspects (1-3)
        print("\n--- ADDITIONAL ASPECTS ---")
        print("You can define 1-3 additional aspects.")
        print("Examples: 'Defender of the Weak', 'Bond with a Companion', 'Distrusts Magic Users'")
        
        other_aspects = []
        for i in range(3):
            print(f"\nAspect {i+1} of 3 (press Enter to skip):")
            aspect = input("  > ").strip()
            if aspect:
                other_aspects.append(aspect)
            elif i == 0:
                # First aspect is required
                print("⚠️  You need at least 1 additional aspect!")
                while not aspect:
                    aspect = input("  > ").strip()
                other_aspects.append(aspect)
        
        character['aspects']['other_aspects'] = other_aspects
        
        print("\n✓ Aspects defined:")
        print(f"  High Concept: {character['aspects']['high_concept']}")
        print(f"  Trouble: {character['aspects']['trouble']}")
        for i, aspect in enumerate(other_aspects, 1):
            print(f"  Aspect {i}: {aspect}")
    
    def prompt_for_skills(self, character):
        """Prompt player to select skills following the Fate Core pyramid"""
        print("\n" + "="*60)
        print("SKILLS - Build Your Skill Pyramid")
        print("="*60)
        print("\nFate Core uses a skill pyramid:")
        print("  - 1 skill at Great (+4)")
        print("  - 2 skills at Good (+3)")
        print("  - 3 skills at Fair (+2)")
        print("  - 4 skills at Average (+1)")
        print("\nAvailable Skills:")
        for i, skill in enumerate(SKYRIM_SKILLS, 1):
            print(f"  {i:2d}. {skill}")
        
        selected_skills = set()
        
        # Select skills for each level
        for level_name, count in SKILL_PYRAMID.items():
            print(f"\n--- {level_name} ---")
            print(f"Select {count} skill(s):")
            
            level_skills = []
            for i in range(count):
                while True:
                    skill_input = input(f"  Skill {i+1} of {count}: ").strip()
                    
                    # Check if it's a number (index) or skill name
                    if skill_input.isdigit():
                        idx = int(skill_input) - 1
                        if 0 <= idx < len(SKYRIM_SKILLS):
                            skill = SKYRIM_SKILLS[idx]
                        else:
                            print(f"⚠️  Invalid number. Choose 1-{len(SKYRIM_SKILLS)}")
                            continue
                    else:
                        # Try to match skill name
                        skill = None
                        for s in SKYRIM_SKILLS:
                            if s.lower() == skill_input.lower():
                                skill = s
                                break
                        if not skill:
                            print(f"⚠️  '{skill_input}' is not a valid skill. Use number or exact name.")
                            continue
                    
                    if skill in selected_skills:
                        print(f"⚠️  {skill} already selected. Choose a different skill.")
                        continue
                    
                    level_skills.append(skill)
                    selected_skills.add(skill)
                    print(f"    ✓ {skill} at {level_name}")
                    break
            
            character['skills'][level_name] = level_skills
        
        print("\n✓ Skill Pyramid Complete:")
        for level_name, skills in character['skills'].items():
            if skills:
                print(f"  {level_name}: {', '.join(skills)}")
    
    def prompt_for_stunts(self, character):
        """Prompt player to create 3 stunts"""
        print("\n" + "="*60)
        print("STUNTS - Special Abilities")
        print("="*60)
        print("\nStunts are special abilities that make your character unique.")
        print("You start with 3 stunts.")
        print("\nStunt Format: [Name]: [Effect]")
        print("\nExamples:")
        print("  - Whirlwind Attack: Once per scene, attack all enemies in your zone")
        print("  - Battle Fury: +2 to Fight when you take a consequence")
        print("  - Shadow Step: +2 to Stealth when creating advantages in darkness")
        print("  - Arcane Shield: Spend a Fate Point to absorb one hit completely")
        
        stunts = []
        for i in range(3):
            print(f"\n--- Stunt {i+1} of 3 ---")
            stunt = ""
            while not stunt:
                stunt = input("Enter stunt: ").strip()
                if not stunt:
                    print("⚠️  Stunt is required!")
            stunts.append(stunt)
            print(f"  ✓ Added: {stunt}")
        
        character['stunts'] = stunts
        
        print("\n✓ Stunts defined:")
        for i, stunt in enumerate(stunts, 1):
            print(f"  {i}. {stunt}")
    
    def display_neutral_faction_starts(self):
        """Display specific neutral faction starting options"""
        print("\n" + "="*60)
        print("NEUTRAL FACTION STARTING PATHS")
        print("="*60)
        print("\nIf you choose a neutral alignment, you can start with one of these factions:")
        print("Each provides a unique path leading to the Battle of Whiterun.\n")
        
        neutral_starts = [
            {
                "faction": "The Companions",
                "contact": "Kodlak Whitemane",
                "start": "Begin in Jorrvaskr, Whiterun's mead hall",
                "mission": "Kodlak sends you to help defend Whiterun from threats",
                "description": "Honor-bound warriors who focus on glory, not politics"
            },
            {
                "faction": "Thieves Guild",
                "contact": "Brynjolf",
                "start": "Recruited in Riften's marketplace",
                "mission": "Deliver message to Olfrid Battle-Born in Whiterun",
                "description": "Criminal organization focused on profit and stealth"
            },
            {
                "faction": "College of Winterhold",
                "contact": "Tolfdir / Savos Aren",
                "start": "Student at the College",
                "mission": "Assist Farengar Secret-Fire's dragon research in Whiterun",
                "description": "Mages dedicated to magical study and knowledge"
            },
            {
                "faction": "Dark Brotherhood",
                "contact": "Astrid",
                "start": "Recruited by the Brotherhood",
                "mission": "Assassinate Jarl Balgruuf during the battle chaos",
                "description": "Assassins for hire, serving death itself"
            },
            {
                "faction": "The Blades",
                "contact": "Delphine",
                "start": "Meet in Riverwood",
                "mission": "Escort Delphine to meet Farengar about dragon research",
                "description": "Ancient dragon hunters rebuilding their order"
            },
            {
                "faction": "Greybeards",
                "contact": "Personal calling",
                "start": "Independent decision",
                "mission": "Intervene in civil war to protect innocent lives",
                "description": "Follow the Way of the Voice, seeking peace"
            }
        ]
        
        for i, start in enumerate(neutral_starts, 1):
            print(f"{i}. {start['faction']}")
            print(f"   Contact: {start['contact']}")
            print(f"   Starting Location: {start['start']}")
            print(f"   Mission: {start['mission']}")
            print(f"   Description: {start['description']}\n")
        
        print("="*60)
        print("All paths lead to the Battle of Whiterun, where you'll encounter")
        print("both Hadvar (Imperial) and Ralof (Stormcloak) and must choose whom to assist.")
        print("="*60)
    
    def get_neutral_faction_narrative(self, specific_faction=None):
        """Get narrative text for a specific neutral faction start"""
        narratives = {
            "companions": {
                "narrative": (
                    "You've proven yourself worthy to join the Companions, the ancient warrior guild of Jorrvaskr. "
                    "Harbinger Kodlak Whitemane speaks with you personally: 'Jarl Balgruuf has sent word that "
                    "Whiterun faces a threat. The Companions will not stand idle when innocent people need protection. "
                    "I'm sending you to assess the situation and defend those who cannot defend themselves. This isn't "
                    "about choosing sides in the civil war - this is about honor.' You arrive in Whiterun as the Battle "
                    "begins, seeing both Hadvar (Imperial) and Ralof (Stormcloak) rallying forces. You must choose whom to assist."
                ),
                "starting_faction": "companions",
                "key_npc": "kodlak_whitemane",
                "location": "Jorrvaskr, then Whiterun"
            },
            "thieves_guild": {
                "narrative": (
                    "Brynjolf found you in Riften's marketplace and saw potential. After proving yourself, he offers "
                    "a mission: 'I need you to head to Whiterun. Find Olfrid Battle-Born and deliver this message. "
                    "With the war heating up, we need to ensure our operations there stay... profitable.' You arrive "
                    "in Whiterun to find tensions at a breaking point. As you deliver Brynjolf's message to Olfrid, "
                    "news arrives that Stormcloak forces are approaching. The Battle of Whiterun is about to begin, "
                    "and you see both Hadvar and Ralof in the chaos. You must choose a side."
                ),
                "starting_faction": "thieves_guild",
                "key_npc": "brynjolf",
                "location": "Riften, then Whiterun"
            },
            "college": {
                "narrative": (
                    "At the College of Winterhold, Arch-Mage Savos Aren personally approves your assignment. 'The return "
                    "of dragons is no coincidence,' he tells you gravely. Tolfdir adds, 'Farengar Secret-Fire was one of "
                    "my students. He's researching dragon activity in Whiterun. Help him investigate - this could threaten "
                    "all of Skyrim.' You arrive in Whiterun to meet Farengar, but find the city preparing for battle. As "
                    "you're briefed on the research mission, alarms sound - Stormcloak forces approach. The Battle begins, "
                    "and you encounter both Hadvar and Ralof. You must choose whom to assist."
                ),
                "starting_faction": "college_of_winterhold",
                "key_npc": "tolfdir",
                "location": "College of Winterhold, then Whiterun"
            },
            "dark_brotherhood": {
                "narrative": (
                    "Astrid found you, tested you, and deemed you worthy of the Dark Brotherhood. She offers a contract: "
                    "'Jarl Balgruuf in Whiterun. The civil war's chaos provides perfect cover. Kill him during the battle "
                    "preparations, and no one will suspect the Brotherhood.' You arrive in Whiterun as the Battle erupts. "
                    "Chaos surrounds you - the perfect assassination opportunity. But as you watch Hadvar and Ralof meet "
                    "in the chaos, both trying to rally defenders, you must decide: Complete Astrid's contract, or choose "
                    "a side and protect the Jarl?"
                ),
                "starting_faction": "dark_brotherhood",
                "key_npc": "astrid",
                "location": "Dark Brotherhood Sanctuary, then Whiterun"
            },
            "blades": {
                "narrative": (
                    "Delphine reveals herself as one of the last Blades in Riverwood. 'Dragons have returned,' she says "
                    "urgently. 'I've been tracking them for years. I need someone I can trust to escort me to Whiterun - "
                    "Farengar Secret-Fire has research I need to see. The Thalmor are watching, and I can't risk traveling "
                    "alone.' You arrive in Whiterun with Delphine as the Battle erupts. She curses the timing - dragon "
                    "research will have to wait. 'Pick a side and fight,' she commands. 'We need to survive this before we "
                    "can deal with the real threat.' You see both Hadvar and Ralof rallying forces."
                ),
                "starting_faction": "blades",
                "key_npc": "delphine",
                "location": "Riverwood, then Whiterun"
            },
            "greybeards": {
                "narrative": (
                    "Following your own path and the teachings of peace from the Greybeards, you've come to Whiterun hoping "
                    "to help broker peace or at least protect innocent lives from the civil war. Master Arngeir's words echo "
                    "in your mind: 'True strength lies not in violence, but in restraint and wisdom.' However, as you arrive, "
                    "the Battle of Whiterun begins. Stormcloak forces assault the city, and Imperial defenders rally. In the "
                    "chaos, you encounter both Hadvar (Imperial) and Ralof (Stormcloak). Despite your hopes for peace, you "
                    "must choose whom to assist in this battle."
                ),
                "starting_faction": "greybeards",
                "key_npc": "arngeir",
                "location": "High Hrothgar, then Whiterun"
            }
        }
        
        if specific_faction and specific_faction in narratives:
            return narratives[specific_faction]
        return narratives
    
    def update_campaign_state(self, faction_alignment, characters, neutral_subfaction=None):
        """Update campaign_state.json with session zero results"""
        campaign_state_file = self.state_dir / "campaign_state.json"
        
        # Load existing campaign state
        if campaign_state_file.exists():
            with open(campaign_state_file, 'r') as f:
                campaign_state = json.load(f)
        else:
            # Create default campaign state if it doesn't exist
            campaign_state = {
                "campaign_id": "skyrim_fate_core_001",
                "campaign_name": "The Elder Scrolls: Skyrim - Fate Core Campaign",
                "started_date": "4E 201, 17th of Last Seed",
                "current_act": 1,
                "civil_war_state": {
                    "player_alliance": "neutral",
                    "battle_of_whiterun_status": "not_started",
                    "imperial_victories": 0,
                    "stormcloak_victories": 0,
                    "key_battles_completed": [],
                    "faction_relationship": {
                        "imperial_legion": 0,
                        "stormcloaks": 0
                    }
                },
                "main_quest_state": {},
                "thalmor_arc": {},
                "branching_decisions": {},
                "world_consequences": {},
                "active_story_arcs": [],
                "companions": {
                    "active_companions": [],
                    "available_companions": [],
                    "dismissed_companions": [],
                    "companion_relationships": {}
                },
                "session_count": 0
            }
        
        # Update with session zero data
        campaign_state["session_zero_completed"] = True
        campaign_state["starting_location"] = "Whiterun"
        campaign_state["civil_war_state"]["player_alliance"] = faction_alignment
        campaign_state["civil_war_state"]["battle_of_whiterun_status"] = "approaching"
        
        # Set initial faction relationships based on alignment
        if faction_alignment == "imperial":
            campaign_state["civil_war_state"]["faction_relationship"]["imperial_legion"] = 30
            campaign_state["civil_war_state"]["faction_relationship"]["stormcloaks"] = -20
        elif faction_alignment == "stormcloak":
            campaign_state["civil_war_state"]["faction_relationship"]["imperial_legion"] = -20
            campaign_state["civil_war_state"]["faction_relationship"]["stormcloaks"] = 30
        else:  # neutral
            campaign_state["civil_war_state"]["faction_relationship"]["imperial_legion"] = 0
            campaign_state["civil_war_state"]["faction_relationship"]["stormcloaks"] = 0
        
        # Initialize companions structure if it doesn't exist
        if "companions" not in campaign_state:
            campaign_state["companions"] = {
                "active_companions": [],
                "available_companions": [],
                "dismissed_companions": [],
                "companion_relationships": {}
            }
        
        # Add Hadvar or Ralof as starting companion based on faction alignment
        # Record the civil war entry contact decision
        if "branching_decisions" not in campaign_state:
            campaign_state["branching_decisions"] = {}
        
        if faction_alignment == "imperial":
            # Player met Hadvar through Imperial recruitment
            campaign_state["branching_decisions"]["civil_war_entry_contact"] = "Hadvar"
            
            # Add Hadvar to active companions
            hadvar_companion = {
                "npc_id": "npc_stat_hadvar",
                "name": "Hadvar",
                "status": "active",
                "loyalty": 60,
                "location": "With party",
                "recruitment_trigger": "Imperial Legion recruitment",
                "faction_affinity": "imperial_legion",
                "notes": "Met during Imperial recruitment. Pragmatic Imperial soldier with family connections in Riverwood."
            }
            campaign_state["companions"]["active_companions"].append(hadvar_companion)
            campaign_state["companions"]["companion_relationships"]["hadvar"] = 60
            
        elif faction_alignment == "stormcloak":
            # Player met Ralof through Stormcloak recruitment
            campaign_state["branching_decisions"]["civil_war_entry_contact"] = "Ralof"
            
            # Add Ralof to active companions
            ralof_companion = {
                "npc_id": "npc_stat_ralof",
                "name": "Ralof",
                "status": "active",
                "loyalty": 60,
                "location": "With party",
                "recruitment_trigger": "Stormcloak recruitment",
                "faction_affinity": "stormcloaks",
                "notes": "Met during Stormcloak recruitment. Passionate Stormcloak soldier with family connections in Riverwood."
            }
            campaign_state["companions"]["active_companions"].append(ralof_companion)
            campaign_state["companions"]["companion_relationships"]["ralof"] = 60
            
        else:  # neutral
            # For neutral alignment, make both available but neither active yet
            # GM can decide based on player RP which one they meet first
            campaign_state["branching_decisions"]["civil_war_entry_contact"] = "undecided"
            
            hadvar_available = {
                "npc_id": "npc_stat_hadvar",
                "name": "Hadvar",
                "status": "available",
                "loyalty": 50,
                "location": "Riverwood or Whiterun",
                "recruitment_condition": "Party encounters Hadvar and helps with Imperial-related task",
                "faction_affinity": "imperial_legion"
            }
            ralof_available = {
                "npc_id": "npc_stat_ralof",
                "name": "Ralof",
                "status": "available",
                "loyalty": 50,
                "location": "Riverwood or Stormcloak camps",
                "recruitment_condition": "Party encounters Ralof and helps with Stormcloak-related task",
                "faction_affinity": "stormcloaks"
            }
            campaign_state["companions"]["available_companions"].append(hadvar_available)
            campaign_state["companions"]["available_companions"].append(ralof_available)
        
        # Add player characters to campaign state
        campaign_state["player_characters"] = []
        for char in characters:
            campaign_state["player_characters"].append({
                "id": char["id"],
                "name": char["name"],
                "player": char["player"],
                "race": char["race"],
                "standing_stone": char["standing_stone"],
                "faction_alignment": char.get("faction_alignment", faction_alignment)
            })
        
        # Set starting narrative based on faction
        if faction_alignment == "imperial":
            campaign_state["starting_narrative"] = (
                "The party arrives in Whiterun as supporters of the Imperial Legion. "
                "Hadvar, an Imperial soldier who recruited them to the cause, "
                "accompanies the party. Jarl Balgruuf the Greater has reluctantly sided with the Empire, and "
                "the Stormcloaks are preparing to assault the city. The Battle of "
                "Whiterun approaches, and the party must help defend the city alongside "
                "Imperial forces and the Companions of Jorrvaskr."
            )
        elif faction_alignment == "stormcloak":
            campaign_state["starting_narrative"] = (
                "The party arrives in Whiterun as supporters of the Stormcloak Rebellion. "
                "Ralof, a Stormcloak soldier who recruited them to the cause, "
                "accompanies the party. "
                "Jarl Balgruuf has sided with the Empire, making Whiterun a target for "
                "liberation. The party joins Galmar Stone-Fist in preparing to assault "
                "the city and free it from Imperial control. The Battle of Whiterun "
                "is imminent, and Skyrim's future hangs in the balance."
            )
        else:  # neutral
            # Use specific neutral faction narrative if provided
            if neutral_subfaction:
                faction_info = self.get_neutral_faction_narrative(neutral_subfaction)
                if faction_info:
                    campaign_state["starting_narrative"] = faction_info["narrative"]
                    campaign_state["neutral_subfaction"] = neutral_subfaction
                    campaign_state["starting_npc_contact"] = faction_info["key_npc"]
                else:
                    # Default neutral narrative
                    campaign_state["starting_narrative"] = (
                        "The party arrives in Whiterun, trying to remain neutral in the civil war. "
                        "They have not yet committed to either side in the conflict. "
                        "Jarl Balgruuf the Greater has reluctantly sided with the Empire, and "
                        "the Stormcloaks prepare to assault the city. The party may align with "
                        "neutral factions like the Companions, who focus on honor over politics. "
                        "The Battle of Whiterun approaches, and the party must navigate the "
                        "conflict while maintaining their independence. They may encounter Hadvar or Ralof "
                        "in Riverwood or Whiterun and decide whether to accept either as a companion."
                    )
            else:
                # Default neutral narrative
                campaign_state["starting_narrative"] = (
                    "The party arrives in Whiterun, trying to remain neutral in the civil war. "
                    "They have not yet committed to either side in the conflict. "
                    "Jarl Balgruuf the Greater has reluctantly sided with the Empire, and "
                    "the Stormcloaks prepare to assault the city. The party may align with "
                    "neutral factions like the Companions, who focus on honor over politics. "
                    "The Battle of Whiterun approaches, and the party must navigate the "
                    "conflict while maintaining their independence. They may encounter Hadvar or Ralof "
                    "in Riverwood or Whiterun and decide whether to accept either as a companion."
                )
        
        # Update faction relationships based on neutral alignment
        if faction_alignment == "neutral":
            if "faction_relationships" not in campaign_state:
                campaign_state["faction_relationships"] = {}
            
            # Set base neutral faction relationship
            if neutral_subfaction:
                # Specific neutral faction gets higher relationship
                # Use mapping to ensure consistent faction names
                faction_key = FACTION_NAME_MAPPING.get(neutral_subfaction, neutral_subfaction)
                campaign_state["faction_relationships"][faction_key] = 30
            else:
                # Generic neutral gets modest companion relationship
                campaign_state["faction_relationships"]["companions"] = 20
        
        # Update last updated timestamp
        campaign_state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save updated campaign state
        campaign_state_file.parent.mkdir(exist_ok=True)
        with open(campaign_state_file, 'w') as f:
            json.dump(campaign_state, f, indent=2)
        
        print(f"\nCampaign state updated: {campaign_state_file}")
        print(f"Starting location: Whiterun")
        print(f"Faction alignment: {faction_alignment}")
        return campaign_state
    
    def validate_character_data(self, character):
        """Validate that character has all required data"""
        required_fields = ['name', 'player', 'race', 'standing_stone', 'faction_alignment']
        errors = []
        
        for field in required_fields:
            if field not in character or not character[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate faction alignment is one of the valid options
        if 'faction_alignment' in character:
            valid_alignments = ['imperial', 'stormcloak', 'neutral']
            if character['faction_alignment'] not in valid_alignments:
                errors.append(f"Invalid faction alignment: {character['faction_alignment']}. Must be one of: {', '.join(valid_alignments)}")
        
        # Validate neutral subfaction if specified
        if 'neutral_subfaction' in character and character['neutral_subfaction']:
            valid_subfactions = ['companions', 'thieves_guild', 'college', 'dark_brotherhood', 'blades', 'greybeards']
            if character['neutral_subfaction'] not in valid_subfactions:
                errors.append(f"Invalid neutral subfaction: {character['neutral_subfaction']}. Must be one of: {', '.join(valid_subfactions)}")
        
        # Validate standing stone is not empty
        if 'standing_stone' in character and character['standing_stone']:
            if len(character['standing_stone'].strip()) < 3:
                errors.append("Standing Stone selection appears invalid or too short")
        
        # Validate race is not empty
        if 'race' in character and character['race']:
            if len(character['race'].strip()) < 3:
                errors.append("Race selection appears invalid or too short")
        
        # Validate aspects
        if 'aspects' in character:
            aspects = character['aspects']
            
            # Check High Concept
            if not aspects.get('high_concept') or aspects['high_concept'] == "[Player to define - Required]":
                errors.append("High Concept is required and must be defined")
            
            # Check Trouble
            if not aspects.get('trouble') or aspects['trouble'] == "[Player to define - Required]":
                errors.append("Trouble is required and must be defined")
            
            # Check other aspects (need at least 1)
            other_aspects = aspects.get('other_aspects', [])
            if not other_aspects or len(other_aspects) < 1:
                errors.append("At least 1 additional aspect is required")
        else:
            errors.append("Aspects section missing from character")
        
        # Validate skills pyramid
        if 'skills' in character:
            skills = character['skills']
            total_skills = 0
            
            for level_name, count in SKILL_PYRAMID.items():
                level_skills = skills.get(level_name, [])
                if len(level_skills) != count:
                    errors.append(f"Skill pyramid error: {level_name} should have {count} skill(s), but has {len(level_skills)}")
                total_skills += len(level_skills)
            
            expected_total_skills = sum(SKILL_PYRAMID.values())
            if total_skills != expected_total_skills:
                errors.append(f"Total skills should be {expected_total_skills}, but found {total_skills}")
            
            # Check for duplicate skills
            all_skills = []
            for level_skills in skills.values():
                all_skills.extend(level_skills)
            if len(all_skills) != len(set(all_skills)):
                errors.append("Duplicate skills detected - each skill can only be selected once")
        else:
            errors.append("Skills section missing from character")
        
        # Validate stunts (need exactly 3)
        if 'stunts' in character:
            stunts = character['stunts']
            if len(stunts) != 3:
                errors.append(f"Exactly 3 stunts are required, but found {len(stunts)}")
            
            # Check that stunts are not empty or too short
            for i, stunt in enumerate(stunts, 1):
                if not stunt or len(stunt.strip()) < MIN_STUNT_LENGTH:
                    errors.append(f"Stunt {i} is empty or too short (minimum {MIN_STUNT_LENGTH} characters)")
        else:
            errors.append("Stunts section missing from character")
        
        if errors:
            print("\n⚠️  CHARACTER VALIDATION ERRORS:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    def create_session_zero_log(self, characters, campaign_info):
        """Create a session zero log file"""
        logs_dir = self.data_dir.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}_session-00_Session-Zero.md"
        filepath = logs_dir / filename
        
        faction_name = {
            'imperial': 'Imperial Legion',
            'stormcloak': 'Stormcloak Rebellion',
            'neutral': 'Neutral (Independent)'
        }.get(campaign_info.get('faction_alignment', 'neutral'), 'Unknown')
        
        log_content = f"""# Session 0: Session Zero - Campaign Setup

**Date**: {datetime.now().strftime("%Y-%m-%d")}
**In-Game Date**: 17th of Last Seed, 4E 201
**GM**: {campaign_info.get('gm', '[GM Name]')}
**Players Present**: {', '.join([c['player'] for c in characters])}
**Party Faction Alignment**: {faction_name}
**Starting Location**: Whiterun

## Session Summary

This is Session Zero for our Skyrim Fate Core campaign. Players created their characters,
chose their races and Standing Stones, and aligned with a faction for the approaching
Battle of Whiterun.

### Battle of Whiterun Context

The party has chosen to align with the **{faction_name}** for the civil war conflict
centered around Whiterun. Jarl Balgruuf the Greater has reluctantly sided with the
Empire, and the Stormcloaks are preparing to assault the city. Every character must
decide where they stand in this pivotal battle.

## Character Creation

"""
        
        for character in characters:
            log_content += f"""### {character['name']} (played by {character['player']})
- **Race**: {character['race']}
- **Standing Stone**: {character['standing_stone']}
- **Faction Alignment**: {faction_name}

#### Aspects
- **High Concept**: {character['aspects']['high_concept']}
- **Trouble**: {character['aspects']['trouble']}
"""
            for i, aspect in enumerate(character['aspects'].get('other_aspects', []), 1):
                log_content += f"- **Aspect {i}**: {aspect}\n"
            
            log_content += "\n#### Skills\n"
            for level_name, skills in character['skills'].items():
                if skills:
                    log_content += f"- **{level_name}**: {', '.join(skills)}\n"
            
            log_content += "\n#### Stunts\n"
            for i, stunt in enumerate(character.get('stunts', []), 1):
                log_content += f"{i}. {stunt}\n"
            
            log_content += f"\n**Backstory Summary**: {character.get('backstory', '[To be developed]')}\n\n"
        
        # Add faction-specific starting narrative
        if campaign_info.get('faction_alignment') == 'imperial':
            narrative = """
## Starting Narrative - Imperial Path

The party arrives in Whiterun as supporters of the Imperial Legion. General Tullius
has ordered the defense of Whiterun, and Legate Rikke coordinates with Jarl Balgruuf's
forces. The Stormcloaks, led by Galmar Stone-Fist, gather their forces to assault
the city.

The party's role is to help defend Whiterun's walls, protect civilians, and ensure
the city remains under Imperial control. The Companions of Jorrvaskr may aid in the
defense, though they prefer to remain politically neutral.
"""
        elif campaign_info.get('faction_alignment') == 'stormcloak':
            narrative = """
## Starting Narrative - Stormcloak Path

The party arrives in Whiterun as supporters of the Stormcloak Rebellion. Ulfric
Stormcloak has ordered the capture of Whiterun, and Galmar Stone-Fist leads the
assault. Jarl Balgruuf has sided with the Empire, making the city a target for
liberation.

The party's role is to breach Whiterun's walls, overcome Imperial defenders, and
force the Jarl's surrender. This is a crucial step in freeing Skyrim from Imperial
rule and expelling the Thalmor from Nordic lands.
"""
        else:  # neutral
            narrative = """
## Starting Narrative - Neutral Path

The party arrives in Whiterun, determined to remain independent in the civil war.
The Companions of Jorrvaskr offer a model of honor-bound neutrality, focusing on
warrior traditions rather than politics.

As the Battle of Whiterun approaches, the party must navigate between both sides,
potentially aiding the defense of the city while maintaining independence. They
may seek to minimize bloodshed or focus on protecting civilians caught in the
crossfire.
"""
        
        log_content += narrative
        
        default_hooks = "- The Battle of Whiterun approaches\n- Choose your role in the civil war\n- Protect or challenge Jarl Balgruuf"
        hooks_text = campaign_info.get("hooks", default_hooks)
        
        log_content += f"""
## Campaign Setup

### Campaign Premise
{campaign_info.get('premise', 'The civil war between Imperials and Stormcloaks threatens to tear Skyrim apart. Ancient forces stir in the depths of Nordic ruins. The Battle of Whiterun approaches.')}

### Starting Location
Whiterun - The heart of Skyrim, about to become a battlefield.

### Initial Hooks
{hooks_text}

### House Rules Discussed
- Standing Stones MUST be selected during Session Zero (cannot be skipped)
- Standing Stones can be changed during play by visiting the physical location
- Dragonbreaks will be used for major canon divergences
- Fate Point economy: Compels will be frequent, players encouraged to accept
- Session format: Mix of combat, investigation, and social encounters
- Faction alignment affects starting relationships and narrative

### Faction Alignments
"""
        
        for character in characters:
            alignment = character.get('faction_alignment', campaign_info.get('faction_alignment', 'neutral'))
            faction_display = {
                'imperial': 'Imperial Legion',
                'stormcloak': 'Stormcloak Rebellion',
                'neutral': 'Neutral (Independent)'
            }.get(alignment, 'Unknown')
            
            additional = character.get('additional_faction_interests', 'None yet')
            log_content += f"\n**{character['name']}**: {faction_display}"
            if additional and additional != "None yet":
                log_content += f" | Also interested in: {additional}"
        
        log_content += """

## Next Session Preview

The party begins in Whiterun as the Battle of Whiterun approaches. They must decide
their exact role in the conflict, establish relationships with key NPCs (Jarl Balgruuf,
the Companions, local guards), and prepare for the coming battle.

The civil war will test their loyalty, honor, and combat prowess. Their choices in
the Battle of Whiterun will shape Skyrim's future.

---

**Session End Time**: Campaign start (pre-adventure)
**Real World Duration**: Session Zero setup
"""
        
        with open(filepath, 'w') as f:
            f.write(log_content)
        
        print(f"\nSession Zero log created: {filepath}")
        return filepath
    
    def run_interactive_session_zero(self):
        """Run interactive Session Zero process"""
        print("\n" + "="*60)
        print("WELCOME TO SKYRIM FATE CORE - SESSION ZERO")
        print("="*60)
        print("\nThis script will guide you through character creation.")
        print("You will choose your faction alignment for the Battle of Whiterun,")
        print("select a Standing Stone (required), and create your characters.")
        print("\nLet's begin!\n")
        
        # Get GM name
        gm_name = input("GM Name: ").strip()
        while not gm_name:
            print("⚠️  GM name is required!")
            gm_name = input("GM Name: ").strip()
        
        # Get campaign info
        print("\n--- Campaign Setup ---")
        campaign_premise = input("Campaign Premise (or press Enter for default): ").strip()
        if not campaign_premise:
            campaign_premise = "Dragons have returned to Skyrim. The civil war rages. Your story begins..."
        
        # Display civil war context and get party faction alignment
        self.display_civil_war_context()
        
        print("\n--- Party Faction Alignment ---")
        print("The entire party must choose a faction alignment for the Battle of Whiterun.")
        print("This sets your starting narrative and relationships in Skyrim.\n")
        
        faction_alignment = None
        while not faction_alignment:
            print("\nChoose party faction alignment:")
            print("1. Imperial Legion - Defend Whiterun with the Empire")
            print("2. Stormcloak Rebellion - Assault Whiterun for independence")
            print("3. Neutral Factions - Stay independent (e.g., Companions)")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                faction_alignment = "imperial"
                print("\n✓ Party aligned with the Imperial Legion")
                print("  You will defend Whiterun alongside Imperial forces.")
            elif choice == "2":
                faction_alignment = "stormcloak"
                print("\n✓ Party aligned with the Stormcloak Rebellion")
                print("  You will assault Whiterun to free it from Imperial control.")
            elif choice == "3":
                faction_alignment = "neutral"
                print("\n✓ Party remains neutral in the civil war")
                print("  You focus on honor and independence, possibly joining the Companions.")
            else:
                print("⚠️  Invalid choice. Please enter 1, 2, or 3.")
        
        campaign_info = {
            'gm': gm_name,
            'premise': campaign_premise,
            'starting_location': 'Whiterun',
            'faction_alignment': faction_alignment,
            'hooks': f'- The Battle of Whiterun approaches\n- Choose your role in the civil war\n- Protect or challenge Jarl Balgruuf'
        }
        
        # Get number of players
        while True:
            try:
                num_players = int(input("\nHow many players? "))
                if num_players > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
        
        characters = []
        
        # Create each character
        for i in range(num_players):
            print(f"\n{'='*60}")
            print(f"CHARACTER {i+1} OF {num_players}")
            print("="*60)
            
            player_name = input("Player Name: ").strip()
            while not player_name:
                print("⚠️  Player name is required!")
                player_name = input("Player Name: ").strip()
            
            character_name = input("Character Name: ").strip()
            while not character_name:
                print("⚠️  Character name is required!")
                character_name = input("Character Name: ").strip()
            
            # Show races
            self.display_races()
            race = None
            while not race:
                race_input = input("\nChoose your race (name): ").strip()
                if not race_input:
                    print("⚠️  Race selection is required!")
                    continue
                # Validate race exists
                races = self.load_races()
                race_found = False
                for r in races:
                    if r['name'].lower() == race_input.lower():
                        race = r['name']
                        race_found = True
                        break
                if not race_found:
                    print(f"⚠️  Race '{race_input}' not found. Please choose from the list above.")
            
            # Show standing stones - ENFORCED
            self.display_standing_stones()
            standing_stone = None
            while not standing_stone:
                stone_input = input("\nChoose your Standing Stone (name - REQUIRED): ").strip()
                if not stone_input:
                    print("⚠️  Standing Stone selection is REQUIRED! You cannot skip this.")
                    print("   Every adventurer must be blessed by a Standing Stone.")
                    continue
                # Basic validation - at least looks like a stone name
                if len(stone_input) < 5 or "stone" not in stone_input.lower():
                    print("⚠️  Please enter a valid Standing Stone name (e.g., 'The Warrior Stone')")
                    continue
                standing_stone = stone_input
            
            # Create character
            character = self.create_character_template(
                player_name, character_name, race, standing_stone
            )
            
            if character:
                # Add faction alignment to character
                character['faction_alignment'] = faction_alignment
                
                # Prompt for Aspects (High Concept, Trouble, and 1-3 additional)
                self.prompt_for_aspects(character)
                
                # Prompt for Skills (Fate Core pyramid)
                self.prompt_for_skills(character)
                
                # Prompt for Stunts (3 required)
                self.prompt_for_stunts(character)
                
                # Additional backstory prompts
                print("\n--- Backstory Development ---")
                print("Answer these questions to flesh out your character:")
                
                print("\n1. How did you become involved in the Civil War?")
                war_entry = input("   > ").strip()
                
                print("\n2. Why do you support the " + 
                      ("Imperial Legion" if faction_alignment == "imperial" else 
                       "Stormcloak Rebellion" if faction_alignment == "stormcloak" else
                       "neutral cause") + "?")
                civil_war_stance = input("   > ").strip()
                
                print("\n3. What drives you? What are your goals?")
                motivation = input("   > ").strip()
                
                print("\n4. Do you have any significant relationships or connections in Whiterun?")
                connections = input("   > ").strip()
                
                # Build backstory
                backstory = f"""
**Civil War Entry**: {war_entry if war_entry else '[To be determined]'}

**Civil War Stance**: {civil_war_stance if civil_war_stance else '[To be determined]'}

**Motivation**: {motivation if motivation else '[To be determined]'}

**Connections**: {connections if connections else '[To be determined]'}
"""
                character['backstory'] = backstory.strip()
                
                # Display additional faction options
                print("\n--- Additional Faction Interests ---")
                print("Beyond the civil war, you may be interested in other factions:")
                self.display_factions()
                faction_interest = input("\nAre you interested in any other factions? (optional): ").strip()
                character['additional_faction_interests'] = faction_interest if faction_interest else "None yet"
                
                # Validate character data
                if not self.validate_character_data(character):
                    print("\n⚠️  Character creation incomplete. Please restart this character.")
                    continue
                
                # Save character
                self.save_character(character)
                characters.append(character)
                
                print(f"\n✓ Character '{character_name}' created successfully!")
        
        # Validate that we have at least one character
        if not characters:
            print("\n⚠️  No characters were created! Session Zero incomplete.")
            return
        
        # Update campaign state with faction alignment and characters
        print("\n--- Updating Campaign State ---")
        campaign_state = self.update_campaign_state(faction_alignment, characters)
        
        # Create session zero log
        print("\n--- Creating Session Zero Log ---")
        self.create_session_zero_log(characters, campaign_info)
        
        print("\n" + "="*60)
        print("SESSION ZERO COMPLETE!")
        print("="*60)
        print(f"\nCreated {len(characters)} character(s)")
        print(f"Faction Alignment: {faction_alignment.upper()}")
        print(f"Starting Location: Whiterun")
        print(f"Battle of Whiterun Status: Approaching")
        print("\nFiles saved:")
        print("  - Character files: data/pcs/")
        print("  - Session log: logs/")
        print("  - Campaign state: state/campaign_state.json")
        print("\nYou're ready to begin your Skyrim adventure!")
        print("The Battle of Whiterun awaits...")
        print("="*60)


def main():
    """Main function"""
    print("Skyrim Fate Core - Session Zero Manager")
    print("Choose an option:")
    print("1. Interactive Session Zero (guided character creation)")
    print("2. Display Races")
    print("3. Display Standing Stones")
    print("4. Display Factions")
    print("5. Display Civil War Context (Battle of Whiterun)")
    print("6. Exit")
    
    manager = SessionZeroManager()
    
    while True:
        try:
            choice = input("\nEnter choice (1-6): ").strip()
        except EOFError:
            print("Goodbye!")
            break
        
        if choice == "1":
            manager.run_interactive_session_zero()
            break
        elif choice == "2":
            manager.display_races()
        elif choice == "3":
            manager.display_standing_stones()
        elif choice == "4":
            manager.display_factions()
        elif choice == "5":
            manager.display_civil_war_context()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()
