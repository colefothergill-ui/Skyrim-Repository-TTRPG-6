# Elder Scrolls TTRPG Campaign Module - GM Guide

## Overview

This document provides comprehensive instructions for running the **Elder Scrolls: Skyrim - Fate Core Campaign Module**, the foundational narrative framework for your Skyrim TTRPG campaign. This module integrates the Civil War and Thalmor conspiracy into a cohesive, Act-based epic focusing on neutral factions navigating a fractured Skyrim.

## Campaign Structure

### Three-Act Framework

The campaign is structured in three acts, each with distinct themes and story focus:

#### **Act I: The Civil War Begins** (Sessions 1-6)
- **Theme**: Allegiance, survival, and choice
- **Focus**: Civil War erupts, neutral factions face pressure, Thalmor influence grows
- **Climax**: Battle of Whiterun (typically session 4-6)
- **Key NPCs**: Jarl Balgruuf, Irileth, Ulfric Stormcloak, General Tullius
- **Player Agency**: Party's choice of sides (or neutrality) shapes future story

#### **Act II: Shadows and Secrets** (Sessions 7-14)
- **Theme**: Conspiracy, political intrigue, divided loyalties
- **Focus**: Thalmor manipulation revealed, civil war escalates, faction conflicts intensify
- **Climax**: Season Unending (if civil war unresolved) or continued war
- **Key NPCs**: Elenwen, Delphine, Esbern, Legate Rikke or Galmar Stone-Fist
- **Player Agency**: Civil war commitment or peace negotiations, exposing Thalmor plots

#### **Act III: Skyrim's Fate** (Sessions 15-20)
- **Theme**: Unity, sacrifice, destiny
- **Focus**: Final push for civil war resolution, confronting Thalmor endgame
- **Climax**: Decisive battle for Windhelm or Solitude
- **Key NPCs**: Ulfric Stormcloak, General Tullius, Elenwen, faction leaders
- **Player Agency**: How to unite (or divide) Skyrim, final confrontation with Thalmor

---

## Main Quest Integration

### Quest Progression Overview

The main questline consists of Civil War and Thalmor conspiracy quests divided across three acts:

**Act I Quests**:
1. Unbound
2. Before the Storm
3. Message to Whiterun
4. Battle for Whiterun
5. Liberation of the Rift (or other holds)
6. Diplomatic Tensions

**Act II Quests**:
7. Diplomatic Immunity
8. A Cornered Rat (Thalmor Investigation)
9. Uncovering Allegiances
10. Season Unending (Optional Peace)
11. Strategic Holds Campaign
12. Thalmor Network Infiltration

**Act III Quests**:
13. The Final Battle (Windhelm or Solitude)
14. Thalmor Confrontation
15. Skyrim's Future

### Key Story Hooks by Quest

Each quest includes story hooks in `/data/quests/main_quests.json`. Here are the critical integration points:

#### **Before the Storm**
- **Hook**: Jarl Balgruuf is under immense pressure from both Imperials and Stormcloaks
- **GM Guidance**: Show the political tension. Both sides want Whiterun's allegiance. Balgruuf tries to stay neutral but knows he can't forever.
- **Foreshadowing**: The Battle of Whiterun is coming

#### **Battle for Whiterun**
- **Hook**: Civil war erupts in Whiterun, neutral stance no longer viable
- **GM Guidance**: This is a pivotal moment. Make it epic. The choice of sides (or neutrality) will resonate throughout the campaign.
- **Thalmor Connection**: Thalmor observers document everything

#### **Diplomatic Immunity**
- **Hook**: Thalmor manipulation of the civil war is exposed
- **GM Guidance**: This is the conspiracy reveal. The Thalmor want neither side to win decisively. They're playing both sides.
- **Documents**: Ulfric's dossier should be shocking - he's an unwitting asset

---

## Civil War Integration

### The Battle of Whiterun

**Timing**: Typically occurs during Act I/II transition (sessions 4-6)

**Trigger**: When "Battle of Whiterun Countdown" clock reaches 8/8, or when party advances civil war quests

**Setup**:
- Ulfric issues ultimatum to Balgruuf: "Join us or face attack"
- Balgruuf must choose: Imperial or Stormcloak
- Party may influence this decision based on their relationship with Balgruuf

**Possible Outcomes**:
1. **Imperial Victory**: Whiterun remains neutral/Imperial, Stormcloak momentum slowed
2. **Stormcloak Victory**: Whiterun falls, Ulfric gains major strategic position
3. **Stalemate**: Both sides weakened, Thalmor benefit most

**Integration with Main Quest**:
- If party is pursuing main quest actively, the battle may occur while they're away (at High Hrothgar, etc.)
- Party can return to find Whiterun's allegiance has shifted
- This creates urgency - the world moves forward whether party is there or not

### Civil War Questlines

**Parallel Progression**: Civil war quests run parallel to the main quest. Party can pursue both simultaneously or focus on one.

**Key Civil War Quests** (see `/data/quests/civil_war_quests.json`):
- Joining the Legion/Stormcloaks
- The Jagged Crown
- Message to Whiterun / Battle for Whiterun
- Regional hold battles
- Final assault (Windhelm or Solitude)

**GM Guidance**:
- Don't force the party to choose immediately
- Neutrality is valid but has consequences (pressure from both sides)
- If civil war unresolved by Act III, Season Unending becomes mandatory

### Season Unending (Optional Quest)

**Trigger**: Party needs to use Dragonsreach for "The Fallen" quest, but civil war is still raging

**Purpose**: Temporary truce to allow main quest progression

**Setup**:
- Greybeards host peace conference at High Hrothgar
- Party mediates between Imperials and Stormcloaks
- Thalmor represented by Elenwen (if invited)

**Outcomes**:
- Temporary truce achieved (both sides make concessions)
- Civil war resumes after Alduin is defeated
- Party's negotiation skills affect terms

---

## Thalmor Arcs

### The Thalmor as Villains

The Thalmor are sophisticated antagonists operating on multiple levels:

1. **Public Face**: Diplomatic representatives enforcing the White-Gold Concordat
2. **Secret Agenda**: Prolong civil war, eliminate Talos worship, hunt Blades, investigate dragons
3. **Long Game**: Weaken both Empire and Skyrim for eventual Dominion takeover

### Key Thalmor Schemes (Track with Clocks)

See `/data/clocks/thalmor_influence_clocks.json` for detailed tracking.

#### **Civil War Manipulation**
- **Goal**: Neither side wins decisively
- **Methods**: Intelligence to losing side, sabotage peace efforts, assassinate moderates
- **Exposure**: Diplomatic Immunity quest reveals documents
- **Party Impact**: Exposing this can unite Imperials and Stormcloaks against Thalmor

#### **Talos Persecution**
- **Goal**: Eliminate Talos worship completely
- **Methods**: Justiciar patrols, arrests, shrine destruction
- **Visibility**: High - creates moral dilemmas for party
- **Party Impact**: Defending Talos worshippers increases Thalmor hostility

#### **Blades Elimination**
- **Goal**: Exterminate remaining Blades members
- **Methods**: Active hunting, interrogation, informant networks
- **Connection**: Blades actively work against Thalmor interests
- **Party Impact**: Protecting Blades makes party Thalmor enemies

#### **Political Infiltration**
- **Goal**: Place Thalmor agents in positions of power
- **Methods**: Bribery, blackmail, strategic marriages
- **Key Question**: Which faction leaders are compromised?
- **Party Impact**: Uncovering compromised leaders affects faction trust

### Key Thalmor NPCs

#### **Elenwen** (First Emissary)
- **Role**: Spy mistress and political manipulator
- **Location**: Thalmor Embassy
- **Key Scenes**: Battle of Whiterun (Act I), Diplomatic Immunity (Act II), Season Unending (Act III)
- **Tactics**: Information, leverage, diplomatic immunity
- **Vulnerability**: Exposure of her schemes

#### **Thalmor Justiciars**
- **Role**: Talos worship enforcers
- **Location**: Road patrols, Talos shrines
- **Key Scenes**: Random encounters, enforcing Concordat
- **Tactics**: Shock magic, arrests, intimidation
- **Vulnerability**: Isolated patrols can be ambushed

#### **Ancano** (College Agent)
- **Role**: Thalmor operative at College of Winterhold
- **Location**: College of Winterhold
- **Key Scenes**: College questline (separate from main module)
- **Connection**: Shows Thalmor presence in all major institutions

### Running Thalmor Encounters

**Frequency**: Sparingly - make each encounter meaningful

**Moral Complexity**: Not all Thalmor are cartoonish villains. Some truly believe in their mission.

**Consequences**: Attacking Thalmor has serious repercussions:
- Diplomatic incidents
- Increased patrols
- Price on party's heads
- Imperial cooperation becomes difficult

**Opportunities**: Thalmor can be:
- Sources of intelligence (if captured)
- Temporary allies against greater threats (dragons)
- Diplomatic obstacles
- Direct combat encounters

---

## NPC Overview

### Act I Key NPCs

#### **Jarl Balgruuf the Greater** (Whiterun)
- **Role**: Neutral Jarl under pressure
- **Key Scenes**: Before the Storm, Dragon Rising, Battle for Whiterun
- **Relationship**: Can become strong ally if party proves themselves
- **Conflict**: Must choose sides eventually

#### **Irileth** (Whiterun Housecarl)
- **Role**: Balgruuf's advisor and military commander
- **Key Scenes**: Dragon Rising, Battle for Whiterun
- **Relationship**: Respects strength and loyalty

#### **Greybeards** (High Hrothgar)
- **Role**: Teaches the Way of the Voice
- **Key Scenes**: The Way of the Voice, The Throat of the World
- **Philosophy**: Peace through the Voice, protect Paarthurnax

#### **Delphine** (Blade Agent)
- **Role**: Last Blade operative, intelligence gatherer
- **Key Scenes**: Diplomatic Immunity, exposing Thalmor plots
- **Conflict**: Wants to eliminate Thalmor influence

### Act II Key NPCs

#### **Elenwen** (Thalmor First Emissary)
- **Stat Sheet**: `/data/npc_stat_sheets/elenwen.json`
- **Role**: Master manipulator, spy mistress
- **Key Scenes**: Diplomatic Immunity, Season Unending
- **Tactics**: Political pressure, intelligence networks

#### **Esbern** (Blades Historian)
- **Role**: Knowledge of historical lore and Thalmor tactics
- **Key Scenes**: A Cornered Rat, strategic planning
- **Value**: Interprets historical patterns, reveals Thalmor weaknesses

#### **Legate Rikke** (Imperial Commander)
- **Stat Sheet**: `/data/npc_stat_sheets/legate_rikke.json`
- **Role**: Imperial military leader, secret Talos worshipper
- **Key Scenes**: Civil war quests (Imperial side)
- **Complexity**: Nord serving Empire, conflicted loyalties

#### **Galmar Stone-Fist** (Stormcloak Commander)
- **Stat Sheet**: `/data/npc_stat_sheets/galmar_stonefist.json`
- **Role**: Ulfric's housecarl and war chief
- **Key Scenes**: Civil war quests (Stormcloak side)
- **Personality**: Direct, traditional, absolutely loyal to Ulfric

### Act III Key NPCs

#### **Ulfric Stormcloak** (Stormcloak Leader)
- **Role**: Leader of the rebellion, unwitting Thalmor asset
- **Key Scenes**: Civil war resolution, confronting Thalmor manipulation
- **Relationship**: Complex - hero to some, traitor to others

#### **General Tullius** (Imperial Commander)
- **Role**: Imperial military leader in Skyrim
- **Key Scenes**: Civil war quests, final battle
- **Personality**: Pragmatic, strategic, focused on Imperial victory

---

## Faction Dynamics

### Trust Clocks

Track party standing with each faction using `/data/clocks/faction_trust_clocks.json`.

**Trust Levels**:
- **0-2**: Stranger (neutral/suspicious)
- **3-5**: Ally (trusted, offers aid)
- **6-8**: Champion (hero status, major support)
- **9-10**: Legend (highest honor, full resources)

### Mutually Exclusive Factions

Some factions cannot both be at high trust:
- **Imperial Legion** vs **Stormcloaks**: Joining one makes the other hostile
- **Blades** vs **Thalmor**: Sworn enemies
- **Dark Brotherhood**: Destroying them ends that faction path

### Neutral Factions

These don't take sides in the civil war:
- Companions
- Thieves Guild
- College of Winterhold
- Dark Brotherhood (cares only about contracts)

---

## Clock System

### Civil War Clocks

See `/data/clocks/civil_war_clocks.json` for full details.

**Primary Clocks**:
1. **Imperial Military Dominance** (3/10): Imperial progress toward victory
2. **Stormcloak Rebellion Momentum** (4/10): Stormcloak progress toward victory
3. **Battle of Whiterun Countdown** (2/8): Tension builds toward pivotal battle
4. **Thalmor Civil War Manipulation** (2/8): Thalmor efforts to prolong war
5. **Civilian War Weariness** (5/10): Toll on common people

**Advancement Guidance**:
- Advance clocks every 2-3 sessions or after major events
- Player actions should significantly impact progression
- Keep both sides roughly balanced until party commits or Act III

### Thalmor Influence Clocks

See `/data/clocks/thalmor_influence_clocks.json` for full details.

**Primary Clocks**:
1. **Thalmor Influence in Skyrim** (3/10)
2. **Talos Persecution Campaign** (5/10)
3. **Intelligence Network** (4/8)
4. **Blades Elimination** (7/10)
5. **Political Infiltration** (2/8)
6. **Ulfric Manipulation** (6/8)

**Advancement Guidance**:
- Advance Thalmor clocks slowly but steadily
- Major setbacks require significant player action (infiltrating embassy, exposing schemes)
- Thalmor plans are long-term

### Faction Trust Clocks

See `/data/clocks/faction_trust_clocks.json` for full details.

Track individual faction relationships:
- Imperial Legion (0/10)
- Stormcloaks (0/10)
- Companions (0/10)
- Thieves Guild (0/10)
- College of Winterhold (0/10)
- Greybeards (0/10)
- Blades (0/10)
- Whiterun (0/10)
- Dark Brotherhood (0/10)

**Update After**:
- Completing faction quests
- Major decisions affecting factions
- Defending/attacking faction members
- Showing respect/disrespect for faction values

---

## GM Best Practices

### Session Structure

**Opening**:
1. Recap previous session
2. Review active clocks and world state
3. Ask: "What are you doing?"

**During Play**:
- Advance clocks based on time passage and player actions
- Show consequences of clock progression (e.g., civilians fleeing Whiterun as Battle clock advances)
- Create urgency through multiple advancing threats

**Closing**:
- Update campaign state
- Advance appropriate clocks
- Foreshadow next session's content

### Pacing Recommendations

**Act I** (4-6 sessions):
- Focus on establishing the world and civil war tensions
- Introduce competing factions and force difficult choices
- Culminate in Battle of Whiterun
- Optional: Early Thalmor encounters

**Act II** (6-8 sessions):
- Slower pace for investigation and conspiracy
- Diplomatic Immunity should feel like a heist
- Multiple side quests and faction work
- Build toward Season Unending or continued warfare

**Act III** (4-6 sessions):
- Accelerate pace for climax
- Focus on civil war resolution
- Confront Thalmor endgame
- Epic finale with the fate of Skyrim at stake

### Player Agency

**Respect Choices**:
- Don't force civil war allegiance
- Allow neutrality (with consequences)
- Support creative solutions to problems

**Branching Paths**:
- Civil War: Imperial, Stormcloak, or peace
- Thalmor: Expose, ignore, or work with (reluctantly)
- Neutral Factions: Which to support

**Consequences Matter**:
- Choices should have lasting impact
- Update world state based on decisions
- NPCs remember party's actions

### Integrating Side Content

**Faction Questlines**: Can run parallel to main quest. Companions, Thieves Guild, College, Dark Brotherhood all have their own arcs.

**Daedric Quests**: Provide moral complexity and powerful rewards. See `/data/daedric_quests.json`.

**Random Encounters**: Use Thalmor Justiciars, civil war patrols to keep world feeling alive.

---

## Troubleshooting

### "Players Won't Choose a Side"

**Solution**: That's valid! Neutrality has consequences:
- Both sides pressure them
- Battle of Whiterun happens without them
- Season Unending becomes mandatory
- NPCs question their commitment

### "Civil War Is Overshadowing Other Content"

**Solution**: Use Thalmor threats to remind everyone of the real enemy:
- Thalmor attacks during civil war battles
- NPCs beg party to focus on the true threat
- Season Unending: Both sides realize Thalmor manipulation is more important

### "Party Killed Elenwen/Major NPC"

**Solution**: Roll with it!
- Killing Elenwen: Major diplomatic incident, new Thalmor leader (possibly worse)
- Killing Delphine: Lose Blades questline, but creative players might rebuild
- Killing Jarl Balgruuf: Whiterun gets new leader, major story shift

### "Players Want to Skip Civil War"

**Solution**: That's their choice!
- Civil war continues in background
- Thalmor manipulation grows unchecked
- World deteriorates without intervention
- Show consequences through NPC suffering

---

## Quick Reference

### Essential Files
- **Main Quests**: `/data/quests/main_quests.json`
- **Civil War Quests**: `/data/quests/civil_war_quests.json`
- **Civil War Clocks**: `/data/clocks/civil_war_clocks.json`
- **Thalmor Clocks**: `/data/clocks/thalmor_influence_clocks.json`
- **Faction Trust**: `/data/clocks/faction_trust_clocks.json`
- **Campaign State**: `/state/campaign_state.json`

### Key NPCs Stat Sheets
- **Galmar Stone-Fist**: `/data/npc_stat_sheets/galmar_stonefist.json`
- **Legate Rikke**: `/data/npc_stat_sheets/legate_rikke.json`
- **Elenwen**: `/data/npc_stat_sheets/elenwen.json`
- **Thalmor Justiciar**: `/data/npc_stat_sheets/thalmor_justiciar.json`

### Python Tools
- **story_manager.py**: Track quest progression, branching decisions
- **faction_logic.py**: Update faction clocks and relationships
- **gm_tools.py**: Campaign overview and suggestions

---

## Conclusion

The Elder Scrolls TTRPG Campaign Module provides a rich, branching narrative that respects player agency while delivering an epic story. The three-act structure, integrated civil war and Thalmor conspiracy, and dynamic clock system create a living world that responds to player choices. The Dragonbreak system allows for parallel timelines and divergent story paths.

Remember: The best campaigns emerge from the intersection of your preparation and your players' creativity. Use this module as a framework, not a script. Adapt, improvise, and most importantly, have fun!

**May your road lead you to warm sands, and may Skyrim's fate be worthy of song.**

---

*For additional guidance, see:*
- `/docs/how_to_gm.md` - Comprehensive GM protocols
- `/CAMPAIGN_INTEGRATION.md` - Technical integration details
- `/README.md` - Repository overview
- `/scripts/dragonbreak_manager.py` - Dragonbreak timeline system
