"""Entry points for morning brief and evening archive Cloud Functions.

Run locally:
    python main.py --dry-run            # generate brief, don't write
    python main.py morning              # generate + write to Todoist
    python main.py evening              # archive today's Todoist state to daily-log.md
    python main.py backfill SINCE UNTIL # read-only: print completed tasks in
                                         # an explicit date range (YYYY-MM-DD),
                                         # no writes. Recovery tool for the
                                         # 7/12-7/18 completed-items envelope bug.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from aios_reader import fetch_aios_context
from archiver import archive
from brief_generator import generate_brief
from todoist_client import (
    clear_active_tasks,
    create_task,
    get_completed_range,
    get_completed_today,
    get_or_create_project,
    get_today_tasks,
)


def _current_phase(state_md: str) -> str:
    """Best-effort phase extraction from state.md."""
    m = re.search(r"Phase:\s*\*\*([^*]+)\*\*", state_md)
    if m:
        return m.group(1).strip()
    m = re.search(r"Phase:\s*([^\n]+)", state_md)
    return m.group(1).strip() if m else "Phase"


def morning_brief(request=None):
    """HTTP-triggered Cloud Function: generate today's brief, write to Todoist."""
    aios = fetch_aios_context()
    tasks = generate_brief(aios)

    project_id = get_or_create_project()
    cleared = clear_active_tasks(project_id)
    created = [
        create_task(
            project_id,
            t["title"],
            t["area"],
            t["priority"],
            sm_id=t.get("sm_id"),
            description=t.get("description"),
        )
        for t in tasks
    ]

    return {
        "cleared": cleared,
        "created": len(created),
        "tasks": [t["title"] for t in tasks],
    }


def evening_archive(request=None):
    """HTTP-triggered Cloud Function: archive today's Todoist state to daily-log.md."""
    aios = fetch_aios_context()
    phase = _current_phase(aios["state"])
    project_id = get_or_create_project()

    active = get_today_tasks(project_id)
    completed = get_completed_today(project_id)
    archive(active, completed, phase=phase)

    return {"phase": phase, "active": len(active), "completed": len(completed)}


def backfill_report(since_str: str, until_str: str) -> dict:
    """Read-only: fetch + print Todoist completions in [since_str, until_str)
    (YYYY-MM-DD, Phoenix-local calendar days). Writes nothing — for manually
    reconciling a period where the archiver silently under-recorded."""
    tz = ZoneInfo("America/Phoenix")
    since_dt = datetime.strptime(since_str, "%Y-%m-%d").replace(tzinfo=tz)
    until_dt = datetime.strptime(until_str, "%Y-%m-%d").replace(tzinfo=tz)

    aios = fetch_aios_context()
    project_id = get_or_create_project()
    completed = get_completed_range(project_id, since_dt, until_dt)

    by_day: dict[str, list[str]] = {}
    for t in completed:
        completed_at = t.get("completed_at") or t.get("completedAt") or ""
        day = completed_at[:10] if completed_at else "unknown"
        by_day.setdefault(day, []).append(t.get("content", "(unknown)"))

    result = {"since": since_str, "until": until_str, "total": len(completed), "by_day": by_day}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def _dry_run() -> None:
    aios = fetch_aios_context()
    tasks = generate_brief(aios)
    print(json.dumps(tasks, indent=2))


if __name__ == "__main__":
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", choices=["morning", "evening", "backfill", "dry-run"], default="dry-run")
    parser.add_argument("range", nargs="*", help="backfill mode: SINCE UNTIL (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    mode = "dry-run" if args.dry_run else args.mode

    if mode == "morning":
        print(json.dumps(morning_brief(), indent=2))
    elif mode == "evening":
        print(json.dumps(evening_archive(), indent=2))
    elif mode == "backfill":
        if len(args.range) != 2:
            print("Usage: python main.py backfill YYYY-MM-DD YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
        backfill_report(args.range[0], args.range[1])
    else:
        _dry_run()
        sys.exit(0)
