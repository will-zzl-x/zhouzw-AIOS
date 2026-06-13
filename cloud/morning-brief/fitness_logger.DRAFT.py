"""DRAFT — Fitness logging pipeline for AIOS (task #74).

STATUS: design + stub only. NOT WIRED, NOT DEPLOYED. Do not import from main.py
until the data-source auth questions below are resolved with Will.

------------------------------------------------------------------------------
WHY THIS EXISTS
------------------------------------------------------------------------------
state.md (2026-06-03): "Fitness logging pipeline broken. Liftosaur CSV + weight
spreadsheet + step source don't auto-flow to AIOS — synthesis false-flagged
'fitness signal: zero' 5/29 while Wk2 actually had a Larsen Press top-set rep PR.
Manual Sunday paste habit until pipeline build (task #74)."

GOAL: kill the manual Sunday-paste habit. Land workout + weight + steps into
journals/daily-log.md (and/or workout-log.md / health-log.md) on a schedule, so
Friday /weekly-synthesis reads real data instead of empty journals.

------------------------------------------------------------------------------
DATA SOURCES (3) — where logs come from
------------------------------------------------------------------------------
1. WORKOUTS — Liftosaur.
   - Liftosaur stores history in a per-account cloud account. Two access paths:
     a) Manual CSV/JSON export (Liftosaur app -> Settings -> Export) dropped into
        a known folder / Drive, then ingested. Zero-auth, but reintroduces a
        manual step (smaller than the full Sunday paste — just an export tap).
     b) Liftosaur has no public OAuth API as of writing. The cloud-sync uses a
        Google/Apple sign-in token. Scraping it is brittle. RECOMMEND path (a)
        for v1: a single "export + drop file" tap, parsed automatically.
   - History note: token expired 5/24-5/25 and a session was lost (see
     archives/2026-05-25-reflection.md). Any pull path must surface auth failure
     LOUDLY, not silently log zero.

2. BODY WEIGHT — weight spreadsheet.
   - Currently a spreadsheet (Google Sheet most likely, per personal-laptop MCP
     set). v1: read via Google Sheets API (gspread / Sheets REST) OR export to
     CSV in the same drop folder as Liftosaur. RECOMMEND: Sheets API read-only
     if the sheet is in Google Drive (Will already has Google MCP on personal
     laptop); CSV-drop fallback otherwise.

3. STEPS — Apple Watch / Apple Health.
   - Apple Health has no cloud API. Options:
     a) iOS Shortcut: "Log steps to AIOS" Shortcut posts steps to a webhook /
        appends to a Drive CSV daily. Lowest friction, runs on phone automation.
     b) Health Auto Export app -> daily CSV to iCloud Drive / Google Drive ->
        ingested with the others.
   - RECOMMEND (a): a daily iOS Shortcut automation -> the same drop folder.

CONVERGENCE: all three land as files in ONE cloud drop folder (Google Drive
folder "aios-fitness-drop" is the cleanest given existing Google MCP), OR get
posted to a small webhook. v1 = file-drop folder (no new always-on service).

------------------------------------------------------------------------------
HOW IT LANDS IN daily-log.md
------------------------------------------------------------------------------
- Reuse the existing GitHub Contents API append pattern from health_logger.py
  (fetch file + sha -> append entry -> PUT). Same REPO / BRANCH / token.
- A new Cloud Function entry point `fitness_archive` (sibling to evening_archive)
  OR fold into evening_archive in main.py. Scheduled ~8:30pm AZ (before the 9pm
  evening_archive, or merged into it).
- For each source with new data for today, append a line to journals/daily-log.md
  under today's date header, mirroring health_logger's "key: value flag" style.
  Workouts (multi-line, structured) are better appended to journals/workout-log.md
  under a dated session header (matches the existing manual format there).
- IDEMPOTENCY: before appending, check the target file for today's date + source
  marker so a re-run (or the 3-day parallel-run window, task #53) does not double
  log. health_logger.py currently has NO idempotency guard — this pipeline must
  add one (the same gap that DELETE-not-close guards against in todoist_client).

------------------------------------------------------------------------------
OPEN QUESTIONS FOR WILL (block full build)
------------------------------------------------------------------------------
Q1. Liftosaur: OK to commit to "export + drop file" tap, or do you want a
    zero-touch scrape (more brittle)?
Q2. Weight spreadsheet: is it a Google Sheet? Share the sheet id / range.
Q3. Steps: build the iOS Shortcut, or use Health Auto Export -> CSV?
Q4. Drop target: Google Drive folder vs. small webhook? (Drive folder = no new
    service to keep alive.)
Q5. Where should workouts land — daily-log.md (summary line) or workout-log.md
    (full session)? Recommend: summary line in daily-log.md + full session in
    workout-log.md.
"""

import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from health_logger import _fetch_file, _put_file  # reuse the GitHub append plumbing

TZ = ZoneInfo("America/Phoenix")
WORKOUT_LOG_PATH = "journals/workout-log.md"
DAILY_LOG_PATH = "journals/daily-log.md"


# ---------------------------------------------------------------------------
# SOURCE PARSERS (stubs — wire to the chosen drop mechanism in Q1-Q4 above)
# ---------------------------------------------------------------------------
def parse_liftosaur_export(raw: str) -> list[dict]:
    """Parse a Liftosaur CSV/JSON export into per-session dicts.

    Returns list of {"date": "YYYY-MM-DD", "program_day": str,
    "sets": [{"lift": str, "weight": float, "reps": [int], "rpe": [float]}]}.
    STUB: real shape depends on Liftosaur's export schema (Q1).
    """
    raise NotImplementedError("Confirm Liftosaur export schema (Q1) before wiring.")


def parse_weight_sheet(rows: list[list[str]]) -> list[dict]:
    """Parse weight-spreadsheet rows into {"date","weight_lb"} dicts.

    STUB: real shape depends on the sheet layout (Q2).
    """
    raise NotImplementedError("Confirm weight-sheet layout (Q2) before wiring.")


def parse_steps_drop(raw: str) -> dict | None:
    """Parse the daily steps drop (Shortcut/Health Auto Export) -> {"date","steps"}.

    STUB: real shape depends on the chosen steps mechanism (Q3).
    """
    raise NotImplementedError("Confirm steps mechanism (Q3) before wiring.")


# ---------------------------------------------------------------------------
# IDEMPOTENT APPEND HELPERS (the part health_logger.py is missing)
# ---------------------------------------------------------------------------
def _already_logged(content: str, date_str: str, marker: str) -> bool:
    """True if content already has a line for date_str carrying `marker`."""
    pat = re.compile(rf"^.*{re.escape(date_str)}.*{re.escape(marker)}", re.MULTILINE)
    return bool(pat.search(content))


def log_workout_session(session: dict) -> dict:
    """Append a full session to workout-log.md under a dated header, idempotently.

    Mirrors the existing manual format in workout-log.md:
        **<Day Mon DD> — <program_day>**
        - <lift> <weight> — <reps> @ RPE <rpe>
    """
    date_str = session["date"]  # YYYY-MM-DD
    pretty = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a %b %d")
    marker = f"[liftosaur:{date_str}]"  # idempotency marker, kept on header line

    header = f"**{pretty} — {session.get('program_day','')}**  <!--{marker}-->"
    body_lines = []
    for s in session["sets"]:
        reps = ", ".join(str(r) for r in s.get("reps", []))
        rpe = "/".join(str(x) for x in s.get("rpe", [])) if s.get("rpe") else ""
        suffix = f" @ RPE {rpe}" if rpe else ""
        body_lines.append(f"- {s['lift']} {s.get('weight','')} — {reps}{suffix}")
    entry = "\n".join([header, *body_lines]) + "\n"

    current, sha = _fetch_file_path(WORKOUT_LOG_PATH)
    if _already_logged(current, date_str, marker):
        return {"status": "skipped (already logged)", "date": date_str}
    sep = "\n" if current.endswith("\n") else "\n\n"
    _put_file_path(WORKOUT_LOG_PATH, current + sep + entry, sha,
                   f"Log Liftosaur session {date_str}")
    return {"status": "logged", "date": date_str, "sets": len(session["sets"])}


def log_fitness_summary(date_str: str, weight_lb: float | None, steps: int | None,
                        trained: bool) -> dict:
    """Append a one-line fitness summary to daily-log.md for date_str, idempotently."""
    marker = f"[fitness:{date_str}]"
    pretty = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d (%a)")
    parts = [f"**{pretty}** — Fitness <!--{marker}-->"]
    if trained:
        parts.append("Trained: yes")
    if weight_lb is not None:
        parts.append(f"Weight: {weight_lb} lb")
    if steps is not None:
        flag = "✓" if steps >= 10000 else "✗"
        parts.append(f"Steps: {steps:,} {flag}")
    entry = "  |  ".join(parts) + "\n"

    current, sha = _fetch_file_path(DAILY_LOG_PATH)
    if _already_logged(current, date_str, "[fitness:"):
        return {"status": "skipped (already logged)", "date": date_str}
    sep = "\n" if current.endswith("\n") else "\n\n"
    _put_file_path(DAILY_LOG_PATH, current + sep + entry, sha,
                   f"Log fitness summary {date_str}")
    return {"status": "logged", "date": date_str}


# health_logger.py hardcodes its FILE_PATH into _fetch_file/_put_file. To reuse
# the plumbing across two target files, generalize those two helpers to take a
# path arg (small refactor), OR copy the 15-line fetch/put pair here. Stubbed:
def _fetch_file_path(path: str) -> tuple[str, str]:
    raise NotImplementedError("Generalize health_logger._fetch_file to take a path.")


def _put_file_path(path: str, content: str, sha: str, message: str) -> None:
    raise NotImplementedError("Generalize health_logger._put_file to take a path.")


def fitness_archive(request=None):
    """Cloud Function entry point — pull the drop folder, log new fitness data.

    Schedule ~8:30pm AZ (before 9pm evening_archive) or merge into evening_archive.
    WIRING: read drop folder (Q4) -> parse_* -> log_workout_session / log_fitness_summary.
    """
    raise NotImplementedError("Resolve Q1-Q5 with Will, then wire the drop reader.")
