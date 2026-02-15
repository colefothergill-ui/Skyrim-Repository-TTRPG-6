#!/usr/bin/env python3
"""
Shared utility functions for location trigger modules.

This module provides common helper functions used by location trigger modules
to reduce code duplication and improve maintainability.
"""


def is_companion_present(active_companions, companion_name):
    """
    Check if a specific companion is present in the active companions list.
    
    Args:
        active_companions: List of active companions (can be strings or dicts)
        companion_name: Name of companion to check for (case-insensitive)
    
    Returns:
        bool: True if companion is present, False otherwise
    
    Examples:
        >>> is_companion_present(["Lydia", "Hadvar"], "lydia")
        True
        >>> is_companion_present([{"name": "Lydia"}], "lydia")
        True
        >>> is_companion_present([], "lydia")
        False
    """
    companion_name_lower = companion_name.lower()
    
    for companion in active_companions:
        if isinstance(companion, dict):
            # Check dictionary companions by name or npc_id/id field
            comp_name = str(companion.get("name", "")).lower()
            comp_id = str(companion.get("npc_id", companion.get("id", ""))).lower()
            # Use startswith to allow variations like "Lydia" or "Lydia (Housecarl)"
            if comp_name.startswith(companion_name_lower) or comp_id.startswith(companion_name_lower):
                return True
        else:
            # Check string companions
            # Use startswith to allow variations like "Lydia" or "Lydia the Housecarl"
            if str(companion).lower().startswith(companion_name_lower):
                return True
    
    return False


def is_quest_active(campaign_state, quest_id):
    """
    Check if a quest is currently active or completed.
    
    Args:
        campaign_state: Dictionary containing campaign state including quests
        quest_id: The ID of the quest to check
    
    Returns:
        bool: True if quest is active or completed, False otherwise
    
    Examples:
        >>> is_quest_active({"quests": {"active": ["quest1"]}}, "quest1")
        True
        >>> is_quest_active({"quests": {"completed": ["quest2"]}}, "quest2")
        True
        >>> is_quest_active({}, "quest3")
        False
    """
    quests = campaign_state.get("quests", {})
    active_quests = quests.get("active", [])
    completed_quests = quests.get("completed", [])
    
    # Check if quest_id is in active or completed lists
    if quest_id in active_quests or quest_id in completed_quests:
        return True
    
    # Also check for dictionary format quests
    for quest in active_quests:
        if isinstance(quest, dict) and quest.get("id") == quest_id:
            return True
    
    for quest in completed_quests:
        if isinstance(quest, dict) and quest.get("id") == quest_id:
            return True
    
    return False


def is_night_time(campaign_state):
    """
    Check if it's nighttime in the game.
    
    Args:
        campaign_state: Dictionary containing campaign state including time of day
    
    Returns:
        bool: True if it's night (8 PM to 5:59 AM, i.e., hours 20-23 and 0-5), False otherwise
    
    Examples:
        >>> is_night_time({"time_of_day": "night"})
        True
        >>> is_night_time({"time_of_day": 22})
        True
        >>> is_night_time({"time_of_day": "day"})
        False
    """
    time_of_day = campaign_state.get("time_of_day", "")
    
    # Check various night indicators
    if isinstance(time_of_day, str):
        time_lower = time_of_day.lower()
        return "night" in time_lower or "evening" in time_lower or "midnight" in time_lower
    
    # If time is given as an hour (0-23)
    if isinstance(time_of_day, int):
        return time_of_day >= 20 or time_of_day < 6
    
    return False
