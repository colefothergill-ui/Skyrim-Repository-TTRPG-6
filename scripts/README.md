# Skyrim TTRPG Scripts

This directory contains Python scripts for managing and automating your Skyrim TTRPG campaign.

## Scripts Overview

### 1. query_data.py
**Purpose**: Search and filter campaign data

**Usage**:
```bash
python3 query_data.py
```

**Features**:
- Query NPCs by name, location, or faction
- Query PCs by name or player
- Search quests by status, type, or name
- Search factions
- Get world state information
- Search rules documentation
- View session logs
- Get character relationships

**Example in your own code**:
```python
from query_data import DataQueryManager

manager = DataQueryManager("../data")

# Find all NPCs in Whiterun
whiterun_npcs = manager.query_npcs(location="Whiterun")

# Find active quests
active = manager.query_quests(status="Active")

# Search rules
magic_rules = manager.search_rules("magic")
```

---

### 2. story_progression.py
**Purpose**: Automate story advancement and world state changes

**Usage**:
```bash
python3 story_progression.py
```

**Features**:
- Advance in-game time
- Update faction clocks
- Generate story events based on world state
- Progress quests
- Add major events to timeline
- Generate rumors

**Example in your own code**:
```python
from story_progression import StoryProgressionManager

manager = StoryProgressionManager("../data")

# Advance time by 3 days
manager.advance_time(3)

# Update faction clock
manager.update_faction_clock("whiterun_guard", 2)

# Generate events
events = manager.generate_story_events()

# Add major event
manager.add_major_event("Dragon attack on Western Watchtower")
```

---

### 3. session_manager.py
**Purpose**: Create and manage session logs

**Usage**:
```bash
python3 session_manager.py
```

**Features**:
- Create new session logs
- Update existing sessions
- Generate session summaries
- Get campaign timeline
- Track character participation
- Update character data from session results

**Example in your own code**:
```python
from session_manager import SessionContextManager

manager = SessionContextManager("../data")

# Create new session
session = manager.create_session(
    session_number=2,
    title="Journey to Whiterun",
    gm="Your Name",
    players_present=["Alice", "Bob", "Charlie"]
)

# Update session
manager.update_session(2, {
    "key_events": ["Fought bandits", "Reached Whiterun"],
    "experience_gained": 50
})

# Generate summary
summary = manager.generate_session_summary(2)
```

---

### 4. export_repo.py
**Purpose**: Export campaign as .zip for ChatGPT integration

**Usage**:
```bash
python3 export_repo.py
```

**Features**:
- Creates `skyrim_ttrpg_export.zip`
- Includes all campaign data
- Generates context file for ChatGPT
- Creates quick reference guide
- Compiles campaign statistics

**Output**: `skyrim_ttrpg_export.zip` (ready to upload to ChatGPT 5.2)

**What's included**:
- All data files (NPCs, PCs, quests, etc.)
- Scripts directory
- Documentation
- `_chatgpt_context.json` (AI instructions)
- `_statistics.json` (campaign stats)

---

### 5. triggers/whiterun_triggers.py
**Purpose**: Location-based narrative triggers and events for Whiterun

**Usage**:
```python
from triggers.whiterun_triggers import whiterun_location_triggers

# Campaign state tracks which events have occurred
campaign_state = {}

# Get events for a location
events = whiterun_location_triggers("Whiterun - Plains District", campaign_state)

# Display events to players
for event in events:
    print(event)
```

**Features**:
- First-time descriptive text for each district (Plains, Wind, Cloud)
- Repeatable atmospheric flavor text on subsequent visits
- Dynamic event triggers (Gray-Mane vs Battle-Born feud)
- Quest hooks (Missing in Action quest)
- Integration with campaign state flags
- Jarl audience trigger after dragon fight

**Districts covered**:
- **Plains District**: Market area, initial feud encounter
- **Wind District**: Residential area, Companions and Temple, quest hooks
- **Cloud District/Dragonsreach**: Jarl's palace, formal audiences

**Integration**: Call `whiterun_location_triggers()` from your story manager whenever the player location changes to a Whiterun area. The function returns a list of narrative descriptions and event prompts to present to the players.

---

### 6. workflow_example.py
**Purpose**: Demonstrates complete workflow

**Usage**:
```bash
cd scripts
python3 workflow_example.py
```

**What it does**:
1. Queries current campaign state
2. Reviews previous session
3. Generates story events
4. Generates rumors
5. Creates quick reference
6. Shows campaign statistics

**Use this to**: Learn how to combine multiple scripts in your own automation

---

## Running Scripts

### From the scripts directory:
```bash
cd scripts
python3 query_data.py
python3 story_progression.py
python3 session_manager.py
python3 export_repo.py
python3 workflow_example.py
```

### From the repository root:
```bash
python3 scripts/query_data.py
python3 scripts/story_progression.py
# etc.
```

## Dependencies

**None!** All scripts use only Python standard library:
- `json` - For reading/writing data files
- `os` / `pathlib` - For file operations
- `datetime` - For timestamps
- `zipfile` - For export functionality

**Requirements**: Python 3.7 or higher

## Data Directory Structure

Scripts expect this data structure:
```
data/
├── npcs/           # NPC JSON files
├── pcs/            # PC JSON files
├── sessions/       # Session log JSON files
├── factions/       # Faction JSON files
├── world_state/    # World state JSON files
├── quests/         # Quest JSON files
└── rules/          # Rules markdown files
```

## Tips for Using Scripts

### Automation Ideas

**Pre-Session Preparation**:
```bash
# Review current state
python3 query_data.py

# Generate story hooks
python3 story_progression.py
```

**Post-Session Cleanup**:
```bash
# Update session log (manual editing)
# Then update characters
python3 session_manager.py

# Progress the story
python3 story_progression.py
```

**Weekly Export for ChatGPT**:
```bash
# Export campaign
python3 export_repo.py

# Upload skyrim_ttrpg_export.zip to ChatGPT
```

### Custom Scripts

Create your own scripts using these as libraries:

```python
#!/usr/bin/env python3
"""My custom campaign script"""

from query_data import DataQueryManager
from story_progression import StoryProgressionManager

# Your custom logic here
query = DataQueryManager("../data")
story = StoryProgressionManager("../data")

# Example: Auto-progress all faction clocks by 1
import json
from pathlib import Path

factions_dir = Path("../data/factions")
for faction_file in factions_dir.glob("*.json"):
    with open(faction_file) as f:
        faction = json.load(f)
    
    faction_id = faction_file.stem
    story.update_faction_clock(faction_id, 1)
    print(f"Updated {faction['name']}")
```

## Troubleshooting

**"No world state found"**
- Make sure `data/world_state/current_state.json` exists
- Run `python3 story_progression.py` to verify it loads

**"FileNotFoundError"**
- Check you're running from the correct directory
- Scripts use relative paths (`../data` from scripts/)

**"Module not found"**
- Make sure you're running scripts from the `scripts/` directory
- Or adjust Python path in your custom scripts

## Next Steps

1. Explore the example data files in `data/`
2. Run each script to see what it does
3. Modify the example data for your campaign
4. Create your own NPCs, quests, and sessions
5. Export and use with ChatGPT 5.2

---

For more information, see the main [README.md](../README.md) and [Getting Started Guide](../docs/getting_started.md).
