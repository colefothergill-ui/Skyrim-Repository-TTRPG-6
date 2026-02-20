#!/usr/bin/env python3
"""
Whiterun Location Triggers

This module handles location-based triggers for Whiterun and its districts.
It provides contextual events, NPC interactions, and companion commentary
specific to Whiterun Hold.  When the Battle of Whiterun is active, district
text and companion barks switch to siege context keyed to the current stage.
"""

from .trigger_utils import is_companion_present


def whiterun_location_triggers(loc, campaign_state):
    """
    Generate location-specific triggers for Whiterun locations.
    
    Args:
        loc: Current location string (e.g., "whiterun", "whiterun_plains_district")
        campaign_state: Dictionary containing campaign state including companions
        
    Returns:
        List of event strings to be narrated to players
    """
    events = []
    
    # Normalize location for case-insensitive matching
    loc_lower = str(loc).lower()

    # ------------------------------------------------------------------
    # Siege state detection
    # ------------------------------------------------------------------
    cw_state = campaign_state.get("civil_war_state", {})
    battle_status = cw_state.get("battle_of_whiterun_status", "")
    siege_active = battle_status == "active"
    battle_stage = int(cw_state.get("battle_of_whiterun_stage", 0))
    battle_faction = str(cw_state.get("battle_of_whiterun_faction", "")).lower()

    if siege_active:
        # Emit the universal siege header
        faction_label = battle_faction.capitalize() if battle_faction else "Unknown"
        events.append(
            f"[Battle of Whiterun | {faction_label} | Stage {battle_stage}/5]"
        )

    # ------------------------------------------------------------------
    # District-specific triggers - siege vs. peacetime text
    # ------------------------------------------------------------------
    if "plains" in loc_lower and "whiterun" in loc_lower:
        if siege_active:
            if battle_stage >= 3:
                events.append(
                    "The Plains District is a war zone. Market stalls are overturned, "
                    "fires lick at the Bannered Mare's eaves, and Imperial and Stormcloak "
                    "dead share the cobblestones. Every shadow might be an ambush."
                )
            else:
                events.append(
                    "The Plains District is on edge. Merchants have shuttered their stalls "
                    "and armed Whiterun guards patrol in force. The distant sound of battle "
                    "echoes off the stone walls."
                )
        else:
            events.append(
                "You enter the bustling Plains District. Merchants call out their wares, "
                "and the smell of fresh bread wafts from the Bannered Mare."
            )

    elif "wind" in loc_lower and "whiterun" in loc_lower:
        if siege_active:
            if battle_stage >= 4:
                events.append(
                    "The Wind District is contested. The Gildergreen stands witness to the "
                    "fighting below it; its branches are speckled with ash. Jorrvaskr's doors "
                    "are barred, and the clash of steel rings where prayers once echoed."
                )
            else:
                events.append(
                    "The Wind District is braced for violence. Citizens have retreated indoors "
                    "and the Temple of Kynareth's healers move urgently between the wounded. "
                    "The Gildergreen sways as if it knows what is coming."
                )
        else:
            events.append(
                "The Wind District stretches before you. The Gildergreen's branches sway "
                "gently, and Jorrvaskr's mead hall stands proud among the homes."
            )

    elif "cloud" in loc_lower and "whiterun" in loc_lower:
        if siege_active:
            if battle_stage >= 1:
                events.append(
                    "The Cloud District is locked down. Dragonsreach's great doors are "
                    "sealed from within; Imperial guards hold the bridge chokepoint. "
                    "The air smells of smoke and drawn steel."
                )
            else:
                events.append(
                    "You ascend to the Cloud District under a sky heavy with tension. "
                    "Dragonsreach looms above, its banners snapping in a wind carrying "
                    "the distant sound of war drums."
                )
        else:
            events.append(
                "You ascend to the Cloud District. Dragonsreach looms above, its ancient "
                "Nordic architecture a testament to Whiterun's storied past."
            )

    elif loc_lower.startswith("whiterun"):
        if siege_active:
            events.append(
                "Whiterun is at war. The gates are reinforced with improvised barricades "
                "and the guards' faces are grim. Every entrance is watched. "
                "The city you knew is a battlefield now."
            )
        else:
            events.append(
                "The gates of Whiterun stand before you. Guards watch from the walls as "
                "merchants and travelers pass through the ancient stone gateway."
            )

    # ------------------------------------------------------------------
    # Companion barks - siege context for Hadvar and Ralof
    # ------------------------------------------------------------------
    active_companions = campaign_state.get("companions", {}).get("active_companions", [])

    if siege_active:
        if is_companion_present(active_companions, "hadvar") and "whiterun" in loc_lower:
            if battle_faction == "imperial":
                events.append(
                    'Hadvar scans the street and nods grimly. '
                    '"Hold the line. We protect these people - that\'s why we\'re here."'
                )
            else:
                events.append(
                    'Hadvar is tense beside you. He says nothing, but his hand never '
                    'leaves his sword hilt.'
                )

        if is_companion_present(active_companions, "ralof") and "whiterun" in loc_lower:
            if battle_faction == "stormcloak":
                events.append(
                    'Ralof grips your arm. "Push forward! Skyrim is watching what we do here."'
                )
            else:
                events.append(
                    'Ralof surveys the fighting with a complicated expression. He says '
                    'nothing - but you can see he is weighing every step.'
                )
    else:
        # Peacetime Lydia commentary
        if is_companion_present(active_companions, "lydia") and loc_lower.startswith("whiterun"):
            events.append(
                'Lydia smiles fondly as she looks around. '
                '"It\'s good to be back in Whiterun, my Thane," she says softly.'
            )

    return events
