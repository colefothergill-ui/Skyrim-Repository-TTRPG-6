"""
Utility functions for Skyrim TTRPG scripts
"""


def location_matches(search_location, sheet_location):
    """
    Check if a search location matches a stat sheet location.
    
    Uses bidirectional partial matching:
    - Returns True if search term is in sheet location
    - Returns True if sheet location is in search term
    - Case-insensitive comparison
    
    Args:
        search_location: Location to search for (e.g., "Whiterun", "ruins")
                        Can be None or empty string, which returns False
        sheet_location: Location from stat sheet (e.g., "Ancient Nordic Ruins")
                       Can be None or empty string, which returns False
    
    Returns:
        bool: True if locations match, False if either location is invalid
    
    Examples:
        >>> location_matches("Whiterun", "Whiterun")
        True
        >>> location_matches("ruins", "Ancient Nordic Ruins")
        True
        >>> location_matches("Nordic ruins", "Ancient Nordic Ruins")
        True
        >>> location_matches("Solitude", "Whiterun")
        False
        >>> location_matches(None, "Whiterun")
        False
        >>> location_matches("", "Whiterun")
        False
    """
    # Defensive check: ensure both inputs are valid strings
    if not search_location or not sheet_location:
        return False
    
    # Type checking for safety
    if not isinstance(search_location, str) or not isinstance(sheet_location, str):
        return False
    
    search_lower = search_location.lower()
    sheet_lower = sheet_location.lower()
    
    # Bidirectional partial match
    return search_lower in sheet_lower or sheet_lower in search_lower
