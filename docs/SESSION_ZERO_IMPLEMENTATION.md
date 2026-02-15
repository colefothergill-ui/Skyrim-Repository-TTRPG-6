# Session Zero Implementation - Complete Character Creation

## Overview
This document describes the comprehensive Session Zero system for Skyrim Fate Core, including full character creation with Aspects, Skills, and Stunts following Fate Core rules.

## Character Creation Features

### 1. **Aspects** (Fate Core Core Mechanic)

The system now enforces complete aspect definition:

#### High Concept (Required)
- Defines the core identity of the character
- Cannot be skipped or left as placeholder
- Examples: "Nord Warrior Seeking Redemption", "Cunning Thief with a Heart of Gold"

#### Trouble (Required)
- A defining problem or complication that makes life interesting
- Must be defined during Session Zero
- Cannot be skipped
- Examples: "Haunted by Past Mistakes", "Wanted by the Thalmor", "Can't Resist a Challenge"

#### Additional Aspects (1-3 Required)
- Players must define at least 1 additional aspect
- Can define up to 3 additional aspects
- Examples: "Defender of the Weak", "Bond with a Companion", "Distrusts Magic Users"

**Implementation**: `prompt_for_aspects()` method guides players through interactive aspect creation with validation.

### 2. **Skills** (Fate Core Pyramid/Column Rule)

The system enforces the Fate Core skill pyramid:
- **1 skill** at Great (+4)
- **2 skills** at Good (+3)
- **3 skills** at Fair (+2)
- **4 skills** at Average (+1)

#### Available Skills for Skyrim:
1. Fight - Melee combat
2. Shoot - Ranged combat (bows, crossbows)
3. Athletics - Physical activities, running, climbing
4. Physique - Raw strength and endurance
5. Notice - Perception and awareness
6. Stealth - Sneaking and hiding
7. Lore - Knowledge of history, magic, and creatures
8. Will - Mental fortitude and magic resistance
9. Rapport - Social interaction and persuasion
10. Deceive - Lying and trickery
11. Empathy - Understanding others' emotions
12. Crafts - Creating and repairing items
13. Survival - Wilderness skills

**Implementation**: `prompt_for_skills()` method enforces pyramid structure with validation.

### 3. **Stunts** (3 Initial Stunts Required)

Players must create exactly 3 stunts during Session Zero:
- Stunts are special abilities that make characters unique
- Can interact with campaign mechanics (Thu'um, faction bonuses, etc.)
- Examples:
  - "Whirlwind Attack: Once per scene, attack all enemies in your zone"
  - "Battle Fury: +2 to Fight when you take a consequence"
  - "Shadow Step: +2 to Stealth when creating advantages in darkness"

**Implementation**: `prompt_for_stunts()` method with validation.

## Session Zero Workflow

### Enhanced Interactive Process

1. **GM Setup**
   - Enter GM name
   - Define campaign premise

2. **Party Faction Alignment** (Required)
   - Choose: Imperial Legion, Stormcloak Rebellion, or Neutral
   - Affects starting narrative and relationships

3. **For Each Character**:
   
   a. **Basic Information**
      - Player name
      - Character name
      - Race selection (from races.json)
      - Standing Stone selection (REQUIRED)
   
   b. **Aspects** (NEW)
      - Define High Concept
      - Define Trouble
      - Define 1-3 additional aspects
   
   c. **Skills** (NEW)
      - Build skill pyramid
      - Select 1/2/3/4 skills at Great/Good/Fair/Average
      - Validation prevents duplicates
   
   d. **Stunts** (NEW)
      - Create 3 unique stunts
      - Examples provided for guidance
   
   e. **Backstory**
      - Civil War involvement
      - Faction stance motivation
      - Character goals
      - Whiterun connections

4. **Validation & Export**
   - Complete validation of all fields
   - Character saved to `data/pcs/[character_id].json`
   - Campaign state updated
   - Session Zero log generated with full stats

## Validation System

The `validate_character_data()` method ensures:

✅ **Required Fields**: name, player, race, standing_stone, faction_alignment  
✅ **Aspects**:
  - High Concept is defined (not placeholder)
  - Trouble is defined (not placeholder)
  - At least 1 additional aspect exists
✅ **Skills**:
  - Exactly 1 skill at Great (+4)
  - Exactly 2 skills at Good (+3)
  - Exactly 3 skills at Fair (+2)
  - Exactly 4 skills at Average (+1)
  - No duplicate skills
✅ **Stunts**:
  - Exactly 3 stunts defined
  - Each stunt has meaningful content

## Changes Made

### 1. Enhanced `scripts/session_zero.py`

#### New Constants:
- `SKYRIM_SKILLS`: List of 13 Fate Core skills for Skyrim
- `SKILL_PYRAMID`: Skill distribution requirements (1/2/3/4)

#### New Methods:
- `prompt_for_aspects()`: Interactive aspect creation
- `prompt_for_skills()`: Interactive skill pyramid builder
- `prompt_for_stunts()`: Interactive stunt creation

#### Enhanced Methods:
- `create_character_template()`: Updated to use `other_aspects` array
- `validate_character_data()`: Comprehensive validation including aspects, skills, stunts
- `create_session_zero_log()`: Displays complete character stats including all aspects, skills, and stunts

#### Existing Features (Unchanged):

1. **Battle of Whiterun Context Display** (`display_civil_war_context()`)
   - Presents detailed information about the Imperial/Stormcloak conflict
   - Shows pros/cons of each faction choice
   - Explains the neutral option (Companions, College of Winterhold, etc.)
   - Sets the stage for the Battle of Whiterun

2. **Mandatory Faction Alignment**
   - Party must choose between: Imperial, Stormcloak, or Neutral
   - Choice is enforced during session zero (cannot be skipped)
   - Affects starting narrative and faction relationships
   - Determines starting scene context in Whiterun

3. **Enforced Standing Stone Selection**
   - Standing Stone choice is now REQUIRED (cannot skip)
   - Validation ensures a valid stone name is entered
   - Warning messages if player tries to skip

4. **Campaign State Integration** (`update_campaign_state()`)
   - Automatically updates `state/campaign_state.json` with:
     - `starting_location`: Set to "Whiterun"
     - `session_zero_completed`: True
     - `player_alliance`: Imperial/Stormcloak/Neutral
     - `battle_of_whiterun_status`: "approaching"
     - Faction relationships based on alignment
     - Starting narrative tailored to faction choice
     - Player character roster

5. **Data Validation** (`validate_character_data()`)
   - Validates all required fields are present
   - Ensures Standing Stone is not empty
   - Verifies faction alignment is valid (imperial/stormcloak/neutral)
   - Checks race selection is valid
   - Prevents progression with incomplete data

6. **Enhanced Session Zero Log**
   - Includes Battle of Whiterun context
   - Records party faction alignment
   - Documents faction-specific starting narrative
   - Notes mandatory Standing Stone selections
   - Links all characters to faction choice

### 2. Campaign State Structure

The updated `campaign_state.json` now includes:

```json
{
  "session_zero_completed": true,
  "starting_location": "Whiterun",
  "civil_war_state": {
    "player_alliance": "imperial|stormcloak|neutral",
    "battle_of_whiterun_status": "approaching",
    "faction_relationship": {
      "imperial_legion": 30|-20|0,
      "stormcloaks": -20|30|0
    }
  },
  "faction_relationships": {
    "companions": 20  // For neutral alignment
  },
  "starting_narrative": "...",
  "player_characters": [...]
}
```

### 3. Faction Relationships by Alignment

#### Imperial Alignment:
- Imperial Legion: +30
- Stormcloaks: -20
- Narrative: Defend Whiterun with Imperial forces

#### Stormcloak Alignment:
- Imperial Legion: -20
- Stormcloaks: +30
- Narrative: Assault Whiterun for the rebellion

#### Neutral Alignment:
- Imperial Legion: 0
- Stormcloaks: 0
- Companions: +20
- Narrative: Maintain independence, possibly join Companions

### 4. Starting Narratives

Each faction alignment gets a unique starting narrative:

- **Imperial**: Focus on defending Whiterun, working with Legate Rikke and Jarl Balgruuf
- **Stormcloak**: Focus on liberating Whiterun, following Galmar Stone-Fist
- **Neutral**: Focus on honor and independence, possibly joining the Companions

## Testing

Created comprehensive test suite in `tests/test_session_zero.py`:

1. **Initialization Test**: Verifies SessionZeroManager setup
2. **Validation Test**: Tests character data validation logic
3. **Campaign State Test**: Verifies all three faction alignments update correctly
4. **Character Template Test**: Ensures character creation works properly

**Test Results**: 4/4 tests passing ✓

Created demonstration script in `tests/demo_session_zero.py`:
- Shows complete workflow
- Demonstrates all features
- Validates output correctness

## Validation Rules

### Required Fields:
- `name`: Character name
- `player`: Player name
- `race`: Character race
- `standing_stone`: Standing Stone choice (cannot be empty)
- `faction_alignment`: One of: imperial, stormcloak, neutral

### Validation Checks:
1. All required fields must be present
2. Standing Stone must be at least 5 characters and contain "stone"
3. Race must be at least 3 characters
4. Faction alignment must be one of the three valid options
5. GM name cannot be empty
6. Character name cannot be empty

## User Experience Flow

1. GM enters name (required)
2. System displays Battle of Whiterun context
3. Party selects faction alignment (required, validated)
4. For each player:
   - Enter player name (required)
   - Enter character name (required)
   - Select race from list (validated)
   - Select Standing Stone (required, validated)
   - Answer backstory questions
   - Express interest in additional factions (optional)
5. System validates all character data
6. System updates campaign_state.json
7. System creates session zero log
8. Summary displayed with all key information

## Files Changed

1. `scripts/session_zero.py`: Main implementation
2. `tests/test_session_zero.py`: Test suite (new)
3. `tests/demo_session_zero.py`: Demonstration script (new)

## Backwards Compatibility

The changes maintain backwards compatibility:
- Existing data structures are preserved
- New fields are added without removing old ones
- Default values provided where needed
- Existing campaign_state.json files can be loaded and updated

## Key Benefits

1. **No Skipping**: Players cannot skip critical setup steps
2. **Clear Context**: Battle of Whiterun context sets clear expectations
3. **Integrated State**: Campaign state automatically reflects session zero choices
4. **Validated Data**: All character data is validated before saving
5. **Tailored Narratives**: Starting narrative adapts to party choices
6. **Faction Relationships**: Relationships set correctly from the start
7. **Whiterun Focus**: Starting location locked to Whiterun as required

## Future Enhancements

Possible future improvements:
1. GUI for session zero process
2. Pre-built character templates
3. Random backstory generators
4. Integration with character sheet generators
5. Visual faction relationship diagrams
