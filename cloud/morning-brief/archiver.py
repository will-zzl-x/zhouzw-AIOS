"""Append completion log entries to journals/daily-log.md via the GitHub API.

Also stamps a dated "worked" flag on backlog.md rows for any completed tasks
carrying an 'sm:<id>' tag in their Todoist description (strategic movers).
It deliberately does NOT change row Status — see flag_worked() in backlog.py.
"""

import os
from datetime import datetime
from zoneinfo import ZoneInfo

from github_writer import fetch_file, put_file
from backlog import flag_worked
from todoist_client import extract_sm_id

REPO = "will-zzl-x/zhouzw-aios"
OWNER, REPO_NAME = REPO.split("/", 1)
BRANCH = os.environ.get("AIOS_BRANCH", "master")
FILE_PATH = "journals/daily-log.md"
BACKLOG_PATH = "backlog.md"
TZ = ZoneInfo("America/Phoenix")


def _format_entry(active: list[dict], completed: list[dict], phase: str) -> str:
    """Format a daily-log entry. active = uncompleted today; completed = closed today."""
    now = datetime.now(TZ)
    header = f"**{now.strftime('%Y-%m-%d (%a)')}** — {phase}"
    lines = [header]

    for t in completed:
        title = t.get("content", "(unknown)")
        lines.append(f"✓ {title}")
    for t in active:
        title = t.get("content", "(unknown)")
        lines.append(f"□ {title}")

    return "\n".join(lines) + "\n"


def flag_worked_strategic_moves(completed_tasks: list[dict]) -> list[str]:
    """Stamp a dated "worked" flag on each completed strategic mover's row.

    Pulls sm:<id> tags from Todoist task descriptions, accumulates the stamps
    into a single fetch/put cycle against backlog.md, and commits with a
    concise message. Returns the list of sm_ids flagged (empty if none).

    Status is intentionally left alone: completing a daily task means one
    day's slice of the move happened, not that the move is finished. The
    Sunday reflection decides status. See backlog.flag_worked()."""
    sm_ids: list[str] = []
    for t in completed_tasks:
        sm_id = extract_sm_id(t)
        if sm_id:
            sm_ids.append(sm_id)

    if not sm_ids:
        return []

    current, sha = fetch_file(OWNER, REPO_NAME, BACKLOG_PATH, branch=BRANCH)
    today_str = datetime.now(TZ).strftime("%Y-%m-%d")
    new_content = current
    for sm_id in sm_ids:
        new_content = flag_worked(new_content, sm_id, today_str)

    if new_content == current:
        return []

    put_file(
        OWNER,
        REPO_NAME,
        BACKLOG_PATH,
        new_content,
        sha,
        f"Flag strategic moves worked: {', '.join(sm_ids)}",
        branch=BRANCH,
    )
    return sm_ids


def archive(active: list[dict], completed: list[dict], phase: str = "Phase") -> None:
    """Append today's entry to daily-log.md on GitHub, then stamp a dated
    "worked" flag on any completed strategic-mover rows in backlog.md."""
    current, sha = fetch_file(OWNER, REPO_NAME, FILE_PATH, branch=BRANCH)
    entry = _format_entry(active, completed, phase)

    if current.endswith("\n"):
        new_content = current + "\n" + entry
    else:
        new_content = current + "\n\n" + entry

    today_str = datetime.now(TZ).strftime("%Y-%m-%d")
    put_file(
        OWNER,
        REPO_NAME,
        FILE_PATH,
        new_content,
        sha,
        f"Archive daily-log entry for {today_str}",
        branch=BRANCH,
    )

    flag_worked_strategic_moves(completed)
