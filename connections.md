# Connections

Tracks what external data sources are wired to the AIOS and what's pending.

## Status

| Domain | Tier | Source | Status | Notes |
|--------|------|--------|--------|-------|
| Calendar | 1 | Google Calendar | **Configured** | MCP: `@gongrzhe/server-gcalendar-mcp`. Needs OAuth credentials in `.env` to activate. |
| Comms / Email | 1 | Gmail (full read) | **Configured** | MCP: `@gongrzhe/server-gmail-autoauth-mcp`. Full read access (not read-only). Needs OAuth credentials in `.env` to activate. |
| Web fetch / Listings | 1 | Playwright | **Configured** | MCP: `@playwright/mcp`. Used by `/deal-eval` for URL-based listing fetch. Needs `npx playwright install` to download browsers. |
| Tasks | 1 | — | Not wired | Will doesn't currently use a task manager |
| Meetings | 1 | — | Not wired | No meeting transcription set up |
| Knowledge | 1 | Local files | Wired | AIOS has access to all local context files |
| Revenue / Money | 1 | Acquisition project | **Wired** | context/acquisition.md + journals/acquisition-log.md + /acquisition skill |
| Relationships / CRM | 1 | — | Not wired | Deferred — build after 2 weeks of acquisition project running |

## MCP Activation Steps (Gmail + Calendar)

MCPs are configured in `.claude/settings.json`. To activate:

1. Go to [Google Cloud Console](https://console.cloud.google.com) → create a project
2. Enable Gmail API + Google Calendar API
3. Create OAuth 2.0 credentials (Desktop app type) → download `credentials.json`
4. Add path to `.env`: `GMAIL_CREDENTIALS_PATH=/path/to/credentials.json`
5. Run `claude` — the MCP will trigger OAuth consent flow on first use (browser-based, one-time)
6. Token is saved and refreshed automatically

For Playwright: run `npx playwright install` to download browser binaries. No auth needed.

---

## How to Add a Connection

1. Identify the tool and check if it has an MCP server or REST API.
2. **Prefer API endpoints over MCP** — more token-efficient, more control.
3. Ask Claude to research the API documentation and save it as `references/<tool>-api.md`.
4. Create a `.env` entry for the API key (never commit the key to git).
5. Update this file with the new status.
6. Test with a simple read operation before building anything on top of it.

## Priority Order for Wiring

1. **Google Calendar** — daily planning (EA mode), weekly reflection (past week review)
2. **Gmail** (read-only, work account) — escalation monitoring, SCM II behavior tracking
3. **TBD** — once side business is active, add relevant tool
