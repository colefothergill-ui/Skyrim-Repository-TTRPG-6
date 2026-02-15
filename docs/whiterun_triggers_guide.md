# Whiterun Location Triggers

## Overview

The Whiterun Location Triggers module provides location-specific events and companion commentary for Whiterun Hold locations. This system enables dynamic, context-aware narrative events that respond to the player's location and party composition.

## Features

### Location-Specific Events

The module provides unique descriptive events for different areas of Whiterun:

- **Plains District**: Lower district with marketplace and shops
- **Wind District**: Central residential district with Jorrvaskr and the Temple of Kynareth
- **Cloud District**: Upper district containing Dragonsreach
- **General Whiterun**: Main city entrance

### Companion Commentary

The system includes a placeholder for companion-specific dialogue that triggers when companions return to familiar locations. Currently implemented:

- **Lydia (Housecarl of Whiterun)**: Comments when entering any Whiterun location

## Usage

### Basic Usage

```python
from triggers.whiterun_triggers import whiterun_location_triggers

# Basic campaign state
campaign_state = {
    "companions": {
        "active_companions": []
    }
}

# Get events for a location
events = whiterun_location_triggers("whiterun", campaign_state)
for event in events:
    print(event)
```

### With Companions

```python
# Campaign state with active companions
campaign_state = {
    "companions": {
        "active_companions": ["Lydia", "Hadvar"]
    }
}

# Lydia will comment when in Whiterun
events = whiterun_location_triggers("whiterun", campaign_state)
# Returns both location description and Lydia's commentary
```

## API Reference

### `whiterun_location_triggers(loc, campaign_state)`

Generate location-specific triggers for Whiterun locations.

**Parameters:**
- `loc` (str): Current location string (e.g., "whiterun", "whiterun_plains_district")
- `campaign_state` (dict): Dictionary containing campaign state including companions

**Returns:**
- List[str]: Event strings to be narrated to players

**Example:**
```python
events = whiterun_location_triggers("whiterun_wind_district", campaign_state)
# Returns: ["The Wind District stretches before you..."]
```

## Location Keys

The following location keys are recognized:

- `"whiterun"` - General Whiterun entrance
- `"whiterun_plains_district"` - Lower marketplace district
- `"whiterun_wind_district"` - Central residential district
- `"whiterun_cloud_district"` - Upper district with Dragonsreach

Location matching is case-insensitive and uses substring matching, so variations like "Whiterun_Plains_District" or "whiterun plains district" will work.

## Extending the System

### Adding New Companions

To add commentary for additional companions, follow the pattern established for Lydia:

```python
# In whiterun_triggers.py, after the Lydia check:

# Check for Aela (Companion member from Jorrvaskr)
if _is_companion_present(active_companions, "aela") and loc_lower.startswith("whiterun"):
    events.append('Aela stretches and grins. "Good to be back at Jorrvaskr. The road is fine, but nothing beats a warm meal and mead with the Companions."')

# Check for Farkas (Another Companion member)
if _is_companion_present(active_companions, "farkas") and loc_lower.startswith("whiterun"):
    events.append('Farkas looks around with a contented smile. "Home. Good to be home."')
```

Note: The `_is_companion_present()` helper function handles both string and dictionary companion formats automatically.

### Adding New Locations

To add triggers for new locations within Whiterun:

```python
# Add after existing district checks
elif "dragonsreach" in loc_lower:
    events.append("You ascend the wooden ramp into Dragonsreach. The great hall opens before you, dominated by Jarl Balgruuf's throne.")
```

### Adding District-Specific Companion Commentary

For more specific companion reactions:

```python
# Lydia commenting specifically in the Cloud District
if "cloud" in loc_lower and _is_companion_present(active_companions, "lydia"):
    events.append('Lydia looks up at Dragonsreach. "I served here before becoming your Housecarl. Many memories in these halls."')
```

## Testing

Run the test suite to verify functionality:

```bash
python3 tests/test_whiterun_triggers.py
```

Run the demo to see example scenarios:

```bash
python3 tests/demo_whiterun_triggers.py
```

## Design Notes

### Minimal Impact

The system is designed to be:
- **Non-intrusive**: Returns empty lists when no triggers match
- **Graceful**: Handles missing campaign state keys without errors
- **Flexible**: Works with both string companions and complex companion objects
- **Modular**: Easy to extend with new locations and companions

### Future Development

This implementation provides a foundation for:
1. More sophisticated companion AI that responds to specific story beats
2. Dynamic dialogue based on companion loyalty levels
3. Companion-to-companion interactions in specific locations
4. Weather and time-of-day dependent commentary
5. Quest-state dependent location descriptions

## Integration with Story Manager

The triggers can be integrated with the Story Manager:

```python
from triggers.whiterun_triggers import whiterun_location_triggers
from story_manager import StoryManager

story_manager = StoryManager()
campaign_state = story_manager.load_campaign_state()

# When player moves to a new location
current_location = "whiterun_wind_district"
events = whiterun_location_triggers(current_location, campaign_state)

# Add events to story manager's narrative queue
for event in events:
    story_manager.add_narrative_event(event)
```

## Companion Data Structure

The system supports companions in two formats:

### Simple Format (Strings)
```python
campaign_state = {
    "companions": {
        "active_companions": ["Lydia", "Hadvar", "Ralof"]
    }
}
```

In this format, companion names are checked directly against the string.

### Complex Format (Objects)
```python
campaign_state = {
    "companions": {
        "active_companions": [
            {
                "name": "Lydia",
                "npc_id": "lydia",
                "loyalty": 70
            },
            {
                "name": "Hadvar",
                "npc_id": "hadvar",
                "loyalty": 65
            }
        ]
    }
}
```

In this format, the function checks both the `name` and `npc_id` fields of the companion dictionary. Both formats are fully supported and will correctly trigger companion commentary.
