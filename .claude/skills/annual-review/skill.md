---
name: annual-review
description: Annual Review — the yearly altitude of the Abdaal LifeOS stack. Celebrate/learn the year, Wheel of Life year-over-year, re-sketch the 3-year vision, set 2–3 yearly themes that feed the next four quarterly quest selections. Anchored to the first Sunday of January — Abdaal's own annual-planning window. Triggered by "annual review", "yearly review", "year planning", or "/annual-review".
---

## Goal

Run the annual altitude of the planning stack: a 60–90 minute session that looks back across the whole year, refreshes the vision, and sets **yearly themes** — NOT quests. Quests stay quarterly (`/quarterly-review` owns them). The annual review's job is to give the next four quarterly reviews a direction to draw from, so quest selection in Feb/May/Aug/Nov stops re-deriving the big picture from scratch.

**Anchor: first Sunday of January** (first run: Jan 3, 2027) — the New Year window where Abdaal runs his own Annual Planning Workshop (~Jan 6). Sits ~8 weeks after the November quarterly; the February quarterly is the first consumer of the themes. If it's been >100 days since the last quarterly review, run `/quarterly-review` first — the annual needs fresh quarterly data to look back on.

**System lineage:** Ali Abdaal LifeOS (life compass → yearly themes → quarterly quests → weekly/daily) — `references/abdaal.md`. Stack ratified in `decisions/2026-07-12-planning-cadence.md`.

## Reads

- All four `archives/YYYY-QN-quarterly-review.md` from the year (or however many exist)
- Last annual review (`archives/YYYY-annual-review.md`) if one exists
- `state.md`, `dashboard.md`, `backlog.md`
- `goals/` — every GPS doc touched this year, including completed/parked ones
- `decisions/` — the year's decision records
- `references/abdaal.md`, `references/integrated-coach.md`
- Skim the year's weekly reflections (`archives/*-reflection.md`) for texture, not exhaustively

## Writes

- `archives/YYYY-annual-review.md` — the annual review document
- `state.md` — refreshed 3-year sketch + a `Yearly Themes` line the quarterlies reference
- Commit: `annual review [YYYY]`

Does NOT regenerate `dashboard.md` or re-rank `backlog.md` — the next weekly reflection and quarterly review own those.

---

## Steps

### Phase 1 — Load Context (silent)

Read everything above. Build a private timeline of the year: quests set vs. quests landed, re-baselines, the 2–3 decisions that actually shaped the year. Note where the quarterlies drifted from last year's vision (if an annual exists) — that drift is tonight's raw material.

### Phase 2 — Celebrate / Learn (the 12-month look-back)

Ask, one at a time:

> "Across the whole year — what are you actually proud of? Not what scored well. What would January-you not believe you pulled off?"

> "What did this past year teach you that you didn't know last January? Skills, but also things about yourself."

> "What did you try that didn't work — and was it the goal, the plan, or the system that failed?" (GPS diagnosis at annual altitude — most failures are System.)

Reflect back a synthesis. Name the year in one sentence — a title, like a chapter.

### Phase 3 — Wheel of Life, Year-over-Year

Same 10 axes as `/quarterly-review` (Mission, Money, Growth, Body, Mind, Heart, Romantic, Family, Friends, Joy), rated 0–10 first-instinct. Then show the **trendline, not the snapshot**: this rating next to each quarterly's ratings from the year.

```
Axis      Feb  May  Aug  Nov  Annual  Trend
Joy        4    4    5    6     7      ↑ +3 on the year
...
```

Flag: which axis moved most, which stayed flat all year despite attention, which was never targeted by any quest. A flat axis with four quarters of effort is a System failure — say so.

### Phase 4 — Vision Re-sketch

Re-run the 3-year sketch **fresh — do not show Will the old one first** (anchoring kills it):

> "It's January [year + 3]. Things went well. Where are you living, what's the work, what's the marriage like, what does your body feel like, what do ordinary Tuesdays feel like?"

THEN diff against last year's sketch (or the latest quarterly's). What dropped out? What's new? What's been in the sketch for 2+ years with zero quests ever pointed at it? — that's either a fantasy to cut or a theme for Phase 5.

### Phase 5 — Yearly Themes (the output that matters)

Set **2–3 themes** for the coming year. A theme is a direction, not a deliverable — it constrains and inspires the four quarterly quest picks without pre-writing them.

Rules for a valid theme:
- Names which Wheel axis it exists to lift. Can't name one → cut it.
- Broad enough that each quarter can pick a different quest under it; concrete enough that you can tell whether a proposed quest serves it.
- Test each theme: "name one plausible Q1 quest and one plausible Q3 quest under this" — if you can't produce two different quests, it's a quest wearing a theme costume; send it to February.
- 2 is fine. 4 is too many. (Same constraint logic as quests: the limit is the point.)

Optionally attach one 12-month milestone per theme — a "by next annual review" marker, verifiable, not a plan.

### Phase 6 — Write Outputs

**1. Write `archives/YYYY-annual-review.md`:**

```
# Annual Review — [YYYY]
Date: [date] · Next annual: [first Sunday of next January]
System: Abdaal LifeOS annual layer (references/abdaal.md)

## The Year in One Sentence
[chapter title]

## Celebrate / Learn
**Proud of:** [bullets] · **Learned:** [bullets] · **Didn't work (G/P/S diagnosis):** [bullets]

## Wheel of Life — Year over Year
[trend table + the flat-axis / most-moved callouts]

## 3-Year Sketch — January [year+3]
[fresh sketch paragraph + directional themes]
**Diff vs. last year:** [what entered, what left, what's stale]

## Yearly Themes — [the year just starting]
1. [Theme] — lifts [axis]. 12-mo marker: [optional]
2. [Theme] — lifts [axis]. 12-mo marker: [optional]
3. [Theme] — lifts [axis]. 12-mo marker: [optional]

## Note to February's Quarterly Review
[2–3 sentences: what the Q1 quest selection should remember from tonight]
```

**2. Update `state.md`:** refresh the 3-year sketch reference and add/replace a `Yearly Themes:` line under Quests. Do not touch current-quarter quests.

**3. Commit** with message `annual review [YYYY]`.

---

## Rules

- **Themes are not quests.** If it has a deadline and a win condition, it belongs to a quarterly review. Push back.
- 2–3 themes, hard cap. Every theme names its Wheel axis.
- Vision sketch is written fresh before diffing — never show the old sketch first.
- A Wheel axis that stayed flat all year despite quest attention gets named out loud as a System failure, not papered over with a new theme.
- If Joy is still the low axis at annual altitude two years running, the recommendation is outside help (therapist/coach), not another theme — per `goals/desire-polarity.md`'s standing note.
- This session does not set daily targets, does not re-rank the backlog, does not regenerate the dashboard. Altitude discipline: the annual feeds the quarterly, the quarterly feeds the weekly, the weekly feeds the daily brief.
- Runs once, at the New Year (first week of January). If Will invokes it off-anchor (mid-year drift check — Abdaal's "Summer Reset" equivalent), run Phases 2–4 as a lightweight pulse and explicitly skip theme-setting — themes change annually, not on vibes.
