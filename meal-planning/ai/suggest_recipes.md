# AI Template — Suggest Recipes to Fill a Coverage Gap (TOKENS)

**When to run:** `make coverage` printed a gap (slot short N servings) and you want
recipe picks to fill it. Run this ONLY after coverage shows a real gap — the gap is
the trigger, not a guess.

**Output contract:** a short ranked list of recipe ids (from data/recipes.json) +
optionally one "vet a new one" suggestion. Name the slot each fills and the serving
math. No essays.

---

## Inputs (paste these — all from scripts, no extra tokens to gather)
- The `make coverage` output (the gaps).
- `data/tier_list.yaml` (Elena ranking + on_break bench).
- `data/inventory.json` (what's on hand — prefer recipes that use it up).
- `data/seasonal.yaml` for the current month (prefer in-season produce sides).
- Each member's `macro_targets` + `modular_assembly` notes from `data/config.yaml`
  (replaces the old `cut:` block — Will's targets are now phase-based, see
  `goals/nyc-cut.md`; Elena's are gaintain-phase with a low-appetite protocol).

## How to choose
Rank candidates by, in order:
1. **Slot fit** — recipe's `meal_slots` must include the gap's slot. M2/M3 must be
   microwave-reheatable; M4 can be home-cooked (salmon = M4 only, never microwave).
2. **Meal-type pool** — shared slots (M4 + Elena M2) → A/S-tier vetted recipes;
   Will-only solo (M3 + Will M2) → convenience stack (rotisserie, slow-cooker
   shredded chicken, canned-salmon bowls, air-fryer bakes).
3. **Tier** — higher Elena tier first for shared meals. Skip `on_break` recipes.
4. **Inventory use-up** — favor recipes whose ingredients are already on hand or
   near freshness_date (reduce waste + grocery spend).
5. **Macro fit** — check the gap's member against their current `macro_targets`
   (protein/cal/fat/carb, phase-based — see `data/config.yaml`). M1/M2 starch-free
   is a standing slot rule regardless of phase. For a modular-fork recipe, Will's
   portion leans volume/fiber, Elena's leans density — see `modular_assembly`.
6. **Variety** — don't repeat a protein already heavy in the cycle.

## Output format
```
Gap: <member> <slot> short <N>
Picks (ranked):
  1. [<id>] <name> — fills <N1> srv, tier <t>, uses on-hand <items>, <why>
  2. [<id>] <name> — ...
If no good fit: run ai/vet_recipe.md to add <type of dish> for <slot>.
```
Then the user edits the cycle yaml `selections` and re-runs `make coverage` to confirm the gap closed (no tokens).
