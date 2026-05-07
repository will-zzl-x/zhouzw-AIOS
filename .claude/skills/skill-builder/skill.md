---
name: skill-builder
description: Interactive 6-question interview to build a new skill from scratch. Triggered by "build a skill", "create a new skill", "/skill-builder". Writes the skill file and updates the CLAUDE.md registry.
---

## Goal

Take a process or repeated workflow that Will does, and convert it into a fully structured skill file at `.claude/skills/<name>/skill.md`. Add it to the CLAUDE.md skill registry.

## Reads

- `CLAUDE.md` — existing skill registry to avoid duplicates
- `.claude/skills/` — existing skills for reference

## Writes

- `.claude/skills/<new-skill-name>/skill.md`
- `CLAUDE.md` — adds skill entry to Skills section

## Steps

### Phase 1 — Interview
Ask each question one at a time and wait for the answer.

**Q1 — Name and trigger:**
"What should this skill be called? And what phrase would you naturally say to trigger it — e.g., 'analyze my week' or 'create a post'?"

**Q2 — Goal:**
"In one sentence, what does this skill accomplish? What's the output when it's done?"

**Q3 — Steps:**
"Walk me through what you'd do manually, step by step, from start to finish. Don't skip anything."

**Q4 — References:**
"Does this skill need to read any specific files — like context files, reference docs, or external data? Which ones?"

**Q5 — Rules and guardrails:**
"What could go wrong? What should the skill always or never do?"

**Q6 — Success criteria:**
"How will you know the skill worked? What does a good output look like?"

### Phase 2 — Build

Construct the skill file using the standard format:

```markdown
---
name: [skill-name]
description: [One-sentence description for progressive context loading]
---

## Goal

[Q2 answer]

## Reads

[Q4 answer — list of files]

## Steps

[Q3 answer — structured as numbered steps]

## Rules

[Q5 answer — bulleted rules]
```

### Phase 3 — Register

Add the skill to `CLAUDE.md` under the Skills section:
```
### `/skill-name` — [Display Name]
**Triggers:** [Q1 trigger phrases]
**Action:** [Q2 goal, one sentence]
```

### Phase 4 — Confirm

Show Will the completed skill file and ask:
"Does this look right? Want to run it now to test?"

## Rules

- Don't start building until all 6 questions are answered.
- Keep the skill.md under 500 lines — move heavy reference content to separate files.
- Name the skill folder with kebab-case: `skill-name/skill.md`.
- After writing the file, confirm it was written and offer to test it immediately.
- If the skill requires external connections that aren't set up, flag it: "This skill needs [X connection] — want to set that up first?"
