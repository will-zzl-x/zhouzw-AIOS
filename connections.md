# Connections

Tracks what external data sources are wired to the AIOS and what's pending. Two layers depending on which laptop you're on — personal-laptop MCPs in `.claude/settings.json`, work-laptop MCPs configured at the user level.

## Status — Personal laptop

| Domain | Tier | Source | Status | Notes |
|--------|------|--------|--------|-------|
| Calendar | 1 | Google Calendar | **Configured** | MCP: `@gongrzhe/server-gcalendar-mcp`. Needs OAuth credentials in `.env` to activate. |
| Comms / Email | 1 | Gmail (full read) | **Configured** | MCP: `@gongrzhe/server-gmail-autoauth-mcp`. Full read access (not read-only). Needs OAuth credentials in `.env` to activate. |
| Web fetch / Listings | 1 | Playwright | **Configured** | MCP: `@playwright/mcp`. Used by `/deal-eval` for URL-based listing fetch. Needs `npx playwright install` to download browsers. |
| Tasks | 1 | Todoist | **Wired** | MCP: `@abhiz123/todoist-mcp-server`. Daily brief auto-generated 7am AZ by `cloud/morning-brief/`. Evening archive 9pm AZ writes completions to `journals/daily-log.md`. |
| Meetings | 1 | — | Not wired | No meeting transcription set up |
| Knowledge | 1 | Local files | Wired | AIOS has access to all local context files |
| Revenue / Money | 1 | Acquisition project | **Wired** | `context/acquisition.md` + `journals/acquisition-log.md` + `/acquisition` skill |
| Relationships / CRM | 1 | — | Not wired | Deferred — build after 2 weeks of acquisition project running |

## Status — Work laptop (`C:/Users/zhouzw/`)

| Domain | Tier | Source | Status | Notes |
|--------|------|--------|--------|-------|
| Calendar (work) | 1 | Outlook MCP (`aws-outlook-mcp`) | Live | Calendar + email via this server |
| Comms / Email (work) | 1 | Outlook MCP (`aws-outlook-mcp`) | Live | inbox, search, read, calendar — all wired |
| Comms / Slack (work) | 1 | `ai-community-slack-mcp` | Live | search, DMs, drafts, reactions |
| Internal docs / code | 1 | `builder-mcp` | Live | Quip, Sim, Taskei, code search, internal search |
| Data / Redshift | 1 | `andes-mcp`, `datanet-mcp` | Live | Andes datasets + Datanet jobs |
| Wiki | 1 | `xwiki-mcp` | Live | w.amazon.com pages |
| SharePoint | 1 | `amazon-sharepoint-mcp` | Live | Lists, files, libraries |
| Work-state truth layer | 1 | `C:/Users/zhouzw/ict_automation/` JSON snapshots | Live | Daily flash, ESS, WBR, SIM auditor, redirect budget. Read by `daily_sync.md`. |

## MCP Activation Steps (Personal laptop — Gmail + Calendar)

MCPs are configured in `.claude/settings.json`. To activate:

1. Go to [Google Cloud Console](https://console.cloud.google.com) → create a project
2. Enable Gmail API + Google Calendar API
3. Create OAuth 2.0 credentials (Desktop app type) → download `credentials.json`
4. Add path to `.env`: `GMAIL_CREDENTIALS_PATH=/path/to/credentials.json`
5. Run `claude` — the MCP will trigger OAuth consent flow on first use (browser-based, one-time)
6. Token is saved and refreshed automatically

For Playwright: run `npx playwright install` to download browser binaries. No auth needed.

## Bridge skills (work laptop)

When on `C:/Users/zhouzw/`, three skills under `~/.claude/steering/` bind this AIOS to live work data:

- `daily_sync.md` — `/daily-sync` — end-of-day catch-up; reads `ict_automation` JSON + Outlook + Slack + tickets, writes `journals/<date>.md`, proposes `state.md` diff. **Auto-fires Mon–Fri 6:43pm AZ** via `Claude_Daily_Sync` Windows scheduled task.
- `workstream_tracker.md` — `/refresh-workstreams` — refreshes `context/work-state.md` from inbox+slack across all active projects.
- `runner_panel.md` — `/runners` — read-only freshness board for `ict_automation` runners.

Use these instead of `/ea-mode` when on the work laptop and `state.md` may be stale.

---

## How to Add a Connection

1. Identify the tool and check if it has an MCP server or REST API.
2. **Prefer API endpoints over MCP** — more token-efficient, more control.
3. Ask Claude to research the API documentation and save it as `references/<tool>-api.md`.
4. Create a `.env` entry for the API key (never commit the key to git).
5. Update this file with the new status.
6. Test with a simple read operation before building anything on top of it.

## Priority Order for Wiring

1. **Google Calendar** (personal) — daily planning (EA mode), weekly reflection past-week review. Work calendar already covered via Outlook MCP.
2. **Gmail** (personal) — escalation monitoring, deal-alert ingestion for `/acquisition scan-inbox`. Work email already covered via Outlook MCP.
3. **TBD** — once side business is active, add relevant tool.
