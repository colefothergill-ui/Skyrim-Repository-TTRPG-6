# Daedric Prince Quests and Mechanics

## Overview
Daedric Princes are god-like beings who offer mortals power in exchange for service. Their quests should feel significant, morally complex, and have lasting consequences.

## The Sixteen Daedric Princes

### Azura - Lady of Dawn and Dusk
**Sphere**: Dusk and dawn, twilight, mystery
**Artifact**: Azura's Star (reusable soul gem)
**Quest Theme**: Maintaining balance, honoring the dead
**Moral Alignment**: Neutral to Good

### Boethiah - Prince of Plots
**Sphere**: Deceit, conspiracy, treachery, unlawful overthrow of authority
**Artifact**: Ebony Mail (silence and poison aura armor)
**Quest Theme**: Betrayal, proving strength through cunning
**Moral Alignment**: Evil

### Clavicus Vile - Prince of Bargains
**Sphere**: Wishes, power, deals, pacts
**Artifact**: Masque of Clavicus Vile (speech and pricing)
**Quest Theme**: Careful what you wish for, monkey's paw deals
**Moral Alignment**: Neutral Evil

### Hermaeus Mora - Demon of Knowledge
**Sphere**: Knowledge, memory, the unknown
**Artifact**: Oghma Infinium (skill boost tome)
**Quest Theme**: Forbidden knowledge, cost of learning secrets
**Moral Alignment**: Neutral

### Hircine - Huntsman
**Sphere**: The hunt, lycanthropy, wild nature
**Artifact**: Savior's Hide (magic and poison resistance) OR Ring of Hircine (werewolf control)
**Quest Theme**: The thrill of the hunt, predator vs prey
**Moral Alignment**: True Neutral

### Malacath - God of Curses
**Sphere**: The spurned, the ostracized, the keeper of oaths
**Artifact**: Volendrung (stamina-draining warhammer)
**Quest Theme**: Honor among outcasts, revenge for broken oaths
**Moral Alignment**: Lawful Neutral

### Mehrunes Dagon - Prince of Destruction
**Sphere**: Destruction, change, revolution, ambition, energy
**Artifact**: Mehrunes' Razor (instant-kill dagger)
**Quest Theme**: Chaos, destruction, ambition without restraint
**Moral Alignment**: Chaotic Evil

### Mephala - Webspinner
**Sphere**: Lies, secrets, murder, sex
**Artifact**: Ebony Blade (life-draining sword empowered by betrayal)
**Quest Theme**: Secrets that corrupt, murder of loved ones
**Moral Alignment**: Evil

### Meridia - Lady of Infinite Energies
**Sphere**: Life, light, anti-undead
**Artifact**: Dawnbreaker (undead-slaying sword)
**Quest Theme**: Purging undead, cleansing corruption
**Moral Alignment**: Good (with zealotry)

### Molag Bal - King of Rape
**Sphere**: Domination, enslavement, vampirism
**Artifact**: Mace of Molag Bal (soul trap and stamina drain)
**Quest Theme**: Domination, corruption of the innocent
**Moral Alignment**: Pure Evil

### Namira - Lady of Decay
**Sphere**: Decay, repulsiveness, darkness, cannibalism
**Artifact**: Ring of Namira (cannibalism benefits)
**Quest Theme**: Embracing the disgusting, rejecting beauty
**Moral Alignment**: Evil

### Nocturnal - Mistress of Shadows
**Sphere**: Night, darkness, luck, thieves
**Artifact**: Skeleton Key (ultimate lockpick - usually Thieves Guild)
**Quest Theme**: Luck, shadow, debt and service
**Moral Alignment**: Neutral

### Peryite - Taskmaster
**Sphere**: Pestilence, natural order, tasks
**Artifact**: Spellbreaker (magic-blocking shield)
**Quest Theme**: Maintaining order through plague, doing thankless work
**Moral Alignment**: Lawful Neutral

### Sanguine - Lord of Revelry
**Sphere**: Debauchery, dark indulgences, hedonism
**Artifact**: Sanguine Rose (summons Dremora)
**Quest Theme**: Consequences of excess, wild adventures
**Moral Alignment**: Chaotic Neutral

### Sheogorath - Mad God
**Sphere**: Madness, creativity, chaos
**Artifact**: Wabbajack (random effects staff)
**Quest Theme**: Madness as liberation, chaos as creativity
**Moral Alignment**: Chaotic Neutral

### Vaermina - Dreamweaver
**Sphere**: Dreams, nightmares, mental torment
**Artifact**: Skull of Corruption (nightmare-based staff)
**Quest Theme**: Using dreams against others, nightmares made real
**Moral Alignment**: Evil

## Fate Core Mechanics for Daedric Quests

### Quest Structure

1. **Contact**: Prince contacts player (dream, cultist, artifact)
2. **Task**: Morally complex task with consequences
3. **Choice Point**: Player decides to obey, defy, or subvert
4. **Reward/Consequence**: Artifact + permanent aspect

### Mechanical Rewards

**Daedric Artifacts** (Stunts):
- Must be significant magical items
- Grant +2 to specific actions OR unique ability
- Come with a compel-able aspect
- Can never be sold or destroyed (cursed)

**Example Artifact Stunt**:
> **Mehrunes' Razor**: Once per session, make a Fight attack. On a success with style, instantly take out target (regardless of stress/consequences). Gain aspect "Tempted by Murder" that can be compelled.

### Aspects from Daedric Service

When completing a Daedric quest, players must take an aspect related to the Prince:
- "Marked by Azura"
- "Boethiah's Champion"
- "Indebted to Clavicus Vile"
- "Hermaeus Mora's Seeker"
- "Hircine's Prey and Predator"

These aspects can be invoked for benefits but should regularly be compelled.

### Moral Complexity

**Never make Daedric quests simple**:
- Evil Princes ask for evil acts (players can refuse)
- Good Princes ask for acts with hidden costs
- Neutral Princes have alien morality

**Example Complications**:
- Meridia wants you to kill a necromancer... who's trying to resurrect their child
- Molag Bal wants you to corrupt a priest... who's actually a hypocrite exploiting people
- Azura wants you to serve her... but means abandoning another obligation

### GM Guidelines

1. **Telegraph Consequences**: Make clear this is a Daedric quest with lasting impact
2. **Honor Player Choice**: If they refuse, that's valid (and interesting!)
3. **Persistent NPCs**: Daedric Princes don't forget service or insults
4. **Faction Impact**: Serving Daedra affects reputation with temples, guilds
5. **Compel Regularly**: Daedric aspects should create ongoing complications

### Tracking Daedric Relationships

In character files, track:
```json
"daedric_relationships": {
  "Azura": "Honored champion",
  "Mehrunes_Dagon": "Refused service",
  "Hermaeus_Mora": "Knowledge debt"
}
```

### Multiple Daedric Artifacts

- Limit players to 2-3 artifacts maximum
- Each additional artifact increases cosmic attention
- Create world aspect: "Too Many Masters" that can be compelled
- Princes may demand exclusive service

## Sample Daedric Quest Template

**Quest Name**: [Prince's Name]'s [Theme]
**Contact Method**: [How Prince reaches player]
**Initial Task**: [Seemingly simple request]
**Complication**: [Moral complexity revealed]
**Choice Point**: [Obey/Defy/Subvert options]
**Rewards**: [Artifact + Aspect]
**Consequences**: [Faction changes, NPC reactions, future complications]

## Integration with Campaign

- Daedric quests should be rare (2-3 per campaign)
- Space them out across many sessions
- Use as major story beats
- Connect to character aspects when possible
- Allow player-initiated contact (via shrines, cultists)
