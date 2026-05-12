"""Todoist REST API v2 client."""

import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

API_BASE = "https://api.todoist.com/rest/v2"
PROJECT_NAME = "AIOS Daily"
TZ = ZoneInfo("America/Phoenix")


def _headers() -> dict:
    return {"Authorization": f"Bearer {os.environ['TODOIST_API_KEY']}"}


def _get(path: str) -> list | dict:
    r = requests.get(f"{API_BASE}{path}", headers=_headers(), timeout=15)
    r.raise_for_status()
    return r.json()


def _post(path: str, body: dict) -> dict:
    r = requests.post(f"{API_BASE}{path}", headers=_headers(), json=body, timeout=15)
    r.raise_for_status()
    return r.json() if r.text else {}


def get_or_create_project() -> str:
    """Return the project ID for AIOS Daily, creating it if missing."""
    projects = _get("/projects")
    for p in projects:
        if p["name"] == PROJECT_NAME:
            return p["id"]
    created = _post("/projects", {"name": PROJECT_NAME})
    return created["id"]


def get_today_tasks(project_id: str) -> list[dict]:
    """All active (uncompleted) tasks in the project."""
    return _get(f"/tasks?project_id={project_id}")


def get_completed_today(project_id: str) -> list[dict]:
    """Tasks completed today (Phoenix time)."""
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    url = (
        f"https://api.todoist.com/sync/v9/completed/get_all"
        f"?project_id={project_id}&since={today}T00:00:00Z"
    )
    r = requests.get(url, headers=_headers(), timeout=15)
    r.raise_for_status()
    return r.json().get("items", [])


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
