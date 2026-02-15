# Getting Started Guide

Welcome to the Skyrim TTRPG Campaign Manager! This guide will help you set up and run your first session.

## Step 1: Understand the Basics

### What is Fate Core?
Fate Core is a narrative-focused RPG system where:
- Characters are defined by **Aspects** (descriptive phrases)
- **Skills** determine what you're good at
- **Fate Points** let you influence the story
- Conflicts use 4dF (Fudge dice) or a standard d6 conversion

### The Skyrim Setting
This campaign uses The Elder Scrolls V: Skyrim as the setting, with:
- Dragons returning after thousands of years
- Civil war between Imperials and Stormcloaks
- Nine holds, each with unique challenges
- Rich lore and diverse factions

## Step 2: Create Your Campaign

### Set Up World State
1. Review `data/world_state/current_state.json`
2. Adjust the starting situation:
   - Date and timeline
   - Political situation
   - Dragon crisis status
   - Faction standings

### Create Factions
1. Add factions relevant to your campaign
2. Set up faction clocks for major goals
3. Define relationships between factions

Example: Create a new faction file in `data/factions/`:
```json
{
  "name": "Companions",
  "type": "Guild",
  "leader": "Kodlak Whitemane",
  "clock": {
    "name": "Hunt the Silver Hand",
    "progress": 2,
    "segments": 6
  }
}
```

## Step 3: Create Characters

### Player Characters
1. Have each player create a character using the example in `data/pcs/example_pc.json`
2. Each PC needs:
   - Name, race, and class
   - 5 Aspects (High Concept, Trouble, + 3 others)
   - Skills distributed across the ladder
   - 3 Stunts
   - Starting equipment

### Important NPCs
1. Create key NPCs using `data/npcs/example_npc.json` as a template
2. Focus on NPCs the party will interact with regularly
3. Include:
   - Name and location
   - Aspects that make them memorable
   - Relationships to other characters
   - Goals and motivations

## Step 4: Prepare Your First Session

### Session 0 (Character Creation)
1. Discuss campaign themes and tone
2. Create characters together
3. Establish party connections
4. Set expectations for play style

### Session 1 (First Adventure)
1. Start with a strong opening scene
2. Introduce the main conflict (dragons, civil war, etc.)
3. Give players immediate choices
4. End on a cliffhook

Example first session structure:
```
1. Cold Open: Dragon attack or dramatic event
2. Escape/Survival: Players work together
3. Safe Haven: Meet important NPCs, gather information
4. Call to Action: Clear quest or goal
5. First Choice: Players decide how to proceed
```

## Step 5: Run the Session

### During the Game
1. Describe scenes vividly
2. Ask "What do you do?"
3. Call for rolls when outcomes are uncertain
4. Offer compels to create drama
5. Award Fate Points for good roleplay

### Taking Notes
1. Track key events as they happen
2. Note NPCs encountered
3. Record loot and rewards
4. Note any aspects created during play

### Using the Scripts
During the session:
```bash
# Quick NPC lookup
python3 scripts/query_data.py

# Check world state
python3 scripts/query_data.py
```

## Step 6: Post-Session

### Update Session Log
1. Create session file: `data/sessions/session_NNN.json`
2. Fill in:
   - Session summary
   - Key events
   - NPCs encountered
   - Quests updated
   - Loot acquired
   - Experience and Fate Points awarded

Example:
```bash
python3 scripts/session_manager.py
```

### Progress the Story
1. Update faction clocks
2. Advance time if needed
3. Update world state based on player actions
4. Prepare for next session

```bash
python3 scripts/story_progression.py
```

### Update Character Data
1. Add experience to PCs
2. Handle milestones if earned
3. Update equipment and relationships
4. Clear stress and mild consequences

## Step 7: Prepare Next Session

### Review Progress
1. Read previous session log
2. Check active quests
3. Review NPC relationships
4. Consider faction movements

### Plan Content
1. Design 2-3 scenes
2. Prepare NPCs for those scenes
3. Create potential complications
4. Have backup content ready

### Use Automation
```bash
# Export for ChatGPT assistance
python3 scripts/export_repo.py

# Upload to ChatGPT and ask:
# "Generate 3 quest hooks based on my current campaign state"
# "Create dialogue for Jarl Balgruuf meeting the party"
# "Suggest complications for the dragon investigation"
```

## Common Workflows

### Adding a New NPC
1. Copy `data/npcs/example_npc.json`
2. Rename and update fields
3. Focus on aspects and relationships
4. Add to faction if applicable

### Creating a Quest
1. Copy `data/quests/before_the_storm.json`
2. Define objectives clearly
3. Set appropriate rewards
4. Link to relevant NPCs and locations

### Advancing a Faction Clock
```bash
python3 scripts/story_progression.py
# Then manually call:
# manager.update_faction_clock('faction_id', progress_change)
```

### Generating Story Events
```bash
python3 scripts/story_progression.py
# Reviews world state and suggests events
```

## Tips for Success

### For Game Masters
- **Prep light, improvise heavy**: Know your NPCs' aspects, then roleplay them naturally
- **Use clocks for drama**: Show players the faction clocks to create urgency
- **Fail forward**: Even failed rolls should move the story ahead
- **Compel frequently**: Offer Fate Points to complicate character aspects
- **Say "Yes, and..."**: Build on player ideas when possible

### For Players
- **Invoke your aspects**: Spend Fate Points to be awesome
- **Accept compels**: Let your aspects complicate your life for Fate Points
- **Create advantages**: Use skills to create helpful aspects for the scene
- **Collaborate**: Fate Core is collaborative storytelling

### For Everyone
- **Track Fate Points**: Use physical tokens or tracking sheet
- **Describe actions**: Instead of "I attack," say "I charge with my sword raised, roaring a battle cry!"
- **Build on each other's ideas**: "Yes, and..." is the golden rule
- **Focus on the narrative**: Mechanics serve the story, not the other way around

## Troubleshooting

### "I don't know the Fate Core rules well"
- Read `data/rules/fate_core_skyrim.md`
- Start simple: roll skill + 4dF vs. opposition
- Learn one new rule per session
- Use ChatGPT to explain rules during play

### "My players aren't engaging with aspects"
- Offer compels frequently
- Show the benefits of invoking aspects
- Create situation aspects they can use
- Make aspects relevant to the situation

### "I'm not sure what to do next"
- Check active quests
- Review faction clocks (what's progressing?)
- Ask players what they're interested in
- Generate events with `story_progression.py`

### "Combat is taking too long"
- Use zones instead of detailed maps
- Group minor NPCs
- Let players describe their actions first
- Use concessions to end fights dramatically

## Next Steps

Once you're comfortable with the basics:
1. Add more factions and clocks
2. Create deeper NPC networks
3. Develop custom quests
4. Experiment with unique faction abilities and stunt systems
5. Create custom stunts for unique abilities
6. Develop your own house rules

## Resources

- **Fate Core SRD**: https://fate-srd.com/
- **Skyrim Wiki**: https://elderscrolls.fandom.com/wiki/Skyrim
- **This Repository**:
  - `data/rules/fate_core_skyrim.md` - Complete rules
  - Example files - Reference for data structure
  - Scripts - Automation tools

---

**You're ready to start your campaign!** Good luck, and may your adventures be legendary! 🐉
