---
name: workout-log
description: Workout Log — log a training session with exercise, weight, reps, and RPE. Tracks progress toward intermediate strength standards. Triggered by "log workout", "log session", "just finished training", or "/workout-log".
---

## Goal

Two modes:
1. **Log** — capture a completed training session.
2. **Check** — surface progress toward intermediate standards and recent trends.

## Reads

- `journals/workout-log.md` — running training log
- `state.md` — current program, phase, and active modifications

## Writes

- `journals/workout-log.md` — appends new session entry

## Intermediate Standards (Male, ~180 lb)

Track progress toward these targets:
| Lift | Current Est. | Intermediate Target |
|------|-------------|---------------------|
| Squat | — | 225 lb × 5 |
| Deadlift / RDL | ~140 lb/hand (~310 lb equiv) | 315 lb × 5 |
| Bench Press | — | 185 lb × 5 |
| Overhead Press | — | 115 lb × 5 |
| Pull-up | BW + 0 | BW + 45 lb × 5 |
| Lat Pulldown | — | 160 lb × 8 |
| Curl (DB) | — | 40 lb/hand × 10 |

Update as actual numbers come in from logs.

## Steps — Log Mode

Triggered by: "log workout", "log session", "just finished", details of a session.

1. Read `journals/workout-log.md`.
2. Parse what Will provided: session type, exercises, sets/reps/weight, RPE if given.
3. If details are missing and it would help track progress (weight for a main lift), ask once. Don't ask about accessories if you have the compound lifts.
4. Append to `journals/workout-log.md`:
   ```
   ---
   **[Date]** — [Session Type: e.g., Torso A / Legs / Bro Day / Bodyweight]
   Program: [GVS Ravage Week X / Bodyweight / etc.]

   | Exercise | Sets × Reps | Weight | RPE |
   |----------|------------|--------|-----|
   | [name]   | [3×8]      | [135]  | [7] |

   Notes: [PR? Something felt off? Substitution made?]
   ```
5. Call out any PR or milestone toward intermediate standards.
6. Confirm: "Logged. [one-line observation if anything noteworthy]."

## Steps — Check Mode

Triggered by: "/workout-log check", "how's my training", "where am I on strength"

1. Read `journals/workout-log.md` in full.
2. Read `state.md` for current phase and program modifications.
3. Output:
   ```
   ## Training Check — [Date]

   **Last session:** [date + type]
   **Sessions this week:** [count]
   **Current phase:** [Maintenance / NYC Cut / etc.]

   **Main lift progress:**
   [Table: lift | last logged | trend | target | gap]

   **Observations:**
   [1–3 bullets — what's progressing, what's stalling, what to watch]
   ```

## Rules

- Don't give programming advice unless asked. Log and observe only.
- If `journals/workout-log.md` doesn't exist, create it with a header before logging.
- RPE is optional but useful — note if missing, don't demand it.
- Bodyweight sessions count — log them. Progress tracking includes consistency.
