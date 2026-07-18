---
name: health-os
description: Health OS — log and review the non-exercise pillars of your health system: sleep, diet/nutrition, and meal planning. Exercise is handled by /workout-log. Triggered by "log sleep", "log meals", "health check", "meal plan", "plan a cycle", "grocery list", "health os", or "/health-os".
---

## Goal

Four modes:
1. **Sleep log** — capture last night's sleep.
2. **Diet log** — capture today's nutrition (protein target, rough meals).
3. **Health check** — surface how sleep and diet are trending this week vs. targets.
4. **Meal planning** — run the weekly cook-cycle system in `meal-planning/`.

Exercise tracking lives in `/workout-log`. This skill handles the other three pillars.

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

## Steps — Meal Planning

Triggered by: "meal plan", "plan a cycle", "grocery list", "what should I cook", "vet this recipe", "fill the coverage gap", "produce pairing", "cook rescue".

The full system lives in `meal-planning/` (its own README + Makefile). **It is
token-efficient by design: the weekly loop is deterministic Python — run the scripts,
do NOT reason through serving math / grocery aggregation / scheduling yourself.** Only
four tasks spend tokens, via the prompt templates in `meal-planning/ai/`.

**Cycle layout:** the CURRENT cycle (`cycles/<date>.yaml` + `<date>-cook-plan.md`)
sits at the TOP LEVEL of `meal-planning/cycles/`; all past cycles are in
`cycles/archive/` (see `cycles/README.md` for the index + CURRENT pointer — keep it
updated when a new cycle starts). Never delete archived cycles.

**Planning order (Will's preferences — encoded in `data/config.yaml`):**
1. `deplete --apply` the FINISHED cycle first (the `make week` preflight nudges if
   skipped). Only then plan the new week — otherwise inventory lies.
2. **COVER-FIRST:** lock Elena's meals first (only things she likes —
   `data/tier_list.yaml`), then fill Will's around her. `make coverage` leads
   with her gap analysis.
3. Weekend-cook model: all cooking Sat+Sun (3-4 cooks Sat — aging-ingredient dish
   is cook #1 — + 3-4 preps Sun); Sat M2 = hot dogs; fresh-vs-frozen pack swap
   when a cook moves earlier; day-old rice for fried rice. Cycles are Sat→Fri;
   Walmart order Fri night, Costco Sat AM.
4. Macro closer = larger portion of an existing high-protein item (7oz
   breaded-chunk bowl ≈ 410 cal/39g) — NOT whey/cottage-cheese/egg snacks. Fill
   with on-hand first, then in-season fruit; bananas only in shakes; shakes get
   flax + chia. (`config.cut.macro_closer`)

**Deterministic loop (NO TOKENS — run the script, report the output):**

| Ask | Command (from `meal-planning/`) |
|---|---|
| start a new week | `make new-cycle` (writes top-level cycle, auto-archives the old one) |
| run the whole weekly check | `make week` (preflight incl. deplete-nudge + coverage + grocery + defrost + schedule) |
| what's covered / what's short | `make coverage` (Elena cover-first leads) |
| grocery list | `make grocery` |
| is every ingredient really on hand? | `make validate-cycle` — per-recipe checklist vs inventory.json; covered = name match AND qty>0 AND unit-convertible AND enough. Run before shopping; surface every ⚠ to Will, never assume. |
| defrost schedule | `make defrost` |
| cook order | `make schedule` |
| phone cook plan | `make cook-plan` — generates `cycles/<date>-cook-plan.md` scaffold; hand-finish day mapping, then commit + push (phone access) |
| update pantry after the week | `make deplete APPLY=1` (records to `data/deplete_log.json`) |
| check the recipe DB | `make validate` |
| run the regression tests | `make test` |

(`make` may be absent on Windows — fall back to `python scripts/<name>.py`.
`recipes.json` is the source of truth; never modify recipe data.)

**inventory_snapshot ADDS, never overrides:** a cycle's `inventory_snapshot` adds
to `data/inventory.json` — listing an item tracked in both double-counts it.
Deplete the finished cycle first; snapshot only genuinely NEW purchases (or better,
add them to inventory.json and leave the snapshot empty).

**Git model (single branch, always push):** the AIOS repo default branch is
`master`. Phone/web sessions commit to `master`; laptop meal work commits
`meal-planning/` paths to `master` and PUSHES immediately (the cook plan is read
on Will's phone). Never work on a stale side-branch — that's what caused the
2026-06-27 banff-cycle divergence. If push is rejected, `git pull --rebase` and
push; stop if conflicts touch non-meal files.

**AI touchpoints (TOKENS — only these four):** read the matching template in
`meal-planning/ai/` and follow its output contract:
- **vet a new recipe** (image/URL/text → one schema-ready JSON object): `ai/vet_recipe.md`, then `make validate`.
- **fill a coverage gap** (only after `make coverage` shows a gap): `ai/suggest_recipes.md`.
- **homeless produce** → `ai/produce_pairing.md` (check `data/seasonal.yaml` first — usually free).
- **cook rescue** (real-time): `ai/troubleshoot.md`.

**Rule:** if a script can answer it, run the script — don't spend tokens. Surface the
script output; only invoke an `ai/` template for the four genuinely-fuzzy tasks above.

## Rules

- Don't give advice unless asked. Log and surface data.
- If `journals/health-log.md` doesn't exist, create it with a header before logging.
- Protein target is the primary diet metric — don't get lost in calories unless Will is in the NYC Cut phase, where both matter.
- Keep it short. A log confirmation is one line. A check is one screen.
