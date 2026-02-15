"""
Dawnstar (The Pale) Triggers Script

This script defines location-based scene descriptors and quest triggers for The Pale hold and its capital Dawnstar. 
It covers arrival ambiance, the nightmare plague quest hook, local bounty quests, environmental hazards, and integrates with the broader narrative trigger system.
"""

def pale_get_next_scene(campaign_state):
    """
    Main scene assembly function for The Pale.
    Checks for triggered events and returns a scene descriptor if one fires.
    
    Args:
        campaign_state: Dictionary containing campaign state
        
    Returns:
        Dictionary with scene information if a trigger fires, None otherwise
    """
    # Check for Erandur intersect trigger
    evt = trigger_erandur_intersect(campaign_state)
    if evt:
        return evt
    
    return None

def scene_dawnstar_arrival(party_state=None):
    """
    Scene trigger: Party arrives in Dawnstar for the first time.
    Describes the frigid coastal town, its Stormcloak presence, and an uneasy atmosphere (locals troubled by nightmares).
    """
    description = (
        "Cresting a frozen ridge, you catch sight of Dawnstar's small cluster of buildings hugging the coast. "
        "Snow crunches underfoot as you approach. Fishing boats sway in the icy harbor and wind whistles through the moored ship masts. "
        "A few weary-eyed townsfolk trudge past, bundled in furs – their faces drawn as if sleep has eluded them. "
        "Above the din of the sea, the blue bear banner of the Stormcloaks flaps defiantly from the Jarl's longhouse. "
        "You sense that beneath this sleepy port's routine lies a tension in the air, as cold and palpable as the sea breeze."
    )
    print(description)
    if party_state is not None:
        party_state['seen_dawnstar_intro'] = True  # mark that Dawnstar intro scene has been shown

def scene_windpeak_inn_commotion(party_state=None):
    """
    Scene trigger: Party enters the Windpeak Inn during the nightmare crisis.
    Depicts townsfolk in distress and introduces Erandur trying to calm everyone.
    """
    scene = (
        "Inside the Windpeak Inn, a normally cheerful firelit tavern, chaos reigns. "
        "Half the town seems to be crammed within. Pale-faced miners argue with sailors, all on edge from lack of sleep. "
        "One woman sobs into her hands, describing a terror from her last night's dream. "
        "By the hearth stands a robed Dunmer – Erandur, a Priest of Mara – his voice raised to get everyone's attention. "
        "\"Please, I know you're afraid,\" he implores the crowd, \"but Mara will help us cure these nightmares.\" "
        "The room hushes slightly at his words, though fear and exhaustion still hang thick in the air."
    )
    print(scene)
    if party_state is not None:
        party_state['heard_nightmare_rumors'] = True  # flag that the party witnessed the nightmare commotion scene

def trigger_erandur_waking_nightmare(campaign_state):
    """
    Event trigger: Erandur offers the Waking Nightmare quest if not already taken.
    Should be called when the party speaks to Erandur at the Windpeak Inn and the quest hasn't started yet.
    """
    if not campaign_state.get('waking_nightmare_quest_given'):
        dialogue = (
            "Erandur pulls you aside as the inn's din settles for a moment. His lavender eyes are earnest. "
            "\"You've seen what's happening to these people, yes?\" he asks quietly. \"Every night, the same horrible nightmares. I've seen this before – it's Vaermina's work. "
            "There's an old temple, Nightcaller Temple, on the hill overlooking this town. I journeyed here to put an end to this curse. But I need help.\" "
            "He takes a deep breath, then pleads, \"Please, come with me. Together we can stop these nightmares and save Dawnstar's people from this torment.\""
        )
        print(dialogue)
        campaign_state['waking_nightmare_quest_given'] = True

def trigger_skald_giant_bounty(campaign_state):
    """
    Event trigger: Jarl Skald offers a giant-slaying bounty quest if not already given.
    Intended to be called when the party speaks to Skald (usually after helping Dawnstar or at higher level).
    """
    if not campaign_state.get('skald_giant_quest_given'):
        decree = (
            "Jarl Skald the Elder scowls down from his wooden throne, his thick grey brows furrowing. "
            "\"The Empire's war pressure isn't our only problem,\" he growls by way of greeting. "
            "\"A damned giant has been spotted, harassing caravans on the road south of here. We Pale folk can handle our own, but…\" "
            "He eyes your group up and down. \"You lot look capable. Kill that giant, and I'll see you compensated. Do this for The Pale, and you'll have my respect — maybe more.\""
        )
        print(decree)
        campaign_state['skald_giant_quest_given'] = True

def trigger_wayfinder_void_salts(campaign_state):
    """
    Event trigger: Captain Wayfinder requests Fine-Cut Void Salts (Salty Sea-Dogs quest) if not already taken.
    Call when the party meets Wayfinder at Dawnstar's docks.
    """
    if not campaign_state.get('wayfinder_void_salts_quest_given'):
        request = (
            "On the Dawnstar docks, a young Nord in a captain's coat flags you down with an eager wave. "
            "\"Ahoy there!\" he calls. \"Name's Captain Wayfinder, of the ship *Sea Squall*. I could use a hand from a capable adventurer.\" "
            "He explains his predicament: having inherited his ship, he wants to treat the hull with a special coating. "
            "\"I need a pinch of Fine-Cut Void Salts,\" he explains, shivering as a sea breeze kicks up. "
            "\"Rare stuff, but it'll keep my ship safe on the seas. If you can find me some, I'll pay well. What do you say?\""
        )
        print(request)
        campaign_state['wayfinder_void_salts_quest_given'] = True

def trigger_pale_blizzard(campaign_state=None):
    """
    Event trigger: A sudden blizzard strikes while traveling in The Pale's wilderness.
    This can be invoked during overland travel to simulate a weather hazard.
    """
    scene = (
        "Without warning, the tranquil snowfall turns into a howling blizzard. Within minutes, the world around you becomes a white blur. "
        "Frozen wind slashes at your faces, and the temperature plummets sharply. The road ahead vanishes in driving snow and gale-force gusts. "
        "Traveling further in these conditions is perilous – exposed skin numbs and each step grows heavier. "
        "If you don't seek shelter or proper warmth soon, the relentless cold of The Pale could seep into your bones, threatening to turn the journey lethal."
    )
    print(scene)
    if campaign_state is not None:
        # Mark that a blizzard event is happening (could be used to apply penalties or require survival checks)
        campaign_state['blizzard_active'] = True

def trigger_erandur_intersect(campaign_state):
    """
    Fires once when the PC approaches Nightcaller Temple directly (esp. via Clairvoyance),
    allowing Erandur to intersect on the road/sleeper camp rather than at Windpeak Inn.
    """
    flags = campaign_state.get("scene_flags", {})
    
    # If the Waking Nightmare quest has already been given via another path
    # (e.g., Windpeak Inn), skip this alternate intersection to avoid a
    # duplicated introduction to Erandur.
    # Check both campaign_state root (historical location) and scene_flags (newer location).
    if campaign_state.get("waking_nightmare_quest_given") or flags.get("waking_nightmare_quest_given"):
        return None
    
    if flags.get("erandur_introduced"):
        return None

    if flags.get("session04_whitefin_location_divined") or flags.get("session04_nightcaller_temple_targeted"):
        # Ensure scene_flags exists in campaign_state only when the trigger actually fires
        if "scene_flags" not in campaign_state:
            campaign_state["scene_flags"] = {}
        campaign_state["scene_flags"]["erandur_introduced"] = True
        campaign_state["scene_flags"]["erandur_intersection_method"] = "sleeper_camp_roadside"
        return {
            "scene_id": "A1-S15-ERANDUR",
            "title": "Roadside Sleeper Camp — Erandur Intersects",
            "type": "social",
            "location": "The Pale — Roadside camp below Nightcaller Temple",
            "tags": ["erandur", "vaermina", "waking_nightmare", "arisann_hook"]
        }

    return None

# (Optional) Additional triggers for Dawnstar Sanctuary or Civil War changes can be added when relevant.
# These functions are designed to integrate with the existing narrative engine, 
# providing dynamic descriptions and quest hooks without overriding core game logic.
# Each trigger uses state flags to ensure one-time events (e.g., quest offers don't repeat)
# and to maintain consistency with other hold modules.
