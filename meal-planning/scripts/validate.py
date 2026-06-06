#!/usr/bin/env python3
"""validate.py — DETERMINISTIC recipe-DB schema + integrity checks. No AI.

HARD FAIL (exit 1) on structural breakage:
  - duplicate recipe ids
  - meal_slots value not in {2,3,4}, or empty
  - store not in {Costco, Walmart, Asian Mart} (allowing "" / "varies" for water/flex)
  - an ingredient with BOTH amount AND unit blank that is NOT a known seasoning
  - missing required fields / wrong types

SOFT WARN (exit 0) — the seasoning allowlist:
  - amount is "to taste"/"as needed"/etc. with empty unit, on a spice/seasoning
    ("five spice", "white pepper", "salt", "chili powder", ...). recipes.json
    intentionally carries these; per Will they are warnings, not failures.

--strict promotes every WARN to a FAIL (use when hand-entering new recipes via
ai/vet_recipe.md, so future additions carry real baseline numbers).

Exit 0 = pass (warnings allowed), exit 1 = hard failure(s).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.models import load_recipes_raw, VALID_SLOTS, VALID_STORES, STORE_FLEX
from lib import units

# Seasonings/spices where "to taste" + blank unit is acceptable (warn, not fail).
SEASONING_HINTS = {
    "salt", "pepper", "five spice", "white pepper", "black pepper",
    "chili powder", "chili flakes", "garlic powder", "onion powder", "paprika",
    "cumin", "oregano", "cilantro", "scallion", "scallions", "chives", "parsley",
    "togarashi", "gochugaru", "sesame seed", "smoked paprika", "italian seasoning",
    "taco seasoning", "porcini", "seasoning", "garnish", "spring onion",
    "green onion", "oil spray", "olive oil spray", "cooking", "sriracha",
    "scallion", "ancho", "chipotle", "wasabi",
}
# Non-measured-but-legitimate amount phrases (flex sides, sprays, garnishes).
FLEX_AMOUNT_HINTS = {"flex", "as needed", "light coat", "to taste", "per cycle"}


def is_seasoning(name: str) -> bool:
    n = name.lower()
    return any(h in n for h in SEASONING_HINTS)


def validate(recipes, strict=False):
    """Return (hard_errors, warnings) lists of strings."""
    hard, warn = [], []
    seen_ids = {}

    for idx, r in enumerate(recipes):
        rid = str(r.get("id", ""))
        rname = r.get("name", f"<recipe index {idx}>")
        tag = f"[{rid}] {rname}"

        # id present + unique
        if not rid:
            hard.append(f"{tag}: missing id")
        elif rid in seen_ids:
            hard.append(f"id '{rid}' duplicated ({rname} & {seen_ids[rid]})")
        else:
            seen_ids[rid] = rname

        # required fields / types
        for fld in ("name", "meal_slots", "servings", "ingredients"):
            if fld not in r:
                hard.append(f"{tag}: missing required field '{fld}'")

        # meal_slots in {2,3,4}, non-empty
        slots = r.get("meal_slots", [])
        if not slots:
            hard.append(f"{tag}: meal_slots is empty")
        for s in slots:
            if s not in VALID_SLOTS:
                hard.append(f"{tag}: meal_slot {s!r} not in {sorted(VALID_SLOTS)}")

        # servings positive int
        sv = r.get("servings")
        if not isinstance(sv, int) or sv <= 0:
            hard.append(f"{tag}: servings {sv!r} must be a positive int")

        # tier S-E or null
        tier = r.get("tier")
        if tier not in (None, "S", "A", "B", "C", "D", "E"):
            hard.append(f"{tag}: tier {tier!r} not in S/A/B/C/D/E or null")

        # on_break boolean vs notes consistency (warn — recipes.json not modified here)
        notes_break = "ON BREAK" in str(r.get("notes", "")).upper()
        if notes_break and not r.get("on_break", False):
            warn.append(f"{tag}: notes say 'ON BREAK' but on_break=false (scripts treat it ACTIVE)")

        # ingredients
        ingrs = r.get("ingredients", [])
        if not ingrs:
            hard.append(f"{tag}: no ingredients")
        for i in ingrs:
            iname = i.get("name", "<unnamed>")
            amount = str(i.get("amount", "")).strip()
            unit = str(i.get("unit", "")).strip()
            store = i.get("store", "")

            # store membership
            if store not in VALID_STORES and store not in STORE_FLEX:
                hard.append(f"{tag}: ingredient '{iname}' bad store {store!r}")

            # amount/unit completeness
            both_blank = (not amount) and (not unit)
            no_number = units.parse_amount(amount) is None
            flex_amount = any(h in amount.lower() for h in FLEX_AMOUNT_HINTS)

            if both_blank:
                msg = f"{tag}: ingredient '{iname}' has blank amount AND unit"
                (warn if is_seasoning(iname) else hard).append(msg)
            elif no_number and not flex_amount:
                # amount is non-numeric and not a recognized flex phrase
                msg = f"{tag}: ingredient '{iname}' amount {amount!r} has no baseline number"
                (warn if is_seasoning(iname) else warn).append(msg)
            elif no_number and flex_amount and not is_seasoning(iname):
                # flex phrase on a non-seasoning (e.g. flex veggie side) — informational warn
                warn.append(f"{tag}: ingredient '{iname}' amount {amount!r} is flex (no number)")

    if strict:
        hard = hard + warn
        warn = []
    return hard, warn


def main():
    strict = "--strict" in sys.argv
    recipes = load_recipes_raw()
    hard, warn = validate(recipes, strict=strict)

    print(f"validate.py — {len(recipes)} recipes" + (" [STRICT]" if strict else ""))
    if warn:
        print(f"\n  {len(warn)} WARNING(S):")
        for w in warn:
            print(f"    ! {w}")
    if hard:
        print(f"\n  {len(hard)} HARD ERROR(S):")
        for e in hard:
            print(f"    X {e}")
        print("\nFAIL")
        sys.exit(1)
    print(f"\nPASS ({len(warn)} warning(s), 0 hard errors)")
    sys.exit(0)


if __name__ == "__main__":
    main()
