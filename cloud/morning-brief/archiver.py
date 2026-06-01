"""Append completion log entries to journals/daily-log.md via the GitHub API.

Also flips backlog.md status:done for any completed tasks that carry an
'sm:<id>' tag in their Todoist description (strategic movers).
"""

import os
from datetime import datetime
from zoneinfo import ZoneInfo

from github_writer import fetch_file, put_file
from backlog import mark_done
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


def archive_completed_strategic_moves(completed_tasks: list[dict]) -> list[str]:
    """Flip backlog.md status to 'done' for each completed strategic mover.

    Pulls sm:<id> tags from Todoist task descriptions, accumulates flips into a
    single fetch/put cycle against backlog.md, and commits with a concise
    message. Returns the list of sm_ids flipped (empty if none)."""
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
        new_content = mark_done(new_content, sm_id, today_str)

    if new_content == current:
        return []

    put_file(
        OWNER,
        REPO_NAME,
        BACKLOG_PATH,
        new_content,
        sha,
        f"Archive strategic moves done: {', '.join(sm_ids)}",
        branch=BRANCH,
    )
    return sm_ids


def archive(active: list[dict], completed: list[dict], phase: str = "Phase") -> None:
    """Append today's entry to daily-log.md on GitHub, then flip any completed
    strategic-mover rows in backlog.md to status:done."""
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

    archive_completed_strategic_moves(completed)
