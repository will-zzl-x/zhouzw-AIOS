---
name: gps
description: GPS Method — Goal, Plan, System. A structured 9-question framework for any goal. Run it to set up a new goal properly or as a diagnostic when you're struggling with something. Triggered by "GPS", "run GPS on", "set up a goal", "why am I not making progress on", or "/gps".
---

## Goal

Two modes:
1. **Setup** — build a complete GPS for a new goal. Takes ~10 minutes.
2. **Diagnostic** — run an existing goal through GPS to identify exactly where it's breaking down.

Output: a structured goal file written to `goals/<slug>.md`.

## Reads

- `state.md` — current life context, active goals, constraints
- `context/priorities.md` — life area priorities
- `goals/` — existing GPS docs (to avoid duplication or surfacing conflicts)

## Writes

- `goals/<goal-slug>.md` — completed GPS document

---

## The GPS Framework

### G — Goal (what you're aiming for)
1. **What** — specific, concrete, quantifiable. If you can't put a number on it, get more specific.
2. **Why** — intrinsic reasons you actually care. Not "should" or obligation. Why does this matter to you personally?
3. **Anti-goals** — what you want to avoid on the way there. Constraints that protect the rest of your life.

### P — Plan (your roadmap)
4. **Major moves** — 3–5 actions that, if you did them consistently, would get you to the goal.
5. **Realism check** — two questions:
   - In theory: if you followed the plan perfectly, would it actually get you there? (0–100%)
   - In practice: what's the realistic chance you follow through? (0–100%)
   - If either is under 80%, the plan needs to change before you start.
6. **Crystal ball** — project forward and imagine you failed to hit the goal. What are the top 3 reasons why? Then: what's the mitigation for each?

### S — System (how you make sure you stick to the plan)
7. **Tracking** — what metric or log will you look at to know if the plan is working?
8. **Reminders** — how will you keep the goal and plan in front of you? Calendar blocks, journal, dashboard, habit app?
9. **Accountability** — who or what holds you accountable if you drift?

---

## Steps — Setup Mode

Triggered by: "run GPS", "set up a goal", "/gps [goal description]"

1. Read `state.md` to understand current context and active goals.
2. Ask the 9 questions in three passes. Don't ask all 9 at once — group them by section. Will can answer each group before moving on:

   **Pass 1 — Goal:**
   > "What's the goal? Be as specific as you can — ideally with a number attached. Why does it matter to you? And what do you want to avoid on the way there?"

   **Pass 2 — Plan:**
   > "What are the 3–5 things you'd need to do consistently to actually get there? If you followed those exactly, do you think it would work? And realistically, how likely are you to follow through?"

   **Pass 3 — System:**
   > "How will you track progress? How will you keep it in front of you week to week? Is there anyone holding you accountable?"

3. After all three passes, synthesize and write to `goals/<slug>.md`:

```
# GPS: [Goal Name]
Created: [Date]

---

## G — Goal

**What:** [specific, quantifiable goal]
**Why:** [intrinsic reasons]
**Anti-goals:** [constraints]

---

## P — Plan

**Major moves:**
1. [action]
2. [action]
3. [action]
(+ up to 2 more)

**Realism check:**
- In theory (will it work?): [X]%
- In practice (will I follow through?): [X]%
- [Flag if either is <80% and note what needs to change]

**Crystal ball — top 3 failure reasons + mitigations:**
1. Risk: [reason] → Mitigation: [what to do about it]
2. Risk: [reason] → Mitigation: [what to do about it]
3. Risk: [reason] → Mitigation: [what to do about it]

---

## S — System

**Tracking:** [what gets measured]
**Reminders:** [how it stays in front of you]
**Accountability:** [who or what]

---

## Status

Active as of [date]. Review at weekly reflection.
```

4. Confirm: "GPS written to `goals/<slug>.md`." Name one thing Will should do today or this week to activate the plan.

---

## Steps — Diagnostic Mode

Triggered by: "why am I not making progress on X", "GPS diagnostic", running GPS on an existing goal that's stalling

1. Read the relevant `goals/<slug>.md` if it exists.
2. Walk through the 9 components and identify where the breakdown is. The common failure points:
   - **G broken:** Goal is vague or the why is weak → will quit when it gets hard
   - **P broken at realism:** Plan is theoretically wrong (wrong actions) or practically too aggressive (won't follow through)
   - **P broken at crystal ball:** Known obstacles weren't mitigated, and now they've shown up
   - **S broken at tracking:** No feedback loop → no idea if it's working
   - **S broken at reminders:** Goal fell out of view → stopped feeling urgent
   - **S broken at accountability:** No external pressure → easy to let slide
3. Output:
   ```
   ## GPS Diagnostic — [Goal]

   **Where it's breaking down:** [specific component]
   **Why:** [one clear sentence]
   **Fix:** [specific, actionable change to make right now]
   ```

---

## Rules

- Don't move past the Goal section until What, Why, and Anti-goals are clear. Vague goals produce useless plans.
- If the realism check on the plan is under 80% on either dimension, stop and redesign the plan before continuing to System. A bad plan with a great system still fails.
- The crystal ball step is not optional. Most people skip it and then get surprised by the exact obstacles they could have predicted.
- Completed GPS docs live in `goals/`. Name the file clearly: `goals/scm-ii-promotion.md`, `goals/nyc-cut.md`, etc.
- If a goal strongly overlaps with something already in `state.md` or `dashboard.md`, note the connection — don't create a parallel reality.
