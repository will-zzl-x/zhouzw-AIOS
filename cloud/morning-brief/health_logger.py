"""Append a daily health entry to journals/health-log.md via the GitHub API."""

import base64
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

REPO = "will-zzl-x/zhouzw-aios"
BRANCH = os.environ.get("AIOS_BRANCH", "master")
FILE_PATH = "journals/health-log.md"
TZ = ZoneInfo("America/Phoenix")
API_BASE = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"


def _headers() -> dict:
    return {
        "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    }


def _fetch_file() -> tuple[str, str]:
    r = requests.get(f"{API_BASE}?ref={BRANCH}", headers=_headers(), timeout=15)
    r.raise_for_status()
    payload = r.json()
    return base64.b64decode(payload["content"]).decode(), payload["sha"]


def _put_file(content: str, sha: str, message: str) -> None:
    r = requests.put(API_BASE, headers=_headers(), timeout=15, json={
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "sha": sha,
        "branch": BRANCH,
    })
    r.raise_for_status()


def log_health(steps: int, calories: int | None = None, protein_g: int | None = None) -> dict:
    now = datetime.now(TZ)
    date_str = now.strftime("%Y-%m-%d (%a)")

    steps_flag = "✓" if steps >= 10000 else "✗"
    cal_flag = "✓" if calories and calories >= 1820 else ("✗" if calories else "—")
    prot_flag = "✓" if protein_g and protein_g >= 150 else ("✗" if protein_g else "—")

    parts = [f"**{date_str}**"]
    parts.append(f"Steps: {steps:,} {steps_flag}")
    if calories:
        parts.append(f"Calories: {calories} {cal_flag}")
    if protein_g:
        parts.append(f"Protein: {protein_g}g {prot_flag}")

    entry = "  |  ".join(parts)

    current, sha = _fetch_file()
    separator = "\n" if current.endswith("\n") else "\n\n"
    _put_file(current + separator + entry + "\n",
              sha,
              f"Log health data for {now.strftime('%Y-%m-%d')}")

    return {"date": date_str, "steps": steps, "calories": calories, "protein_g": protein_g}
