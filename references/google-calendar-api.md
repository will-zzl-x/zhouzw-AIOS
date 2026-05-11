# Google Calendar API Connection

## Status

Wired via MCP server `@cocal/google-calendar-mcp` (project-scoped in `.mcp.json`). OAuth flow needs to be completed once before tools work.

## Configuration

- **MCP server:** `@cocal/google-calendar-mcp` (npx, auto-installed)
- **Credentials file:** `/root/.config/aios/google-credentials.json` (chmod 600, NEVER commit)
- **OAuth client type:** Desktop app
- **Google Cloud project:** `ai-os-496000`
- **Calendar API:** enabled

## First-Time Auth

1. Restart Claude Code so it picks up the new `.mcp.json`.
2. Ask Claude: "authenticate with Google Calendar."
3. Browser opens → log in with the Google account whose calendar you want → grant scopes.
4. Token is written next to the credentials file (handled by the MCP server).
5. After that, MCP tools (`list_events`, `create_event`, etc.) work without prompts.

## Gotchas

- **Test-mode OAuth tokens expire every 7 days.** To get a stable token: in Google Cloud Console → OAuth consent screen → set publishing status to **In production** (or accept the 7-day re-auth cadence).
- Must add your Google address as a Test User if staying in Testing mode.
- Credentials file path is absolute in `.mcp.json` — moving it breaks the wiring.

## If It Breaks

- Re-run auth: ask Claude to authenticate again; the MCP server will re-trigger the browser flow.
- Token corrupted: delete the token file next to `google-credentials.json` and re-auth.
- Rotate client secret: regenerate in Google Cloud Console → Credentials, overwrite `google-credentials.json`, re-auth.
