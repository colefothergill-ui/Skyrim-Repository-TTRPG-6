# NPC/Enemy Stat Sheets

This directory contains stat sheets for NPCs and enemies in the Skyrim TTRPG campaign. These stat blocks use Fate Core mechanics and can be dynamically queried and applied to scenes.

## Directory Contents

### Friendly NPCs
- **whiterun_guard.json** - Standard city guard, loyal to Jarl Balgruuf

### Hostile NPCs
- **thalmor_agent.json** - Elite Aldmeri Dominion operative with magical abilities

### Enemies
- **bandit_marauder.json** - Common road bandits and outlaws
- **draugr_overlord.json** - Ancient Nord undead warriors in tombs
- **frost_dragon.json** - Epic dragon encounter with breath attacks
- **giant.json** - Peaceful unless provoked, devastating in combat
- **vampire.json** - Intelligent undead with supernatural abilities

## Stat Sheet Structure

Each stat sheet contains:

### Core Information
- `name`: Entity name
- `id`: Unique identifier
- `type`: Entity type (e.g., "Ally", "Dragon", "Undead")
- `category`: "Friendly NPC", "Hostile NPC", or "Enemy"
- `location`: Where this entity is typically found
- `faction`: Faction affiliation

### Fate Core Mechanics
- `aspects`: High Concept, Trouble, and other aspects
- `skills`: Rated on Fate ladder (Average +1 to Legendary +8)
- `stunts`: Special abilities and bonuses
- `stress`: Physical and Mental stress tracks
- `consequences`: Mild, Moderate, Severe consequence slots
- `refresh` / `fate_points`: Fate point economy

### Additional Fields

**For Friendly NPCs:**
- `trust_clock`: Tracks relationship development with party
- `personality_notes`: Speaking style, motivations, fears, quirks
- `relationships`: Connections to other NPCs and factions

**For Enemies:**
- `combat_tactics`: How the enemy fights
- `special_mechanics`: Armor, immunities, weaknesses, unique abilities
- `scene_triggers`: When/where to use this enemy
- `loot`: Guaranteed, possible, and location-specific drops
- `variants`: Stronger/weaker versions

## Usage

### Query Stat Sheets

```python
from query_data import DataQueryManager

manager = DataQueryManager()

# Search by name
guards = manager.query_npc_enemy_stats(name="guard")

# Search by location
whiterun_npcs = manager.query_npc_enemy_stats(location="Whiterun")

# Search by category
enemies = manager.query_npc_enemy_stats(category="Enemy")

# Get all stat sheets
all_stats = manager.list_all_stat_sheets()
```

### Apply to Scenes

```python
from story_manager import StoryManager

manager = StoryManager()

# Get NPCs for a scene
scene_setup = manager.trigger_scene_event({
    'location': 'Nordic ruins',
    'type': 'combat'
})

# Apply combat consequences
consequences = manager.apply_combat_consequences(
    enemy_type="dragon",
    outcome="victory"
)
```

### GM Tools

```python
from gm_tools import GMTools

tools = GMTools()

# Get suggestions for scene
tools.suggest_npc_stats_for_scene(
    location="Whiterun",
    scene_type="combat"
)

# Set up combat encounter
tools.inject_npc_stats_to_combat(
    enemy_types=["bandit", "draugr"],
    difficulty="hard"
)

# Get relationship advice
tools.get_npc_relationship_advice("Jarl Balgruuf")
```

## Creating New Stat Sheets

To create a new stat sheet:

1. **Choose Template**: Use an existing stat sheet as a template
2. **Fill Core Fields**: Name, type, category, location, faction
3. **Define Aspects**: Create thematic high concept and trouble
4. **Assign Skills**: Use Fate ladder (typically 2-4 skill levels)
5. **Create Stunts**: 2-4 stunts that reflect abilities
6. **Set Stress**: Physical (2-4 boxes for tough enemies), Mental (2-4 for intelligent foes)
7. **Write Tactics**: Describe how they fight/interact
8. **Define Triggers**: When/where to use this entity

### Skill Distribution Guidelines

**Friendly NPCs** (Low Combat):
- Focus on social skills (Rapport, Empathy, Contacts)
- 1-2 combat skills at Fair or Good
- 2-3 fate points, Refresh 2-3

**Hostile NPCs** (Balanced):
- Mix of combat and social/mental skills
- Great or Superb in primary skills
- 3-4 fate points, Refresh 3

**Standard Enemies** (Combat Focus):
- Good to Great combat skills
- Few or no fate points
- 2-3 stress boxes

**Boss Enemies** (Epic Encounters):
- Superb to Fantastic primary skills
- 4-6 stress boxes
- Multiple stunts and special mechanics
- Consider phases for dramatic fights

## Integration with Game Systems

Stat sheets integrate with:
- **Query System**: Dynamic searching and filtering
- **Story Manager**: Scene-based application
- **GM Tools**: Suggestions and encounter building
- **World State**: Combat consequences affect campaign
- **Faction System**: Awareness and relationship tracking
- **Quest System**: Automatic progression triggers

## Best Practices

1. **Match to Location**: Ensure location field is accurate for queries
2. **Scene Triggers**: List specific situations where entity appears
3. **Balanced Stats**: Follow Fate Core guidelines for skill distribution
4. **Interesting Aspects**: Make aspects compellable and invokable
5. **Varied Tactics**: Give enemies distinct combat approaches
6. **Consequence Integration**: Consider how defeating this enemy affects the world
7. **Loot Appropriateness**: Match rewards to difficulty and type
8. **Variants**: Create stronger versions for escalation

## Stat Sheet Categories Explained

### Friendly NPC
- Allies, merchants, quest givers
- Can be reasoned with and befriended
- Use trust clocks for relationship tracking
- Focus on personality and social interaction

### Hostile NPC
- Intelligent adversaries with complex motivations
- Can sometimes be negotiated with
- Political/faction consequences for killing
- Mix of combat and non-combat abilities

### Enemy
- Monsters, creatures, mindless foes
- Pure combat encounters
- Focus on interesting tactics and mechanics
- Provide loot and experience

## File Naming Convention

Use lowercase with underscores:
- `npc_name.json` - Standard format
- `enemy_type.json` - For enemies
- `faction_member.json` - For faction-specific NPCs

Examples:
- `whiterun_guard.json`
- `frost_dragon.json`
- `thalmor_agent.json`

## Maintenance

When updating stat sheets:
1. Maintain JSON validity (test with `python3 -m json.tool filename.json`)
2. Keep fields consistent with existing sheets
3. Update this README if adding new fields
4. Test queries after adding new sheets
5. Consider impact on existing encounters

## Support

For questions or issues:
- See `docs/how_to_gm.md` for usage in gameplay
- Check script documentation in `scripts/README.md`
- Review existing stat sheets as examples
