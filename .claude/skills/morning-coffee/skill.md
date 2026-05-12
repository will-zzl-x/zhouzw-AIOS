---
name: morning-coffee
description: Morning Coffee — daily planning ritual. Reads state.md and dashboard.md, then outputs today's single priority and a loose time block plan for the day. Run each morning as a grounding ritual before diving in. Triggered by "morning coffee", "plan my day", "what's my day look like", or "/morning-coffee".
---

## Goal

Start the day with a grounding plan: one priority, one time block layout. Not a to-do list — a structure that makes it easy to start and hard to drift.

**Relationship to Todoist brief:** Will's 3–5 daily tasks already land in Todoist at 7am AZ via the morning-brief Cloud Function. This skill is for *deeper* planning when Will wants it — picking the one priority, structuring time blocks. Don't duplicate the Todoist task list verbatim; reference it.

## Reads

- `state.md` — live context: what phase, what's active, any travel or constraints
- `dashboard.md` — current week's movers by life area
- `context/priorities.md` — weekday vs. weekend routing rules
- `context/daily-standard.md` — today's required targets (what "done" looks like)
- **Google Calendar MCP** (if wired) — today's events and any time-blocking constraints

## Steps

1. Read `state.md` and `dashboard.md`.
2. **If Google Calendar MCP is wired:** fetch today's events. Note any meetings, appointments, or pre-committed blocks that constrain the day.
3. Check: weekday or weekend? Apply routing rules (weekday: career fair game; weekend: fitness, relationships, side income only — not Amazon work).
4. Check for any hard constraints today: travel, appointments, vacation, unusual schedule (from state.md and calendar).
5. Identify the single most important thing to move today — the one mover from dashboard that has the most leverage given the current context.
6. Build a loose time block structure. Do not schedule every minute. Leave air. Blocks should reflect what Will actually has to work with, not an idealized day. Work around any calendar commitments.
7. Read `context/daily-standard.md` and pull today's required targets for the current phase.
8. Output format:

```
**[Day, Date] — [Phase]**

**Priority:** [The one thing — specific and startable]

**Rough blocks:**
Morning   [time range] — [what]
Midday    [time range] — [what or "free / flexible"]
Afternoon [time range] — [what]
Evening   [time range] — [what]

**Calendar:** [list today's events if Calendar MCP is wired, or omit if not]

**Today's targets:**
□ [Target 1 from daily-standard]
□ [Target 2]
□ [Target 3]

**Flag:** [Only if there's something time-sensitive from state.md that needs attention today — otherwise omit]
```

## Rules

- One priority only. Never two.
- Time blocks are rough — not commitments, not a schedule. They're a default structure.
- If Will is on vacation or traveling, apply the weekend rule and adjust the blocks accordingly.
- Don't repeat what's already in state.md back at him verbatim. Synthesize.
- If `state.md` or `dashboard.md` are stale (>7 days), flag it first.
- No affirmations. No "great day ahead." Just the plan.
