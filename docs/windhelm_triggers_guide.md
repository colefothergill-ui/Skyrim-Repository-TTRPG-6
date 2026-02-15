# Windhelm Location Triggers & Eastmarch Side Quests

## Overview

The Windhelm Location Triggers module provides location-specific events, companion commentary, and quest hooks for Windhelm and Eastmarch. This system includes dynamic narrative events that respond to location, time of day, and quest status, specifically designed to integrate the "Blood on the Ice" and "The White Phial" side quests.

## Features

### Location-Specific Events

The module provides unique descriptive events for different areas of Windhelm:

- **Gray Quarter**: Home to Windhelm's Dark Elf population, depicting the tension and prejudice
- **Graveyard**: Atmospheric location that serves as the quest hook for "Blood on the Ice"
- **Market District**: Bustling marketplace with hooks for "The White Phial" quest
- **Palace of the Kings**: Seat of Jarl Ulfric Stormcloak
- **Candlehearth Hall**: The local inn and tavern
- **General Windhelm**: Main city entrance with historical context

### Quest Integration

The system includes intelligent quest hooks that activate based on:
- **Location**: Specific areas trigger different quests
- **Time of Day**: Some events only occur at night or during the day
- **Quest State**: Hooks only appear when quests haven't been started or completed

#### Blood on the Ice
A murder mystery investigation triggered by visiting the graveyard:
- **Night**: Full discovery scene with guards and crime scene
- **Day**: Subtle hints from guards about the murders
- **Auto-disable**: Quest hook disappears once the quest is active or completed

#### The White Phial
An alchemist's quest triggered in the marketplace:
- Overheard conversation between Nurelion and his assistant Quintus
- Hints at the elderly alchemist's desperate search for the legendary artifact
- **Auto-disable**: Quest hook disappears once the quest is active or completed

### Companion Commentary

The system includes commentary for companions with connections to Windhelm:
- **Stenvar**: A Nord mercenary who comments on the city's politics
- **Uthgerd the Unbroken**: Appreciates Windhelm's historical significance

## Quest Definitions

Complete quest data is available in `data/quests/eastmarch_side_quests.json`:

### Blood on the Ice
**Quest Giver**: Windhelm Guard (crime scene discovery)

**Overview**: A serial killer investigation in Windhelm. The player must investigate murders, gather clues, and unmask "The Butcher" before more victims fall.

**Key Features**:
- Multi-stage investigation with clue gathering
- Interview witnesses and suspects
- Multiple outcomes (correct identification vs. false accusation)
- Affects player reputation in Windhelm
- Can be a step toward becoming Thane of Eastmarch

**Objectives**:
1. Investigate the crime scene in the graveyard
2. Interview witnesses (Helgird, Viola Giordano)
3. Search Hjerim (the abandoned house)
4. Identify Calixto Corrium as the killer
5. Stop the Butcher from claiming another victim

**Rewards**:
- Increased reputation in Windhelm
- Monetary reward from Jorleif (Ulfric's steward)
- Access to purchase Hjerim
- Progress toward Thaneship

### The White Phial
**Quest Giver**: Nurelion (Windhelm Alchemist)

**Overview**: Retrieve a legendary alchemical artifact for an elderly, dying alchemist.

**Key Features**:
- Personal, emotional journey
- Dungeon crawl to Forsaken Cave
- Bittersweet outcome (Phial is found but broken)
- Follow-up quest potential (Repairing the Phial)

**Objectives**:
1. Speak to Nurelion at the White Phial alchemy shop
2. Travel to Forsaken Cave west of Windhelm
3. Navigate dangers (draugr, frost traps)
4. Retrieve the cracked White Phial
5. Return to Nurelion with the broken artifact

**Rewards**:
- Gold reward from Nurelion
- Potions and reagents from Quintus
- Experience from clearing Forsaken Cave
- Unlocks follow-up quest: Repairing the Phial

## Usage

### Basic Usage

```python
from triggers.windhelm_triggers import windhelm_location_triggers

# Basic campaign state
campaign_state = {
    "companions": {
        "active_companions": []
    },
    "time_of_day": "night",
    "quests": {
        "active": [],
        "completed": []
    }
}

# Get events for a location
events = windhelm_location_triggers("windhelm_graveyard", campaign_state)
for event in events:
    print(event)
```

### Quest Hook Example

```python
# Player visits graveyard at night, Blood on the Ice not started
campaign_state = {
    "companions": {"active_companions": []},
    "time_of_day": "night",
    "quests": {"active": [], "completed": []}
}

events = windhelm_location_triggers("windhelm_graveyard", campaign_state)
# Returns: Graveyard description + "You hear distant shouts near the graveyard..."
```

### With Active Quest

```python
# Player visits graveyard with quest already active
campaign_state = {
    "companions": {"active_companions": []},
    "time_of_day": "night",
    "quests": {"active": ["blood_on_the_ice"], "completed": []}
}

events = windhelm_location_triggers("windhelm_graveyard", campaign_state)
# Returns: Only graveyard description (no quest hook)
```

### With Companions

```python
# Campaign state with Stenvar as companion
campaign_state = {
    "companions": {
        "active_companions": ["Stenvar"]
    }
}

events = windhelm_location_triggers("windhelm", campaign_state)
# Returns: Location description + Stenvar's commentary about Windhelm
```

## API Reference

### `windhelm_location_triggers(loc, campaign_state)`

Generate location-specific triggers for Windhelm locations.

**Parameters:**
- `loc` (str): Current location string (e.g., "windhelm", "windhelm_graveyard")
- `campaign_state` (dict): Dictionary containing campaign state including:
  - `companions`: Dict with `active_companions` list
  - `time_of_day`: String or int representing current time
  - `quests`: Dict with `active` and `completed` quest lists

**Returns:**
- List[str]: Event strings to be narrated to players

**Example:**
```python
events = windhelm_location_triggers("windhelm_market", campaign_state)
# Returns: ["The marketplace of Windhelm bustles with activity...", ...]
```

## Location Keys

The following location keys are recognized:

- `"windhelm"` - General Windhelm entrance
- `"windhelm_gray_quarter"` or `"windhelm_grey_quarter"` - Dark Elf district
- `"windhelm_graveyard"` - Quest hook location for Blood on the Ice
- `"windhelm_market"` - Quest hook location for The White Phial
- `"windhelm_palace_of_the_kings"` or `"windhelm_palace"` - Jarl's palace
- `"windhelm_candlehearth_hall"` or `"windhelm_candlehearth"` - Local inn

Location matching is case-insensitive and uses substring matching.

## Time of Day

The system recognizes time in two formats:

### String Format
```python
campaign_state = {
    "time_of_day": "night"  # or "evening", "midnight", "day", "morning", etc.
}
```

### Integer Format (24-hour)
```python
campaign_state = {
    "time_of_day": 22  # 10 PM (night is 20-23 or 0-5)
}
```

Night is defined as 8 PM to 6 AM (hours 20-23 and 0-5).

## Quest State Management

### Quest Formats

The system supports quests in two formats:

**Simple Format (Strings)**:
```python
campaign_state = {
    "quests": {
        "active": ["blood_on_the_ice", "the_white_phial"],
        "completed": ["bleak_falls_barrow"]
    }
}
```

**Complex Format (Objects)**:
```python
campaign_state = {
    "quests": {
        "active": [
            {"id": "blood_on_the_ice", "stage": 2},
            {"id": "the_white_phial", "stage": 1}
        ],
        "completed": [
            {"id": "bleak_falls_barrow", "completed_date": "..."}
        ]
    }
}
```

Both formats are fully supported.

## Extending the System

### Adding New Locations

To add triggers for new locations within Windhelm:

```python
# In windhelm_triggers.py
elif "docks" in loc_lower and "windhelm" in loc_lower:
    events.append("The docks of Windhelm stretch along the White River. Ships from across Skyrim and beyond unload their cargo here.")
    
    # Optional quest hook for "Rise in the East"
    if not _is_quest_active(campaign_state, "rise_in_the_east"):
        events.append("You notice a well-dressed merchant arguing with dock workers. He looks frustrated and in need of help.")
```

### Adding New Companions

To add commentary for additional companions:

```python
# Check for Brunwulf Free-Winter (Windhelm resident)
if _is_companion_present(active_companions, "brunwulf"):
    if loc_lower.startswith("windhelm"):
        events.append('Brunwulf sighs heavily. "My home, yet so divided. The Dunmer deserve better treatment than they receive here."')
```

### Adding New Quest Hooks

To add hooks for additional quests:

```python
# In the market area
if not _is_quest_active(campaign_state, "rise_in_the_east"):
    events.append("You overhear a conversation about pirates disrupting trade on the northern coast. The East Empire Company seeks help.")
```

## Testing

Run the test suite to verify functionality:

```bash
python3 tests/test_windhelm_triggers.py
```

Run the demo to see example scenarios:

```bash
python3 tests/demo_windhelm_triggers.py
```

## Design Notes

### Quest Hook Intelligence

The system is designed to be intelligent about when to show quest hooks:
- **Context-aware**: Only shows hooks at relevant locations
- **Time-sensitive**: Some hooks only appear at specific times
- **State-aware**: Automatically disables when quest is active/completed
- **Non-repetitive**: Players won't see the same hook multiple times

### Integration with Campaign

These quests are designed to:
1. **Flesh out Windhelm**: Provide local flavor and depth to the city
2. **Complement Main Quest**: Run parallel to the main storyline
3. **Affect Reputation**: Impact player standing in Eastmarch
4. **Enable Progression**: Steps toward becoming Thane of Eastmarch

### Narrative Variety

The quest hooks vary by context:
- **Night at graveyard**: Dramatic discovery scene (Blood on the Ice)
- **Day at graveyard**: Subtle guard conversation
- **Market**: Overheard desperate plea (The White Phial)
- **General entrance**: Atmospheric hints about city tension

## Integration with Story Manager

Example integration with a story management system:

```python
from triggers.windhelm_triggers import windhelm_location_triggers

def on_location_change(player_location, campaign_state):
    """Called when player moves to a new location"""
    
    # Get location-specific events
    events = windhelm_location_triggers(player_location, campaign_state)
    
    # Present events to players
    for event in events:
        narrate_to_players(event)
    
    # Check for quest activation
    if "blood_on_the_ice" in events and not is_quest_active("blood_on_the_ice"):
        # Offer to start the quest
        if player_chooses_to_investigate():
            activate_quest("blood_on_the_ice")
```

## Future Expansion

Additional Eastmarch quests mentioned in the system but not yet fully implemented:

1. **Rise in the East**: Deal with pirates disrupting East Empire Company trade
2. **Argonian Labor Disputes**: Help resolve tensions at the docks
3. **Repairing the Phial**: Follow-up to The White Phial quest

These can be added following the same patterns established in this implementation.

## Companion Data Structure

The system supports companions in two formats:

### Simple Format (Strings)
```python
campaign_state = {
    "companions": {
        "active_companions": ["Stenvar", "Uthgerd"]
    }
}
```

### Complex Format (Objects)
```python
campaign_state = {
    "companions": {
        "active_companions": [
            {"name": "Stenvar", "npc_id": "stenvar"},
            {"name": "Uthgerd the Unbroken", "npc_id": "uthgerd"}
        ]
    }
}
```

The `_is_companion_present()` helper function handles both formats automatically, checking both `name` and `npc_id` fields.

## Quest Notes for GMs

### Blood on the Ice
- This is a complex investigation that rewards careful attention to detail
- Allow players to make mistakes (accusing wrong person) for dramatic tension
- The false accusation path leads to interesting roleplay opportunities
- Consider using skill checks for investigating clues
- The quest impacts reputation significantly - emphasize this to players

### The White Phial
- This is a more straightforward fetch quest with emotional weight
- Emphasize the elderly alchemist's frailty and desperation
- The broken Phial creates a bittersweet moment - roleplay Nurelion's reaction
- The follow-up quest (Repairing the Phial) can be introduced later
- Use this quest to teach players that not all rewards are immediate

Both quests contribute to the player becoming Thane of Eastmarch and establish them as a hero in Windhelm.
