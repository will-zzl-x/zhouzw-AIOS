"""Todoist API v1 (unified) client."""

import os
import re
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
    """GET a paginated list endpoint, walking next_cursor until exhausted.

    Diagnostic (2026-07-19): get_completed_today() returned 0 tasks on every
    run for a week despite Will actively checking tasks off — but /tasks and
    /projects (also routed through this function) work correctly every day.
    Two live differences on the completed-items endpoint that /tasks and
    /projects don't have: (1) it may use a different response envelope key
    ('items' vs 'results') since it's the unified-API successor to the old
    Sync API's completed-items lookup, and (2) it's the only call that takes
    since/until params, so a silent format/interpretation mismatch there
    would also zero out results without erroring (which matches: every run
    shows conclusion:success, no exception, just an empty list). This logs
    the raw envelope + falls back to 'items' so a future occurrence of either
    is diagnosable from the Action log instead of requiring live API access,
    and self-heals if the envelope-key guess is right."""
    out: list = []
    cursor: str | None = None
    while True:
        p = dict(params or {})
        if cursor:
            p["cursor"] = cursor
        r = _request("GET", f"{API_BASE}{path}", params=p)
        data = r.json()
        items = data.get("results")
        if items is None:
            items = data.get("items", [])
        print(f"DEBUG _get_paginated {path}: keys={list(data.keys())} "
              f"params={p} returned={len(items)}")
        out.extend(items)
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
        # Explicit 'Z' suffix (2026-07-19 fix): bare timestamps aren't valid
        # RFC3339 and some APIs interpret a missing offset as local-server
        # time rather than UTC, silently shifting the window instead of
        # erroring — which would explain a clean 200 + empty results every
        # single day with no exception in the logs.
        "since": since.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "until": until.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return _get_paginated("/tasks/completed/by_completion_date", params)


def clear_active_tasks(project_id: str) -> int:
    """DELETE all currently-active tasks. Best-effort — partial failures
    don't abort the brief. Returns count successfully deleted.

    Why DELETE not close: closing completes the task, which makes it visible to
    get_completed_today() at 9pm. Evening archive would then see those auto-closed
    sm-tagged tasks and silently flip backlog.md status:done for movers Will
    never actually finished. DELETE removes the task entirely so only Will's real
    completions are archived."""
    tasks = get_today_tasks(project_id)
    deleted = 0
    for t in tasks:
        try:
            _request("DELETE", f"{API_BASE}/tasks/{t['id']}")
            deleted += 1
        except requests.exceptions.RequestException as e:
            print(f"WARN: failed to delete task {t['id']}: {e}")
    return deleted


def create_task(
    project_id: str,
    title: str,
    area: str,
    priority: int,
    sm_id: str | None = None,
    description: str | None = None,
) -> dict:
    """Create a task in the AIOS Daily project.

    The Todoist description field carries up to two things:
      - the strategic-mover tag 'sm:<id>' (so completions correlate back to
        backlog rows), and/or
      - the human-readable context (the full dashboard.md / daily-standard.md
        bullet for Daily Consistents and gates — e.g. the desire-polarity
        rotation menu, the Z2 scenario detail).

    Layout rule (load-bearing): when both are present, 'sm:<id>' MUST be on the
    FIRST line, followed by a blank line, then the context. extract_sm_id() and
    archiver.py read the tag with `^sm:(\\S+)`, which stops at the first
    whitespace/newline — so 'sm:<id>\\n\\n<context>' parses correctly and the
    human text is free-form below it.
    """
    desc = compose_description(sm_id, description)
    body = {
        "content": title,
        "project_id": project_id,
        "priority": 5 - priority,  # Todoist: 4=highest, our spec: 1=highest
        "labels": [area],
        "due_string": "today",
    }
    if desc:
        body["description"] = desc
    return _post("/tasks", body)


def compose_description(sm_id: str | None, description: str | None) -> str:
    """Build the Todoist description from the optional sm-tag + optional context.

    - both:         'sm:<id>\\n\\n<context>'  (tag on line 1, archiver-safe)
    - sm only:      'sm:<id>'
    - context only: '<context>'
    - neither:      ''
    """
    sm_part = f"sm:{sm_id}" if sm_id else ""
    ctx_part = (description or "").strip()
    if sm_part and ctx_part:
        return f"{sm_part}\n\n{ctx_part}"
    return sm_part or ctx_part


def extract_sm_id(task: dict) -> str | None:
    """Return the strategic-mover id embedded in a Todoist task description.

    Convention: strategic movers carry an exact 'sm:<id>' prefix in the task
    description. Returns the id portion if present, else None.
    """
    desc = task.get("description") or ""
    m = re.match(r"^sm:(\S+)", desc)
    return m.group(1) if m else None
