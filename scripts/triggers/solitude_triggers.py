#!/usr/bin/env python3
"""
Solitude Location Triggers

This module handles location-based triggers for Solitude and Haafingar Hold.
It provides contextual events, NPC interactions, and companion commentary
specific to Solitude, the capital of Skyrim and seat of Imperial power.
"""

from .trigger_utils import is_companion_present


def solitude_location_triggers(loc, campaign_state):
    """
    Generate location-specific triggers for Solitude locations.

    Args:
        loc: Current location string (e.g., "solitude", "blue palace", "castle dour")
        campaign_state: Dictionary containing campaign state including companions

    Returns:
        List of event strings to be narrated to players
    """
    events = []
    loc_lower = str(loc).lower()
    companions = campaign_state.get("companions", {}).get("active_companions", [])

    # Entering the Blue Palace (Jarl's Residence)
    if "blue palace" in loc_lower:
        events.append("Guards snap to attention as you enter the Blue Palace courtyard. Elisif the Fair stands atop the stairs; she nods solemnly at your approach and inquires, 'How may I serve Skyrim today?'")

    # Entering Castle Dour (Legion HQ)
    if "castle dour" in loc_lower:
        events.append("You step under Castle Dour's portcullis. Imperial Legionnaires in red\u2011black armor march down the ramparts. An officer eyes you sharply, then salutes, 'At ease, stranger. Keep your steel sheathed inside Imperial walls.'")

    # Entering the Winking Skeever (inn)
    if "winking skeever" in loc_lower:
        events.append("The inn's hearth and ale welcome you. Patrons clank mugs and a bard strums a lute in the corner. Dervorin the innkeeper greets you with a grin: 'Sit, have a drink on the house. Solitude's always safer with a friend.'")

    # Companion commentary: if Marcurio is present and in Solitude, he comments on Imperial hold
    if is_companion_present(companions, "marcurio") and "solitude" in loc_lower:
        events.append('Marcurio (mistress of the arcane) raises an eyebrow. "Your Highness\'s city is well-protected\u2026 impressive. But I sense discontent beneath the loyalty."')

    return events
