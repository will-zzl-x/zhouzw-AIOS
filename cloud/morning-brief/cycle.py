"""Deterministic cycle-phase calculator for calibrating the Differentiation
Cue rotation in the morning brief.

Reads the tracked fields out of context/relationships.md's "Elena's Cycle"
section (last period start date + typical cycle length) and computes which
phase today falls in. Zero LLM tokens spent on the arithmetic — the phase is
handed to brief_generator.py as a plain fact; cue *selection* given that fact
stays an LLM (Rule 8) job, per the project's usual deterministic-script /
fuzzy-LLM split (see meal-planning/README.md for the same pattern).

This is Will's own behavior-calibration tool, never a tracker surfaced to
Elena or used to grade her.

Stdlib only. No PyYAML.
"""

from __future__ import annotations

import re
from datetime import date, datetime

# Phase boundaries as (start_day, end_day) inclusive, keyed to a 28-day
# cycle and scaled proportionally for other lengths. Day 1 = period start.
_PHASE_BOUNDARIES_28D = [
    ("Menstrual", 1, 5),
    ("Follicular", 6, 13),
    ("Ovulatory", 14, 16),
    ("Mid-Luteal", 17, 24),
    ("Late-Luteal", 25, 28),
]

_LAST_PERIOD_RE = re.compile(r"\*\*Last period start:\*\*\s*(\d{4}-\d{2}-\d{2})")
_CYCLE_LENGTH_RE = re.compile(r"\*\*Typical cycle length:\*\*\s*(\d+)\s*days")


def parse_cycle_tracker(relationships_md: str) -> tuple[date, int] | None:
    """Extract (last_period_start, cycle_length) from relationships.md text.

    Returns None if the tracker section isn't present (e.g. not yet set up),
    so callers can skip cycle-awareness gracefully rather than crash.
    """
    m_date = _LAST_PERIOD_RE.search(relationships_md)
    m_len = _CYCLE_LENGTH_RE.search(relationships_md)
    if not m_date or not m_len:
        return None
    try:
        last_period_start = datetime.strptime(m_date.group(1), "%Y-%m-%d").date()
        cycle_length = int(m_len.group(1))
    except ValueError:
        return None
    if cycle_length <= 0:
        return None
    return last_period_start, cycle_length


def compute_phase(last_period_start: date, cycle_length: int, today: date) -> tuple[str, int]:
    """Return (phase_name, cycle_day) for `today` given the tracked anchor.

    cycle_day is 1-indexed from the last logged period start, wrapped by
    cycle_length. Phase boundaries scale proportionally if cycle_length != 28
    (e.g. a 30-day cycle stretches Late-Luteal slightly wider).
    """
    days_since = (today - last_period_start).days
    cycle_day = (days_since % cycle_length) + 1

    for phase, start, end in _PHASE_BOUNDARIES_28D:
        scaled_start = round((start - 1) / 28 * cycle_length) + 1
        scaled_end = round(end / 28 * cycle_length)
        if scaled_start <= cycle_day <= scaled_end:
            return phase, cycle_day

    # Fallback for rounding edge cases at the very end of the cycle.
    return "Late-Luteal", cycle_day


def cycle_phase_today(relationships_md: str, today: date) -> tuple[str, int] | None:
    """Convenience wrapper: parse + compute in one call. None if untracked."""
    parsed = parse_cycle_tracker(relationships_md)
    if parsed is None:
        return None
    last_period_start, cycle_length = parsed
    return compute_phase(last_period_start, cycle_length, today)


__all__ = ["parse_cycle_tracker", "compute_phase", "cycle_phase_today"]
