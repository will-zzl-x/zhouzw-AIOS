---
name: scm-tracker
description: SCM II Behavior Tracker — log a strategic moment at work or run a weekly review to surface your promotion narrative. Triggered by "log a behavior", "scm log", "promotion moment", or "/scm-tracker review".
---

## Goal

Two modes:
1. **Log** — capture a specific behavioral moment tied to an L5 threshold behavior before it's forgotten.
2. **Review** — synthesize the log into a promotion narrative for the current window.

## Reads

- `journals/scm-behaviors.md` — running behavior log
- `context/work-state.md` — L5 threshold behaviors and active projects

## Writes

- `journals/scm-behaviors.md` — appends new entry (Log mode)

## L5 Threshold Behaviors

Tag each log entry with one or more:
- `[strategic-framing]` — reframed a problem at a higher level than assigned
- `[cross-functional-influence]` — shaped outcome with someone who doesn't report to you
- `[proactive-risk]` — flagged an issue before it escalated
- `[new-process]` — created something that didn't exist
- `[ambiguous-leadership]` — drove an unclear situation to a defined outcome

## Steps — Log Mode

Triggered by: "log a behavior", "scm log", "promotion moment", anything describing a work situation worth capturing.

1. Read `journals/scm-behaviors.md`.
2. Identify which L5 threshold behavior(s) the moment demonstrates — pick from the list above.
3. Append to `journals/scm-behaviors.md`:
   ```
   ---
   **[Date]** `[tag]` `[tag]`
   **Situation:** [What was happening — 1 sentence]
   **Action:** [What Will specifically did — 1–2 sentences]
   **Impact / Signal:** [What changed or who noticed — 1 sentence, or "TBD" if unknown yet]
   ```
4. Confirm: "Logged. [behavior tag(s)]."

## Steps — Review Mode

Triggered by: "/scm-tracker review", "review my scm behaviors", "what's my promotion narrative"

1. Read `journals/scm-behaviors.md` in full.
2. Read `context/work-state.md` for the L5 threshold behaviors.
3. Group entries by behavior tag.
4. Output:
   ```
   ## SCM II Behavior Review — [Date]

   **Strongest signal:** [The 1–2 entries that most clearly demonstrate L5 behavior]

   **Coverage by threshold:**
   - strategic-framing: [count] entries
   - cross-functional-influence: [count] entries
   - proactive-risk: [count] entries
   - new-process: [count] entries
   - ambiguous-leadership: [count] entries

   **Gaps:** [Which threshold behaviors have 0 or weak entries]

   **Promotion narrative draft:**
   [2–3 sentences that could be said in a promo conversation — specific, behavioral, no fluff]

   **Next: create a moment in [weakest area] — [one specific suggestion based on current projects]**
   ```

## Rules

- In Log mode: do not evaluate quality of the behavior or coach. Just classify and log.
- In Review mode: be direct. If the log is thin, say so plainly.
- Never inflate weak entries into strong signals.
- If `journals/scm-behaviors.md` doesn't exist, create it with a header before logging.
