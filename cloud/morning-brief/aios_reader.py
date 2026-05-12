"""Fetch AIOS markdown files from GitHub raw URLs."""

import os
import requests

GITHUB_REPO = "will-zzl-x/zhouzw-aios"
GITHUB_BRANCH = os.environ.get("AIOS_BRANCH", "claude/build-coding-skills-K5mpd")
RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}"

FILES = {
    "priorities": "context/priorities.md",
    "state": "state.md",
    "daily_standard": "context/daily-standard.md",
    "dashboard": "dashboard.md",
}


def fetch_aios_context() -> dict[str, str]:
    """Fetch all AIOS context files. Returns dict keyed by short name."""
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}

    out = {}
    for key, path in FILES.items():
        url = f"{RAW_BASE}/{path}"
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        out[key] = r.text
    return out
