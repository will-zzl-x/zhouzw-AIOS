# Meal Planning — AI-assisted weekly cycle, token-efficient by design

A meal-planning system that runs my real weekly cook cycle. **Governing principle:
most of the workflow is deterministic and runs as plain Python with zero AI calls.**
AI is invoked only for four genuinely fuzzy tasks. Lives inside the AIOS repo and is
wired to the `/health-os` skill (see "AIOS integration" below).

`data/recipes.json` (33 vetted recipes) is the **source of truth** and is never
modified by any script.

---

## The loop

| Step | Command | Tokens? | What it does |
|------|---------|---------|--------------|
| 0 | `make deplete APPLY=1` *(prior cycle)* | **no tokens** | **Before planning a new week**, draw down the FINISHED cycle's consumption so inventory is true. `make week` nudges loudly if you skip this (via `data/deplete_log.json`). |
| 1 | `make new-cycle` | **no tokens** | Interactive: prompts dates/exceptions/carryover/selections → writes `cycles/<YYYY-MM-DD>.yaml` at the TOP LEVEL and auto-archives the prior cycle to `cycles/archive/` |
| **★** | **`make week`** | **no tokens** | **The weekly run.** PREFLIGHT healthcheck (recipes/inventory/cycle valid + prior-cycle deplete-nudge) → coverage (Elena cover-first leads) → grocery → defrost → schedule in one command, one clean report. Fails fast before any step can crash; stops before `deplete` (which mutates state). `make week CYCLE=cycles/<date>.yaml`. |
| 2 | `make coverage` | **no tokens** | Servings needed per slot/person − carryover − dining-out vs. planned. **Leads with the COVER-FIRST member's (Elena's) gap analysis** — lock her meals first, then fill Will's. |
| → | *(only if gap)* run `ai/suggest_recipes.md` | **TOKENS** | Suggest recipes to fill the gap |
| 3 | `make grocery` | **no tokens** | Aggregate ingredients × servings − inventory, group by store, flag every unconfirmed item |
| 3b | `make validate-cycle` | **no tokens** | Per-recipe, per-ingredient checklist vs `inventory.json`: file value vs need, ⚠ on anything short / zero / missing / unit-unverifiable / multi-row-summed. **Covered = name match AND qty>0 AND unit-convertible AND enough — a name hit alone is never covered.** Run before shopping. |
| 4 | `make defrost` | **no tokens** | Freezer→fridge move schedule. Stages proteins actually **in the freezer** (`inventory.json` location=freezer), cut-aware (won't thaw thighs for a breast recipe); fresh-buys skipped. |
| 5 | `make schedule` | **no tokens** | Ordered cook plan: perishable → marinade-lead → slow/long-simmer → rotisserie(Sat) → standard |
| 5b | `make cook-plan` | **no tokens** | Generate the phone-readable `cycles/<date>-cook-plan.md` scaffold (buy list by store, Sat cooks / Sun preps, defrost checklist, week-at-a-glance skeleton, macro line). Hand-finish the day mapping, then commit+push for phone access. Refuses to overwrite without `FORCE=1`. |
| 6 | *(cook the week)* | — | — |
| 7 | `make deplete APPLY=1` | **no tokens** | Subtract the cycle's consumed items from `data/inventory.json` and record the cycle in `data/deplete_log.json`. Uses the **same fuzzy-name + unit-scaling matcher as grocery** (`lib.units`), so what grocery calls "covered" is exactly what deplete draws down — inventory stays true week over week. |
| any | `make validate` | **no tokens** | Recipe-DB schema + integrity. `STRICT=1` hardens the seasoning rule. |
| any | `make test` | **no tokens** | Regression tests (`scripts/tests/`) — units matcher, validate-cycle gates, cycles layout, deplete-nudge. |

> **Run-it-weekly tip:** `make week` is the front door — preflight + the whole read-only loop in one shot. Use the individual targets only to re-run one step. `deplete` stays separate on purpose (the only step that writes inventory).

> **App-ready (`--json`):** every read-only step (`coverage`, `grocery`, `defrost`, `cook_schedule`) and `run_week.py` accept `--json` and emit a structured result instead of text — same compute, machine-readable. `python scripts/run_week.py [cycle] --json` returns the whole **WeekReport** (preflight + coverage + grocery + defrost + schedule) as one JSON object. That object is the contract a future app/UI consumes — no CLI scraping. Text remains the default for terminal use.

**The only token-spending tasks** (run by hand, never `make`):

| Template | When |
|---|---|
| `ai/vet_recipe.md` | Add a new recipe from image/URL/text → one schema-ready JSON object to append |
| `ai/suggest_recipes.md` | Coverage showed a gap → ranked recipe picks to fill it |
| `ai/produce_pairing.md` | Homeless leftover produce → assign each to a recipe/side |
| `ai/troubleshoot.md` | Ad-hoc cook rescue (sauce broke, protein overcooking, timing collision) |

Everything else — serving math, coverage, grocery aggregation + store grouping,
defrost timing, cook ordering, inventory depletion, recipe validation — is a script.
Never spend tokens on what a script can do.

---

## Quick start

```bash
cd meal-planning
make validate          # confirms recipes.json is sound (PASS with warnings)
make demo              # runs validate + coverage + grocery + defrost + schedule on the latest cycle
```

A sample cycle (`cycles/archive/2026-06-07.yaml`), seed `inventory.json`, `config.yaml`,
`tier_list.yaml`, and `seasonal.yaml` ship in `data/` so every target is demoable
immediately. `PY=python3 make ...` if your interpreter is named differently.

> **Windows note:** `make` isn't installed by default. Either install it
> (`choco install make`, or use WSL/Git-for-Windows with make), or run the
> scripts directly — every target is a one-liner: e.g. `python scripts/coverage.py`,
> `python scripts/grocery.py cycles/2026-06-07.yaml`. The Makefile is a convenience
> wrapper, not a dependency.

Requires `pyyaml` (`pip install pyyaml`); everything else is Python stdlib.

---

## Layout

```
meal-planning/
  data/
    recipes.json      # vetted recipes — SOURCE OF TRUTH, never modified
    config.yaml       # household, members+slots, planning prefs (cover-first, weekend-cook,
                      # macro closer), stores, equipment, cut rules, defrost/cook rules
    tier_list.yaml    # Elena S–E tier + on_break bench
    inventory.json    # fridge/freezer/pantry state
    deplete_log.json  # which cycles were deplete --apply'd (drives the run_week nudge)
    seasonal.yaml     # cached Chandler AZ produce by month (so produce Qs cost no tokens)
  cycles/
    <date>.yaml            # the CURRENT cycle (Sat→Fri): dates, exceptions, carryover, selections
    <date>-cook-plan.md    # its phone-readable cook plan
    README.md              # cycle index, newest-first, CURRENT pointer
    archive/               # every past cycle + artifacts — preserved, never deleted
  scripts/
    new_cycle.py coverage.py grocery.py defrost.py cook_schedule.py deplete.py
    validate.py validate_cycle.py cook_plan.py balance_check.py run_week.py
    lib/models.py     # dataclasses (Recipe/Ingredient/Cycle/InventoryItem/Member) + loaders
    lib/units.py      # free-text amount parser + unit normalization + fuzzy name matcher
    tests/            # regression tests (make test)
  ai/                 # the 4 prompt templates (TOKENS) — not make targets
  Makefile  README.md
```

**Cycle layout rule:** the top level of `cycles/` holds ONLY the current cycle;
everything older is in `cycles/archive/` (moved, never deleted — see
`cycles/README.md` for the index). `lib/models.latest_cycle_path()` reads only the
top level on purpose, so a no-arg `make week` always runs the current cycle and
archiving can never change behavior. `make new-cycle` auto-archives the outgoing
cycle (pass `--keep-old` to skip).

## Git model — one branch, always push

The AIOS repo's default branch is **`master`**, and meal-planning work lives on it:

- **Phone/web sessions** commit straight to `master`.
- **Laptop meal work** commits `meal-planning/` paths to `master` and **pushes
  immediately** — the cook plan is read on Will's phone, so an unpushed commit
  doesn't exist as far as the kitchen is concerned.
- **Never work on a stale side-branch.** The 2026-06-27 "banff cycle" divergence
  happened exactly this way: laptop edits sat on a side branch while phone edits
  landed on `master`, and the two views of the same cycle drifted until a manual
  merge had to adjudicate which was real. One branch, commit small, push now.
- If a push is rejected (remote ahead — usually a phone commit), `git pull --rebase`
  your meal-planning commit on top and push again. Meal files rarely conflict; if a
  conflict touches NON-meal files, stop and resolve deliberately — don't force.

## How Will actually runs the week (encoded preferences)

These are durable workflow preferences learned from real cycles (esp. 2026-07-18)
— they live in `data/config.yaml` (`planning`, `weekend_cook`, `cut.macro_closer`)
and the scripts read them. Update the config when the preference changes.

- **COVER-FIRST (Elena):** plan Elena's coverage FIRST — only meals she likes /
  will eat (`data/tier_list.yaml`; e.g. chipotle bowls are Will-only). THEN fill
  Will's meals around her. `make coverage` leads with her gap analysis for this
  reason. (`config.planning.cover_first`)
- **WEEKEND-COOK model:** ALL cooking happens Sat+Sun; the week eats
  leftovers/reheats. Typically 3-4 cooks Sat + 3-4 preps Sun. The
  **aging-ingredient dish is always cook #1** (7/18: aging coleslaw → egg-roll
  ramen first). Rotisserie breaks down Saturday. **Sat M2 = hot dogs** (standing
  no-cook exception, not a recipe). Cycles run **Sat→Fri**; Walmart order Friday
  night, Costco Saturday AM. (`config.weekend_cook`)
- **FRESH-vs-FROZEN pack swap:** when a cook moves EARLIER, give it a FRESH
  same-day-bought protein pack (no thaw needed) and let the frozen packs thaw
  freezer→fridge for the LATER cook. (7/18: #36 chinese chicken moved to Sat and
  took the fresh Costco pack; freezer breasts thawed for Sunday's #41 fried rice.)
- **Day-old rice:** rice for fried rice is cooked a day ahead — cook the rice
  SATURDAY, fry SUNDAY.
- **MACRO CLOSER:** Will's cut target is ~150g protein/day. Close the day's
  remaining macros with a **larger portion of an existing high-protein item**
  (e.g. bump the breaded-chunk bowl to 7oz ≈ 410 cal / 39g protein) — NOT whey
  top-ups / cottage cheese / hard-boiled eggs (he dislikes snacking on those).
  Fill remaining calories with ON-HAND items first, then in-season fruit
  (`data/seasonal.yaml`). **Bananas only go in shakes** — never as standalone
  fruit (pineapple was the 7/18 pick). Shakes always get flax + chia.
  (`config.cut.macro_closer`)
- **COOK-PLAN artifact:** every cycle gets a phone-readable
  `cycles/<date>-cook-plan.md` (buy list split Costco/Walmart, Sat cooks, Sun
  preps, week-at-a-glance table, daily macro line). `make cook-plan` generates
  the scaffold; hand-finish the day mapping and portions, then commit + push.

## inventory_snapshot ADDS — it never overrides

A cycle's `inventory_snapshot` list **ADDS to the on-hand pool on top of
`data/inventory.json`** — it does not replace or override it. Listing an item that
inventory.json already tracks **double-counts it** (this caused real
double-counting: grocery/validate-cycle read the item as 2x on hand).
`validate-cycle` now flags such summed coverage as ⚠ MULTI.

**Correct pattern:**
1. Finish the week → `make deplete APPLY=1` for the finished cycle FIRST, so
   `inventory.json` is true.
2. Use `inventory_snapshot` ONLY for genuinely new purchases / items
   inventory.json doesn't track yet.
3. Better still: put new purchases into `inventory.json` itself
   (`scripts/inventory_add.py`) and leave the snapshot empty — the 2026-07-18
   cycle does exactly this (`inventory_snapshot: []`).

## Data model (summary)

- **Members:** Will (M1 light · M2 microwave lunch · M3 microwave solo work meal ·
  M4 dinner) and Elena (M1 protein bar · M2 · M4 shared). Will is on an active cut.
- **Slot rules:** M2/M3 microwave-reheatable only; M4 home-cooked (salmon reheats
  325°F oven/air-fryer, **never** microwave). Overflow M2→M3/M4, M3→M4. Dining-out /
  covered meals are flexible → assigned to the slot with greatest deficit.
- **Cut constraints:** M1/M2 starch-free/low-carb; ~150g protein/day, ~45g/feeding;
  low-cal sauces on hand; dining out = carb-forward low-fat refeed.
- **Meal-type split:** shared meals (M4 + Elena M2) → A/S-tier vetted recipes;
  Will-only solo (M3 + Will M2) → convenience stack (rotisserie, slow-cooker shredded
  chicken, canned-salmon + Greek-yogurt bowls, air-fryer bakes, low-cal sauces).
- **Stores:** Costco, Walmart, Asian Mart. Cycle Sat→Fri; Walmart Fri-night order;
  Costco Sat AM.

## validate.py — the seasoning carve-out

`recipes.json` intentionally has seasoning entries like `{"amount":"to taste","unit":""}`.
validate.py **hard-fails** only structural breakage (duplicate ids, meal_slot not in
{2,3,4}, bad store, blank amount+unit on a *non-seasoning*) and **warns** (passes) on
to-taste seasonings via an allowlist. `make validate STRICT=1` promotes warnings to
failures — use it when hand-entering new recipes so future additions carry baselines.
It also surfaces a known data note: recipe 7's notes say "ON BREAK" but `on_break:false`
(scripts honor the boolean → treat it active; flip the field if you want it benched).

## Known limits (deliberate, safe-direction)

- **Volume↔weight isn't auto-converted.** An ingredient needed in tsp/tbsp/cup is
  not netted against an inventory item stored in oz (that requires per-ingredient
  density to be correct). Such items show as CHECK ("in inventory — confirm
  coverage"), and `deplete.py` under-depletes them rather than guess. Same-family
  (oz↔lb, tsp↔tbsp↔cup) and descriptive-unit ("thighs (1 Costco pack)"↔"thighs")
  matches DO net out. Net: the system never silently under-buys or corrupts counts.
- These were the findings of an adversarial self-review (see git history); the
  3 output-corrupting defects were fixed, the remaining density limit is documented here.

## Free-text amounts (why grocery is "good enough", not exact)

`recipes.json` amounts are human text ("2-3", "~1/3", "24oz", "1 Tbsp + 1 tsp",
"to taste"). `lib/units.parse_amount` parses what it can (ranges→midpoint,
fractions, mixed numbers, leading numbers) and treats the rest as non-numeric
"CHECK" items the grocery list flags rather than guesses. Units are grouped by the
verbatim string, so descriptive units ("cup per bowl (2 cups total)") don't merge
with bare ones — faithful to the data, occasionally verbose. **The grocery list
flags every BUY/CHECK item as unconfirmed — never assume spices/sauces on hand.**

## AIOS integration

This system is folded into the **`/health-os`** skill (the meal-planning pillar
alongside sleep/diet logging). The skill points at this deterministic loop for cycle
planning and at the four `ai/` templates for the fuzzy tasks. See
`.claude/skills/health-os/skill.md`.

## Relationship to the meal-planner app

I have a separate web app at `github.com/will-zzl-x/meal-planner` (Streamlit +
service/repository layers, SQLite). **This system does not depend on it and uses a
different, richer recipe schema** (the app's `Recipe`/`Ingredient` require
`Decimal` quantities + `calories_per_serving` and would reject this free-text data).
Two pieces of the app's logic were intentionally mirrored here so a future migration
stays consistent: the **ingredient-aggregation key** (`name`+`unit` → summed
quantity) and the **whole-item rounding** (onion 8oz, garlic clove 0.1oz, bell
pepper 6oz, shallot 2oz, in `lib/units.WHOLE_ITEM_OZ`). For now the app is
deprioritized — I run this AI-assisted cycle instead. If the app is revived, migrate
by mapping each recipes.json record into the app's `Recipe` dataclass and parsing
`amount` via `lib/units.parse_amount` to satisfy the `Decimal` requirement.
