"""Parser + writer for the markdown-table backlog at backlog.md.

The backlog is a single ranked markdown table. Format:

    | id | # | Title | Area | Status | Gate | Depends-on | Notes |
    |---|---|---|---|---|---|---|---|
    | promo-doc-final | 1 | ... | Career | in-progress | deadline:2026-06-30 | — | ... |

Status values: open / in-progress / blocked / done
Gate formats: deadline:YYYY-MM-DD, event:<name>, window:MM-DD..MM-DD,
              window:weekend, window:Q2, drift, your-call, open
Depends-on:   comma-separated id list (no spaces), or "—" (em dash) for none

The "## Inbox (unranked)" section at the bottom is skipped by the parser —
mid-week captures live there until Sunday's reflection sorts them in.

Stdlib only. No PyYAML.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Iterable

EM_DASH = "—"

# Status values that count as "live" (eligible to surface).
_LIVE_STATUSES = {"open", "in-progress"}

# Gates that always pass the time-window check.
_ALWAYS_OPEN_GATES = {"open", "your-call", "drift"}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _split_row(line: str) -> list[str] | None:
    """Split a markdown table row into stripped cells.

    Returns None if the line isn't a valid 8-cell data row. We require exactly
    8 cells so header and separator rows (which have different shapes after
    stripping) are filtered out by the caller.
    """
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    # Drop the leading + trailing pipes, then split. Inner cells are
    # pipe-delimited.
    inner = stripped[1:-1]
    cells = [c.strip() for c in inner.split("|")]
    if len(cells) != 8:
        return None
    return cells


def _is_separator_row(cells: list[str]) -> bool:
    """A separator row looks like |---|---|...|. After stripping, every cell
    is just dashes (and optional colons for alignment)."""
    return all(re.fullmatch(r":?-+:?", c or "") for c in cells)


def _parse_depends_on(raw: str) -> list[str]:
    """Parse the depends-on cell.

    "—" or "-" or "" -> []
    "a,b,c"           -> ["a", "b", "c"]
    """
    raw = (raw or "").strip()
    if not raw or raw in (EM_DASH, "-", "--"):
        return []
    return [tok.strip() for tok in raw.split(",") if tok.strip()]


def parse_backlog(text: str) -> list[dict]:
    """Parse the backlog markdown into a list of move dicts.

    Each dict has keys: id, rank, title, area, status, gate, depends_on, notes.
    `rank` is an int (the # column). `depends_on` is a list[str].
    Rows in the "## Inbox" section are skipped. Header + separator rows are
    skipped. Malformed rows (not exactly 8 pipe-delimited cells) are skipped.
    """
    moves: list[dict] = []
    in_inbox = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        # Section break: anything starting with "## Inbox" toggles us into the
        # inbox section, which we skip entirely.
        stripped = line.strip()
        if stripped.startswith("## Inbox"):
            in_inbox = True
            continue
        if stripped.startswith("## ") and not stripped.startswith("## Inbox"):
            # Hypothetical other H2 — drop back out of inbox mode.
            in_inbox = False
            # fall through; this isn't a table row anyway
        if in_inbox:
            continue

        cells = _split_row(line)
        if cells is None:
            continue
        # Skip header row: "id" / "#" / "Title" ...
        if cells[0].lower() == "id" and cells[1] == "#":
            continue
        # Skip separator row.
        if _is_separator_row(cells):
            continue

        move_id, rank_raw, title, area, status, gate, depends_on, notes = cells
        if not move_id:
            continue
        try:
            rank = int(rank_raw)
        except ValueError:
            # Rank must be an int; if not, skip the row defensively.
            continue

        moves.append({
            "id": move_id,
            "rank": rank,
            "title": title,
            "area": area,
            "status": status.lower(),
            "gate": gate,
            "depends_on": _parse_depends_on(depends_on),
            "notes": notes,
        })

    return moves


# ---------------------------------------------------------------------------
# Eligibility filter
# ---------------------------------------------------------------------------

def _gate_satisfied(gate: str, today: date) -> bool:
    """True if the gate's time window is satisfied by `today`."""
    gate = (gate or "").strip()
    if not gate:
        # Treat missing gate as open.
        return True
    if gate in _ALWAYS_OPEN_GATES:
        return True
    if gate.startswith("deadline:"):
        try:
            deadline = datetime.strptime(gate[len("deadline:"):], "%Y-%m-%d").date()
        except ValueError:
            return False
        return today <= deadline
    if gate.startswith("event:"):
        # Event gates aren't time-bounded by themselves; treat as open.
        return True
    if gate.startswith("window:"):
        spec = gate[len("window:"):].strip()
        # window:weekend -> pass on Sat/Sun
        if spec == "weekend":
            return today.weekday() >= 5
        # window:Q2 / window:Q1 ... -> month-range gate
        if re.fullmatch(r"Q[1-4]", spec):
            q = int(spec[1])
            month = today.month
            return (q - 1) * 3 + 1 <= month <= q * 3
        # window:MM-DD..MM-DD -> calendar-day range, year-agnostic
        m = re.fullmatch(r"(\d{2})-(\d{2})\.\.(\d{2})-(\d{2})", spec)
        if m:
            start = (int(m.group(1)), int(m.group(2)))
            end = (int(m.group(3)), int(m.group(4)))
            today_md = (today.month, today.day)
            if start <= end:
                return start <= today_md <= end
            # Wrapped window (e.g., 12-28..01-03).
            return today_md >= start or today_md <= end
        # Unknown window spec: be conservative and let it through.
        return True
    # Unrecognized gate prefix: let it through rather than silently hide.
    return True


def filter_eligible(moves: list[dict], today: date) -> list[dict]:
    """Apply the brief's eligibility filter and return rank-ordered survivors.

    A move passes when:
      - status is "open" or "in-progress"
      - the gate's time window includes `today`
      - every depends-on id resolves to a move with status == "done"
        (missing-id deps are treated as unsatisfied — fail closed)

    Output is sorted by rank ascending (lowest # = highest priority first).
    """
    by_id = {m["id"]: m for m in moves}
    eligible: list[dict] = []
    for m in moves:
        if m["status"] not in _LIVE_STATUSES:
            continue
        if not _gate_satisfied(m["gate"], today):
            continue
        deps_ok = True
        for dep in m["depends_on"]:
            dep_move = by_id.get(dep)
            if dep_move is None or dep_move["status"] != "done":
                deps_ok = False
                break
        if not deps_ok:
            continue
        eligible.append(m)
    eligible.sort(key=lambda m: m["rank"])
    return eligible


# ---------------------------------------------------------------------------
# Mutators
# ---------------------------------------------------------------------------

# Match a full pipe-delimited row, capturing the cell sequence so we can
# rewrite a single column without disturbing surrounding whitespace.
_ROW_RE = re.compile(r"^(\s*\|)([^\n]*)(\|\s*)$")


def _replace_status_in_row(row: str, new_status: str) -> str:
    """Replace the Status column (cell index 4) of a single table row,
    preserving the original cell padding/width as much as possible."""
    m = _ROW_RE.match(row)
    if not m:
        return row
    leading, body, trailing = m.group(1), m.group(2), m.group(3)
    # body looks like "  cell1 | cell2 | ... | cell8  "
    # Split on the unescaped pipe; tables don't use escaped pipes here.
    parts = body.split("|")
    if len(parts) != 8:
        return row
    original = parts[4]
    # Preserve leading/trailing whitespace inside the cell.
    lead_ws = re.match(r"^\s*", original).group(0)
    trail_ws = re.search(r"\s*$", original).group(0)
    parts[4] = f"{lead_ws}{new_status}{trail_ws}"
    return f"{leading}{'|'.join(parts)}{trailing}"


def mark_done(text: str, sm_id: str, completion_date: str) -> str:
    """Find the table row where id == sm_id, set its Status cell to "done".

    Idempotent: if the row is already done, returns text unchanged.
    Preserves all other cells and surrounding whitespace. `completion_date`
    is accepted for forward-compat (e.g., a future "completed_at" column or
    notes-stamp) but is not currently written into the table.
    """
    out_lines: list[str] = []
    in_inbox = False
    changed = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## Inbox"):
            in_inbox = True
        elif stripped.startswith("## "):
            in_inbox = False

        if changed or in_inbox:
            out_lines.append(line)
            continue

        cells = _split_row(line)
        if cells is None:
            out_lines.append(line)
            continue
        if cells[0] == sm_id:
            current_status = cells[4].strip().lower()
            if current_status == "done":
                out_lines.append(line)  # idempotent no-op
            else:
                out_lines.append(_replace_status_in_row(line, "done"))
            changed = True
            continue

        out_lines.append(line)

    # Preserve trailing newline if present.
    result = "\n".join(out_lines)
    if text.endswith("\n") and not result.endswith("\n"):
        result += "\n"
    return result


def mark_surfaced(text: str, sm_ids: list[str], today_date: str) -> str:
    """No-op for the current table format.

    The table has no surfaced_count column, so there's nothing to update.
    Kept for API parity with the brief generator + future telemetry. If we
    add a surfaced_at / surfaced_count column later, this is where the
    update logic belongs.
    """
    _ = (sm_ids, today_date)  # silence linters
    return text


__all__ = [
    "parse_backlog",
    "filter_eligible",
    "mark_done",
    "mark_surfaced",
]
