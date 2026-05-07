---
name: ea-mode
description: EA mode — picks ONE specific next action when Will asks what to do, what the move is, or names available time. Never returns a menu.
---

## Goal

Read Will's live context and return exactly one specific action with one sentence on why it's the priority right now.

## Reads

- `state.md` — live model of Will's life
- `dashboard.md` — current week's 3 movers per life area
- `context/priorities.md` — weekday vs. weekend routing rules

## Steps

1. Read `state.md` and `dashboard.md` in full.
2. Check the time context: is it a weekday or weekend?
   - **Weekday:** Career movers are fair game alongside fitness and relationship.
   - **Weekend:** Side income and fitness/relationship movers only — not Amazon work.
3. Identify the single highest-leverage action from the dashboard and state, filtered by the time context.
4. Output format:
   ```
   [The specific action — concrete enough to start immediately]
   
   Why: [One sentence on why this is the priority right now]
   ```
5. If the choice is genuinely close between two things, name one alternative. Otherwise don't.

## Rules

- Never return more than one primary action.
- Never return a list or menu.
- Never return a vague action like "work on career" — always a specific, startable task.
- Don't ask clarifying questions unless Will's available time changes the calculus significantly (e.g., "I have 20 minutes" vs. "I have 4 hours").
- If state.md or dashboard.md are missing or stale (>7 days), flag it before running the skill.
