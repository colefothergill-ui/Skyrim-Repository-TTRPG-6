#!/usr/bin/env python3
"""
Riften (The Rift) Location Triggers

This module handles location-based narrative triggers for The Rift hold and its capital city, Riften.
It provides descriptive events for entering key areas of Riften (districts, temple, etc.), environmental triggers for the Rift's wilderness (autumn forests, Lake Honrich), and companion commentary specific to Riften.
It also includes triggers to initiate Thieves Guild recruitment when appropriate.
"""

from .trigger_utils import is_companion_present

def rift_location_triggers(loc, campaign_state):
    """
    Generate location-specific narrative triggers for Riften city and The Rift hold.
    
    Args:
        loc: Current location string (e.g., "riften_marketplace", "the rift wilderness", "temple_of_mara_riften")
        campaign_state: Dictionary containing the campaign state (includes party info, faction statuses, quest flags, etc.)
    
    Returns:
        List[str]: A list of event description strings triggered by this location
    """
    events = []
    loc_lower = str(loc).lower()

    # Riften city - specific district triggers
    if "riften" in loc_lower and "market" in loc_lower:
        events.append("You step into Riften's marketplace. Wooden stalls surround the plaza as townsfolk haggle over fish, produce, and trinkets. The air carries the aroma of spiced mead from the nearby Black-Briar Meadery and the tang of freshly caught fish from Lake Honrich. Guards keep a watchful eye, but you sense nimble fingers in the crowd – this market is fertile ground for thieves.")

    elif "riften" in loc_lower and ("ratway" in loc_lower or "ragged" in loc_lower or "flagon" in loc_lower):
        events.append("You descend into the Ratway, Riften's underground maze of damp tunnels and crumbling stone. The din of the market above fades into echoes of dripping water. In the shadows, figures shuffle away – unsavory vagrants and thieves lurking just out of sight. Deeper in, a faint light and murmured voices lead toward a tavern hidden beneath the city – the Ragged Flagon, den of the Thieves Guild.")

    elif "riften" in loc_lower and "temple" in loc_lower:
        events.append("You arrive at the Temple of Mara, an island of calm amid Riften's chaos. The scent of incense drifts through the wooden chapel as soft light filters in. Sisters and priests of Mara smile warmly at you. A young couple kneels at the altar, hands clasped, while a priest offers a blessing of love. The city's troubles feel distant here, replaced by an aura of compassion and hope.")

    elif "riften" in loc_lower and ("mistveil" in loc_lower or "keep" in loc_lower):
        events.append("Entering Mistveil Keep, you pass under the vigilant gaze of Riften guards. The grand hall is lit by torches and hearthfire, illuminating banners of the Rift. Jarl Laila Law-Giver confers with her advisors at the far end, worry creasing her brow. Courtiers shuffle with scrolls, and you catch a glimpse of Maven Black-Briar in the shadows of a pillar, observing every move with a knowing smirk. The tension between official rule and private power is palpable here.")

    elif loc_lower.startswith("riften"):
        # General Riften entrance if no specific district trigger fired
        events.append("You enter the city of Riften. Tall wooden buildings crowd the narrow streets, many built out over the water of the canal that cuts through the city. The atmosphere is wary; you feel eyes on you from alleyways as vendors shout daily specials. Beneath the pleasant veneer of carved timber and autumn flowers, an undercurrent of mischief and watchfulness permeates the air. Riften feels alive and on edge all at once.")

    # The Rift wilderness - environment triggers
    if (loc_lower.startswith("the rift") or loc_lower == "rift" or ("rift" in loc_lower and "riften" not in loc_lower)) and "forest" in loc_lower:
        # Trigger for being in the autumn forests of The Rift
        events.append("The forest around you is awash in autumn's golden hues. Leaves of orange and red drift down from towering trees, carpeting the ground. The air is crisp with the scent of pine and distant woodsmoke. In the tranquil silence you hear faint rustles – deer foraging or perhaps a predator stalking. The Rift's wilderness is beautiful yet holds its dangers in the dappled shade.")

    if "honrich" in loc_lower or ("riften" in loc_lower and "fishery" in loc_lower) or ("lake" in loc_lower and "riften" in loc_lower):
        # Trigger for Lake Honrich or Riften docks area
        events.append("Lake Honrich stretches out before you, its calm waters reflecting the orange glow of the Rift's foliage. The docks nearby creak as fishers unload the day's catch and workers roll barrels of Black-Briar Mead onto boats. Gull calls mix with the lap of water against the piers. The scene is peaceful, yet one can spot Riften's walls and the silhouettes of watchtowers on the lake's edge – a reminder of both commerce and vigilance on these shores.")

    # Thieves Guild recruitment trigger (Brynjolf in the marketplace)
    if "riften" in loc_lower and "market" in loc_lower and not campaign_state.get("player", {}).get("thieves_guild_member", False):
        events.append("A red-haired man in fine but inconspicuous clothes catches your eye from beside a market stall. He gives a slight nod and a half-smile. **Brynjolf**, a Riften merchant with a certain reputation, seems to be sizing you up. \"Never done an honest day's work in your life, have you?\" he calls out casually, as if inviting you into something more than just a normal market exchange.")

    # Companion commentary for Riften-specific companions
    active_companions = campaign_state.get("companions", {}).get("active_companions", [])
    if is_companion_present(active_companions, "iona") and loc_lower.startswith("riften"):
        events.append('Iona adjusts her stance and rests a hand on her sword hilt as she surveys Riften. "As your housecarl, my Thane, I\'ll be keeping a close eye. Riften\'s streets can be as treacherous as its wilderness," she says, her voice low but resolute.')
    # (Additional companion triggers can be added for other Riften natives, e.g., Mjoll the Lioness if she is a follower, commenting on the corruption she despises.)

    return events
