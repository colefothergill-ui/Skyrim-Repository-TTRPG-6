#!/usr/bin/env python3
"""
Markarth and The Reach Location Triggers

This module handles location-based triggers for Markarth (city) and various locations in The Reach hold.
It provides contextual events, quest hooks, and companion commentary specific to Markarth and the surrounding Reach.
"""

from .trigger_utils import is_companion_present

def markarth_location_triggers(loc, campaign_state):
    """
    Generate location-specific triggers for Markarth city and The Reach locations.
    
    Args:
        loc (str): Current location identifier (e.g., "markarth", "markarth_understone_keep", "karthspire")
        campaign_state (dict): Current campaign state, including companions and quest flags.
    
    Returns:
        list of str: Narration event strings triggered by the location.
    """
    events = []
    loc_lower = str(loc).lower()
    active_companions = campaign_state.get("companions", {}).get("active_companions", [])

    # Markarth City – District triggers
    if ("understone" in loc_lower or "keep" in loc_lower) and "markarth" in loc_lower:
        events.append("You step into Understone Keep, where ancient Dwemer stonework towers above you. The air is cool and echoes with distant dripping water. Jarl Igmund's throne looms ahead under carved arches, and you feel both the weight of history and the tension of modern politics in these halls.")
    elif ("temple" in loc_lower or "dibella" in loc_lower) and "markarth" in loc_lower:
        events.append("Climbing the steps to the Temple of Dibella, you enter a marble sanctuary lit by soft candles. The scent of incense and fresh mountain flowers is soothing. In the hushed silence, a priestess greets you with a serene smile, though you sense a subtle apprehension as if the recent troubles have even intruded here.")
    elif ("warrens" in loc_lower) and "markarth" in loc_lower:
        events.append("You duck into the Warrens, the dimly lit tunnels under Markarth. The chatter of the city fades, replaced by dripping water and hushed coughing. Eyes peer at you from dark alcoves. The oppressed souls living here shuffle away, and an uneasy feeling settles in your gut, as if unseen figures are watching your every move.")
    elif ("treasury" in loc_lower or "treasury house" in loc_lower) and "markarth" in loc_lower:
        events.append("Entering the Treasury House, you notice immediate luxury – polished silver candlesticks and fine rugs that contrast sharply with the cold stone city. A steward eyes you from behind a desk. The air is thick with quiet authority; every footstep falls on wealth. You get the sense that here in the heart of the Silver-Blood power, secrets and gold are exchanged in equal measure.")
    elif ("silver-blood" in loc_lower or "inn" in loc_lower) and "markarth" in loc_lower:
        events.append("The warmth of the Silver-Blood Inn envelops you as you step inside from Markarth's stone streets. A fire crackles in the hearth, and the smell of juniper berry mead mixes with roasting meat. Patrons pause to glance your way – miners, merchants, and off-duty guards. Overhead, you notice the carved emblem of a ram's head, symbol of the Reach, and quietly recall that this cozy tavern is owned by the most powerful family in the city.")

    # General Markarth entrance (if none of the specific districts matched, but still Markarth)
    elif loc_lower.startswith("markarth") and not events:
        events.append("You pass through Markarth's massive stone gates, entering a city carved into the very cliffs. Waterfalls crash down alongside Dwemer aqueducts, and the chatter of miners and merchants fills the air. Above, the imposing facade of Understone Keep watches over the tiers of stone buildings. Markarth feels at once majestic and uneasy – guards in crimson armor stand vigilant, and you can't shake the sense that unseen eyes are following your steps.")

    # Reach Wilderness – Major location triggers
    if "karthspire" in loc_lower:
        events.append("You trek into the Karthspire within the Reach's wilderness – a canyon area marked by ancient standing stones and roaring waterfalls. Forsworn camps dot the approach, their painted hides and bone totems warning off trespassers. In the distance, within the Karthspire cavern, you glimpse carved stone steps and dragon-headed arches, hinting at the Sky Haven Temple hidden beyond. The air crackles with an uneasy energy, as if this place holds great secrets of the past.")
    if "hag" in loc_lower and "rock" in loc_lower:
        events.append("Hag Rock Redoubt looms ahead, a Forsworn stronghold built into a jagged hillside. Totems of twig effigies and animal skulls line the path. You can hear the distant cries of Briarheart warriors and the cawing of hagravens. The very approach feels cursed – bones underfoot and bizarre runes painted on the rocks. Storming this place would be no small feat; its defenders know the terrain and have dark magic on their side.")
    if "druadach" in loc_lower:
        events.append("You stand before Druadach Redoubt, a series of caves and fortifications hidden in the winding Druadach valley. The surrounding forest is unusually quiet. Within the redoubt's confines, Forsworn braves lurk with bows at the ready. Petroglyphs on the cave walls depict ancient Reachmen victories. A narrow escape route into the mountains suggests the Forsworn here never intend to be cornered – they know this land intimately, every secret cleft and tunnel.")
    if "lost" in loc_lower and "valley" in loc_lower:
        events.append("Lost Valley Redoubt opens up before you – a striking hidden valley dominated by a cascading waterfall and ancient Nordic stones atop a plateau. Forsworn tents and lookout perches ring the area. As you move in, you hear an eerie chanting echo off the cliffs; at the pinnacle of the redoubt, a Hagraven performs a blood ritual under the open sky. The whole valley feels like a place out of time, where nature and dark rites entwine dangerously.")
    if "nchuand-zel" in loc_lower or ("dwemer" in loc_lower and "ruin" in loc_lower and "markarth" in loc_lower):
        events.append("Stepping into Nchuand-Zel – the Dwemer ruin beneath Markarth – you are greeted by silence and towering metal gleam. The city above fades away as you wander among colossal stone pillars and dormant brass machines. Faint glows of Dwemer lamps still illuminate parts of the gloom. Every footstep echoes, and it's easy to feel like an intruder in the halls of a vanished people. Be on guard: Falmer and Dwemer automata are said to roam these depths, and the ghosts of Markarth's past linger here.")

    # Quest Hook: Abandoned House (Molag Bal – "The House of Horrors")
    if ("abandoned house" in loc_lower or ("abandoned" in loc_lower and "markarth" in loc_lower)) and "molag" not in campaign_state.get("daedric_princes", {}):
        # If the player enters the Abandoned House in Markarth for the first time
        events.append("The front door closes behind you with an ominous thud as you step into Markarth's abandoned house. Dust motes hang in the air. Suddenly, a deep, unsettling voice slithers through your mind, and the ground quakes. Pots and chairs rattle violently, flying off the shelves by an unseen force. A cold dread grips you – something hungry and malevolent resides here. (A menacing presence urges you forward, hinting at a dark quest within.)")
        # Note: This event suggests the beginning of the Molag Bal quest "The House of Horrors"

    # Quest Hook: Nepos's House (Forsworn Conspiracy)
    if "nepos" in loc_lower:
        events.append("Nepos's house is quiet and dimly lit, the fire in the hearth casting long shadows. Nepos – a frail old man with surprisingly sharp eyes – sits in a carved chair, watching you intently. The air feels thick with secrets. You notice subtle signs of wealth and Reach influence here: fine silverware, a hint of rich Reach spice in the air. Something about this residence feels off, as if danger lurks just beneath the polite veneer. (You have a sense that Nepos knows far more about the recent troubles in Markarth than he lets on.)")
        # Note: This narrative foreshadows the quest "The Forsworn Conspiracy" where Nepos the Nose is more than he appears.

    # Quest Hook: Cidhna Mine (No One Escapes Cidhna Mine)
    if "cidhna mine" in loc_lower or ("markarth" in loc_lower and "mine" in loc_lower and "cidhna" in loc_lower):
        events.append("You stand at the gates of Cidhna Mine, Markarth's notorious prison carved deep into the Reach's rock. A chill wind blows from the tunnel, carrying the echoes of clanging picks and distant anguished shouts. The guards here eye you with a mix of pity and scorn – no one enters this place by choice. Inside, the darkness is oppressive; the air is thick with dust and despair. You can sense that once behind these bars, freedom is a distant dream. (Whispers among the inmates speak of a 'King in Rags' rallying the prisoners – a hint of an infamous escape tale waiting to unfold.)")
        # Note: This sets the scene for "No One Escapes Cidhna Mine", should the player become imprisoned or venture inside.

    # Companion commentary (for any Reach-native or Markarth-related companions, placeholder examples)
    # Example: If a Reach-native companion (e.g., a Forsworn ally or Markarth native) is present, they might comment on returning home or the state of the Reach.
    if is_companion_present(active_companions, "illisif") and loc_lower.startswith("markarth"):
        # (Note: 'Illisif' is a placeholder name for a Reach-native follower for demonstration)
        events.append('Illisif pauses as you enter Markarth. "Home," she whispers, eyes scanning the stone city warily. "Every carving on these walls, I grew up with... and every shadow hides a memory." She grips her weapon. "Be on guard. The Reach doesn\'t forgive."')
    # Lydia or other vanilla companions might also react if appropriate, but none are Markarth natives. This is just an example structure.

    # Additional companion commentary could be added here following the pattern above, checking for specific companions and location.
    return events
