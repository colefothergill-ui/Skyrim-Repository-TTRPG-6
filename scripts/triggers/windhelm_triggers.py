#!/usr/bin/env python3
"""
Windhelm Location Triggers

This module handles location-based triggers for Windhelm and Eastmarch.
It provides contextual events, NPC interactions, and companion commentary
specific to Windhelm Hold, including quest hooks for Blood on the Ice
and The White Phial.
"""

from .trigger_utils import is_companion_present, is_quest_active, is_night_time


def windhelm_location_triggers(loc, campaign_state):
    """
    Generate location-specific triggers for Windhelm locations.
    
    Args:
        loc: Current location string (e.g., "windhelm", "windhelm_graveyard")
        campaign_state: Dictionary containing campaign state including companions and quests
        
    Returns:
        List of event strings to be narrated to players
    """
    events = []
    
    # Normalize location for case-insensitive matching
    loc_lower = str(loc).lower()
    
    # Get active companions
    active_companions = campaign_state.get("companions", {}).get("active_companions", [])
    
    # District/area-specific triggers
    if ("gray_quarter" in loc_lower or "grey_quarter" in loc_lower) and "windhelm" in loc_lower:
        events.append("You enter the Gray Quarter, home to Windhelm's Dark Elf population. The air is thick with incense and the sounds of foreign tongues. Dilapidated buildings and suspicious glances speak to the Dunmer's treatment in this city.")
    
    elif "graveyard" in loc_lower and "windhelm" in loc_lower:
        events.append("The cold wind whistles through Windhelm's graveyard. Stone markers stand as silent witnesses to the city's dead, their names weathered by Skyrim's harsh winters.")
        
        # Blood on the Ice quest hook - nighttime graveyard visit
        if not is_quest_active(campaign_state, "blood_on_the_ice"):
            if is_night_time(campaign_state):
                events.append("You hear distant shouts near the graveyard... A guard's voice cuts through the night: 'Another one! Someone get the steward!' A crowd is gathering around something near the Hall of the Dead.")
            else:
                # Daytime hint
                events.append("A guard stationed nearby mutters to his companion: 'Three murders in as many weeks. The Butcher strikes again, they say. Keep your eyes open after dark.'")
    
    elif "market" in loc_lower and "windhelm" in loc_lower:
        events.append("The marketplace of Windhelm bustles with activity. Vendors hawk their wares while Nord shoppers barter loudly. The imposing Palace of the Kings looms over the district.")
        
        # White Phial shop hint
        if not is_quest_active(campaign_state, "the_white_phial"):
            events.append("As you pass by the White Phial alchemy shop, you hear raised voices inside. An elderly voice rasps: 'I don't have much time, Quintus! The Phial must be found!' followed by a younger man's worried reply.")
    
    elif ("palace_of_the_kings" in loc_lower and "windhelm" in loc_lower) or ("palace" in loc_lower and "windhelm" in loc_lower):
        events.append("You stand before the Palace of the Kings, seat of Jarl Ulfric Stormcloak. The ancient stone fortress radiates power and defiance, a symbol of Nordic tradition and the Stormcloak cause.")
    
    elif ("candlehearth_hall" in loc_lower and "windhelm" in loc_lower) or ("candlehearth" in loc_lower and "windhelm" in loc_lower):
        events.append("Candlehearth Hall's warmth is a welcome respite from Windhelm's bitter cold. The inn is filled with the smell of roasting meat and the sound of travelers sharing tales.")
    
    # General Windhelm entrance
    elif loc_lower.startswith("windhelm") or "windhelm" in loc_lower:
        events.append("The ancient stone walls of Windhelm rise before you, weathered by countless winters. Known as the City of Kings, Windhelm stands as a bastion of Nordic tradition and the current seat of Ulfric Stormcloak's rebellion.")
        
        # General quest hooks when entering the city
        if not is_quest_active(campaign_state, "blood_on_the_ice") and is_night_time(campaign_state):
            events.append("The city feels tense at night. Shadows seem longer here, and few citizens walk the streets after dark. You overhear whispered conversations about recent murders...")
    
    # Companion commentary for Windhelm-relevant companions
    if is_companion_present(active_companions, "stenvar"):
        if loc_lower.startswith("windhelm"):
            events.append('Stenvar grunts as you enter Windhelm. "Never cared much for this place. Too cold, too many politics. But the mead at Candlehearth Hall isn\'t bad."')
    
    # Companions with Nord heritage might comment on the city's history
    if is_companion_present(active_companions, "uthgerd"):
        if loc_lower.startswith("windhelm"):
            events.append('Uthgerd looks around appreciatively. "Windhelm... the oldest city in Skyrim. Built by Ysgramor himself. Whatever you think of Ulfric, you can\'t deny this place has history."')
    
    # Civil War tie-ins for Windhelm
    if "windhelm" in loc_lower:
        # After Battle of Whiterun outcomes
        if campaign_state.get("whiterun_control") == "stormcloak" and not campaign_state.get("windhelm_heard_whiterun_win"):
            events.append("Word of Whiterun's fall to the Stormcloaks has reached Windhelm. The city is alive with celebration – you see blue Stormcloak banners hung from windows and hear a smith shouting, \"Victory for Ulfric!\" in between hammer strikes. In the Palace courtyard, a crowd cheers as a messenger announces Balgruuf's surrender. Windhelm basks in this triumph, however brief it may be.")
            campaign_state["windhelm_heard_whiterun_win"] = True
        elif campaign_state.get("whiterun_control") == "imperial" and not campaign_state.get("windhelm_heard_whiterun_loss"):
            events.append("A hush has fallen over Windhelm. Rumor spreads that the assault on Whiterun failed; Jarl Balgruuf remains with the Empire. You notice doubled patrols – Stormcloak guards drilling with a fierce urgency. Inside Candlehearth Hall, citizens speak in worried tones about what went wrong and how soon Imperials might counterattack. The sting of the loss is palpable in the air.")
            campaign_state["windhelm_heard_whiterun_loss"] = True

        # Siege of Windhelm preparation (Imperial final attack scenario)
        if campaign_state.get("battle_for_windhelm_started") and not campaign_state.get("windhelm_siege_alert"):
            events.append("Alarms ring out across Windhelm – the Imperials are at the gates! The city has been fortified for a siege: barricades line the Stone Quarter and citizens have been evacuated indoors. Overhead, you hear the distant crash of flaming stones hitting the outer walls. Stormcloak soldiers rush through the streets to their posts. The **Battle for Windhelm** has begun, and the city you once knew is now a battlefield.")
            campaign_state["windhelm_siege_alert"] = True

        # Season Unending truce scenario
        if campaign_state.get("truce_active") and not campaign_state.get("windhelm_truce_noticed"):
            events.append("An uneasy peace has settled over Windhelm. You notice Imperial emissaries being grudgingly escorted through the streets, their presence tolerated under the terms of the truce. Stormcloak guards watch them with barely concealed hostility. The tension is thick – this ceasefire feels temporary at best.")
            campaign_state["windhelm_truce_noticed"] = True
    
    return events
