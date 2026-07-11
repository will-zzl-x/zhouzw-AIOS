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
- `state.md` — current phase (maintenance vs. cut vs. reverse diet), protein target, any active constraints
- `context/daily-standard.md` — live phase gates (calorie/protein/fat/carb target), Todoist-facing source of truth for Will
- `meal-planning/data/config.yaml` — structured macro_targets for both Will and Elena, used by the meal-planning workflow

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
- **Don't hardcode numbers here — they rot** (this section already did once).
  Read the live source each time: `context/daily-standard.md`'s "CURRENT PHASE"
  line + that phase's "Done when" gates for Will's calorie/protein/fat/carb
  target, and `meal-planning/data/config.yaml` `members[].macro_targets` for the
  structured version the meal-planning system reads. If they disagree,
  `daily-standard.md` is the Todoist-facing source of truth — flag the drift and
  update `config.yaml` to match.
- Protein ~150g/day has held across every phase so far (cut, reverse diet,
  maintenance) — reasonable default, but confirm against the current phase gate.
- Elena has her own separate target (gaintain, not a cut) in `config.yaml`
  `members[].macro_targets` only — not in `daily-standard.md`, which is Will's
  Todoist-facing framework.

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

**Household is two people with different, independent goals** (Will: phase-based —
cut / reverse diet / maintenance; Elena: gaintain, separate from Will's phase). Read
both members' `macro_targets` in `data/config.yaml` before planning — don't assume
Elena inherits or shares Will's phase.

### Full cycle-planning workflow, in order

0. **Confirm current targets before touching recipes.** Read `context/daily-standard.md`
   CURRENT PHASE for Will's live macro target and `meal-planning/data/config.yaml`
   `members[].macro_targets` for both Will and Elena (structured version). If
   Will's phase changed since the config was last touched (e.g. a new reverse-diet
   step), update `config.yaml` first — the cycle should read current targets, not
   redefine them mid-build. Elena's `cycle_phase` (menstrual-cycle phase) is dynamic
   — update it each cycle if known, it affects appetite/BMR expectations.
1. **Skeleton:** `python scripts/new_cycle.py --noninteractive --date <Saturday>`
   (interactive mode blocks on stdin — not usable in an agent session; the script
   defaults to next Saturday matching the household's real Sat-Sat grocery cadence).
2. **See the real gap list:** `make coverage` — with an empty skeleton this prints
   every slot as a gap. This is the trigger for step 3, not a guess.
3. **Fill gaps via `ai/suggest_recipes.md`** — follow its ranking exactly (slot fit →
   meal-type pool → tier → inventory use-up → macro fit → variety). Before picking,
   actually check:
   - `data/inventory.json` — proteins with a `freshness_date` inside the cycle
     window should get prioritized into a recipe this week (waste-reduction ranks
     above a same-macro-fit alternative). Flag anything with a freshness_date
     already in the past — that's stale data or spoiled stock, not safe to plan
     around silently.
   - `data/seasonal.yaml` for the current month — prefer recipes whose produce is
     in-season.
   - Don't over-concentrate one protein across the week just because the modular
     recipes default to chicken — swap in a variety pick (canned salmon, ground
     beef, pork) where a gap and an on-hand ingredient both point the same way.
4. **Dual-macro / modular households:** default to the "cook once, fork at the
   plate" modular recipes (`for: "both"` in `recipes.json`, currently #28/#31/#32)
   for shared slots (M2 + M4) before reaching for single-profile recipes — they're
   pre-engineered to hit both members' targets from one cook. Apply
   `modular_assembly` from `config.yaml`: the higher-target/higher-volume member's
   fork gets more volume/fiber (extra veg, more rice), the lower-appetite or
   lower-target member's fork gets density (fat/cheese/nut-based toppings) instead
   of a bigger portion. If a modular recipe's fork portions don't match the current
   macro targets (e.g. targets changed since the recipe was last tuned), update the
   ingredient amounts in `recipes.json` directly (hand-edit, same as `vet_recipe.md`
   — it's "never modified by scripts," not "never modified by hand") rather than
   leaving the mismatch to a cycle-file note that the grocery script won't act on.
5. **Write selections into the cycle yaml**, with per-assembly macro notes (cal/
   protein/fat/carb) so the plan is auditable later, and a rollup comment estimating
   a representative day's totals for each member against their `macro_targets`.
6. **⚠️ `inventory_snapshot` gotcha:** this field is ADDITIVE on top of
   `data/inventory.json` (`grocery.py` sums both pools) — it is for genuinely new
   or untracked items, NOT a restatement of something already in the base
   inventory. Restating an already-tracked item there silently doubles its
   on-hand quantity and can cause under-buying. If you want to note something
   about an existing inventory item (expiring soon, stale freshness_date), put it
   in a YAML comment, not an `inventory_snapshot` entry.
7. **Validate the whole thing:** `make validate` (recipe DB integrity) then
   `make week CYCLE=cycles/<date>.yaml` (preflight + coverage + grocery + defrost +
   schedule in one run) — PREFLIGHT now also warns if `data/inventory.json` hasn't
   been git-touched in >10 days (added 2026-07-10, after exactly this went stale
   for 3 weeks and produced a wrong grocery list). Don't ignore that warning —
   confirm actual on-hand quantities with whoever's cooking before trusting
   "covered" anywhere in the output. Confirm 0 gaps and no errors before treating
   the cycle as
   final.
8. **Save curated docs:** write `cycles/<date>-cook-plan.md` (coverage table, cook
   order, modular-fork logic, macro rollup) and `cycles/<date>-grocery.md`
   (grocery list grouped by store, unit-mismatch/CHECK items called out) — condensed
   from the script output, not a raw dump. This isn't scripted; match the format of
   prior `cycles/*-cook-plan.md` / `*-grocery.md` files.
9. **After cooking:** `make deplete CYCLE=cycles/<date>.yaml APPLY=1` to write the
   real consumption back to `data/inventory.json`.

**Deterministic loop reference (NO TOKENS — run the script, report the output):**

| Ask | Command (from `meal-planning/`) |
|---|---|
| start a new week (agent session) | `python scripts/new_cycle.py --noninteractive --date <Sat>` |
| what's covered / what's short | `make coverage` |
| full weekly run | `make week` (preflight + coverage + grocery + defrost + schedule) |
| grocery list | `make grocery` |
| defrost schedule | `make defrost` |
| cook order | `make schedule` |
| update pantry after the week | `make deplete APPLY=1` |
| check the recipe DB | `make validate` |

(`make` may be absent on Windows — fall back to `python scripts/<name>.py`.
`recipes.json` is the source of truth for recipe *content* and is never modified
by any script — but it IS hand-edited for real changes, same as `vet_recipe.md`
already does; see step 4.)

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
- Protein target is the primary diet metric day-to-day — calories/fat/carbs matter equally whenever Will is in an active phase with a calorie target (cut, reverse diet), not just "the NYC Cut" specifically (that phase ended Jul 11 2026; check `daily-standard.md` for whatever phase is current).
- Keep it short. A log confirmation is one line. A check is one screen.
