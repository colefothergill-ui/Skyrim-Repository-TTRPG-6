# Campaign Integration Implementation

This document describes the campaign module integration completed for the Skyrim TTRPG repository.

## Overview

The implementation integrates prioritized content from source ZIP files into a structured, coded system for seamless ChatGPT simulation based on Skyrim Fate Core gameplay.

## New Directory Structure

```
├── state/                          # NEW - Campaign state tracking
│   └── campaign_state.json         # Active campaign state and branching decisions
├── data/
│   ├── quests/
│   │   ├── main_quests.json       # NEW - 15 main questline quests
│   │   └── civil_war_quests.json  # NEW - Civil war questline
│   ├── factions.json               # NEW - 9 major factions with clocks
│   ├── thalmor_arcs.json           # NEW - Thalmor villain arcs
│   ├── npc_relationships.json      # NEW - NPC/companion relationship tracking
│   ├── standing_stones.json        # NEW - 13 Standing Stones structured data
│   ├── racial_traits.json          # NEW - 10 playable races structured data
│   ├── daedric_quests.json         # NEW - 10+ Daedric Prince quests
│   └── hidden_paths.json           # NEW - Secret content and alternatives
└── scripts/
    ├── story_manager.py            # NEW - Dynamic branching quest logic
    ├── faction_logic.py            # NEW - Faction clock and progression manager
    ├── npc_manager.py              # NEW - NPC stats and loyalty manager
    └── gm_tools.py                 # NEW - GM toolkit for campaign management
```

## Key Features Implemented

### 1. Campaign Module Integration
- **Main Questline**: All 15 main quests from "Unbound" to "Sovngarde"
- **Civil War**: Complete questline including Battle of Whiterun (Imperial and Stormcloak versions)
- **Thalmor Arcs**: 4 overarching villain plots with phases and clocks
- **Story Manager**: Python script to track branching decisions and story progression

### 2. Faction System
- **9 Major Factions**: Imperial Legion, Stormcloaks, Thalmor, Companions, Thieves Guild, Dark Brotherhood, College of Winterhold, Greybeards, and Blades
- **Faction Clocks**: Track long-term goals and progression
- **Relationships**: Inter-faction relationships with numeric values
- **Resources**: Military strength, gold, and other faction-specific resources

### 3. NPC & Relationship System
- **Companion Bonds**: Loyalty tracking for companions like Lydia, Farkas, Serana
- **Relationship Mechanics**: -100 to +100 scale for NPC relationships
- **Loyalty Thresholds**: Actions have consequences on companion loyalty
- **NPC Manager**: Python tool to manage NPC stats and loyalty

### 4. Session 0 Enhancements
- **Standing Stones**: Structured data for all 13 Standing Stones with game mechanics
- **Racial Traits**: Complete data for all 10 playable races with abilities and bonuses
- **Session Zero Script**: Already existed, now enhanced with structured data

### 5. Quest Content
- **Daedric Quests**: 10 Daedric Prince quests with moral choices and branching outcomes
- **Hidden Paths**: Secret locations, alternate solutions, and easter eggs
- **Quest Structure**: Objectives, rewards, branching points, and consequences

### 6. GM Tools
- **Clock Viewer**: See all active faction and story clocks
- **Faction Hooks**: Generate plot hooks based on faction goals
- **Campaign Overview**: Complete status of campaign state
- **Session Suggestions**: AI-driven suggestions for next session content
- **Quick Reference**: Difficulty, combat, rewards, and social encounter guidelines

## Using the New System

### For Game Masters

#### Starting a New Campaign
1. Review `state/campaign_state.json` - This tracks your campaign progress
2. Use `scripts/session_zero.py` to create player characters
3. Use `scripts/gm_tools.py` to view campaign overview and get session suggestions

#### During Play
1. **Track Story Progress**: Use `scripts/story_manager.py` to record decisions and advance quests
2. **Manage Factions**: Use `scripts/faction_logic.py` to update faction clocks and relationships
3. **Handle NPCs**: Use `scripts/npc_manager.py` to track NPC loyalty and relationships
4. **Get GM Help**: Use `scripts/gm_tools.py` for quick reference and suggestions

#### Example Workflow
```bash
# View campaign status
cd scripts
python3 gm_tools.py
# Choose option 3: Campaign Overview

# Record a major decision
python3 story_manager.py
# Choose option 2: Record Branching Decision

# Update faction after quest
python3 faction_logic.py
# Choose option 3: Update Faction Clock

# Check companion loyalty
python3 npc_manager.py
# Choose option 2: Check NPC/Companion Status
```

### For ChatGPT Integration

All data files are structured in JSON format for easy parsing by ChatGPT. The system tracks:

- **Campaign State**: Current act, civil war status, main quest progress, Thalmor threat
- **Quest Status**: Available, active, completed, or failed quests
- **Faction Clocks**: Progress toward faction goals
- **NPC Relationships**: Party standing with companions and major NPCs
- **World Consequences**: Deaths, alliances, and major decisions made

## Data File Reference

### Campaign State (`state/campaign_state.json`)
Tracks the active campaign including:
- Civil war alliance and battles
- Main quest progression
- Thalmor arc advancement
- Branching decisions made
- World consequences

### Main Quests (`data/quests/main_quests.json`)
Contains all 15 main questline quests with:
- Prerequisites and objectives
- Branching choices and consequences
- Rewards and unlocks
- Next quest progression

### Factions (`data/factions.json`)
9 major factions with:
- Leaders and headquarters
- Goals and alignment
- Progress clocks
- Resources and military strength
- Inter-faction relationships
- Joinable ranks

### Thalmor Arcs (`data/thalmor_arcs.json`)
4 overarching villain plots:
- Perpetual Warfare
- Talos Eradication
- Dragon Investigation
- Blades Elimination

Each with phases, objectives, and discovery mechanics.

### NPC Relationships (`data/npc_relationships.json`)
Relationship tracking including:
- Companion bond mechanics
- Major NPC relationships
- NPC-to-NPC dynamics
- Loyalty thresholds and consequences

### Standing Stones (`data/standing_stones.json`)
13 Standing Stones with:
- Location and lore
- Game mechanics (Fate Core format)
- Best suited for character types

### Racial Traits (`data/racial_traits.json`)
10 playable races with:
- Racial abilities and powers
- Skill bonuses
- Cultural traits
- Starting aspects

### Daedric Quests (`data/daedric_quests.json`)
10+ Daedric Prince quests with:
- Moral alignments
- Branching choices
- Artifacts and rewards
- Themes and difficulty

### Hidden Paths (`data/hidden_paths.json`)
Secret content including:
- Hidden locations (Blackreach, Forgotten Vale)
- Alternate quest solutions
- Hidden questlines
- Easter eggs and secrets

## Python Scripts Reference

### story_manager.py
Campaign progression manager:
- Record branching decisions
- Update civil war state
- Advance main quest
- Track Thalmor arcs
- Generate story summaries

### faction_logic.py
Faction management:
- Update faction clocks
- Modify faction relationships
- Manage resources
- Simulate faction turns
- Resolve faction conflicts

### npc_manager.py
NPC and companion management:
- Track NPC loyalty
- Update relationships
- Check companion status
- Create NPC templates
- Loyalty checks for situations

### gm_tools.py
GM toolkit:
- View all active clocks
- Get faction plot hooks
- Campaign overview
- Session content suggestions
- Quick reference guides
- Random encounter generator

## Integration with Existing Files

The new system integrates with:
- `scripts/session_zero.py` - Uses new standing_stones.json and racial_traits.json
- `docs/how_to_gm.md` - Referenced by gm_tools.py for guidelines
- `data/world_state/current_state.json` - Parallel tracking with campaign_state.json
- `data/npcs/*.json` - Extended by npc_relationships.json

## Future Enhancements

Potential additions:
- [ ] Companion-specific quest integration
- [ ] Dynamic faction event generation
- [ ] Automated session log generation
- [ ] Integration with existing story_progression.py
- [ ] Web-based dashboard for campaign tracking

## Credits

Implementation based on:
- Elder Scrolls: Skyrim - Fate Core Campaign Module
- Skyrim Faction Pack: Side Plot C – Allegiances in War
- Daedric Princes, Man & Mer, and the Standing Stones of Skyrim
- Dragonbreaks, Creatures, and Companions Module

All structured for optimal ChatGPT integration and tabletop gameplay.
