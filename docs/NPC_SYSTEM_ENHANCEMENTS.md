# NPC System Enhancement Documentation

## Overview
The NPC system has been enhanced with structured stat sheets for prominent characters, a comprehensive companion management system, decision point mechanics, and dialogue tree support.

## New Features

### 1. Structured NPC Stat Sheets

Four major NPCs now have complete stat sheets in the `data/npcs/` directory:

#### General Tullius (`general_tullius.json`)
- **Role**: Imperial Legion Commander
- **Skills**: Tactics (Great), Will (Great), Fight/Notice/Command (Good)
- **Key Features**:
  - Dialogue trees for recruitment and political discussions
  - Decision points for civil war choices and battle strategy
  - Trust clock system (0-8 scale)
  - Faction-aware interactions

#### Ulfric Stormcloak (`ulfric_stormcloak.json`)
- **Role**: Stormcloak Rebellion Leader & Jarl of Windhelm
- **Skills**: Rapport (Great), Will (Great), Fight/Provoke/Lore (Good)
- **Special Abilities**: Thu'um (Unrelenting Force)
- **Key Features**:
  - Complex motivations and internal conflicts
  - Dialogue trees addressing his justifications for the rebellion
  - Decision points for loyalty to his cause
  - Trust clock system (0-10 scale)
  - Dark secrets (Thalmor dossier)

#### Lydia (`lydia.json`)
- **Role**: Housecarl and Companion
- **Skills**: Fight (Great), Physique/Notice (Good)
- **Key Features**:
  - Full companion mechanics (recruitment, dismissal, loyalty tracking)
  - Loyalty modifiers for various actions
  - Combat style: Tank/Shield-Maiden
  - Marriage system support
  - Burden bearer mechanics

#### Aela the Huntress (`aela_the_huntress.json`)
- **Role**: Companion & Werewolf of the Inner Circle
- **Skills**: Shoot (Great), Notice/Athletics (Good)
- **Special Abilities**: Werewolf transformation with separate stat block
- **Key Features**:
  - Werewolf form mechanics
  - Can grant lycanthropy to player
  - Radiant quest system
  - Marriage system support
  - Beast blood decision points

### 2. Enhanced NPC Manager (`scripts/npc_manager.py`)

#### New Methods

##### Companion Management
```python
recruit_companion(npc_id)
```
Recruit an available companion to the active party. Checks recruitment conditions and updates campaign state.

```python
dismiss_companion(npc_id)
```
Dismiss an active companion. They return to their home location and can be re-recruited later.

```python
get_active_companions()
```
Returns list of currently active companions traveling with the party.

```python
get_available_companions()
```
Returns list of companions available for recruitment.

##### Faction Integration
```python
check_faction_alignment(npc_id, faction)
```
Determines NPC's relationship with a faction. Returns: 'allied', 'neutral', 'hostile', or 'unknown'.

```python
update_companion_based_on_faction_clock(faction, clock_value)
```
Adjusts companion loyalty based on faction clock progress (0-10 scale). Allied companions gain loyalty when their faction succeeds; hostile companions lose loyalty.

##### Decision Points
```python
process_decision_point(npc_id, decision_key, chosen_option)
```
Process an NPC decision point based on player choice. Handles loyalty changes, relationship updates, quest triggers, and branching consequences.

**Example Decision Point Structure**:
```json
{
  "civil_war_choice": {
    "condition": "player_must_choose_side",
    "options": ["imperial", "stormcloak", "delay"],
    "consequences": {
      "imperial": {
        "loyalty_change": 10,
        "unlocks": "imperial_questline",
        "relationship": "ally"
      }
    }
  }
}
```

##### Dialogue Trees
```python
handle_dialogue_interaction(npc_id, dialogue_key, response_option=None)
```
Handle branching dialogue interactions. First call displays dialogue and response options. Second call with response_option processes player choice and applies consequences.

**Example Dialogue Tree Structure**:
```json
{
  "initial_meeting": {
    "greeting": "I am Jarl Ulfric Stormcloak. What do you seek?",
    "responses": [
      {
        "option": "I want to fight for Skyrim's freedom",
        "leads_to": "recruitment_path",
        "loyalty_change": 5,
        "quest_trigger": "joining_the_stormcloaks"
      }
    ]
  }
}
```

### 3. Campaign State Companion System

The `state/campaign_state.json` now includes a `companions` section:

```json
{
  "companions": {
    "active_companions": [],
    "available_companions": [
      {
        "npc_id": "lydia",
        "name": "Lydia",
        "status": "available",
        "loyalty": 60,
        "location": "Dragonsreach, Whiterun",
        "recruitment_condition": "Become Thane of Whiterun",
        "faction_affinity": "whiterun"
      }
    ],
    "dismissed_companions": [],
    "companion_relationships": {}
  }
}
```

#### Companion States
- **available**: Can be recruited (conditions met)
- **unavailable**: Exists but cannot be recruited yet (conditions not met)
- **active**: Currently traveling with party
- **dismissed**: Previously active, can be re-recruited

#### Loyalty System
- **Range**: 0-100
- **Thresholds**:
  - 80+: Deeply loyal, will sacrifice for party
  - 60-79: Loyal companion
  - 40-59: Questioning loyalty
  - 20-39: May refuse dangerous orders
  - 0-19: At risk of leaving

## Usage Examples

### Recruiting a Companion
```python
from npc_manager import NPCManager

manager = NPCManager()

# Check available companions
companions = manager.get_available_companions()
for comp in companions:
    print(f"{comp['name']}: {comp['recruitment_condition']}")

# Recruit Lydia
manager.recruit_companion('lydia')

# Check active companions
active = manager.get_active_companions()
print(f"Party size: {len(active)}")
```

### Processing a Decision Point
```python
# Player joins the Imperial Legion
result = manager.process_decision_point(
    'general_tullius',
    'civil_war_choice',
    'imperial'
)

print(f"Loyalty change: {result.get('loyalty_change')}")
print(f"Unlocked: {result.get('unlocked')}")
```

### Handling Dialogue
```python
# Get initial dialogue
result = manager.handle_dialogue_interaction('ulfric_stormcloak', 'initial_meeting')

# Display responses
for i, response in enumerate(result['responses']):
    print(f"{i+1}. {response['option']}")

# Choose response 0
result = manager.handle_dialogue_interaction('ulfric_stormcloak', 'initial_meeting', 0)

if 'quest_triggered' in result:
    print(f"Quest started: {result['quest_triggered']}")
```

### Faction Clock Integration
```python
# Imperial Legion wins a major battle
# Update clock value to 8/10
affected = manager.update_companion_based_on_faction_clock('imperial_legion', 8)

for comp in affected:
    print(f"{comp['name']}: {comp['change']:+d} loyalty ({comp['reason']})")
```

## Testing

Run the comprehensive test suite:
```bash
cd tests
python3 test_npc_enhancements.py
```

Tests cover:
- Companion recruitment and dismissal
- Faction alignment checking
- Decision point processing
- Dialogue tree interactions
- JSON schema validation
- Campaign state structure

## Integration with Existing Systems

### Fate Core Mechanics
All NPCs follow Fate Core stat structures:
- **Aspects**: High concept, trouble, and additional aspects
- **Skills**: Ranked from Great (+4) to Average (+1)
- **Stunts**: Special abilities and bonuses
- **Stress & Consequences**: Physical and mental damage tracking
- **Refresh & Fate Points**: Resource management

### Civil War Module
- NPCs have faction alignments (Imperial Legion, Stormcloaks, neutral)
- Decision points tied to civil war choices
- Faction clocks affect companion loyalty
- Battle outcomes influence NPC relationships

### Quest System
- Dialogue trees trigger quests
- Decision points unlock new quest paths
- Companion recruitment tied to quest completion
- Branching quest outcomes based on NPC interactions

## Future Enhancements

Potential additions:
1. **Romance System**: Deep relationship mechanics for marriageable NPCs
2. **Combat AI**: More sophisticated companion combat tactics
3. **Party Composition**: Bonuses for specific companion combinations
4. **Dynamic Events**: Companions interacting with each other
5. **Reputation System**: Word-of-mouth affecting recruitment options
6. **Companion Quests**: Personal storylines for major companions
