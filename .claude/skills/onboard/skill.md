---
name: onboard
description: 7-question interview to populate or refresh the AIOS context files. Run when setting up a new instance or when context files need a full refresh.
---

## Goal

Populate `context/about-me.md`, `context/priorities.md`, `context/relationships.md`, `context/work-state.md`, and `context/financial-state.md` from a guided interview. Produces day-one files from scratch or refreshes stale ones.

## Reads

- `context/` — current state of context files (to avoid overwriting good content)

## Writes

- `context/about-me.md`
- `context/priorities.md`
- `context/work-state.md`
- Any context file that is stale or empty

## Steps

### Question 1 — Identity
"Who are you? What do you do, what are you building, and who matters most in your life?"

*Saves to: `context/about-me.md` — identity, role, trajectory section*

### Question 2 — Voice
"Paste 1–2 things you've written recently — a message, an email, a note to yourself. Don't edit them."

*Saves to: `context/about-me.md` — voice and communication style section*

### Question 3 — Priorities
"What are your 2–3 biggest priorities for the next 90 days? Be specific — what does 'done' look like for each?"

*Saves to: `context/priorities.md`*

### Question 4 — Work
"Describe your work situation — role, what you're optimizing for, and what's actively in flight right now."

*Saves to: `context/work-state.md`*

### Question 5 — Relationships
"Describe your key relationships — who matters most, what's going well, what's the current active dynamic or opportunity?"

*Saves to: `context/relationships.md`*

### Question 6 — Money
"What's your financial situation — income, savings, what you're deploying toward, and what you're actively evaluating?"

*Saves to: `context/financial-state.md`*

### Question 7 — AIOS Goals
"What do you want this AIOS to help you do that you're not doing well on your own? What would 'working great' look like in 30 days?"

*Saves to: `CLAUDE.md` — cadence section and AIOS goals*

## Rules

- Ask questions one at a time. Wait for the answer before moving to the next.
- After each answer, confirm what you're saving: "Saving that to context/about-me.md."
- Don't edit or clean up Will's answers significantly — preserve voice.
- If a context file already has good content, show it and ask: "Does this still apply, or should we update it?"
- At the end, summarize: what files were created/updated, what day-one questions Can can now answer.
