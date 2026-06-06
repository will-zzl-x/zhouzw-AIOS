# AI Template — Vet a New Recipe (TOKENS)

**When to run:** you have a new recipe from an image, URL, or pasted text and want
it added to `data/recipes.json` in the exact schema. This is one of only four
token-spending tasks in the system. Everything else is scripts.

**Output contract:** return ONE JSON object (a single recipes.json element) ready
to append. Do not return prose, do not rewrite other recipes, do not recompute the
whole file. After appending, the user runs `make validate`.

---

## Inputs to provide
- The recipe source (paste text / URL / describe the image).
- Target servings for our household (default: scale to a meal-prep batch).
- Which meal slot(s) it serves: 2 (lunch), 3 (Will solo work meal), 4 (dinner).
- Elena tier guess (S/A/B/C/D/E) or null if convenience/utility.

## Rules for the returned object
Match this schema EXACTLY (see existing entries in data/recipes.json):
```json
{
  "id": "<next unused id as a string>",
  "name": "<dish name>",
  "tier": "S|A|B|C|D|E or null",
  "meal_slots": [2 and/or 3 and/or 4],
  "servings": <int>,
  "protein": "<e.g. Chicken Thigh / Ground Beef / Salmon / Steak>",
  "ingredients": [
    {"name": "...", "amount": "...", "unit": "...", "store": "Costco|Walmart|Asian Mart|\"\"|varies"}
  ],
  "notes": "<macros if known, source, scaling notes, reheat caveats>",
  "recipe_available": true,
  "recipe_steps": ["step 1", "step 2", ...],
  "on_break": false
}
```

Hard requirements so `make validate` passes:
- **Every measured ingredient gets a baseline number in `amount` and a real `unit`.**
  Seasonings may be "to taste" with empty unit (validate warns, doesn't fail) — but
  prefer a baseline (e.g. "1 tsp") when you can infer one.
- `store` must be one of Costco / Walmart / Asian Mart (or "" / "varies" for water + flex sides).
  Default proteins+bulk → Costco; produce/pantry → Walmart; Asian sauces/noodles → Asian Mart.
- `meal_slots` values only 2, 3, 4.
- Convert units to our kitchen's working units (tsp/Tbsp/cup/oz/lb). Use lib/units
  conventions; whole-item produce (onion/garlic/bell pepper) can stay as counts.
- Honor the cut: prefer lean proteins, low-cal sauces, starch-aware. Flag in `notes`
  if the dish is carb-heavy (M3/refeed only) or doesn't reheat (M4 only, e.g. salmon
  → "reheat 325F oven/air-fryer, never microwave").
- Pick `id` = max existing numeric id + 1 (string).

## After you paste it in
```bash
# append the object to data/recipes.json (keep it valid JSON — inside the array)
make validate          # must stay PASS (warnings OK)
```
