# Skyrim TTRPG Campaign Manager

**Post-Alduin Timeline Campaign System**

A comprehensive storytelling and campaign management repository for running a Fate Core TTRPG set in The Elder Scrolls V: Skyrim. This system tracks all aspects of your campaign including session logs, NPC stats, PC profiles, faction clocks, and world state.

**Campaign Setting:** This repository is designed for campaigns set **after Alduin's defeat**. The dragon crisis has been resolved, and the focus shifts to the **Civil War between the Imperial Legion and Stormcloaks**, with the **Thalmor working behind the scenes** as the ultimate antagonists.

## Features

### 📊 Data Management
- **NPCs**: Track non-player characters with complete Fate Core stats, aspects, relationships, and inventory
- **PCs**: Manage player characters with progression, equipment, and milestone tracking
- **Sessions**: Log each session with events, encounters, loot, and experience
- **Factions**: Monitor faction goals, resources, and clocks for dynamic world progression
- **World State**: Track the overall state of Skyrim including politics, civil war dynamics, and rumors
- **Quests**: Manage quest objectives, rewards, and progression (Civil War focus)
- **Rules**: Complete Fate Core rules adapted for the Skyrim setting
- **PDF Integration**: Organized source materials with structured Markdown/JSON conversions for efficient querying

### 🤖 Automation Scripts
- **story_manager.py**: Dynamic branching quest logic, campaign state tracking, and story progression
- **faction_logic.py**: Faction clock management, relationships, and conflict resolution
- **npc_manager.py**: NPC stats, loyalty tracking, and companion management
- **gm_tools.py**: GM toolkit with clock viewer, faction hooks, and session suggestions
- **story_progression.py**: Automate story advancement, faction clocks, and event generation
- **query_data.py**: Search and filter NPCs, quests, rules, world state, and PDF topics
- **session_manager.py**: Create and update session logs, track character progression
- **session_zero.py**: Interactive Session 0 character creation with race and Standing Stone selection
- **export_repo.py**: Package everything as a .zip for ChatGPT 5.2 integration

### 📖 GM Guidance & Protocols
- **How to GM Guide**: Comprehensive GM protocol document with tone, decision frameworks, and gameplay rules
- **Canon Management**: Three-tier canon system with Dragonbreak protocol for handling divergences
- **Session Boot Protocol**: Structured session start procedures
- **Tri-Check System**: Resolve critical moments with meaningful outcomes
- **Daedric Quest Guidelines**: Morally complex quest structure with artifact mechanics
- **Faction Clocks**: Track long-term goals and create dynamic world changes

### 🎮 ChatGPT Integration
Export your entire campaign as a structured .zip file designed to work seamlessly with ChatGPT 5.2 for:
- Dynamic narrative generation
- Real-time NPC interactions
- Rules adjudication
- Quest and encounter suggestions
- World state management

## Directory Structure

```
├── state/              # Campaign state tracking (NEW)
│   └── campaign_state.json
├── data/
│   ├── npcs/           # Non-player character data
│   ├── pcs/            # Player character profiles
│   ├── sessions/       # Session logs
│   ├── factions/       # Individual faction files
│   ├── factions.json   # Complete faction system (NEW)
│   ├── world_state/    # Current world state
│   ├── quests/         # Quest information
│   │   ├── main_quests.json        # Main questline (NEW)
│   │   └── civil_war_quests.json   # Civil war (NEW)
│   ├── thalmor_arcs.json           # Thalmor villain plots (NEW)
│   ├── npc_relationships.json      # NPC bonds (NEW)
│   ├── standing_stones.json        # Standing Stones data (NEW)
│   ├── racial_traits.json          # Race data (NEW)
│   ├── daedric_quests.json         # Daedric quests (NEW)
│   ├── hidden_paths.json           # Secrets & alternatives (NEW)
│   ├── rules/          # Fate Core rules for Skyrim
│   └── pdf_index.json  # Index for querying PDF content
├── source_material/
│   ├── raw_pdfs/       # Original PDF source materials
│   └── converted_pdfs/ # Structured Markdown/JSON conversions
├── scripts/
│   ├── story_manager.py    # Campaign progression (NEW)
│   ├── faction_logic.py    # Faction management (NEW)
│   ├── npc_manager.py      # NPC/companion manager (NEW)
│   ├── gm_tools.py         # GM toolkit (NEW)
│   ├── story_progression.py
│   ├── query_data.py
│   ├── session_manager.py
│   ├── session_zero.py
│   └── export_repo.py
├── docs/
│   ├── how_to_gm.md    # Comprehensive GM guidance
│   ├── getting_started.md
│   ├── quick_reference.md
│   └── templates.md
├── logs/               # Session and dragonbreak logs
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Basic understanding of Fate Core RPG system
- Familiarity with The Elder Scrolls V: Skyrim setting

### Installation

1. Clone this repository:
```bash
git clone https://github.com/colefothergill-ui/The-Skyrim-Repository-3.git
cd The-Skyrim-Repository-3
```

2. No additional dependencies required! All scripts use Python standard library.

### Quick Start

### For Game Masters

#### New Campaign Setup
1. **Character Creation**: Run `scripts/session_zero.py` for interactive character creation
2. **Campaign State**: Review `state/campaign_state.json` to understand initial setup
3. **GM Overview**: Run `scripts/gm_tools.py` and select option 3 for campaign overview

#### During Play
- **Track Story**: Use `scripts/story_manager.py` to record decisions and advance quests
- **Manage Factions**: Use `scripts/faction_logic.py` to update clocks and relationships
- **Handle NPCs**: Use `scripts/npc_manager.py` to track loyalty and relationships
- **GM Assistance**: Use `scripts/gm_tools.py` for suggestions and quick reference

#### For Detailed Information
See [CAMPAIGN_INTEGRATION.md](CAMPAIGN_INTEGRATION.md) for complete documentation on:
- Campaign module integration (main quests, civil war, Thalmor arcs)
- Faction system with 9 major factions
- NPC and relationship tracking
- Standing Stones and racial traits
- Daedric quests and hidden paths
- Python script usage guides

## Quick Start

#### 0. Session Zero - Character Creation
Start your campaign with the interactive Session Zero script:

```bash
cd scripts
python3 session_zero.py
```

This guides you through:
- Choosing from 10 playable races (Nord, Imperial, Breton, etc.)
- Selecting a Standing Stone blessing (Warrior, Mage, Thief, etc.)
- Developing character backstory
- Discussing faction alignments
- Creating properly structured character files

#### 1. View Example Data
Explore the example files to understand the data structure:
- `data/npcs/example_npc.json` - Example NPC (Lydia)
- `data/pcs/example_pc.json` - Example PC
- `data/sessions/session_001.json` - Example session log
- `data/world_state/current_state.json` - Current world state

#### 2. Query Data and PDF Content
Use the query script to search your campaign data and PDF topics:

```bash
cd scripts
python3 query_data.py
```

Example queries in your own scripts:
```python
from query_data import DataQueryManager

manager = DataQueryManager("../data")

# Find NPCs in Whiterun
npcs = manager.query_npcs(location="Whiterun")

# Get active quests
quests = manager.query_quests(status="Active")

# Search rules for "magic"
rules = manager.search_rules("magic")

# Query PDF topics
standing_stones = manager.query_pdf_topics("standing stones")
races_info = manager.get_pdf_content("races")
```

#### 3. Manage Sessions
Create and manage session logs:

```bash
python3 session_manager.py
```

Example usage:
```python
from session_manager import SessionContextManager

manager = SessionContextManager("../data")

# Create new session
session = manager.create_session(
    session_number=2,
    title="Journey to Whiterun",
    gm="Your Name",
    players_present=["Player1", "Player2"]
)

# Update session with events
manager.update_session(2, {
    "key_events": ["Encountered bandits on the road", "Arrived at Whiterun"],
    "experience_gained": 50
})

# Generate summary
summary = manager.generate_session_summary(2)
print(summary)
```

#### 4. Progress the Story
Automate story progression:

```bash
python3 story_progression.py
```

Example usage:
```python
from story_progression import StoryProgressionManager

manager = StoryProgressionManager("../data")

# Advance time
manager.advance_time(3)  # 3 days pass

# Update faction clock
manager.update_faction_clock("whiterun_guard", 2)  # Progress by 2 segments

# Generate story events
events = manager.generate_story_events()
for event in events:
    print(f"{event['type']}: {event['description']}")
```

#### 5. Export for ChatGPT
Create a .zip package for ChatGPT 5.2:

```bash
python3 export_repo.py
```

This creates `skyrim_ttrpg_export.zip` containing:
- All campaign data
- Context file for ChatGPT
- Quick reference guide
- Statistics

Upload this .zip to ChatGPT 5.2 and use prompts like:
- "Generate dialogue for an encounter with Lydia"
- "What are the current active threats in Skyrim?"
- "Suggest a complication for the 'Before the Storm' quest"
- "Create a combat encounter appropriate for level 3 characters"

## Data Format Examples

### NPC Format
```json
{
  "name": "Lydia",
  "id": "npc_001",
  "type": "Companion",
  "location": "Whiterun",
  "aspects": {
    "high_concept": "Sworn Shield of the Thane",
    "trouble": "Duty Before Personal Desires"
  },
  "skills": {
    "Great": ["Fight"],
    "Good": ["Physique", "Will"]
  },
  "relationships": {
    "Jarl Balgruuf": "Loyal servant"
  }
}
```

### Quest Format
```json
{
  "quest_id": "quest_001",
  "name": "Before the Storm",
  "type": "Main Quest",
  "status": "Active",
  "objectives": [
    {
      "description": "Speak to the Jarl of Whiterun",
      "status": "Active"
    }
  ]
}
```

### Faction Format
```json
{
  "name": "Whiterun Guard",
  "clock": {
    "name": "Dragon Defense Preparations",
    "progress": 3,
    "segments": 8
  },
  "relationships": {
    "Imperial Legion": "Allied"
  }
}
```

## Advanced Usage

### Custom Scripts
Create your own scripts using the data structure:

```python
import json
from pathlib import Path

# Load world state
with open("data/world_state/current_state.json", "r") as f:
    world_state = json.load(f)

# Your custom logic here
if world_state["dragon_crisis"]["status"] == "Beginning":
    print("Dragons are attacking!")
```

### Faction Clocks
Faction clocks represent long-term goals:
- Progress clocks during story progression
- When a clock fills, trigger a major event
- Example: "Dragon Defense Preparations" reaching 8/8 means Whiterun is ready for dragon attack

### Session Workflow
1. **Pre-Session**: Review previous session, prepare NPCs and encounters
2. **During Session**: Take notes on events, NPCs encountered, loot
3. **Post-Session**: Update session log, advance characters, progress story
4. **Between Sessions**: Update faction clocks, generate new events

## GM Protocols and Guidelines

### How to GM
The comprehensive GM guide (`docs/how_to_gm.md`) provides:
- **Tone & Philosophy**: Epic but grounded, respectful of player agency
- **Five-Option Decision Framework**: Present meaningful choices with 5 structured options
- **Session Boot Protocol**: Start each session with context refresh and status check
- **Tri-Check System**: Resolve critical moments with three sequential checks
- **Dragonbreak Protocol**: Handle canon divergences with timeline fractures
- **Daedric Quest Guidelines**: Create morally complex quests with lasting consequences

### Canon Management
Three-tier system for handling Elder Scrolls canon:
- **Tier 1 - Immutable Core**: Dragons returned, civil war, major cities (requires Dragonbreak to change)
- **Tier 2 - Flexible Canon**: Quest outcomes, NPC fates, faction relationships (can change through play)
- **Tier 3 - Player-Driven**: Backstories, new NPCs, original quests (completely open)

### Dragonbreaks
When player actions irrevocably conflict with canon:
1. Announce the Dragonbreak
2. Document in `logs/dragonbreak_log.md`
3. Create world aspect ("Time Broke at Dragonsreach")
4. Allow both timelines to coexist narratively

### Session Logging
Logs follow standardized format: `/logs/YYYY-MM-DD_session-##_TITLE.md`

Example: `/logs/2026-01-23_session-05_Battle-for-Whiterun.md`

Includes:
- Session summary and key events
- NPCs encountered and locations visited
- Combat encounters and loot
- Quest updates and faction clock progress
- Experience and character progression
- Dragonbreaks (if any occurred)

### PDF Source Materials
All source PDFs organized in `source_material/`:
- **raw_pdfs/**: Original PDF files
- **converted_pdfs/**: Structured Markdown/JSON for efficient querying
- **pdf_index.json**: Topic mapping for query system

Converted content includes:
- All 10 playable races with mechanics
- 13 Standing Stones with Fate Core translations
- Dragonbreak and canon management protocols
- Complete Daedric Prince quest guide

## Tips for Game Masters

### Using Aspects
- Compel PC aspects to create drama: "Your 'Impulsive' aspect means you rush in before the trap is disarmed..."
- Invoke NPC aspects to make them memorable: "Lydia's 'Duty Before Personal Desires' means she insists on checking the dangerous room first"

### Managing Faction Clocks
- Progress clocks based on narrative time and player actions
- Use clocks to create urgency and consequences
- Example clocks:
  - "Stormcloak Advance on Whiterun" (threat)
  - "Rebuilding Helgen" (opportunity)
  - "Research Dragon Weakness" (player-driven)

### World State Updates
Update world state regularly:
- After major events
- When time advances significantly
- When factions achieve goals
- When new threats emerge

### ChatGPT Integration
For best results with ChatGPT:
1. Export your campaign regularly
2. Include specific context in your prompts
3. Reference exact NPC/quest names from your data
4. Ask for Fate Core mechanics compliance
5. Request NPCs stay "in character" based on their aspects
6. Share the `docs/how_to_gm.md` file for AI GM guidance

### Session Zero Best Practices
- Use `session_zero.py` for structured character creation
- Allow players to explore all race and Standing Stone options
- Discuss campaign premise and tone expectations
- Establish faction preferences early
- Document everything in session zero log

## Documentation

- [How to GM Guide](docs/how_to_gm.md) - Comprehensive GM protocols and guidelines
- [Getting Started Guide](docs/getting_started.md) - Detailed setup and first session guide
- [Fate Core Skyrim Rules](data/rules/fate_core_skyrim.md) - Complete rules reference
- [Source Material README](source_material/README.md) - PDF integration and querying guide

## Contributing

This is a personal campaign repository, but feel free to:
- Fork it for your own Skyrim campaign
- Adapt the structure for other settings
- Share improvements and suggestions

## System Requirements

- **Python**: 3.7+
- **Storage**: Minimal (typically <10MB for full campaign)
- **ChatGPT**: Compatible with ChatGPT 5.2 file upload feature

## License

This is a campaign management tool. Skyrim and The Elder Scrolls are property of Bethesda Softworks. Fate Core is a product of Evil Hat Productions.

## Credits

- **Game System**: Fate Core by Evil Hat Productions
- **Setting**: The Elder Scrolls V: Skyrim by Bethesda Softworks
- **Framework**: Custom campaign management system

## Support

For questions or issues:
1. Check the example data files
2. Review the script documentation
3. Consult the Fate Core Skyrim rules in `data/rules/`

---

**Ready to start your epic Skyrim adventure!** 🐉⚔️

*"I used to be an adventurer like you, then I took an arrow in the knee... Now I'm a Game Master."*