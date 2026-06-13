#!/usr/bin/env python3
"""grocery.py — DETERMINISTIC. No AI.

Sum recipe ingredients x (planned servings / recipe base servings), subtract
inventory, group by store, FLAG every item not confirmed in inventory
("never assume spices"). Plain-text output.

Aggregation mirrors the meal-planner app: key on (ingredient_name, unit), sum
scaled quantities. recipes.json amounts are free text, so:
  - numeric amounts (parsed via lib/units) are scaled by servings ratio + summed
  - non-numeric amounts ("to taste", "flex") are listed once as CHECK items
Inventory subtraction matches on normalized item name + compatible unit; partial
matches still FLAG to confirm (we never assume an on-hand quantity covers it).

Usage: python grocery.py [cycles/<date>.yaml]   (defaults to latest cycle)
"""
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models
from lib import units


def norm_name(s):
    return " ".join(str(s).lower().split())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    cycle_path = Path(args[0]) if args else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Run `make new-cycle` or pass cycles/<date>.yaml."); sys.exit(1)

    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)
    inventory = models.load_inventory()

    # Inventory index: normalized name -> list of (qty, unit, location)
    inv_index = defaultdict(list)
    for it in inventory:
        inv_index[norm_name(it.item)].append((it.quantity, units.normalize_unit(it.unit), it.location))

    # Aggregate: (store, name, unit) -> {"qty": float|None, "raw_amounts": [str], "numeric": bool}
    agg = {}
    for sel in cycle.selections:
        rid = str(sel.get("recipe_id", ""))
        r = recipes.get(rid)
        if not r:
            print(f"  ! cycle references unknown recipe id {rid}", file=sys.stderr)
            continue
        planned = int(sel.get("planned_servings", r.servings))
        ratio = planned / r.servings if r.servings else 1.0
        for ing in r.ingredients:
            unit = units.normalize_unit(ing.unit)
            key = (ing.store or "", norm_name(ing.name), unit)
            qty = units.parse_amount(ing.amount)
            entry = agg.setdefault(key, {"qty": 0.0, "numeric": True, "raw": [], "disp_name": ing.name})
            if qty is None:
                entry["numeric"] = False
                entry["raw"].append(f"{ing.amount}".strip())
            else:
                if entry["numeric"]:
                    entry["qty"] += qty * ratio
                entry["raw"].append(f"{ing.amount} {ing.unit}".strip())

    # Subtract inventory + decide flag. Returns rows grouped by store.
    by_store = defaultdict(list)
    for (store, name, unit), e in agg.items():
        # Name-first inventory match (units in recipes.json are descriptive, e.g.
        # "thighs (1 costco pack)" vs inventory "thighs"; never gate the match on
        # the full unit string). units.units_compatible() decides whether the
        # on-hand quantity is directly comparable for subtraction.
        on_hand = inv_index.get(name, [])
        in_inventory = bool(on_hand)
        have_qty = 0.0
        unit_comparable = False
        inv_units = []
        for q, u, loc in on_hand:
            inv_units.append(u)
            if units.units_compatible(unit, u):
                have_qty += q
                unit_comparable = True

        # Blank-store / water flex items: no purchase needed (matches footer).
        is_water = "water" in name
        if (store in models.STORE_FLEX) and (is_water or unit == ""):
            status = "FLEX"
            line = f"{e['disp_name']} — flex/water, no purchase"
            by_store[store or "(unspecified)"].append((status, line))
            continue

        if e["numeric"]:
            need = e["qty"]
            if unit_comparable:
                net = need - have_qty
                if net <= 0:
                    status = "HAVE"
                    line = f"{e['disp_name']}: need {need:.2f} {unit}, have {have_qty:.2f} — covered"
                else:
                    status = "BUY"
                    line = f"{e['disp_name']}: need {need:.2f} {unit} (have {have_qty:.2f}) -> buy ~{net:.2f} {unit}"
            elif in_inventory:
                # On hand but unit can't be netted (oz vs tbsp etc.) — confirm, don't reorder blind.
                status = "CHECK"
                iu = "/".join(sorted(set(u for u in inv_units if u))) or "?"
                line = f"{e['disp_name']}: need {need:.2f} {unit} — in inventory (have {have_qty:.0f} {iu}); confirm coverage"
            else:
                status = "BUY"
                line = f"{e['disp_name']}: need {need:.2f} {unit} (not in inventory) -> buy ~{need:.2f} {unit}"
        else:
            # non-numeric (to taste / flex) — always a CHECK, never assume
            status = "CHECK"
            seen = "; ".join(dict.fromkeys(e["raw"]))
            hav = " (in inventory)" if in_inventory else " (NOT in inventory — confirm)"
            line = f"{e['disp_name']} [{seen}]{hav}"

        by_store[store or "(unspecified)"].append((status, line))

    # Output
    print(f"Grocery list — cycle {cycle.date} ({Path(cycle_path).name})")
    print(f"Selections: {', '.join(s.get('recipe_id','?') for s in cycle.selections)}")
    print("Rule: every BUY/CHECK item is unconfirmed — never assume spices/sauces on hand.\n")

    store_order = ["Costco", "Walmart", "Asian Mart", "(unspecified)"]
    stores = sorted(by_store, key=lambda s: store_order.index(s) if s in store_order else 99)
    order = {"BUY": 0, "CHECK": 1, "HAVE": 2, "FLEX": 3}
    mark_for = {"BUY": "[ ]", "CHECK": "[?]", "HAVE": "[x]", "FLEX": "[-]"}
    n_buy = n_check = 0
    for store in stores:
        rows = sorted(by_store[store], key=lambda r: order[r[0]])
        print(f"== {store} ==")
        for status, line in rows:
            print(f"  {mark_for[status]} {line}")
            if status == "BUY":
                n_buy += 1
            elif status == "CHECK":
                n_check += 1
        print()
    print(f"Summary: {n_buy} to buy, {n_check} to confirm (spices/flex/in-inventory), rest on hand.")
    print("Water and blank-store items shown under (unspecified) — no purchase needed.")


if __name__ == "__main__":
    main()
