#!/usr/bin/env python3
"""
Triggers Module

This module contains location-based triggers for various regions in Skyrim.
"""

from .whiterun_triggers import whiterun_location_triggers
from .windhelm_triggers import windhelm_location_triggers
from .markarth_triggers import markarth_location_triggers

__all__ = ['whiterun_location_triggers', 'windhelm_location_triggers', 'markarth_location_triggers']
