"""Shared GitHub Contents API helpers.

Single source of truth for GitHub writes from the morning-brief Cloud Function.
Both archiver.py (daily-log appends) and main.py (backlog reads / brief writes)
import fetch_file / put_file from this module so auth, encoding, and retry
behavior stay consistent across the function.

Owner / repo / branch / file_path are passed in by callers — nothing is
hardcoded here so consumers can target different paths (journals/daily-log.md,
backlog.md, etc.) and so the case-mismatch fix can be applied later by
adjusting the caller, not this module.
"""

import base64
import os
from urllib.parse import quote

import requests


def _headers() -> dict:
    return {
        "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    }


def _api_url(owner: str, repo: str, file_path: str) -> str:
    # Path-segment encode each segment so spaces / unicode survive,
    # but preserve the "/" separators between path segments.
    encoded_path = quote(file_path, safe="/")
    return f"https://api.github.com/repos/{owner}/{repo}/contents/{encoded_path}"


def fetch_file(
    owner: str,
    repo: str,
    file_path: str,
    branch: str = "master",
) -> tuple[str, str]:
    """Fetch a file from GitHub via the Contents API.

    Returns (file_content, sha). Raises on non-2xx.
    """
    url = _api_url(owner, repo, file_path)
    r = requests.get(f"{url}?ref={branch}", headers=_headers(), timeout=15)
    r.raise_for_status()
    payload = r.json()
    content = base64.b64decode(payload["content"]).decode()
    return content, payload["sha"]


def put_file(
    owner: str,
    repo: str,
    file_path: str,
    content: str,
    sha: str,
    message: str,
    branch: str = "master",
) -> dict:
    """PUT a file to GitHub with sha-based optimistic concurrency.

    Retries once on HTTP 409 (sha conflict) by re-fetching the current sha
    and retrying the PUT. Raises on any non-2xx after the retry.
    """
    url = _api_url(owner, repo, file_path)

    def _do_put(current_sha: str) -> requests.Response:
        body = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "sha": current_sha,
            "branch": branch,
        }
        return requests.put(url, headers=_headers(), json=body, timeout=15)

    r = _do_put(sha)
    if r.status_code == 409:
        # sha conflict — re-fetch and retry once
        _, fresh_sha = fetch_file(owner, repo, file_path, branch=branch)
        r = _do_put(fresh_sha)

    r.raise_for_status()
    return r.json()
