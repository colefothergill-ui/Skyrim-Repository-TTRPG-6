# Hadvar and Ralof Companion Guide

## Overview

Hadvar (Imperial Legion) and Ralof (Stormcloaks) are potential starting companions who join the party based on their civil war allegiance choice during Session Zero. These companions serve as early-game allies, provide narrative hooks, and offer tactical support during the Battle of Whiterun.

## Session Zero Integration

### Allegiance Selection

During Session Zero, players choose their party's faction alignment:

1. **Imperial Legion** - Hadvar joins as an active companion
2. **Stormcloak Rebellion** - Ralof joins as an active companion  
3. **Neutral** - Both become available companions (players can recruit one or both later through roleplay)

### Automatic Assignment

The system automatically:
- Assigns the appropriate companion to `active_companions` in campaign state
- Sets starting loyalty at 60/100
- Records the civil war choice decision in branching_decisions
- Updates starting narrative to mention the companion

## Companion Mechanics

### Hadvar (Imperial Legion)

**Faction**: Imperial Legion  
**Starting Loyalty**: 60/100  
**Role**: Defensive tank and tactical support

#### Combat Abilities
- **Imperial Training**: +2 to Fight when defending a position or ally
- **Steady Under Fire**: +2 to Will when resisting fear/intimidation
- **Shield Brother**: When fighting alongside an ally, both gain +1 to defend

#### Loyalty Increases (+5 to +10)
- Defend innocent civilians
- Complete Imperial Legion quests
- Visit Riverwood and check on family (Alvor)
- Make pragmatic, honorable decisions
- Stand up against Thalmor oppression
- Show mercy to defeated Stormcloaks

#### Loyalty Decreases (-3 to -50)
- Attack Imperial soldiers (-20)
- Join Stormcloaks (-50, will leave party)
- Harm civilians (-15)
- Act dishonorably (-5)
- Ignore family in Riverwood (-3)

#### Key Relationships
- **Alvor** (Uncle) - Blacksmith in Riverwood, provides free services at high loyalty
- **Sigrid** (Aunt) - Connection to Riverwood community
- **Legate Rikke** - Direct commander, admires her leadership
- **General Tullius** - Respects but questions some tactics

#### Companion Quests
1. **Protecting Riverwood** (Loyalty 70+): Help defend Riverwood from threats
   - Reward: +10 loyalty, free smithing from Alvor
2. **The Right Side of History** (Loyalty 80+): Investigate Thalmor influence
   - Reward: +15 loyalty, access to Imperial intelligence

### Ralof (Stormcloaks)

**Faction**: Stormcloaks  
**Starting Loyalty**: 60/100  
**Role**: Aggressive fighter and morale booster

#### Combat Abilities
- **For Skyrim!**: Once per scene, rally all allies in zone with +1 to attack
- **Nord's Fury**: +2 to Fight when fighting Imperial forces
- **Unbreakable Spirit**: Once per session, auto-succeed on Will roll to resist intimidation

#### Loyalty Increases (+3 to +10)
- Complete Stormcloak quests
- Defend Talos worship or shrines
- Visit Riverwood and check on family (Gerdur)
- Stand against the Thalmor
- Show respect for Nord traditions
- Fight honorably in battle

#### Loyalty Decreases (-3 to -50)
- Attack Stormcloak soldiers (-20)
- Join Imperial Legion (-50, will leave party)
- Disrespect Talos or Nordic culture (-10)
- Harm civilians (-15)
- Cooperate with Thalmor (-20)
- Ignore family in Riverwood (-3)

#### Key Relationships
- **Gerdur** (Sister) - Runs lumber mill in Riverwood, provides shelter
- **Hod** (Brother-in-law) - Respects him
- **Frodnar** (Nephew) - Protective, wants better future
- **Ulfric Stormcloak** - Unwavering loyalty to Jarl and leader
- **Galmar Stone-Fist** - Commander, respects as warrior

#### Companion Quests
1. **Protecting Riverwood** (Loyalty 70+): Help defend Riverwood from Imperial scouts/bandits
   - Reward: +10 loyalty, shelter and supplies from Gerdur
2. **The Talos Legacy** (Loyalty 80+): Find and protect hidden Talos shrine from Thalmor
   - Reward: +15 loyalty, Blessing of Talos bonus, unique Talos amulet

## Location-Specific Dialogue Hooks

### Riverwood

**Hadvar**:
- "We should visit my uncle Alvor's forge. He'll help us, no questions asked."
- At forge: "Uncle! It's good to see you. These are allies I've fought beside in Skyrim's troubled times."

**Ralof**:
- "My sister Gerdur runs the lumber mill here. She and her husband will shelter us."
- At mill: "Gerdur! By Talos, it's good to see you alive. These are friends."

### Whiterun

**Hadvar**:
- Approaching: "Whiterun. The heart of Skyrim. We need to inform the Jarl about the escalating civil war."
- Civil war: "The Battle of Whiterun is coming. I believe the Empire is necessary, but... I hope we can end this with minimal bloodshed."

**Ralof**:
- Approaching: "Whiterun. For now, Balgruuf sits the fence, but he's already made his choice - the Empire's lap dog."
- Civil war: "The Battle of Whiterun will decide Skyrim's future. We fight for freedom, Talos worship, and our children's future."

### Combat

**Hadvar**:
- Start: "Form up! Protect the vulnerable and watch your flanks!"
- Victory: "Well fought. Let's help the wounded and regroup."

**Ralof**:
- Start: "For Skyrim! Show these bastards what true Nords are made of!"
- Victory: "That's how we do it! Skyrim's freedom is worth every drop of blood!"

## Battle of Whiterun Integration

### Imperial Version (with Hadvar)

**Tactical Bonuses**:
- All party members gain +1 to defend actions when fighting alongside Hadvar
- Shield Brother stunt applies to all party members in his zone
- Provides tactical coordination for defensive positioning

**Loyalty Reward**: +15 loyalty if Hadvar participates and survives the battle

**Narrative Role**: Hadvar coordinates with Imperial forces and Whiterun guards, using his credentials and tactical training to hold defensive positions.

### Stormcloak Version (with Ralof)

**Tactical Bonuses**:
- All party members gain +1 to attack actions when fighting alongside Ralof
- "For Skyrim!" stunt can be used twice in this battle (instead of once per scene)
- Rallies Stormcloak troops and boosts morale

**Loyalty Reward**: +15 loyalty if Ralof participates and survives the battle

**Narrative Role**: Ralof leads charges alongside the party, inspiring Stormcloak warriors and demonstrating Nord fury in assault tactics.

## Neutral Party Options

When players choose neutral alignment:

1. **Both Available**: Hadvar and Ralof both appear in `available_companions` list
2. **No Starting Companion**: No one is in `active_companions` initially
3. **Recruitment Triggers**:
   - Players may encounter Hadvar in Whiterun (Imperial connection)
   - Players may encounter Ralof in Stormcloak camps
   - GM decides based on party actions and choices which companion they meet first
4. **Dynamic Recruitment**: Players can roleplay choosing which companion to recruit based on their actions

### GM Guidance for Neutral Parties

- If party helps Imperial NPCs or soldiers, introduce Hadvar
- If party helps Stormcloak sympathizers or stands up for Talos worship, introduce Ralof
- At critical moments (e.g., just before Battle of Whiterun), present choice between both
- Recruiting one may make the other unavailable or hostile depending on circumstances

## Using Story Manager Methods

### Get Starting Companion
```python
from story_manager import StoryManager

story_mgr = StoryManager()
companion = story_mgr.get_starting_companion()

if companion:
    print(f"Active companion: {companion['name']}")
    print(f"Loyalty: {companion['loyalty']}")
```

### Get Dialogue Hooks
```python
dialogue_hooks = story_mgr.get_companion_dialogue_hooks("Whiterun", "arrival")

for companion in dialogue_hooks['companions']:
    print(f"\n{companion['name']} in {companion['location']}:")
    for hook in companion['hooks']:
        print(f"  {hook['trigger']}: {hook['dialogue']}")
```

## Loyalty Thresholds

### 80-100: Deeply Loyal
- Will sacrifice themselves for party
- Shares personal quests and secrets
- Provides faction intelligence and warnings
- Maximum tactical bonuses

### 60-79: Loyal Companion
- Reliable and trustworthy
- Fights alongside party without question
- Shares relevant information
- Standard tactical bonuses

### 40-59: Questioning Loyalty
- Professional but distant
- Questions party decisions
- May refuse particularly dangerous or dishonorable orders
- Reduced tactical effectiveness

### 20-39: At Risk of Leaving
- Seriously considers leaving
- Refuses to fight against their faction
- Openly disagrees with party
- May warn enemies in some situations

### 0-19: Will Leave
- Abandons party
- May become hostile if party joins opposing faction
- Relationship irreparably damaged

## Character Growth and Variants

### Veteran Progression

After participating in 3+ major battles, companions can advance:

**Hadvar (Veteran)**:
- Fight increases to Superb (+5)
- Adds mental stress box
- New stunt: "Battle-Hardened: Ignore first mild consequence in combat"

**Ralof (Veteran)**:
- Fight increases to Superb (+5)
- Adds mental stress box
- New stunt: "War Hero: Once per session, inspire all allies in scene with +2 to all rolls for one exchange"

## Tips for GMs

1. **Use Companions as Narrative Guides**: Let them suggest visiting family in Riverwood, explain civil war context, or provide local knowledge

2. **Loyalty Drives Story**: Track loyalty carefully and use it to create dramatic moments (e.g., companion refusing to fight their former allies)

3. **Family Connections**: Alvor (Hadvar) and Gerdur (Ralof) provide safe havens and resources - reward players for engaging with these NPCs

4. **Faction Tension**: If party has high loyalty but acts against companion's faction, create internal conflict and roleplay opportunities

5. **Battle of Whiterun Impact**: This battle should be the culmination of Act I - use companion presence to make it emotionally impactful

6. **Neutral Path Complexity**: For neutral parties, the choice between Hadvar and Ralof (or recruiting neither) should feel meaningful and consequential

7. **Companion Death**: If a companion dies, it should have major narrative impact on their family and faction relations

## Integration with Other Systems

- **Thalmor Arc**: Both Hadvar and Ralof hate the Thalmor - use this as common ground
- **Civil War Context**: Both witnessed early civil war conflicts - they can share their perspective
- **Whiterun Politics**: Both have opinions on Jarl Balgruuf's neutrality
- **Faction Narrative**: Companions provide faction-specific perspectives on loyalty, honor, and Skyrim's future

## Code References

- **NPC Stat Sheets**: `data/npc_stat_sheets/hadvar.json`, `data/npc_stat_sheets/ralof.json`
- **Session Zero Integration**: `scripts/session_zero.py` (lines 375-500)
- **Story Manager Methods**: `scripts/story_manager.py` (get_starting_companion, get_companion_dialogue_hooks)
- **Civil War Quests**: `data/quests/civil_war_quests.json` (Battle of Whiterun sections)
- **Tests**: `tests/test_hadvar_ralof_integration.py`
