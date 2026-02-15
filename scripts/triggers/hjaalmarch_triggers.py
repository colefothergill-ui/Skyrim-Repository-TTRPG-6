#!/usr/bin/env python3
"""
Hjaalmarch (Morthal) Location Triggers

This module handles location-based triggers for Morthal and Hjaalmarch Hold.
It provides contextual events, NPC interactions, and dynamic quest hooks specific to Morthal's eerie swamp environment.
Key quest integrations include the vampire investigation "Laid to Rest" and Falion's secret ritual for curing vampirism.
Faction alignment is subtle here, but shifts (Imperial vs. Stormcloak control of the hold) can alter the Jarl and local atmosphere.
"""
from .trigger_utils import is_companion_present, is_quest_active, is_night_time

def hjaalmarch_location_triggers(loc, campaign_state):
    """
    Generate location-specific triggers for Morthal and Hjaalmarch locations.
    
    Args:
        loc: Current location string (e.g., "morthal", "morthal_highmoon_hall", "movarths_lair")
        campaign_state: Dictionary containing campaign state (companions, quest states, time of day, etc.)
        
    Returns:
        List of narrative event strings triggered by the location.
    """
    events = []
    loc_lower = str(loc).lower()
    active_companions = campaign_state.get("companions", {}).get("active_companions", [])
    
    # District-specific triggers for Morthal
    if ("highmoon" in loc_lower or ("jarl" in loc_lower and "longhouse" in loc_lower)) and "morthal" in loc_lower:
        events.append("You step into Highmoon Hall, the Jarl's longhouse. The interior is dim and smells of herbs and smoke. Jarl Idgrod Ravencrone sits on her wooden throne, eyes half-closed as if listening to unseen voices. An uneasy quiet fills the hall; even the guards shift nervously, as if troubled by the same unseen presence that occupies Idgrod's mind.")
    elif ("moorside" in loc_lower or "inn" in loc_lower) and "morthal" in loc_lower:
        events.append("You enter the Moorside Inn, a low-ceilinged tavern lit by a few sputtering torches. The conversation inside hushes for a moment as the locals size you up. Jonna, the innkeeper, gives a polite nod and continues cleaning a mug. In the corner, an Orc bard plucks a lute off-key, singing a morose tune that matches the town's mood. You catch murmurs about a recent tragedy and worries of something unnatural in the marsh.")
    elif ("swamp" in loc_lower or "perimeter" in loc_lower or "outskirts" in loc_lower) and "morthal" in loc_lower:
        events.append("At the edge of Morthal, the village gives way to the open marsh. Wooden boardwalks slick with moss pass by a few lonely houses. One is Falion's, the resident mage, set apart from the others and faintly aglow with candlelight. The fog here is thick; reeds rustle with unseen movement. It's hard to tell if the uneasy feeling creeping up your spine is from the chill in the air or something lurking in the bog.")
    
    # Quest hook: Laid to Rest (vampire investigation in Morthal)
    if "morthal" in loc_lower:
        is_burned = "burned" in loc_lower
        is_graveyard = "graveyard" in loc_lower
        if (is_burned or is_graveyard) and not is_quest_active(campaign_state, "laid_to_rest"):
            if is_night_time(campaign_state):
                if is_burned:
                    events.append("Among the charred remains of the burned house, a pale spectral figure of a little girl appears for just a moment. Her whisper carries on the fog: 'Play with me...' before she fades into the darkness. The air grows unnaturally cold.")
                    events.append("Suddenly, a woman's anguished cry shatters the silence. From the shadows near the ruined house rushes a frenzied figure—it's Laelette, a missing Morthal resident, now a feral vampire thrall! Her eyes glow with bloodlust as she attacks, defending some terrible secret.")
                elif is_graveyard:
                    events.append("In Morthal's small graveyard, mist coils around crooked tombstones and a few leaning wooden markers. A pale spectral figure of a little girl appears for just a moment atop a fresh mound. Her whisper carries on the fog: 'Play with me...' before she fades into the darkness. The air grows unnaturally cold.")
                    events.append("Suddenly, a woman's anguished cry shatters the silence. From behind a crooked tombstone rushes a frenzied figure—it's Laelette, a missing Morthal resident, now a feral vampire thrall! Her eyes glow with bloodlust as she attacks, defending some terrible secret.")
            else:
                if is_burned:
                    events.append("During the day, villagers give the blackened ruins of Hroggar's old house a wide berth. Two women gossip quietly as they hurry past: 'First the fire, now Hroggar shacks up with Alva? I tell you, something's not right.' 'And poor Helgi... some nights I swear I hear a child laughing near those ruins.' They cross themselves and quicken their pace.")
                elif is_graveyard:
                    events.append("During the day, Morthal's graveyard sits quiet at the edge of the marsh. A thin, stooped caretaker tends to a few fresh graves while villagers hurry past on the road, careful not to linger. You overhear a hushed remark: 'Poor Helgi... they say sometimes you can still hear a child laughing among those stones at night.' The speaker quickly changes the subject and walks on.")
    elif "movarth" in loc_lower:
        if is_quest_active(campaign_state, "laid_to_rest"):
            events.append("Torches in hand, you descend into Movarth's Lair. The cave is deathly quiet—too quiet. The stench of dried blood hits you as your light reveals desiccated skeevers and an overturned wooden cart. From deeper within, a silky male voice echoes off the tunnel walls: 'Ahh... fresh blood.' The master vampire is aware of your intrusion, and his brood no doubt lies in ambush.")
        else:
            events.append("You find a heavy wooden door concealed in a hillside, leading into darkness. Inside, the air is stale and the ground underfoot is littered with bones. Webs hang from the ceiling like drapes. There's an unsettling feeling here, as if you're being watched by unseen eyes. Anyone foolish enough to dwell here must be truly monstrous.")
    
    # Quest hook: Falion's secret vampirism cure ritual ("Rising at Dawn")
    if "morthal" in loc_lower and is_night_time(campaign_state) and not is_quest_active(campaign_state, "rising_at_dawn"):
        events.append("Late at night, you notice Falion leaving Morthal, heading out into the marsh with a purposeful stride. He carries a large black soul gem that glimmers faintly in the moonlight. If you choose to follow from a safe distance, you eventually see him stop at a circle of ancient standing stones. As dawn approaches, Falion begins a low chant, and the soul gem radiates power—it's clear he is performing some kind of powerful ritual, perhaps one that could cure even the darkest of afflictions.")
    
    # General entrance to Morthal (if no other specific event has triggered)
    if loc_lower.startswith("morthal") and not events:
        events.append("A blanket of mist covers the quiet town of Morthal as you arrive. The wooden structures seem to emerge from the fog only when you're nearly upon them. A few residents bundled in cloaks pause on their porches to watch you warily. The whole settlement feels distant from the rest of Skyrim, isolated by its marshy surroundings and the weight of unspoken troubles.")
    
    # Companion commentary for any Morthal-native follower (e.g., Benor)
    if is_companion_present(active_companions, "benor") and "morthal" in loc_lower:
        events.append("Benor scans the dimly lit village and grips his weapon hilt. \"Not much has changed,\" he mutters. \"Morthal may be quiet, but don't let your guard down. These marshes breed odd troubles.\"")
    
    # Civil War impact triggers (Jarl change if hold switches sides)
    if "morthal" in loc_lower:
        # Stormcloak takeover of Hjaalmarch - check this first
        if campaign_state.get("jarl_hjaalmarch") == "sorli" and not campaign_state.get("morthal_stormcloak_banner"):
            events.append("The atmosphere in Morthal has shifted subtly after the Stormcloaks' takeover. The blue bear banners of Windhelm now hang limp in the mist. Jarl Sorli the Builder, a commoner-turned-Jarl, governs with a practical hand from Highmoon Hall. Many townsfolk carry on as before, indifferent to the new regime, but there's a sense of wary optimism among some that the hold is now free of Imperial influence.")
            campaign_state["morthal_stormcloak_banner"] = True
        # Imperial reconquest of Hjaalmarch (Idgrod restored)
        elif campaign_state.get("civil_war_phase") == "imperial_victory" and campaign_state.get("jarl_hjaalmarch") != "idgrod" and not campaign_state.get("morthal_imperial_restored"):
            events.append("Morthal has quietly returned to Imperial control. Jarl Idgrod Ravencrone sits once again in Highmoon Hall, her gaze as distant as ever, but there's a slight relief among the Imperial loyalists in town. A few more Legion guards now stand at the sparse wooden barricades, their red dragon sigils barely visible in the fog. Life in Morthal continues much as it always has—slow and cautious—but under the surface, people gossip about the futility of these power swaps.")
            campaign_state["morthal_imperial_restored"] = True
    
    return events
