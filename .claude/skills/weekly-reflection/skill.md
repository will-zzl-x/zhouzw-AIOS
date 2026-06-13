---
name: weekly-reflection
description: Sunday weekly reflection — guided review of all life areas, updates state.md, regenerates dashboard.md, clears inbox, commits repo. Triggered by "weekly reflection", "sunday chat", or "weekly chat".
---

## Goal

Run a complete weekly synthesis: surface what happened, what shifted, and what matters next week. Update all live files. Leave the AIOS current.

## Reads

- `journals/inbox.md` — mid-week captures
- `journals/daily-log.md` — this week's daily completions (auto-archived from Todoist nightly)
- `archives/` — last reflection file (for continuity)
- `context/priorities.md` — current quarter priorities
- `context/relationships.md` — relationship context
- `context/work-state.md` — career context
- `context/financial-state.md` — money context
- `references/integrated-coach.md` — coaching voice
- `state.md` and `dashboard.md` — current state
- **Todoist MCP** (optional) — this week's completed tasks if richer detail than daily-log is needed

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

### Phase 2B — Weekly Quest Check (Abdaal)

After the area interview, run the three Abdaal weekly-review questions explicitly against each Main Quest. This is what separates people who set quests from people who complete them (`references/abdaal.md` L57–62).

Read current Main Quests from `state.md` first. Then ask each question against each Main Quest, in turn.

**For each Main Quest (work + life):**

1. **On-track check:** "Are you on track for the win condition? If the quest's 90-day deadline is X, what's the projected completion at current pace?"
2. **Single most important thing this week:** "What's the ONE thing this week that, if done, moves this quest the furthest?"
3. **Removal:** "What got in the way last week, and how do you remove it this week?"

Format the synthesis as:

```
Weekly Quest Check — [Date]

Work Main: [quest name]
  - On track: [yes/at risk/off] — [one sentence why]
  - This week's #1: [specific action]
  - Removing: [specific blocker + how to clear it]

Life Main: [quest name]
  - On track: [yes/at risk/off] — [one sentence why]
  - This week's #1: [specific action]
  - Removing: [specific blocker + how to clear it]
```

**If either Main Quest is "at risk" or "off":** the weekly reflection's carry-forward MUST reference the recovery move. Don't paper over a drifting Main Quest with side quest progress.

### Phase 3 — Synthesize
Based on Will's answers + the context files, identify:
- What changed this week vs. last (state drift)
- **Completion rates per area** from `journals/daily-log.md` — count ✓ vs □ per area across the week. Surface any area with <50% completion as a flag.
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

3. Regenerate `dashboard.md`: Daily Consistents section + Major Moves This Week section pulling top of newly-regenerated backlog.md (rows where status != done AND eligibility filter passes today).

4. Regenerate `backlog.md`:
   - Read current backlog.md (preserve existing open/in-progress/blocked/parked entries — do NOT regenerate from scratch)
   - Move all rows with status=='done' to archives/backlog-done.md, append a 'Completed' column with current ISO date
   - Process the '## Inbox (unranked)' section: convert each captured item into a ranked row in the main table. For each new row, set: next available rank, status=open, gate based on context, **and tag the Quest column** (`work-main` / `life-main` / `side` / `not-quest`) per the current Main Quests in state.md. New items default to `side` unless they clearly serve a Main Quest.
   - Re-rank the table: row order = priority. Items with hard deadlines get priority bumps if deadlines tightened. Within the same rank tier, `work-main` and `life-main` items beat `side` and `not-quest`.
   - Update the 'Last sorted: YYYY-MM-DD' header timestamp
   - Clear the Inbox section back to the empty stub comment
   - Skill should NEVER auto-drop entries — only Will retires items, by editing backlog.md by hand or marking status:done / status:parked. The reflection PROPOSES candidates for retirement or parking (entries with no movement in 4+ weeks) but doesn't apply automatically.

5. Clear `journals/inbox.md` — replace content with empty stub:
   ```
   # Inbox
   <!-- Mid-week captures go here. Cleared each Sunday. -->
   ```

6. Commit the repo with message: `weekly reflection YYYY-MM-DD`

## Rules

- Don't skip the interview phase — synthesis without input is fiction.
- Don't ask all questions at once — go one life area at a time.
- Dashboard movers must be specific and startable, not vague.
- If state.md hasn't been updated since last reflection, note the drift explicitly.
- Don't fabricate coach observations — only surface what genuinely fits.
