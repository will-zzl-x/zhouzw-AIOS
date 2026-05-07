---
name: morning-coffee
description: Morning Coffee — daily planning ritual. Reads state.md and dashboard.md, then outputs today's single priority and a loose time block plan for the day. Run each morning as a grounding ritual before diving in. Triggered by "morning coffee", "plan my day", "what's my day look like", or "/morning-coffee".
---

## Goal

Start the day with a grounding plan: one priority, one time block layout. Not a to-do list — a structure that makes it easy to start and hard to drift.

## Reads

- `state.md` — live context: what phase, what's active, any travel or constraints
- `dashboard.md` — current week's movers by life area
- `context/priorities.md` — weekday vs. weekend routing rules

## Steps

1. Read `state.md` and `dashboard.md`.
2. Check: weekday or weekend? Apply routing rules (weekday: career fair game; weekend: fitness, relationships, side income only — not Amazon work).
3. Check for any hard constraints today: travel, appointments, vacation, unusual schedule.
4. Identify the single most important thing to move today — the one mover from dashboard that has the most leverage given the current context.
5. Build a loose time block structure. Do not schedule every minute. Leave air. Blocks should reflect what Will actually has to work with, not an idealized day.
6. Output format:

```
**[Day, Date]**

**Priority:** [The one thing — specific and startable]

**Rough blocks:**
Morning   [time range] — [what]
Midday    [time range] — [what or "free / flexible"]
Afternoon [time range] — [what]
Evening   [time range] — [what]

**Flag:** [Only if there's something time-sensitive from state.md that needs attention today — otherwise omit]
```

## Rules

- One priority only. Never two.
- Time blocks are rough — not commitments, not a schedule. They're a default structure.
- If Will is on vacation or traveling, apply the weekend rule and adjust the blocks accordingly.
- Don't repeat what's already in state.md back at him verbatim. Synthesize.
- If `state.md` or `dashboard.md` are stale (>7 days), flag it first.
- No affirmations. No "great day ahead." Just the plan.
