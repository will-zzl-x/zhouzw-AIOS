---
name: health-os
description: Health OS — log and review the non-exercise pillars of your health system: sleep and diet/nutrition. Exercise is handled by /workout-log. Triggered by "log sleep", "log meals", "health check", "health os", or "/health-os".
---

## Goal

Three modes:
1. **Sleep log** — capture last night's sleep.
2. **Diet log** — capture today's nutrition (protein target, rough meals).
3. **Health check** — surface how sleep and diet are trending this week vs. targets.

Exercise tracking lives in `/workout-log`. This skill handles the other two pillars.

## Reads

- `journals/health-log.md` — running sleep and diet log
- `state.md` — current phase (maintenance vs. cut), protein target, any active constraints

## Writes

- `journals/health-log.md` — appends new entries

## Targets (from state.md — update if they change)

**Sleep:**
- Target: 8 hours
- Bedtime: flexible, but consistent window preferred
- Room temp target: ~68°F / 19°C
- No phone in bed
- Morning sunlight within 30 min of waking

**Diet:**
- Protein: **150g/day** (hard target)
- Calories: phase-dependent — maintenance until May 16, NYC Cut starts May 17
- NYC Cut target: deficit to reach 172 lb / 12.5% BF by Jul 4

## Steps — Sleep Log

Triggered by: "log sleep", "slept X hours", "sleep last night was..."

1. Read `journals/health-log.md`.
2. Parse: hours slept, rough bedtime/wake time, quality if mentioned (1–5 or word), any notes (woke up, vivid dreams, Whoop score if shared).
3. Append to `journals/health-log.md`:
   ```
   ---
   **[Date]** SLEEP
   Hours: [X] | Bed: [time] → Wake: [time] | Quality: [score or note]
   Notes: [any context — if none, omit]
   ```
4. Confirm. If <6 hours, flag it plainly: "Short night. Worth watching if it stacks."

## Steps — Diet Log

Triggered by: "log meals", "protein today was X", "ate...", tracking nutrition

1. Read `journals/health-log.md`.
2. Parse what Will shared: protein estimate, calories if known, rough meals, anything notable.
3. Append to `journals/health-log.md`:
   ```
   ---
   **[Date]** DIET
   Protein: [X]g / 150g target | Calories: [X or "not tracked"]
   Meals: [brief summary]
   Notes: [any context — if none, omit]
   ```
4. Confirm. If protein is meaningfully short of 150g, note the gap plainly.

## Steps — Health Check

Triggered by: "/health-os check", "health check", "how's my health this week"

1. Read `journals/health-log.md` in full.
2. Read `state.md` for current phase and active targets.
3. Output:
   ```
   ## Health OS Check — [Date]

   **Sleep (last 7 days):**
   - Avg hours: [X]
   - Nights under 7h: [count]
   - Trend: [improving / flat / degrading]

   **Diet (last 7 days):**
   - Days hitting 150g protein: [X/7]
   - Avg protein: [X]g
   - Current phase: [Maintenance / NYC Cut] — [any relevant note]

   **Flags:** [Anything that needs attention — otherwise omit]
   ```

## Rules

- Don't give advice unless asked. Log and surface data.
- If `journals/health-log.md` doesn't exist, create it with a header before logging.
- Protein target is the primary diet metric — don't get lost in calories unless Will is in the NYC Cut phase, where both matter.
- Keep it short. A log confirmation is one line. A check is one screen.
