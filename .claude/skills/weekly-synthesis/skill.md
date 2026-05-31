---
name: weekly-synthesis
description: Friday weekly synthesis — bridges work + AIOS into one weekly thread. Reads daily journals, ict_automation snapshots, and sent inbox/Slack to produce Decisions / Results / Patterns / Open Questions / Cross-Domain Bridges. Auto-fires Fridays 4:13pm AZ via Windows Task Scheduler. Read by Sunday's /weekly-reflection.
---

## Goal

Aggregate the work week's signal (decisions, results, patterns) into a single
weekly synthesis file at `archives/synthesis/<YYYY>-W<WW>.md`. The synthesis
is **journalism**, not reflection — Sunday's `/weekly-reflection` reads the
synthesis as input. The unique value is **Cross-Domain Bridges** between work
and AIOS life areas; if no bridge surfaces, the skill failed.

## Triggers

- "weekly synthesis", "/weekly-synthesis", "friday synthesis", "situation report"
- Auto-fired Fridays 4:13pm AZ via `schtasks "Claude_Weekly_Synthesis"`

## Reads

- `journals/<YYYY-MM-DD>.md` for Mon–Fri of current ISO week
- `state.md`, `dashboard.md`, `context/work-state.md`
- `C:/Users/zhouzw/ict_automation/_daily_digest/output/triage_*.md` from this week
- `C:/Users/zhouzw/ict_automation/unified_flash/*.json` (current snapshot)
- `C:/Users/zhouzw/ict_automation/sim_auditor/audit_results.json`
- Slack: `from:@zhouzw after:<Monday>` and VIP DMs back to Will
- Outlook: sent items Mon–Fri (commitments delivered)
- `C:/Users/zhouzw/ict_automation/_notes/` files modified past 7 days

## Writes

- `archives/synthesis/<YYYY>-W<WW>.md` — primary artifact (auto-create dir)
- **Read-only on `state.md`** — proposes deltas, never auto-applies
- **Does NOT touch `dashboard.md`** (Sunday's job)

## Steering

Full procedure in `~/.claude/steering/weekly_synthesis.md` — pre-flight, source
pulls with graceful degradation, output structure, anti-bloat rules, failure
modes to avoid.

## Output structure

```markdown
# Week of <Mon date> – <Fri date>  [<YYYY>-W<WW>]

## Decisions Made
## Results & Outcomes (Work + AIOS)
## Patterns Emerging
## Open Questions Carried Forward
## Cross-Domain Bridges          ← MUST have ≥1 entry
## Bench / Coach Themes          [optional]
## Failed Sources                [optional, only if any]
```

**Rules:**
- Omit empty sections (no "None this week" filler).
- Hard cap 8 bullets per section — force prioritization.
- Cite sources on every Decision and Result bullet: `[src: <journal date or artifact>]`.
- No promotional language. State facts.
- If <3 daily journals exist this week, flag in opening line and proceed.

## State.md proposal flow

After writing the synthesis, scan for AIOS-state implications. If proposed
deltas exist, present as a diff and ask: "Apply now, or leave for Sunday's
`/weekly-reflection`?" Default to leaving for Sunday.

## Integration

- `/daily-sync` (Mon–Fri) → journals → `/weekly-synthesis` (Fri) → `/weekly-reflection` (Sun)
- `/ea-mode` Mon–Wed reads latest synthesis's Open Questions for prioritization
