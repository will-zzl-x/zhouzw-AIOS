---
name: level-up
description: 5-question interview to surface the highest-ROI AIOS improvements. Run when you want to know what to automate or build next. Triggered by "level up", "what should I automate next", "/level-up".
---

## Goal

Identify 3–5 specific improvements to the AIOS with the highest ROI — things that, once built, would save the most time or create the most leverage in Will's actual daily work.

## Reads

- `state.md` — current life priorities
- `context/priorities.md` — what matters this quarter
- `CLAUDE.md` — what skills already exist
- `context/work-state.md` — what Will's work looks like day-to-day

## Steps

### Phase 1 — Load Context (silent)
Read the files above. Note what's already automated and what domains are covered.

### Phase 2 — 5-Question Interview
Ask each question one at a time and wait for the answer.

**Q1 — Drudgery:**
"What's something you did 3+ times this week that you hated doing?"

**Q2 — Forgetting:**
"What do you keep forgetting to do, or what keeps falling through the cracks?"

**Q3 — Wish list:**
"What do you wish the AIOS already knew or could do that it can't right now?"

**Q4 — Smart intern test:**
"Is there anything where you thought 'a smart intern could handle this' but you ended up doing it yourself because explaining would take longer?"

**Q5 — Growth lever:**
"If one thing in your life ran on autopilot starting tomorrow, what would have the biggest impact?"

### Phase 3 — Synthesize
Based on Will's answers + current AIOS state, identify:
- Which answers point to a missing skill
- Which answers point to a missing connection (external data source)
- Which answers point to a missing cadence (something that should run on schedule)

### Phase 4 — Output

Return a ranked list:
```
# AIOS Level-Up Opportunities — [Date]

**Ranked by ROI:**

1. [Specific improvement] — [Why it has high leverage] — [Whether it's a skill, connection, or cadence]
2. [Specific improvement] — ...
3. [Specific improvement] — ...
(up to 5)

**Recommended next build:** [Single most actionable item — what to build first and why]
```

## Rules

- Be specific. "Build a habit tracker" is not useful. "Build a morning coffee skill that reads state.md and dashboard.md and returns the day's single most important action" is.
- Only recommend things that are buildable given current connections. Don't recommend things that require external APIs that aren't set up, unless wiring that API is itself the recommendation.
- If Will has available time right now, offer to run `/skill-builder` immediately on the top pick.
