"""Todoist API v1 (unified) client."""

import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

API_BASE = "https://api.todoist.com/api/v1"
PROJECT_NAME = "AIOS Daily"
TZ = ZoneInfo("America/Phoenix")


def _headers() -> dict:
    return {"Authorization": f"Bearer {os.environ['TODOIST_API_KEY']}"}


def _get_paginated(path: str, params: dict | None = None) -> list:
    """GET a paginated list endpoint, walking next_cursor until exhausted."""
    out: list = []
    cursor: str | None = None
    while True:
        p = dict(params or {})
        if cursor:
            p["cursor"] = cursor
        r = requests.get(f"{API_BASE}{path}", headers=_headers(), params=p, timeout=15)
        r.raise_for_status()
        data = r.json()
        out.extend(data.get("results", []))
        cursor = data.get("next_cursor")
        if not cursor:
            break
    return out


def _post(path: str, body: dict) -> dict:
    r = requests.post(f"{API_BASE}{path}", headers=_headers(), json=body, timeout=15)
    r.raise_for_status()
    return r.json() if r.text else {}


def get_or_create_project() -> str:
    """Return the project ID for AIOS Daily, creating it if missing."""
    projects = _get_paginated("/projects")
    for p in projects:
        if p["name"] == PROJECT_NAME:
            return p["id"]
    created = _post("/projects", {"name": PROJECT_NAME})
    return created["id"]


def get_today_tasks(project_id: str) -> list[dict]:
    """All active (uncompleted) tasks in the project."""
    return _get_paginated("/tasks", {"project_id": project_id})


def get_completed_today(project_id: str) -> list[dict]:
    """Tasks completed today (Phoenix time)."""
    now = datetime.now(TZ)
    since = now.replace(hour=0, minute=0, second=0, microsecond=0)
    until = since + timedelta(days=1)
    params = {
        "project_id": project_id,
        "since": since.strftime("%Y-%m-%dT%H:%M:%S"),
        "until": until.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    return _get_paginated("/tasks/completed/by_completion_date", params)


def clear_active_tasks(project_id: str) -> int:
    """Close (complete) all currently-active tasks. Returns count closed."""
    tasks = get_today_tasks(project_id)
    for t in tasks:
        r = requests.post(
            f"{API_BASE}/tasks/{t['id']}/close",
            headers=_headers(),
            timeout=15,
        )
        r.raise_for_status()
    return len(tasks)


def create_task(project_id: str, title: str, area: str, priority: int) -> dict:
    """Create a task in the AIOS Daily project."""
    body = {
        "content": title,
        "project_id": project_id,
        "priority": 5 - priority,  # Todoist: 4=highest, our spec: 1=highest
        "labels": [area],
        "due_string": "today",
    }
    return _post("/tasks", body)
