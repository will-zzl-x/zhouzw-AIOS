# Meal Planning — AI-assisted weekly cycle, token-efficient by design

A meal-planning system that runs my real weekly cook cycle. **Governing principle:
most of the workflow is deterministic and runs as plain Python with zero AI calls.**
AI is invoked only for four genuinely fuzzy tasks. Lives inside the AIOS repo and is
wired to the `/health-os` skill (see "AIOS integration" below).

`data/recipes.json` (20 vetted recipes) is the **source of truth** and is never
modified by any script.

---

## The loop

| Step | Command | Tokens? | What it does |
|------|---------|---------|--------------|
| 1 | `make new-cycle` | **no tokens** | Interactive: prompts dates/exceptions/carryover/selections → writes `cycles/<YYYY-MM-DD>.yaml` |
| 2 | `make coverage` | **no tokens** | Servings needed per slot/person − carryover − dining-out vs. planned. Prints gaps. |
| → | *(only if gap)* run `ai/suggest_recipes.md` | **TOKENS** | Suggest recipes to fill the gap |
| 3 | `make grocery` | **no tokens** | Aggregate ingredients × servings − inventory, group by store, flag every unconfirmed item |
| 4 | `make defrost` | **no tokens** | Freezer→fridge move schedule (beef/thighs 12–18h, breast 18–24h, move 2 nights before first cook) |
| 5 | `make schedule` | **no tokens** | Ordered cook plan: perishable → marinade-lead → slow/long-simmer → rotisserie(Sat) → standard |
| 6 | *(cook the week)* | — | — |
| 7 | `make deplete APPLY=1` | **no tokens** | Subtract the cycle's consumed items from `data/inventory.json` for next cycle |
| any | `make validate` | **no tokens** | Recipe-DB schema + integrity. `STRICT=1` hardens the seasoning rule. |

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
make demo              # runs validate + coverage + grocery + defrost + schedule on the sample cycle
```

A sample cycle (`cycles/2026-06-07.yaml`), seed `inventory.json`, `config.yaml`,
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
    recipes.json      # 20 vetted recipes — SOURCE OF TRUTH, never modified
    config.yaml       # household, members+slots, stores, equipment, cut rules, defrost/cook rules
    tier_list.yaml    # Elena S–E tier + on_break bench
    inventory.json    # fridge/freezer/pantry state
    seasonal.yaml     # cached Chandler AZ produce by month (so produce Qs cost no tokens)
  cycles/<date>.yaml  # one per Sat→Sat cycle: dates, exceptions, carryover, selections, snapshot
  scripts/
    new_cycle.py coverage.py grocery.py defrost.py cook_schedule.py deplete.py validate.py
    lib/models.py     # dataclasses (Recipe/Ingredient/Cycle/InventoryItem/Member) + loaders
    lib/units.py      # free-text amount parser + unit normalization + whole-item rounding
  ai/                 # the 4 prompt templates (TOKENS) — not make targets
  Makefile  README.md
```

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
- **Stores:** Costco, Walmart, Asian Mart. Cycle Sat→Sat; Walmart Fri-night order;
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
