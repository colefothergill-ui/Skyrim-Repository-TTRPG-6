#!/usr/bin/env python3
"""
Character Creation helpers for Skyrim TTRPG

Provides faction selection and faction-themed backstory questions used
during Session Zero character creation.
"""

STARTING_FACTIONS = [
    "neutral",
    "college_of_winterhold",
    "companions",
    "dark_brotherhood",
    "thieves_guild",
]

_FACTION_LABELS = {
    "neutral": "Neutral (No faction)",
    "college_of_winterhold": "College of Winterhold",
    "companions": "The Companions",
    "dark_brotherhood": "Dark Brotherhood",
    "thieves_guild": "Thieves Guild",
}

_FACTION_QUESTIONS = {
    "college_of_winterhold": "Which school of magic first bent to your will?",
    "companions": "Was it glory, coin, or honor that brought you to Jorrvaskr?",
    "dark_brotherhood": "What was the name of the first life you were paid to take?",
    "thieves_guild": "What is the most valuable thing you have ever stolen, and why?",
    "neutral": "What drove you to Skyrim at a time of civil war?",
}

_BACKSTORY_TAG_MAP = {
    "college_of_winterhold": ["college", "winterhold", "magic"],
    "companions": ["companions", "jorrvaskr", "honor"],
    "dark_brotherhood": ["dark_brotherhood", "assassination", "shadow"],
    "thieves_guild": ["thieves_guild", "riften", "stealth"],
    "neutral": ["independent", "wanderer"],
}


def choose_starting_faction():
    """
    Interactively prompt the player to choose their PC's starting faction.

    Returns:
        str: One of the values in STARTING_FACTIONS
    """
    print("\nWhich path first shaped you?")
    for i, faction in enumerate(STARTING_FACTIONS, 1):
        label = _FACTION_LABELS.get(faction, faction)
        print(f"{i}. {label}")

    chosen = None
    while not chosen:
        raw = input(f"Enter (1-{len(STARTING_FACTIONS)}): ").strip()
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(STARTING_FACTIONS):
                chosen = STARTING_FACTIONS[idx]
        if not chosen:
            print(f"Invalid. Please choose 1-{len(STARTING_FACTIONS)}.")

    return chosen


def ask_faction_backstory_question(faction):
    """
    Return the backstory question for the given faction.

    Args:
        faction: A value from STARTING_FACTIONS

    Returns:
        str: The question string, or a generic fallback
    """
    return _FACTION_QUESTIONS.get(faction, "What is your story?")


def get_backstory_tags(faction):
    """
    Return a list of backstory tags for the given faction.

    Args:
        faction: A value from STARTING_FACTIONS

    Returns:
        list[str]: Tag strings suitable for use in relationship_inference
    """
    return list(_BACKSTORY_TAG_MAP.get(faction, []))
