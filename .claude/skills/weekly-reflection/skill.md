---
name: weekly-reflection
description: Sunday weekly reflection — guided review of all life areas, updates state.md, regenerates dashboard.md, clears inbox, commits repo. Triggered by "weekly reflection", "sunday chat", or "weekly chat".
---

## Goal

Run a complete weekly synthesis: surface what happened, what shifted, and what matters next week. Update all live files. Leave the AIOS current.

## Reads

- `journals/inbox.md` — mid-week captures
- `archives/` — last reflection file (for continuity)
- `context/priorities.md` — current quarter priorities
- `context/relationships.md` — relationship context
- `context/work-state.md` — career context
- `context/financial-state.md` — money context
- `references/integrated-coach.md` — coaching voice
- `state.md` and `dashboard.md` — current state

## Writes

- `archives/YYYY-MM-DD-reflection.md` — new reflection file
- `state.md` — updated live model
- `dashboard.md` — fresh weekly dashboard
- `journals/inbox.md` — cleared after synthesis

## Steps

### Phase 1 — Load Context (silent)
Read all files listed above. Note any stale or missing items.

### Phase 2 — Interview (ask Will)
Ask one question per life area. Don't ask all at once — go area by area and wait for Will's response before moving on.

**Career:**
"What happened at Amazon this week — any SCM II moments, or was it mostly tactical? Anything shifting on the side income front?"

**Fitness:**
"How did training go? Any sessions missed? Anything notable on nutrition, sleep, or the cut progress?"

**Relationships:**
"How are things with Elena this week — anything worth noting, anything you want to carry into next week?"

**Money:**
"Any movement on the side business front? Any new ideas, conversations, or leads?"

**Wedding:**
"Any wedding items that moved or need to move this week?"

**Inbox sweep:**
"Anything in the inbox that isn't captured above, or anything else that's been on your mind?"

### Phase 3 — Synthesize
Based on Will's answers + the context files, identify:
- What changed this week vs. last (state drift)
- What's the single most important carry-forward from this week
- Any flag worth surfacing from the coach perspective

### Phase 4 — Write Outputs

1. Write `archives/YYYY-MM-DD-reflection.md` with:
   - Date and week number
   - One paragraph per life area (what happened + what matters)
   - One "carry-forward" — the thing most worth remembering next week
   - Coach observation (from integrated-coach lens)

2. Update `state.md`:
   - Update each section with current reality
   - Note date updated

3. Regenerate `dashboard.md`:
   - 3 movers per life area for the coming week
   - 12–15 total items
   - Grounded in state.md + priorities.md

4. Clear `journals/inbox.md` — replace content with empty stub:
   ```
   # Inbox
   <!-- Mid-week captures go here. Cleared each Sunday. -->
   ```

5. Commit the repo with message: `weekly reflection YYYY-MM-DD`

## Rules

- Don't skip the interview phase — synthesis without input is fiction.
- Don't ask all questions at once — go one life area at a time.
- Dashboard movers must be specific and startable, not vague.
- If state.md hasn't been updated since last reflection, note the drift explicitly.
- Don't fabricate coach observations — only surface what genuinely fits.
