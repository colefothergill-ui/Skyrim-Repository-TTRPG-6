"""Winterhold & College of Winterhold Location Triggers

This module provides location-based atmospheric barks, faction-aware reactions,
first-time scene flags, and questline hooks for:
- Winterhold town (post-Great Collapse)
- The College of Winterhold
- Saarthal expedition staging

Design goals:
- Light-touch state mutation: we only set boolean scene flags.
- No hard quest progression here; we *suggest* beats and expose hooks.
- Faction/civil-war awareness, but College neutrality is respected.

Location keys (recommended):
- winterhold
- winterhold_town
- winterhold_frozen_hearth
- winterhold_jarls_longhouse
- winterhold_ruins
- winterhold_college_bridge
- college_courtyard
- college_hall_of_elements
- college_hall_of_attainment
- college_arcanaeum
- college_midden
- college_arch_mage_quarters
- saarthal_excavation
"""


def _lower(x):
    return (x or "").strip().lower()


def _player_blob(campaign_state: dict) -> dict:
    return campaign_state.get("player", {}) or {}


def _has_staff_of_cinders(player: dict) -> bool:
    """Best-effort check for the Staff of Cinders.

    We support multiple likely representations:
    - player["has_staff_of_cinders"] == True
    - "staff_of_cinders" in player["artifacts"]
    - "Staff of Cinders" appears in player["inventory"]
    """
    if player.get("has_staff_of_cinders"):
        return True

    artifacts = player.get("artifacts") or []
    if isinstance(artifacts, list) and any(str(a).lower() in ("staff_of_cinders", "staff of cinders") for a in artifacts):
        return True

    inv = player.get("inventory") or []
    if isinstance(inv, list) and any("staff of cinders" in str(i).lower() for i in inv):
        return True

    return False


def winterhold_location_triggers(loc: str, campaign_state: dict) -> list[str]:
    """Return a list of narrative events for a Winterhold/College location."""

    events: list[str] = []
    key = _lower(loc)

    flags = campaign_state.setdefault("scene_flags", {})
    player = _player_blob(campaign_state)

    is_college_member = bool(player.get("college_member"))
    college_rank = player.get("college_rank") or "Member"

    civil = campaign_state.get("civil_war_state", {}) or {}
    alliance = _lower(civil.get("player_alliance"))

    has_staff = _has_staff_of_cinders(player)

    # --- WINTERHOLD TOWN ----------------------------------------------------
    if key in {"winterhold", "winterhold_town", "winterhold_ruins"}:
        if not flags.get("winterhold_first_arrival"):
            events.append(
                "Winterhold greets you like a half-remembered nightmare: broken streets, drifting snow, and the Sea of Ghosts gnawing at the cliff below. Most of the old city is gone—swallowed by the Great Collapse."
            )
            flags["winterhold_first_arrival"] = True

        # Civil war awareness: Winterhold is Stormcloak by default.
        if alliance == "imperial" and not flags.get("winterhold_imperial_tension"):
            events.append(
                "A pair of Winterhold guards watch you with cold arithmetic. Imperial colors (or Imperial friends) earn you a long stare—here, 'Empire' sounds like 'occupation,' even after Alduin's fall."
            )
            flags["winterhold_imperial_tension"] = True

        if has_staff and not flags.get("staff_of_cinders_seen_in_town"):
            events.append(
                "A local fisherman clocks the black-and-ember runes on your staff and goes pale. 'That's… Cindershroud.' He doesn't say it like a compliment—he says it like a warning prayer."
            )
            flags["staff_of_cinders_seen_in_town"] = True

        events.append(
            "The wind here cuts like a lecture. Even the aurora looks judgmental."
        )

    # --- THE FROZEN HEARTH --------------------------------------------------
    if key in {"winterhold_frozen_hearth", "frozen_hearth"}:
        events.append(
            "The Frozen Hearth is cramped warmth: stew, wet wool, and locals pretending they're not listening. Everyone is listening."
        )

        if has_staff and not flags.get("staff_of_cinders_inn_reaction"):
            events.append(
                "A traveling bard falls silent mid-verse when he sees your staff. Then, very softly: 'I thought that heirloom was a story.' The room suddenly remembers it has somewhere else to look."
            )
            flags["staff_of_cinders_inn_reaction"] = True

    # --- JARL'S LONGHOUSE ---------------------------------------------------
    if key in {"winterhold_jarls_longhouse", "jarls_longhouse", "jarl_korir_court"}:
        events.append(
            "Winterhold's court is small and sharp-edged. Even the banners look tired. The Jarl's gaze is the kind that measures strangers by how much trouble they can become."
        )

        if is_college_member and not flags.get("jarl_reacts_to_college"):
            events.append(
                "Korir's mouth tightens when he realizes you're College. 'Keep your spells on your side of the bridge,' he says, like the bridge is a treaty."
            )
            flags["jarl_reacts_to_college"] = True

    # --- COLLEGE BRIDGE / ENTRY --------------------------------------------
    if key in {"winterhold_college_bridge", "college_bridge"}:
        if not flags.get("college_bridge_first_time"):
            events.append(
                "The bridge to the College is a thin line between two worlds: town and tower, suspicion and scholarship, gravity and arrogance. The drop below is… educational."
            )
            flags["college_bridge_first_time"] = True

        if not is_college_member:
            # Faralda admission test.
            if not flags.get("college_admission_test_offered"):
                events.append(
                    "Faralda steps into your path, hands relaxed but ready. 'No one enters the College without demonstrating some measure of ability. Show me a spell—then we talk.'"
                )
                flags["college_admission_test_offered"] = True
            else:
                events.append(
                    "Faralda watches your hands. The air tastes faintly of wards and expectations."
                )
        else:
            events.append(
                f"The wards recognize you—{college_rank}. The shimmer parts like a curtain, and you feel the College's attention settle on you for a heartbeat before it moves on."
            )

        if has_staff and not flags.get("staff_of_cinders_college_notice"):
            events.append(
                "A student whispers as you pass: 'Those runes… that's not common enchantment.' Another answers: 'That's not common anything.'"
            )
            flags["staff_of_cinders_college_notice"] = True

    # --- COLLEGE COURTYARD --------------------------------------------------
    if key in {"college_courtyard", "winterhold_college"}:
        events.append(
            "Inside the courtyard, the wind feels… tamer. Snow settles softly on old stone. The College carries itself like it expects the world to apologize."
        )

        # Soft hook: First Lessons.
        if is_college_member and not flags.get("college_first_lessons_hook"):
            events.append(
                "Tolfdir is mid-lecture, gesturing at an invisible diagram of reality. 'Ah! Good. Another mind willing to be wrong in public. Come—class is starting.'"
            )
            flags["college_first_lessons_hook"] = True

    # --- HALLS / LIBRARY ----------------------------------------------------
    if key in {"college_hall_of_elements", "hall_of_elements"}:
        events.append(
            "The Hall of the Elements hums with practiced danger: sparks that don't quite burn, frost that doesn't quite melt, and the unspoken rule that nobody complains about singed eyebrows."
        )
        
        # Add student trio introduction
        if is_college_member and not flags.get("college_students_intro_done"):
            events.append(
                "Onmund (earnest Nord), Brelyna Maryon (quiet Dunmer), and J'zargo (ambitious Khajiit) step out of the student crowd—your 'main peers' finally present. They react to your Staff of Cinders and your obvious faculty familiarity."
            )
            flags["college_students_intro_done"] = True

    if key in {"college_hall_of_attainment", "hall_of_attainment"}:
        events.append(
            "The Hall of Attainment is quieter—sleeping quarters, murmured study, and the tension of a hundred ambitions stacked like books."
        )

    if key in {"college_arcanaeum", "arcanaeum", "college_library"}:
        events.append(
            "The Arcanaeum smells like ink, old leather, and the kind of silence that judges you. Urag gro-Shub guards the shelves like they're a dragon hoard of ideas."
        )

        if has_staff and not flags.get("staff_of_cinders_arcanaeum"):
            events.append(
                "Urag's eyes follow the staff's runes for a long moment. 'That enchantment is… old.' He pauses. 'Do not wave it near my books.' Somehow, that feels like respect."
            )
            flags["staff_of_cinders_arcanaeum"] = True

    # --- THE MIDDEN ---------------------------------------------------------
    if key in {"college_midden", "midden"}:
        events.append(
            "The Midden is colder than the outside. Not in temperature—in *intent*. Old experiments leave scratches in the stone like regret."
        )

    # --- ARCH-MAGE QUARTERS -------------------------------------------------
    if key in {"college_arch_mage_quarters", "arch_mage_quarters"}:
        events.append(
            "The Arch-Mage's quarters feel like a room that expects history to happen inside it. The air is clean, but the politics are not."
        )

    # --- SAARTHAL -----------------------------------------------------------
    if key in {"saarthal_excavation", "saarthal"}:
        events.append(
            "Saarthal is a mouth in the ice. The College's lantern light spills into carved stone older than Nord songs, and the draugr inside have had centuries to practice patience."
        )

        if not flags.get("saarthal_eye_of_magnus_hook"):
            events.append(
                "Tolfdir clears his throat like he's about to apologize to the past. 'We… may have found something. Something *significant.* Stay close.'"
            )
            flags["saarthal_eye_of_magnus_hook"] = True

    return events
