# Data Templates

This directory contains templates for creating new campaign content.

## NPC Template

Copy this template to create a new NPC in `data/npcs/`:

```json
{
  "name": "Character Name",
  "id": "npc_XXX",
  "type": "Type (Companion, Jarl, Merchant, etc.)",
  "location": "Location Name",
  "faction": "Faction Name (optional)",
  "aspects": {
    "high_concept": "Their High Concept",
    "trouble": "Their Trouble",
    "other_aspects": [
      "Additional Aspect 1",
      "Additional Aspect 2",
      "Additional Aspect 3"
    ]
  },
  "skills": {
    "Great": ["Skill"],
    "Good": ["Skill", "Skill"],
    "Fair": ["Skill", "Skill", "Skill"],
    "Average": ["Skill", "Skill", "Skill", "Skill"]
  },
  "stunts": [
    "Stunt Name: Description",
    "Stunt Name: Description",
    "Stunt Name: Description"
  ],
  "stress": {
    "physical": [false, false, false],
    "mental": [false, false]
  },
  "consequences": {
    "mild": null,
    "moderate": null,
    "severe": null
  },
  "refresh": 3,
  "fate_points": 3,
  "notes": "Background and personality notes",
  "relationships": {
    "Character Name": "Relationship description"
  },
  "quests": ["Quest names they're involved with"],
  "inventory": ["Items they carry"]
}
```

## PC Template

Copy this template to create a new PC in `data/pcs/`:

```json
{
  "name": "Character Name",
  "id": "pc_XXX",
  "player": "Player Name",
  "race": "Race",
  "class": "Class",
  "level": 1,
  "aspects": {
    "high_concept": "High Concept",
    "trouble": "Trouble",
    "other_aspects": [
      "Aspect 1",
      "Aspect 2",
      "Aspect 3"
    ]
  },
  "skills": {
    "Great": ["Skill"],
    "Good": ["Skill", "Skill"],
    "Fair": ["Skill", "Skill", "Skill"],
    "Average": ["Skill", "Skill", "Skill", "Skill"]
  },
  "stunts": [
    "Stunt Name: Description",
    "Stunt Name: Description",
    "Stunt Name: Description"
  ],
  "stress": {
    "physical": [false, false, false],
    "mental": [false, false]
  },
  "consequences": {
    "mild": null,
    "moderate": null,
    "severe": null
  },
  "refresh": 3,
  "fate_points": 3,
  "experience": 0,
  "milestones": [],
  "equipment": ["Starting equipment"],
  "gold": 100,
  "relationships": {
    "NPC Name": "Relationship"
  },
  "quests": ["Active quests"],
  "notes": "Character background and notes"
}
```

## Session Template

Copy this template to create a new session in `data/sessions/`:

```json
{
  "session_number": 1,
  "date": "YYYY-MM-DD",
  "title": "Session Title",
  "gm": "GM Name",
  "players_present": ["Player1", "Player2"],
  "characters_present": ["pc_001", "pc_002"],
  "session_summary": "What happened this session",
  "key_events": [
    "Major event 1",
    "Major event 2"
  ],
  "npcs_encountered": [
    "NPC Name - Role"
  ],
  "locations_visited": [
    "Location Name"
  ],
  "quests_updated": [
    {
      "quest": "Quest Name",
      "status": "Active/Completed/Failed"
    }
  ],
  "loot_acquired": [
    "Item name"
  ],
  "experience_gained": 50,
  "fate_points_awarded": 1,
  "notes": "GM notes for the session",
  "next_session_prep": [
    "Prep item 1",
    "Prep item 2"
  ]
}
```

## Quest Template

Copy this template to create a new quest in `data/quests/`:

```json
{
  "quest_id": "quest_XXX",
  "name": "Quest Name",
  "type": "Main Quest / Side Quest / Faction Quest",
  "status": "Pending / Active / Completed / Failed",
  "giver": "NPC Name",
  "location": "Location Name",
  "description": "Quest description",
  "objectives": [
    {
      "description": "Objective description",
      "status": "Pending / Active / Completed",
      "optional": false
    }
  ],
  "rewards": {
    "experience": 50,
    "gold": 100,
    "items": ["Item name"],
    "reputation": "+10 with Faction"
  },
  "prerequisites": ["Required quest"],
  "consequences": {
    "success": "What happens on success",
    "failure": "What happens on failure"
  },
  "complications": [
    "Possible complication 1",
    "Possible complication 2"
  ],
  "notes": "GM notes",
  "related_npcs": ["NPC names"],
  "related_locations": ["Location names"]
}
```

## Faction Template

Copy this template to create a new faction in `data/factions/`:

```json
{
  "name": "Faction Name",
  "id": "faction_XXX",
  "type": "Guild / Military / Court / etc.",
  "leader": "Leader Name",
  "headquarters": "Location",
  "alignment": "Alignment/Stance",
  "description": "Faction description",
  "goals": [
    "Primary goal",
    "Secondary goal"
  ],
  "resources": {
    "military_strength": "None / Low / Moderate / High",
    "wealth": "None / Low / Moderate / High",
    "influence": "None / Low / Moderate / High"
  },
  "clock": {
    "name": "Clock Name (Current Goal)",
    "progress": 0,
    "segments": 8,
    "description": "What the clock represents"
  },
  "relationships": {
    "Other Faction": "Relationship status"
  },
  "notable_members": [
    "Member name and role"
  ],
  "status": "Current status",
  "notes": "Additional notes"
}
```

## World State Template

Modify `data/world_state/current_state.json` as your campaign progresses:

```json
{
  "game_date": "Day of Month, Year",
  "in_game_days_passed": 0,
  "current_era": "Era Name",
  "major_events": [
    "Major event 1",
    "Major event 2"
  ],
  "political_situation": {
    "skyrim_status": "Status",
    "imperial_control": ["Hold names"],
    "stormcloak_control": ["Hold names"],
    "neutral": ["Hold names"]
  },
  "civil_war_status": {
    "status": "Status description",
    "major_battles": [
      {
        "location": "Location",
        "date": "Date",
        "outcome": "Imperial/Stormcloak/Stalemate"
      }
    ],
    "hero_status": "Current status of player/leading military figures"
  },
  "faction_standings": {
    "Faction Name": {
      "strength": 50,
      "morale": 50,
      "public_support": 50
    }
  },
  "weather_and_season": "Current weather/season",
  "rumors_and_news": [
    "Rumor 1",
    "Rumor 2"
  ],
  "active_threats": [
    "Threat 1",
    "Threat 2"
  ],
  "notes": "Additional world state notes"
}
```

## Quick Tips

### Naming Conventions
- NPCs: `firstname_lastname.json` or `title_name.json`
- PCs: `character_name.json`
- Sessions: `session_NNN.json` (e.g., `session_001.json`)
- Quests: `quest_name.json` (lowercase, underscores)
- Factions: `faction_name.json` (lowercase, underscores)

### IDs
- NPCs: `npc_001`, `npc_002`, etc.
- PCs: `pc_001`, `pc_002`, etc.
- Quests: `quest_001`, `quest_002`, etc.
- Factions: Use descriptive IDs like `whiterun_guard`, `companions`, etc.

### Skills Reference
Common Fate Core skills for Skyrim:
- **Physical**: Fight, Shoot, Athletics, Physique, Stealth
- **Mental**: Notice, Will, Lore, Empathy
- **Social**: Rapport, Deceive, Contacts
- **Technical**: Crafts, Survival

### Aspects Guidelines
- **High Concept**: Who they are in one phrase
- **Trouble**: What complicates their life
- **Other Aspects**: Important traits, relationships, beliefs

Examples:
- "Nord Warrior Seeking Redemption"
- "Duty Before Personal Desires"
- "The Greybeards Called My Name"

### Stress Boxes
- **Physical**: Based on Physique (2-4 boxes typical)
- **Mental**: Based on Will (2-4 boxes typical)

### Consequences
- **Mild (-2)**: Recovers after one scene
- **Moderate (-4)**: Recovers after one session
- **Severe (-6)**: Recovers after one scenario

---

For more information, see the [Getting Started Guide](../docs/getting_started.md) and example files in the `data/` directories.
