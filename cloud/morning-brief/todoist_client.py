"""Todoist API v1 (unified) client."""

import os
import time
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import requests

API_BASE = "https://api.todoist.com/api/v1"
PROJECT_NAME = "AIOS Daily"
TZ = ZoneInfo("America/Phoenix")

RETRY_STATUS = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 4
BACKOFF_SECONDS = (1, 3, 8, 20)


def _headers() -> dict:
    return {"Authorization": f"Bearer {os.environ['TODOIST_API_KEY']}"}


def _request(method: str, url: str, **kwargs) -> requests.Response:
    """HTTP request with retry-with-backoff on transient 5xx/429."""
    last_exc: Exception | None = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            r = requests.request(method, url, headers=_headers(), timeout=15, **kwargs)
            if r.status_code in RETRY_STATUS and attempt < MAX_ATTEMPTS - 1:
                time.sleep(BACKOFF_SECONDS[attempt])
                continue
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as e:
            last_exc = e
            if attempt < MAX_ATTEMPTS - 1:
                time.sleep(BACKOFF_SECONDS[attempt])
                continue
            raise
    if last_exc:
        raise last_exc
    raise RuntimeError("unreachable")


def _get_paginated(path: str, params: dict | None = None) -> list:
    """GET a paginated list endpoint, walking next_cursor until exhausted."""
    out: list = []
    cursor: str | None = None
    while True:
        p = dict(params or {})
        if cursor:
            p["cursor"] = cursor
        r = _request("GET", f"{API_BASE}{path}", params=p)
        data = r.json()
        out.extend(data.get("results", []))
        cursor = data.get("next_cursor")
        if not cursor:
            break
    return out


def _post(path: str, body: dict) -> dict:
    r = _request("POST", f"{API_BASE}{path}", json=body)
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
    """Tasks completed during the Phoenix calendar day.

    Todoist reads since/until as UTC, so we anchor on Phoenix midnight and
    convert to UTC — otherwise the naive-local window is shifted 7h and
    evening completions fall outside it (logged as pending, not done)."""
    now = datetime.now(TZ)
    start_local = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_local = start_local + timedelta(days=1)
    since = start_local.astimezone(timezone.utc)
    until = end_local.astimezone(timezone.utc)
    params = {
        "project_id": project_id,
        "since": since.strftime("%Y-%m-%dT%H:%M:%S"),
        "until": until.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    return _get_paginated("/tasks/completed/by_completion_date", params)


def clear_active_tasks(project_id: str) -> int:
    """Close (complete) all currently-active tasks. Best-effort — partial failures
    don't abort the brief. Returns count successfully closed."""
    tasks = get_today_tasks(project_id)
    closed = 0
    for t in tasks:
        try:
            _request("POST", f"{API_BASE}/tasks/{t['id']}/close")
            closed += 1
        except requests.exceptions.RequestException as e:
            print(f"WARN: failed to close task {t['id']}: {e}")
    return closed


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
