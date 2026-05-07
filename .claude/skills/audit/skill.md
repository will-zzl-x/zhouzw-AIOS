---
name: audit
description: AIOS audit — grades the system on the 4 C's (Context, Connections, Capabilities, Cadence) with evidence, gaps, and one recommended next action per category. Run to find the highest-leverage improvements.
---

## Goal

Score this AIOS on each of the 4 C's on a 1–5 scale, with evidence and a specific recommended next action per category. Output a clear picture of where the system is strong and where to invest next.

## Reads

- `CLAUDE.md` — master config, skill registry
- `context/` — all context files
- `references/` — all reference/coach files
- `.claude/skills/` — all skill files
- `state.md` and `dashboard.md` — live state quality

## Audit Framework

### C1 — Context (1–5)
*What does the AIOS know about Will?*

Score based on:
- Is `context/about-me.md` populated with identity, voice, and trajectory?
- Is `context/priorities.md` current (updated this quarter)?
- Are relationships, work, and financial context files populated and up-to-date?
- Are `state.md` and `dashboard.md` coherent and fresh (<7 days)?

**1:** Context files missing or mostly empty
**3:** Core files exist but some are stale or shallow
**5:** All files populated, current, and coherent

### C2 — Connections (1–5)
*What external data can the AIOS reach?*

Score based on:
- How many of the 7 tier-1 domains are wired? (calendar, email/comms, tasks, meetings, revenue/money, knowledge, relationships)
- Are any API integrations configured?
- Is there a `connections.md` tracking what's been set up?

**1:** No external connections — AIOS only knows what's in local files
**3:** 1–2 connections active
**5:** 4+ connections active covering most tier-1 domains

### C3 — Capabilities (1–5)
*What can the AIOS actually do?*

Score based on:
- How many skills exist and are fully implemented (not stubs)?
- Do skills cover Will's most repeated tasks?
- Are any skills using external connections or running sub-agents?

**1:** 0–1 working skills
**3:** 3–5 skills implemented, covering core life areas
**5:** 7+ skills, including skills that use connections and run autonomously

### C4 — Cadence (1–5)
*When does the AIOS act without being prompted?*

Score based on:
- Is there a weekly reflection routine running?
- Are any routines or scheduled tasks configured (local or cloud)?
- Does the AIOS proactively surface things vs. waiting to be asked?

**1:** Everything is reactive — only responds when prompted
**3:** Weekly reflection is running; maybe 1 scheduled task
**5:** Multiple routines running on schedule, some autonomous

## Output Format

```
# AIOS Audit — [Date]

## Scores
| Category | Score | Evidence |
|----------|-------|----------|
| Context | X/5 | [1-2 sentences] |
| Connections | X/5 | [1-2 sentences] |
| Capabilities | X/5 | [1-2 sentences] |
| Cadence | X/5 | [1-2 sentences] |
| **Total** | **X/20** | |

## Top Gap Per Category
**Context:** [Specific gap + one recommended action]
**Connections:** [Specific gap + one recommended action]
**Capabilities:** [Specific gap + one recommended action]
**Cadence:** [Specific gap + one recommended action]

## Highest-Leverage Next Action
[Single most impactful improvement across all 4 C's]
```

## Rules

- Be honest about gaps. Don't inflate scores because files exist — score on quality and currency.
- Offer to save the audit to `decisions/audit-YYYY-MM-DD.md` for tracking improvement over time.
- If asked, prioritize gaps by leverage: which gap, if closed, would most improve daily usefulness?
