---
name: relationship-os
description: Relationship OS — monthly relationship reviews, standing social event tracking, birthday/touch point system, and Elena's cycle tracker (calibrates the morning brief's Differentiation Cue rotation). Keeps the relationship side of life from drifting under workload. Triggered by "relationship review", "log a touch point", "birthday", "standing events", "log cycle", "period started", or "/relationship-os".
---

## Goal

Four modes:
1. **Monthly review** — structured check-in on the state of Will's key relationships.
2. **Touch point log** — capture a meaningful moment with Elena, family, or a friend.
3. **Event check** — surface upcoming birthdays, standing events, or relationship movers due this week.
4. **Cycle log** — update Elena's cycle tracker anchor date (feeds the morning brief's cycle-aware Differentiation Cue selection).

## Reads

- `context/relationships.md` — current relationship context and coaching notes
- `journals/relationship-log.md` — touch point log and review history
- `state.md` — active relationship movers and current life context

## Writes

- `journals/relationship-log.md` — appends logs and reviews

## Standing Events (update when Will sets them)

Track recurring commitments here. Add as they're established:
- Date night with Elena: [frequency TBD]
- Social standing events: [TBD — flag friendship gap]
- Annual: Will's birthday May 8, Elena's birthday [TBD]

## Steps — Monthly Review

Triggered by: "relationship review", "monthly check-in", "/relationship-os review"

1. Read `context/relationships.md`, `journals/relationship-log.md`, `state.md`.
2. Ask Will four questions (can answer all at once):
   - "How are things with Elena right now — presence, connection, intimacy?"
   - "Have you done anything intentional with her in the last month beyond logistics?"
   - "Friends: any meaningful contact in the last month? Who specifically?"
   - "Family: anything worth noting — mom, brother?"
3. Synthesize responses. Write to `journals/relationship-log.md`:
   ```
   ---
   ## Relationship Review — [Month, Year]

   **Elena:** [state of things — 2–3 sentences]
   **Friendships:** [honest assessment — who was contacted, gap if any]
   **Family:** [brief]
   **One thing to do this month:** [specific, not vague]
   ```
4. If the friendship gap hasn't been addressed in 60+ days, flag it.
5. Confirm written.

## Steps — Touch Point Log

Triggered by: "log a touch point", "had a good moment with Elena", "talked to [person]"

1. Append to `journals/relationship-log.md`:
   ```
   ---
   **[Date]** TOUCH POINT — [Elena / Mom / [friend name]]
   [What happened — 1 sentence]
   ```
2. Confirm: "Logged."

## Steps — Event Check

Triggered by: "relationship check", "what's coming up for relationships", "/relationship-os check"

1. Read `journals/relationship-log.md` and `state.md`.
2. Output:
   ```
   **Relationship check — [Date]**

   Standing events this week: [list or "none scheduled"]
   Upcoming birthdays (next 30 days): [list or "none"]
   Last date night: [date or "not logged"]
   Last friend contact: [who + when or "not logged"]
   Last monthly review: [date or "not done"]

   Due: [anything that's overdue or hasn't happened in too long]
   ```

## Steps — Cycle Log

Triggered by: "log cycle", "period started", "log period start [date]", "/relationship-os log cycle <date>"

1. Read `context/relationships.md`'s "Elena's Cycle" section.
2. Update `**Last period start:**` to the confirmed date (default to today if no date given). Drop the seeded-estimate parenthetical once a real date is logged.
3. If Will mentions cycle length varied from the tracked default, update `**Typical cycle length:**` too.
4. Confirm written: "Cycle anchor updated to [date]. Morning brief's Differentiation Cue rotation will recalculate phase from here."

This is Will's own behavior-calibration input — never framed as tracking Elena for any purpose beyond which of *Will's own* differentiation cues fits the week.

## Rules

- Don't editorialize on Elena's behavior or internal state — Will coaches with respect to Elena as his partner.
- Friendship gap is a known issue. Surface it if it's been >30 days without logged contact.
- If `journals/relationship-log.md` doesn't exist, create it with a header.
- Monthly review should feel like a brief honest check-in, not therapy. 10 minutes max.
- Standing events should be locked into calendar, not just tracked here — flag it if they're not.
