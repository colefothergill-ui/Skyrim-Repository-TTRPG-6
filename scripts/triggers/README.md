# Location Triggers Module

This module contains location-based trigger systems for various regions in Skyrim.

## Purpose

Location triggers provide:
- Atmospheric descriptions when entering new areas
- Context-aware NPC and companion commentary
- Dynamic events based on location and party composition
- Modular hooks for future expansion

## Current Implementations

### Whiterun Triggers (`whiterun_triggers.py`)

Handles all Whiterun Hold locations including:
- Whiterun City (general entrance)
- Plains District
- Wind District  
- Cloud District

Features companion commentary for Whiterun-based followers (currently Lydia).

### Windhelm Triggers (`windhelm_triggers.py`)

Handles all Windhelm and Eastmarch locations including:
- Windhelm City districts:
  - Palace of the Kings (Ulfric's throne room)
  - Gray Quarter (Dunmer district with racial tension)
  - Stone Quarter (market district)
  - Windhelm Docks (Argonian workers, East Empire Company)
- Eastmarch wilderness:
  - Hot Springs (volcanic tundra)
  - Dunmeth Pass (border with Morrowind)

Features one-time narrative events (e.g., Rolff Stone-Fist harassing Dunmer) and evolving ambient descriptions.

### Falkreath Triggers (`falkreath_triggers.py`)

Handles Falkreath Hold locations and Dark Brotherhood integration including:
- Falkreath City (graveyard, Jarl's longhouse, Dead Man's Drink Inn)
- Dark Brotherhood Sanctuary (Black Door, initiation sequences)
- Somber atmosphere and death-themed events

Features Dark Brotherhood contact triggers, Astrid's abduction scene, and sanctuary entry.

### The Pale Triggers (`pale_triggers.py`)

Handles Dawnstar and The Pale Hold including:
- Dawnstar City districts:
  - Harbor (docks, Captain Wayfinder)
  - Jarl's Longhouse (Jarl Skald or Brina Merilis)
  - Windpeak Inn (nightmare crisis hub)
  - Quicksilver & Iron-Breaker Mines
- Quest triggers:
  - Waking Nightmare (Erandur's Daedric quest)
  - Giant bounty (Jarl's quest)
  - Fine-Cut Void Salts (Captain Wayfinder's quest)
- Environmental hazards (blizzards, extreme cold)

Features Stormcloak/Imperial faction awareness and atmospheric cold coastal setting.

### The Rift Triggers (`rift_triggers.py`)

Handles Riften and The Rift Hold locations including the Thieves Guild integration.

## Usage

```python
from triggers import whiterun_location_triggers, windhelm_location_triggers

campaign_state = {
    "companions": {
        "active_companions": ["Lydia"]
    }
}

# Whiterun triggers
events = whiterun_location_triggers("whiterun", campaign_state)

# Windhelm triggers
events = windhelm_location_triggers("windhelm_palace_of_the_kings", campaign_state)
```

## Future Expansions

Additional trigger modules can be added for other holds and locations:
- `riften_triggers.py` - Riften and the Rift Hold ✓ Implemented
- `solitude_triggers.py` - Solitude and Haafingar Hold
- ~~`windhelm_triggers.py` - Windhelm and Eastmarch Hold~~ ✓ Implemented
- `markarth_triggers.py` - Markarth and the Reach
- `winterhold_triggers.py` - Winterhold and its college
- ~~`dawnstar_triggers.py` - Dawnstar and the Pale~~ ✓ Implemented (as `pale_triggers.py`)
- ~~`falkreath_triggers.py` - Falkreath Hold~~ ✓ Implemented
- `morthal_triggers.py` - Morthal and Hjaalmarch
- `wilderness_triggers.py` - Roads, forests, and wilderness areas

## Testing

Each trigger module should have corresponding tests in the `tests/` directory.

Test suites available:
- `tests/test_whiterun_triggers.py` - Whiterun triggers test suite
- `tests/test_windhelm_triggers.py` - Windhelm triggers test suite
- `tests/test_falkreath_triggers.py` - Falkreath triggers test suite
- `tests/test_pale_triggers.py` - The Pale (Dawnstar) triggers test suite
- `tests/test_rift_triggers.py` - The Rift triggers test suite

## Documentation

For detailed information about the triggers, see:
- `docs/whiterun_triggers_guide.md`
- `docs/windhelm_triggers_guide.md`

For demo usage examples, run:
- `tests/demo_whiterun_triggers.py`
- `tests/demo_windhelm_triggers.py`
- `tests/demo_falkreath.py`
- `tests/demo_pale_triggers.py`
- `tests/demo_rift_triggers.py`
