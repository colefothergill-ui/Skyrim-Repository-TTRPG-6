# Dragonbreaks and Canon

## What is a Dragonbreak?

A Dragonbreak is a narrative concept from Elder Scrolls lore where time becomes non-linear, allowing multiple contradictory timelines to exist simultaneously. In TTRPG terms, it's a mechanical tool for resolving player choices that diverge from established canon.

## Using Dragonbreaks in Your Campaign

### When to Invoke a Dragonbreak

1. **Player Actions Contradict Canon**: Players kill an essential NPC or complete a quest in a way that conflicts with established lore
2. **Multiple Timeline Options**: Different choices lead to equally valid but contradictory outcomes
3. **Retcon Needed**: Correcting a previous decision that broke the narrative
4. **Parallel Campaigns**: Reconciling events from multiple game groups in the same world

### How to Implement

**Step 1: Acknowledge the Break**
- Inform players that a Dragonbreak has occurred
- Explain what contradictory events are now simultaneously true
- Frame it as mythic Elder Scrolls lore, not a mistake

**Step 2: Document the Break**
- Record the date and circumstances in world_state.json
- Note which events are "canonically uncertain"
- Track both versions of events if needed

**Step 3: Narrative Impact**
- NPCs may have conflicting memories
- History books might contain contradictions
- Some characters may be aware of the break (very rare)

### Example Dragonbreak Scenarios

**Scenario 1: Ulfric's Fate**
- **Canon**: Ulfric Stormcloak survives to lead the rebellion
- **Player Action**: Players kill Ulfric in Windhelm
- **Dragonbreak Resolution**: 
  - In one timeline, Ulfric died by player hands
  - In another, he survived and continues the civil war
  - NPCs have uncertain memories: "I heard Ulfric died... or was that someone else?"
  - The civil war continues regardless, with a new Stormcloak leader if needed

**Scenario 2: Paarthurnax**
- **Canon**: The ancient dragon mentor survives
- **Player Action**: Players side with the Blades and kill Paarthurnax
- **Dragonbreak Resolution**:
  - Paarthurnax is simultaneously dead and alive
  - Some dragons claim to still hear his voice
  - The Greybeards remember him both ways
  - Future dragon encounters reference both versions

## GM Guidelines for Canon Management

### Flexibility Principle
- **Canon is a guideline, not a prison**
- Player agency > rigid adherence to Skyrim's storyline
- Use Dragonbreaks sparingly to preserve immersion

### Documentation
- Track all major divergences from canon in a "Dragonbreak Log"
- Include: date, event, player choice, narrative resolution
- Store in `/logs/dragonbreak_log.md`

### Communication
- Be transparent with players about when canon is being bent
- Let them know their choices matter and have real consequences
- Frame Dragonbreaks as special Elder Scrolls mysticism, not failures

### Canon Tiers

**Tier 1 - Immutable Canon**: Core events that anchor the setting
- Dragons have returned to Skyrim
- Alduin threatens the world
- The civil war between Imperials and Stormcloaks
- Essential city leaders exist (unless players explicitly target them)

**Tier 2 - Flexible Canon**: Events that can change without breaking the world
- Specific quest outcomes
- Relationships between factions
- Minor NPC fates
- Side quest resolutions

**Tier 3 - Player-Driven**: Completely open to player choice
- Character backstories
- New NPCs and factions
- Original quests
- Personal character arcs

### When NOT to Use Dragonbreaks

- Player makes a simple mistake (use retcon or "it didn't happen" instead)
- Minor deviation from canon that doesn't impact the world
- Player wants to "undo" a choice for mechanical reasons (use Fate Point compels instead)
- Overuse cheapens the mechanic

## Mechanical Implementation

### Dragonbreak Tracking (world_state.json)

Add a `dragonbreaks` array to your `world_state.json` file:

```json
"dragonbreaks": [
  {
    "date": "17th of Last Seed, 4E 201",
    "event": "The Fate of Ulfric Stormcloak",
    "player_choice": "Players assassinated Ulfric in Windhelm",
    "canon_conflict": "Ulfric should survive to lead rebellion",
    "resolution": "Galmar Stone-Fist assumes leadership. Timeline split.",
    "affected_npcs": ["Ulfric Stormcloak", "Galmar Stone-Fist", "General Tullius"],
    "affected_factions": ["Stormcloaks", "Imperial Legion"]
  }
]
```

### Aspect Creation
When a Dragonbreak occurs, consider creating world aspects:
- "Time is Uncertain in Skyrim"
- "Conflicting Histories"
- "The Dragon Broke"

These can be invoked or compelled for narrative effect.

## Player Communication Template

> "Your actions have created what's known as a Dragonbreak - a fracture in time where multiple truths exist simultaneously. In Elder Scrolls lore, this has happened before (the Warp in the West, the Middle Dawn). Your choice mattered, and now the timeline has split. Here's what that means for our campaign..."

## Related Mechanics

- **Tri-Check System**: Use for important divergence points (see tri_check.md)
- **Fate Points**: Players can spend Fate Points to influence Dragonbreak resolution
- **Compels**: GMs can compel aspects to create Dragonbreak scenarios
