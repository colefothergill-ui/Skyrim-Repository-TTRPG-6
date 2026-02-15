# Character Creation Example - Fate Core

This document demonstrates the complete character creation process using the enhanced Session Zero system.

## Example Character: Ragnar Ironheart

### Basic Information
- **Player**: Sarah
- **Character Name**: Ragnar Ironheart
- **Race**: Nord
- **Standing Stone**: The Warrior Stone
- **Faction Alignment**: Imperial Legion

### Aspects

#### High Concept
**"Battle-Hardened Nord Warrior"**

This defines Ragnar's core identity - a seasoned fighter who has seen many battles. Can be invoked for bonuses in combat situations and compelled when his warrior nature causes problems.

#### Trouble
**"Haunted by the Dead of the Civil War"**

Ragnar is troubled by memories of those he's killed in the conflict. This creates interesting complications and roleplay opportunities.

#### Additional Aspects
1. **"Sworn to Protect the Innocent"** - Drives him to defend civilians
2. **"Distrusts the Thalmor"** - Common Nord sentiment with story implications
3. **"Bond with Lydia"** - Relationship aspect providing support and complications

### Skills (Fate Core Pyramid)

The skill pyramid ensures balanced character capabilities:

#### Great (+4) - 1 Skill
- **Fight** - Primary combat skill for melee battles

#### Good (+3) - 2 Skills
- **Athletics** - Running, climbing, physical activities
- **Physique** - Strength, endurance, resisting damage

#### Fair (+2) - 3 Skills
- **Will** - Mental fortitude, magic resistance
- **Notice** - Perception and awareness
- **Rapport** - Social interaction and persuasion

#### Average (+1) - 4 Skills
- **Shoot** - Ranged combat with bows
- **Stealth** - Sneaking when needed
- **Lore** - Knowledge of Skyrim's history
- **Empathy** - Understanding others' emotions

### Stunts (3 Initial Stunts)

Stunts make Ragnar unique and provide mechanical benefits:

1. **Whirlwind Attack**: Once per scene, attack all enemies in your zone with Fight
   - *Represents sweeping blade techniques learned in the Legion*

2. **Battle Fury**: +2 to Fight when you have taken a consequence this scene
   - *Ragnar fights harder when wounded, channeling pain into power*

3. **Unbreakable Will**: +2 to defend against mental attacks when outnumbered
   - *Years of war have steeled his mind against fear*

### Racial Bonuses (Nord)

These come from race selection:

- **Resist Frost**: +2 to Physique rolls to resist cold damage or freezing conditions
- **Battle Cry**: Once per session, create advantage 'Frightened Enemies' with one free invoke

### Character Sheet Summary

```json
{
  "name": "Ragnar Ironheart",
  "race": "Nord",
  "standing_stone": "The Warrior Stone",
  "faction_alignment": "imperial",
  "refresh": 3,
  "fate_points": 3,
  
  "aspects": {
    "high_concept": "Battle-Hardened Nord Warrior",
    "trouble": "Haunted by the Dead of the Civil War",
    "other_aspects": [
      "Sworn to Protect the Innocent",
      "Distrusts the Thalmor",
      "Bond with Lydia"
    ]
  },
  
  "skills": {
    "Great (+4)": ["Fight"],
    "Good (+3)": ["Athletics", "Physique"],
    "Fair (+2)": ["Will", "Notice", "Rapport"],
    "Average (+1)": ["Shoot", "Stealth", "Lore", "Empathy"]
  },
  
  "stunts": [
    "Whirlwind Attack: Once per scene, attack all enemies in your zone with Fight",
    "Battle Fury: +2 to Fight when you have taken a consequence this scene",
    "Unbreakable Will: +2 to defend against mental attacks when outnumbered"
  ]
}
```

## How This Character Works in Play

### Example Scene: Defending Whiterun

**Situation**: Ragnar is defending Whiterun's gates against Stormcloak attackers.

**Actions Ragnar Could Take**:

1. **Use Whirlwind Attack stunt** - Attack multiple enemies at once
2. **Invoke "Battle-Hardened Nord Warrior"** - Get +2 to Fight roll
3. **Invoke "Sworn to Protect the Innocent"** - Extra bonus when defending civilians
4. **Accept compel on "Haunted by the Dead"** - Hesitate before killing, gain Fate Point

**Skill Rolls**:
- Fight at Great (+4) for melee combat
- Notice at Fair (+2) to spot threats
- Will at Fair (+2) to resist fear effects

**Stress & Consequences**:
- Physical stress boxes absorb damage
- If seriously hurt, take consequences that become new aspects
- Battle Fury stunt makes him stronger when wounded

## Tips for Creating Your Own Character

### 1. Start with Concept
Think about who your character is before mechanics:
- What's their background?
- Why are they in Skyrim?
- What do they want?

### 2. Make Aspects Interesting
Good aspects are:
- **Specific** enough to be interesting
- **Broad** enough to be useful
- **Double-edged** - helpful and problematic

Examples:
- ✅ "Thief with a Heart of Gold" - Can steal but also compelled to help
- ✅ "Hunted by the Dark Brotherhood" - Interesting complications
- ❌ "Good Fighter" - Too generic and boring

### 3. Build Skills Around Your Concept
If you're a:
- **Warrior**: Great Fight, Good Athletics/Physique
- **Thief**: Great Stealth, Good Deceive/Athletics
- **Mage**: Great Lore, Good Will/Rapport
- **Scout**: Great Notice, Good Shoot/Stealth

### 4. Create Synergistic Stunts
Make stunts that work with your aspects and skills:
- Link stunts to your high skills
- Reference your aspects in stunt names/descriptions
- Think about what makes your character special

### 5. Leave Room to Grow
You don't need to define everything at Session Zero:
- Backstory can develop through play
- Aspects can be renamed at milestones
- New stunts can be added as you advance

## Running Session Zero

The interactive script guides you through each step:

```bash
cd scripts
python3 session_zero.py
```

Follow the prompts to:
1. Set up GM and campaign info
2. Choose party faction alignment
3. Create each character with:
   - Basic info (name, race, Standing Stone)
   - Aspects (High Concept, Trouble, 1-3 additional)
   - Skills (pyramid structure enforced)
   - Stunts (3 required)
   - Backstory questions

The system validates everything and creates:
- Character JSON files in `data/pcs/`
- Updated campaign state in `state/campaign_state.json`
- Session Zero log in `logs/`

Ready to play!
