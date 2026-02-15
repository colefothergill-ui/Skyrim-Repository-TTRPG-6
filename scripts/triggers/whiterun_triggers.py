#!/usr/bin/env python3
"""
Whiterun Location Triggers

This module handles location-based triggers for Whiterun and its districts.
It provides contextual events, NPC interactions, and companion commentary
specific to Whiterun Hold.
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
    
    # District-specific triggers
    if "plains" in loc_lower and "whiterun" in loc_lower:
        events.append("You enter the bustling Plains District. Merchants call out their wares, and the smell of fresh bread wafts from the Bannered Mare.")
    
    elif "wind" in loc_lower and "whiterun" in loc_lower:
        events.append("The Wind District stretches before you. The Gildergreen's branches sway gently, and Jorrvaskr's mead hall stands proud among the homes.")
    
    elif "cloud" in loc_lower and "whiterun" in loc_lower:
        events.append("You ascend to the Cloud District. Dragonsreach looms above, its ancient Nordic architecture a testament to Whiterun's storied past.")
    
    # General Whiterun entrance
    elif loc_lower.startswith("whiterun"):
        events.append("The gates of Whiterun stand before you. Guards watch from the walls as merchants and travelers pass through the ancient stone gateway.")
    
    # Companion commentary (placeholder logic for Whiterun-based companions)
    active_companions = campaign_state.get("companions", {}).get("active_companions", [])
    # If Lydia (Housecarl of Whiterun) is in the party and we're in Whiterun, she may comment on being home.
    if is_companion_present(active_companions, "lydia") and loc_lower.startswith("whiterun"):
        events.append('Lydia smiles fondly as she looks around. "It\'s good to be back in Whiterun, my Thane," she says softly.')
    # (Additional companion triggers can be added similarly for other Whiterun natives, e.g., if Aela is a follower, etc.)
    
    return events
