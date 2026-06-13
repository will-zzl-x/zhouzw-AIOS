# AI Template — Produce Pairing for Homeless Leftovers (TOKENS)

**When to run:** you have leftover/odd produce with no assigned home and want each
item matched to a recipe or side this cycle. Run ONLY for genuinely ambiguous
leftovers — the common case (what's in season) is answered for free by
`data/seasonal.yaml`, no tokens.

**Output contract:** one line per produce item → the recipe/side it joins + how.
No paragraphs.

---

## Inputs
- The list of homeless produce (item + rough quantity + freshness if known).
- This cycle's `selections` (from cycles/<date>.yaml) — what's already cooking.
- `data/seasonal.yaml` (current month) — confirm it's in-season / how to treat it.
- Recipe 6 (Rotisserie + Garlic Rice) takes a **flex seasonal veggie side** — the
  natural home for odd vegetables. Note its rules: no parsley, no potatoes; air-fried
  kale goes limp in storage (sauté for batch containers, air-fry only fresh-day).

## How to assign
1. If a current recipe already calls for it (or a close sub) → fold it in there.
2. Else → assign to recipe 6's seasonal veggie side, or a steak/dinner side.
3. Respect prep rules: greens medley is most-perishable (use first); avocado
   oxidizes (slice day-of); kale sautéed for storage, not air-fried.
4. Cut-aware: roast/sauté with avocado or olive oil, salt+pepper; no heavy oil.
5. If an item truly fits nothing this cycle → say so + suggest freeze/hold or a
   quick low-cal prep (e.g. quick-pickle cucumbers, roast + fridge for snacks).

## Output format
```
<produce item> -> <recipe/side> : <prep, one line>
...
Unplaceable: <item> -> <freeze / hold / quick prep>
```
