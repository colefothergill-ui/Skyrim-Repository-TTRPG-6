# Custom Content Integration Guide

This guide explains how to use the new custom content features: Civil War and Thalmor Focus Campaign, Dragonbreak system, and Faction Plot Allegations.

## Overview

Three major systems have been added to support custom campaign content:

1. **Dragonbreak Manager** - Manage parallel timeline branches
2. **Faction Allegations** - Track accusations and conspiracies (Side Plot C mechanics)
3. **Story Manager Integration** - Seamlessly integrate timeline branches with story progression

## 1. Dragonbreak Manager

The Dragonbreak Manager allows you to create and manage parallel timelines when players make major decisions.

### Basic Usage

```python
from dragonbreak_manager import DragonbreakManager

manager = DragonbreakManager()

# Create a timeline fracture
branch_id = manager.create_timeline_fracture(
    "Civil War Alliance Split",
    "Timeline diverges based on player's choice of alliance",
    "Battle of Whiterun outcome"
)

# Track an NPC across branches
manager.track_npc_across_branches(
    "ulfric_stormcloak",
    "Ulfric Stormcloak",
    {
        "primary": {"status": "victorious", "location": "Windhelm"},
        branch_id: {"status": "executed", "location": "Solitude"}
    }
)

# Define consequences for a branch
manager.define_branch_consequence(
    branch_id,
    "world_event",
    "Stormcloaks lose Whiterun, Imperial morale increases"
)

# Switch to a different timeline
manager.switch_timeline(branch_id)
```

### CLI Interface

The Dragonbreak Manager includes a CLI for interactive use:

```bash
cd scripts
python3 dragonbreak_manager.py
```

Options:
1. Create Timeline Fracture
2. Track NPC Across Branches
3. Track Faction Across Branches
4. Track Quest Across Branches
5. Define Branch Consequence
6. Switch Timeline
7. Get Timeline State
8. List Active Dragonbreaks
9. List All Timelines
10. Resolve Dragonbreak

### Use Cases

**Example 1: Civil War Alliance**
```python
# Player must choose between Imperial and Stormcloak
imperial_branch = manager.create_timeline_fracture(
    "Imperial Alliance",
    "Player sides with the Imperial Legion",
    "Joining the Legion quest"
)

stormcloak_branch = manager.create_timeline_fracture(
    "Stormcloak Alliance",
    "Player sides with the Stormcloaks",
    "Joining the Stormcloaks quest"
)

# Track Jarl Balgruuf in both timelines
manager.track_npc_across_branches(
    "jarl_balgruuf",
    "Jarl Balgruuf",
    {
        imperial_branch: {"status": "remains_jarl", "trust": 80},
        stormcloak_branch: {"status": "exiled", "trust": 0}
    }
)
```

**Example 2: Negotiation vs Combat**
```python
# Create branches for different approaches
negotiation_branch = manager.create_timeline_fracture(
    "Diplomatic Resolution",
    "Player successfully negotiates peace",
    "Season Unending completion"
)

combat_branch = manager.create_timeline_fracture(
    "Military Victory",
    "Player pursues military victory",
    "Season Unending refused"
)
```

## 2. Faction Allegations (Side Plot C)

The Faction Allegation system tracks accusations, conspiracies, and plots involving factions.

### Basic Usage

```python
from faction_logic import FactionManager

manager = FactionManager()

# Add an allegation against a faction
allegation_id = manager.add_faction_allegation(
    "stormcloaks",
    "thalmor_conspiracy",
    "Imperial Intelligence",
    "Evidence suggests Ulfric is an unwitting Thalmor asset"
)

# Update evidence level (0-10 scale)
manager.update_allegation_evidence(
    "stormcloaks",
    allegation_id,
    3,  # +3 evidence
    "Found Thalmor dossier on Ulfric at the embassy"
)

# Get all allegations for a faction
allegations = manager.get_faction_allegations("stormcloaks", status_filter="pending")

# Resolve an allegation
manager.resolve_allegation(
    "stormcloaks",
    allegation_id,
    "proven",
    consequences=[
        "Ulfric's reputation damaged",
        "Imperial propaganda gains credibility",
        "Some Stormcloaks defect"
    ]
)
```

### Thalmor Plot Tracking

```python
# Track a Thalmor plot
plot_id = manager.track_thalmor_plot(
    "Prolong the Civil War",
    "stormcloaks",
    "Supply intelligence to losing side to maintain stalemate",
    clock_segments=8
)

# Advance the plot
manager.advance_thalmor_plot(
    plot_id,
    2,  # Advance by 2 segments
    discovery="Players intercept Thalmor courier"
)
```

### Allegation Types

- `thalmor_conspiracy` - Thalmor manipulation or infiltration
- `war_crime` - Atrocities committed during civil war
- `betrayal` - Faction betraying its stated principles
- `corruption` - Bribery, embezzlement, or abuse of power
- `espionage` - Spying for enemy factions

### Evidence System

Evidence levels automatically update allegation status:
- **0-2**: Insufficient evidence (can be marked disproven)
- **3-7**: Moderate evidence (status remains pending)
- **8-10**: Strong evidence (auto-marked as proven)

## 3. Story Manager Integration

The Story Manager now integrates Dragonbreak functionality for seamless timeline management.

### Basic Usage

```python
from story_manager import StoryManager

manager = StoryManager()

# Initiate a dragonbreak through a story event
branch_id = manager.initiate_dragonbreak(
    "Alliance Decision",
    "Player must choose between Imperial and Stormcloak",
    "Battle of Whiterun conclusion"
)

# Track parallel events
manager.track_parallel_event(
    'npc',
    {'id': 'balgruuf', 'name': 'Jarl Balgruuf'},
    {
        'primary': {'status': 'remains_jarl', 'alliance': 'imperial'},
        branch_id: {'status': 'deposed', 'alliance': 'stormcloak'}
    }
)

# Handle branching decisions with automatic timeline creation
branches = manager.handle_branching_decision_with_dragonbreak(
    'civil_war_alliance',
    {
        'imperial': {
            'description': 'Player joins Imperial Legion',
            'consequences': {
                'faction_relations': {'imperial_legion': +20, 'stormcloaks': -30},
                'world_event': 'Stormcloaks lose momentum'
            }
        },
        'stormcloak': {
            'description': 'Player joins Stormcloaks',
            'consequences': {
                'faction_relations': {'imperial_legion': -30, 'stormcloaks': +20},
                'world_event': 'Stormcloaks gain strength'
            }
        }
    }
)
```

## Campaign Integration Examples

### Example 1: Battle of Whiterun

```python
from story_manager import StoryManager
from faction_logic import FactionManager

story = StoryManager()
factions = FactionManager()

# Create timeline branches for different outcomes
imperial_victory = story.initiate_dragonbreak(
    "Imperial Victory at Whiterun",
    "Imperials successfully defend Whiterun",
    "Battle of Whiterun"
)

stormcloak_victory = story.initiate_dragonbreak(
    "Stormcloak Victory at Whiterun",
    "Stormcloaks capture Whiterun",
    "Battle of Whiterun"
)

# Track Jarl Balgruuf
story.track_parallel_event('npc', 
    {'id': 'balgruuf', 'name': 'Jarl Balgruuf'},
    {
        'primary': {'status': 'neutral', 'location': 'Dragonsreach'},
        imperial_victory: {'status': 'imperial_ally', 'location': 'Dragonsreach'},
        stormcloak_victory: {'status': 'exiled', 'location': 'Solitude'}
    }
)

# Add Thalmor plot that benefits from either outcome
plot_id = factions.track_thalmor_plot(
    "Capitalize on Whiterun Battle",
    "both_sides",
    "Use battle aftermath to increase Thalmor influence",
    clock_segments=6
)
```

### Example 2: Thalmor Conspiracy Exposed

```python
from faction_logic import FactionManager

factions = FactionManager()

# Add allegation against Ulfric
allegation = factions.add_faction_allegation(
    "stormcloaks",
    "thalmor_conspiracy",
    "Blades Intelligence",
    "Ulfric Stormcloak was interrogated and broken by the Thalmor"
)

# Players find evidence during Diplomatic Immunity quest
factions.update_allegation_evidence(
    "stormcloaks",
    allegation,
    5,
    "Discovered Ulfric's dossier in Thalmor Embassy"
)

# More evidence from other sources
factions.update_allegation_evidence(
    "stormcloaks",
    allegation,
    2,
    "Thalmor agent confesses under interrogation"
)

# Evidence level is now 7/10 - high but not conclusive
# GM decides how to resolve
```

## Testing

Run the integration test suite to verify all systems:

```bash
cd tests
python3 test_integration.py
```

All 4 test suites should pass:
- Dragonbreak Manager
- Story Manager Integration
- Faction Allegations
- Documentation Updates

## Best Practices

1. **Use Dragonbreaks Sparingly**: Only for major, campaign-altering decisions
2. **Track Key NPCs**: Focus on important characters whose fate matters
3. **Evidence Progression**: Add evidence gradually as players investigate
4. **Thalmor Plots**: Make them long-term (6-8 segments) for gradual tension
5. **Document Timelines**: Use the dragonbreak log to keep track of divergences
6. **Consequences Matter**: Always define meaningful consequences for different branches

## Troubleshooting

**Q: Dragonbreak Manager not available in Story Manager**
A: Ensure `dragonbreak_manager.py` is in the scripts directory and importable

**Q: Allegations not saving**
A: Check that `data/factions.json` exists and is writable

**Q: Tests failing**
A: Ensure you're running from the tests directory with correct paths

## Additional Resources

- `/docs/campaign_module.md` - Updated campaign guide
- `/scripts/README.md` - Script documentation
- `/tests/README.md` - Test documentation
- `/source_material/converted_pdfs/dragonbreaks.md` - Lore reference
