"""Fetch AIOS markdown files from GitHub raw URLs or local disk (for dry-run)."""

import os
import requests

GITHUB_REPO = "will-zzl-x/zhouzw-aios"
GITHUB_BRANCH = os.environ.get("AIOS_BRANCH", "master")
RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}"

FILES = {
    "priorities": "context/priorities.md",
    "state": "state.md",
    "daily_standard": "context/daily-standard.md",
    "dashboard": "dashboard.md",
    "daily_log": "journals/daily-log.md",
    "backlog": "backlog.md",
}


def fetch_aios_context() -> dict[str, str]:
    """Fetch all AIOS context files. Returns dict keyed by short name.

    When AIOS_LOCAL_PATH is set, reads from local disk (for dry-run/dev).
    Otherwise fetches from GitHub raw URLs.
    """
    local_root = os.environ.get("AIOS_LOCAL_PATH")
    if local_root:
        return _fetch_local(local_root)
    return _fetch_github()


def _fetch_local(root: str) -> dict[str, str]:
    out = {}
    for key, path in FILES.items():
        full = os.path.join(root, path)
        with open(full, "r", encoding="utf-8") as f:
            out[key] = f.read()
    return out


def _fetch_github() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}

    out = {}
    for key, path in FILES.items():
        url = f"{RAW_BASE}/{path}"
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        out[key] = r.text
    return out
