# Connections

Tracks what external data sources are wired to the AIOS and what's pending.

## Status

| Domain | Tier | Source | Status | Notes |
|--------|------|--------|--------|-------|
| Calendar | 1 | Google Calendar | Wiring in progress | MCP `@cocal/google-calendar-mcp` registered in `.mcp.json`; awaiting first-run OAuth. See `references/google-calendar-api.md` |
| Comms / Email | 1 | Gmail (work read-only) | Not wired | Priority 2 — escalation monitoring |
| Tasks | 1 | — | Not wired | Will doesn't currently use a task manager |
| Meetings | 1 | — | Not wired | No meeting transcription set up |
| Knowledge | 1 | Local files | Partial | AIOS has access to local context files |
| Revenue / Money | 1 | — | Not wired | Side business not yet active |
| Relationships / CRM | 1 | — | Not wired | Not needed yet |

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
