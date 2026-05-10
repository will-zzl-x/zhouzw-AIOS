---
name: daily-check
description: Daily Check — know what today's major moves are, log completions, and get a clear "done" or "X left" at any point in the day. The execution layer between the weekly dashboard and the moment-to-moment EA mode. Triggered by "daily check", "am I done", "what do I need to do today", "log done [thing]", or "/daily-check".
---

## Goal

Three modes:
1. **Today** — show today's required targets (derived from current phase + day type). Run this in the morning.
2. **Log** — mark a target complete. Lightweight. One line.
3. **Done?** — check current completion status and answer: done, or X left.

This is the layer that closes the loop between "I have goals" and "I know I moved today."

## Reads

- `context/daily-standard.md` — what "done" means in the current phase
- `state.md` — current phase, training schedule, active constraints
- `journals/daily-log.md` — what's been logged today
- **Google Calendar MCP** (if wired, Today mode only) — today's commitments that might affect timing

## Writes

- `journals/daily-log.md` — logs completions

---

## Steps — Today Mode

Triggered by: "what do I need to do today", "daily check", "morning check", "/daily-check"

1. Read `state.md` to determine:
   - Current phase (vacation / maintenance / NYC Cut)
   - Day type (weekday / weekend / travel / rest)
   - Any today-specific context (meetings, unusual schedule, travel day)

2. **If Google Calendar MCP is wired:** fetch today's events. Note any meetings or commitments that affect the day's capacity.

3. Read `context/daily-standard.md` and pull today's required targets.

4. Read `journals/daily-log.md` — check if anything has already been logged for today.

5. Output:

```
**[Day, Date] — [Phase]**

Today's targets:
□ [Target 1]
□ [Target 2]
□ [Target 3]
[□ Target 4 if applicable]

[✓ Already logged: [thing] — if applicable]

Done threshold: [X]/[Y] to call it a solid day.

[Calendar: [events if wired, or omit entirely if not]]
```

Keep it short. This is a glance, not a report.

---

## Steps — Log Mode

Triggered by: "log done [thing]", "done with [thing]", "hit protein", "trained", "logged SCM behavior", etc.

1. Read `journals/daily-log.md`.
2. Parse what Will completed.
3. Append to today's entry in `journals/daily-log.md`:

```
---
**[Date]** — [Phase]
✓ [completed item] ([time or note if given])
```

If today already has an entry, append to it rather than creating a new one.

4. Confirm with a one-liner. If this completion hits the done threshold, say so:
   > "Logged. That's 2/3 — done threshold hit."
   > "Logged. 3/3 — complete day."

---

## Steps — Done? Mode

Triggered by: "am I done", "done for the day?", "what's left", "/daily-check done"

1. Read `state.md` and `context/daily-standard.md` for today's required targets.
2. Read `journals/daily-log.md` — count what's been logged today.
3. Output:

**If threshold met (2+ of required targets):**
```
Done. [X]/[Y] targets hit.
✓ [completed]
✓ [completed]
□ [not done — optional at this point]
```

**If threshold not met:**
```
Not yet. [X]/[Y] targets hit.
✓ [completed]
□ [remaining — most important one first]
□ [remaining]
```

No guilt, no padding. Just the status.

---

## Daily Log Format

`journals/daily-log.md` entries look like this:

```
---
**2026-05-08 (Fri)** — Vacation / Destin
✓ Arms & Shoulders BW session
✓ Protein ~150g
□ Elena time — beach walk (planned)
```

Running log — don't clear it. Weekly reflection uses it for synthesis.

---

## Integration with Other Skills

- `/morning-coffee` runs first and sets the day's priority and time blocks. **Daily check shows the targets** — these are two different things. Morning coffee is the plan. Daily check is the scorecard.
- `/ea-mode` picks the next specific action. If Will asks "what should I do?", ea-mode picks from within the remaining targets.
- `/health-os` and `/workout-log` log the actual detail. Daily check reads the outcome (done/not done) not the data.
- When Will logs something in `/workout-log` or `/health-os`, he can also say "log done training" or "log done protein" to hit the daily-check target simultaneously.

---

## Rules

- Required targets come from `context/daily-standard.md` — don't invent targets on the fly.
- Done threshold is 2/3 required targets on a normal day. On a rest/recovery day called explicitly, 1/3 is fine.
- If state.md or daily-standard.md don't match (e.g., phase hasn't been updated), use state.md as ground truth and note the mismatch.
- Never shame a missed day. State it, move on.
- If `journals/daily-log.md` doesn't exist, create it with a header and start the first entry.
- Don't ask for more detail than needed. "Hit protein" is enough — don't ask how many grams.
