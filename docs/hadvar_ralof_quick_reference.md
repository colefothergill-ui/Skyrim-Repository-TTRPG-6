# Hadvar & Ralof - Quick Reference & Examples

## Quick Stats Comparison

| Attribute | Hadvar (Imperial) | Ralof (Stormcloak) |
|-----------|-------------------|-------------------|
| **Faction** | Imperial Legion | Stormcloaks |
| **Combat Style** | Defensive / Tank | Aggressive / Striker |
| **Starting Loyalty** | 60 | 60 |
| **Key Skill** | Fight (Great +4) | Fight (Great +4) |
| **Special Focus** | Physique, Will | Athletics, Provoke |
| **Armor** | 1 | 1 |
| **Family** | Alvor (Riverwood) | Gerdur (Riverwood) |

## Quick Decision Matrix

### At Session Zero:

```
IF player chooses Imperial → Hadvar joins (active companion)
IF player chooses Stormcloak → Ralof joins (active companion)
IF player chooses Neutral → Both available (recruit later via RP)
```

## Example Session Zero Flow

```
GM: "As the civil war tension reaches a breaking point in Skyrim, you witness 
     the beginning of open conflict between Imperial and Stormcloak forces. 
     You see two soldiers - one in Imperial armor (Hadvar), one in Stormcloak 
     gear (Ralof) - both offering you a choice. Who do you follow?"

Player: "We follow the Imperial soldier - Hadvar."

GM: [Records in campaign state]
    - civil_war_choice: "Imperial"
    - active_companions: [Hadvar]
    - Hadvar loyalty: 60

Result: Hadvar is now in party, provides Imperial connections, 
        can introduce party to Uncle Alvor in Riverwood.
```

## Example Riverwood Scene

### With Hadvar (Imperial)

```
GM: "As you approach Riverwood, Hadvar perks up. 'My uncle Alvor runs the 
     forge here. Let's see if he can help us with supplies and shelter.'"

[At Alvor's Forge]

Hadvar: "Uncle! It's good to see you alive."

Alvor: "Hadvar! By the Eight... what's happening? I've heard rumors of war."

Hadvar: "The civil war is escalating. These are the allies I've found - 
         worthy companions in a fractured Skyrim. Can you help us?"

Alvor: [Looks at party] "Any friend of Hadvar's... Come inside. You need 
        food, rest, and likely some repairs to your gear."

Result: Party gains free rest, meal, and basic smithing services from Alvor.
        Hadvar's loyalty +5 for visiting family.
```

### With Ralof (Stormcloak)

```
GM: "As you enter Riverwood, Ralof heads toward the lumber mill. 
     'My sister Gerdur runs the mill. She'll shelter us and help us prepare 
     for what's coming.'"

[At the Lumber Mill]

Ralof: "Gerdur! By Talos, it's good to see you."

Gerdur: "Ralof! I've heard the war is beginning... I feared the worst."

Ralof: "The Empire and Stormcloaks are fighting for control. These friends 
        helped me escape danger. Can you give us shelter?"

Gerdur: [Nods firmly] "Of course. Hod and I have room. You all look 
         exhausted. Come, I'll prepare supper."

Result: Party gains free lodging, meal, and supplies from Gerdur's mill.
        Ralof's loyalty +5 for visiting family.
```

## Example Whiterun Arrival

### Imperial Path (Hadvar)

```
GM: "You approach Whiterun's gates. The guards eye you warily until 
     they notice Hadvar's Imperial armor."

Hadvar: "I need to speak with Jarl Balgruuf. It's urgent - civil war is 
         reaching Skyrim's heartland, and the Jarl must know."

Guard: "Imperial Legion business? Right this way. The Jarl will want to 
        hear this."

Result: Party gains immediate audience with Jarl Balgruuf due to 
        Hadvar's credentials. No persuasion rolls needed.
```

### Stormcloak Path (Ralof)

```
GM: "You approach Whiterun's gates. The guards tense up when they spot 
     Ralof's Stormcloak armor."

Ralof: [Quietly to party] "Keep your weapons sheathed. Whiterun is 
        'neutral' but Balgruuf leans Imperial. Let me do the talking."

Guard: "State your business, Stormcloak."

Ralof: "We bring word of escalating civil war. The Jarl needs to 
        know - this affects all of Skyrim, Empire and free folk alike."

GM: [Requires Rapport or Provoke roll from Ralof or party to convince guards]

Result: Party must work harder to gain audience, but Ralof's Nord heritage 
        and passion for Skyrim can help sway neutral citizens.
```

## Example Combat Scenarios

### Defending Imperial Patrol (with Hadvar)

```
GM: "You encounter an Imperial patrol under attack by bandits on the road."

Hadvar: "We need to help them! Shield wall formation - protect the wounded!"

[Combat begins]

Mechanical Effect:
- Party gains +1 to all defend actions (Shield Brother stunt)
- Hadvar uses Imperial Training for +2 to Fight when defending allies
- Surviving Imperials provide +10 to Imperial faction reputation

Post-Combat:
Hadvar loyalty +5 (defended Imperial soldiers)
Imperial Legion relationship +10
```

### Protecting Talos Shrine (with Ralof)

```
GM: "You discover a hidden Talos shrine in the wilderness. Suddenly, 
     Thalmor agents emerge from the trees, intending to destroy it."

Ralof: [Hand on weapon] "By Talos, I won't let them desecrate this shrine!"

[Combat begins]

Mechanical Effect:
- Ralof gains +2 to Fight (Nord's Fury vs enemies threatening Talos worship)
- Party gains +1 to attack if Ralof uses "For Skyrim!" rally
- Defending the shrine is personal for Ralof

Post-Combat:
Ralof loyalty +10 (defended Talos shrine from Thalmor)
Stormcloak relationship +5
Thalmor awareness of party increases
```

## Example Loyalty Crisis

### Low Loyalty Scenario (Hadvar, 35 loyalty)

```
GM: "The party has been working with Stormcloak sympathizers for weeks. 
     Hadvar has grown increasingly distant."

[Party plans to attack an Imperial supply wagon]

Hadvar: [Stands firm] "I've followed you this far, but I won't attack my 
         own brothers-in-arms. These are good soldiers, just following orders."

Party Options:
1. Abandon plan → Hadvar loyalty +10, stays with party
2. Convince Hadvar it's necessary → Requires Very Hard persuasion, 
   loyalty -5 if successful
3. Proceed without Hadvar → He refuses to participate, loyalty -10
4. Attack anyway with Hadvar present → He leaves party permanently

Result: Loyalty crisis forces party to confront their choices and 
        Hadvar's personal boundaries.
```

### High Loyalty Moment (Ralof, 85 loyalty)

```
GM: "The Battle of Whiterun rages. A group of civilians is trapped in a 
     burning building between the lines."

Ralof: "I'll cover you! Save those people - Nord, Imperial, it doesn't 
        matter. No one deserves to burn alive!"

[Ralof holds off enemies while party rescues civilians]

Mechanical Effect:
- Ralof will risk his life for party's mission
- Gains inspiration (Fate point) for heroic action
- May gain consequence protecting party

Post-Scene:
Ralof loyalty remains high (already 85)
Civilians remember the Stormcloak who saved them
Party gains reputation in Whiterun regardless of faction
```

## Example Battle of Whiterun Integration

### Imperial Version (with Hadvar)

```
GM: "The Stormcloak assault begins. Hadvar stands beside you on the walls."

Hadvar: "Remember your training! Shield wall, protect each other, and 
         trust the man beside you. For the Empire!"

Combat Mechanics:
- All party members in Hadvar's zone gain +1 to defend
- Hadvar coordinates with Whiterun guards for tactical advantage
- His presence prevents some friendly fire from confused guards

Wave 1: Stormcloak infantry assault
- Hadvar uses Imperial Training (+2 to Fight) to hold the line
- Party can use his shield as cover for ranged attacks

Wave 2: Stormcloak archers and mages
- Hadvar's Steady Under Fire (+2 to Will) helps resist fear effects
- He calls out enemy positions using Notice skill

Wave 3: Final assault with Stormcloak commander
- Shield Brother stunt applies to entire party
- Hadvar focuses on protecting weakest party member

Post-Battle:
- Hadvar loyalty +15 (fought for the Empire, protected party)
- Imperial Legion reputation increases
- Jarl Balgruuf thanks party and Hadvar personally
- Hadvar may be promoted or recognized by Legate Rikke
```

### Stormcloak Version (with Ralof)

```
GM: "The assault on Whiterun begins. Ralof charges beside you, battle axe 
     raised high."

Ralof: "For Skyrim! For Talos! Show them what true Nords are made of!"

Combat Mechanics:
- All party members in Ralof's zone gain +1 to attack
- "For Skyrim!" can be used twice (instead of once)
- His presence rallies nearby Stormcloak troops

Wave 1: Breaching the gate
- Ralof uses Athletics to help scale/breach defenses
- Nord's Fury gives +2 vs Imperial defenders
- His battle cry inspires Stormcloak troops (morale bonus)

Wave 2: Fighting through streets
- Ralof knows city layout from visits to family friends
- Suggests tactical routes to avoid civilian casualties
- Rallies scattered Stormcloak units

Wave 3: Storming Dragonsreach
- Unbreakable Spirit activates if needed (auto-succeed Will check)
- Leads final charge alongside party
- Faces off against Imperial defenders with fury

Post-Battle:
- Ralof loyalty +15 (fought for Skyrim's freedom, stood with party)
- Stormcloak reputation increases significantly
- Ulfric Stormcloak or Galmar may personally thank party and Ralof
- New Jarl Vignar Gray-Mane welcomes party as heroes
```

## GM Tips for Different Party Compositions

### Solo Player with Companion
- Companion acts as tactical advisor and moral compass
- Provides backup in combat (treat as full NPC)
- Offers information about Skyrim and the civil war

### Party of 2-3
- Companion fills gaps in party composition
- Can take lead on social interactions with their faction
- Provides flanking and tactical advantages in combat

### Party of 4+
- Companion provides bonus rather than necessity
- Focus on roleplaying and loyalty system
- Use as quest hook and relationship anchor

### Neutral Party (No Starting Companion)
- Present both companions at critical moments
- Let party actions determine which (if any) they recruit
- Use as example of faction conflict made personal

## Session Zero Script Example

```
GM: "Before we begin the adventure proper, you need to decide where your 
     party stands in Skyrim's civil war. The conflict is escalating, and 
     choosing sides will shape your entire campaign."

[Present faction options]

GM: "Your choice here determines your starting companion. If you side with 
     the Empire, Hadvar - an Imperial soldier you meet early in the war - 
     will join you. If you side with the Stormcloaks, it's Ralof who becomes 
     your companion. If you choose to remain neutral initially, you'll meet 
     both and decide later."

[Players discuss and choose Imperial]

GM: "Excellent. Hadvar, the pragmatic Imperial soldier, accompanies you. 
     He's grateful you've proven yourselves as allies and sees you as 
     battle-brothers and sisters. His loyalty starts at 60 out of 100. 
     Treat him well, fight for the Empire, and visit his family in Riverwood, 
     and he'll become a stalwart defender of your party."

[Record in campaign state: civil_war_choice = "Imperial"]
```

## Quick Troubleshooting

**Q: Player chose Imperial but wants Ralof instead?**
A: Allow it! Just swap the companion in campaign state. Loyalty starts at 50 instead of 60 (less initial trust). Requires roleplay justification.

**Q: Companion loyalty at 0, what now?**
A: Companion leaves at next safe location. May become enemy if party joins opposing faction. Creates dramatic moment - use it!

**Q: Party wants both companions?**
A: Possible for neutral path, but creates tension. Hadvar and Ralof won't fight each other but will disagree constantly. Use for roleplaying gold!

**Q: Companion died in combat?**
A: Major narrative impact. Family in Riverwood grieves. Faction sends condolences or honors. Party feels consequences. Don't resurrect easily.

**Q: Player never visits companion's family?**
A: Loyalty slowly decreases (-3 per few sessions). Companion mentions family repeatedly. Eventually becomes a conflict point.

## Code Quick Reference

```python
# Get starting companion
from story_manager import StoryManager
story = StoryManager()
companion = story.get_starting_companion()

# Get dialogue hooks
hooks = story.get_companion_dialogue_hooks("Whiterun", "civil_war")

# Update loyalty (via NPC Manager)
from npc_manager import NPCManager
npc_mgr = NPCManager()
npc_mgr.update_loyalty("hadvar", +5, "Defended innocent civilians")

# Check companion status
status = npc_mgr.check_companion_status("hadvar")
```

## File Locations

- **Stat Sheets**: `data/npc_stat_sheets/hadvar.json`, `ralof.json`
- **Campaign State**: `state/campaign_state.json` (companions section)
- **Tests**: `tests/test_hadvar_ralof_integration.py`
- **Full Guide**: `docs/hadvar_ralof_companion_guide.md`
