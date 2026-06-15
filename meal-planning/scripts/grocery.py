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
    # Windows/Anaconda default console is cp1252, which can't encode the '->' arrow
    # (U+2192) or '×' (U+00D7) this script prints — that raised UnicodeEncodeError
    # mid-output and truncated the grocery list on Will's default shell (audit
    # 2026-06-14). Force UTF-8 stdout so the loop runs without needing PYTHONIOENCODING.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass  # pre-3.7 or already-wrapped stream; still fine on a UTF-8 shell

    as_json = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    cycle_path = Path(args[0]) if args else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Run `make new-cycle` or pass cycles/<date>.yaml."); sys.exit(1)

    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)
    inventory = models.load_inventory()

    # On-hand pool: persistent pantry (data/inventory.json) PLUS this cycle's
    # inventory_snapshot (items Will flagged as already on hand for THIS week).
    # Bug #1 fix: grocery now reads cycle.inventory_snapshot exactly like deplete
    # does, so snapshot items stop showing up as false BUYs. Each entry keeps its
    # display name so fuzzy matching (bug #2) can run per-entry, not via a strict
    # name key. source = "snapshot" | "pantry".
    on_hand_pool = []  # list of dicts: {name, qty, unit, source, loc}
    for it in inventory:
        on_hand_pool.append({
            "name": it.item,
            "qty": float(it.quantity or 0),
            "unit": units.normalize_unit(it.unit),
            "source": "pantry",
            "loc": it.location,
        })
    for snap in cycle.inventory_snapshot:
        q = units.parse_amount(snap.get("amount"))
        on_hand_pool.append({
            "name": str(snap.get("name", "")),
            "qty": float(q) if q is not None else None,  # None => non-numeric on-hand
            "unit": units.normalize_unit(snap.get("unit", "")),
            "source": "snapshot",
            "loc": "snapshot",
        })

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

    # Subtract on-hand (pantry + snapshot) + decide flag. Grouped by store.
    by_store = defaultdict(list)
    for (store, name, unit), e in agg.items():
        # Bug #2 fix: match on-hand entries to this need by FUZZY NAME
        # (units.names_match — token-overlap, case-insensitive) and convert the
        # on-hand quantity into the recipe's unit (units.convert_qty — volume +
        # weight tables) before subtracting. Conservative by design: a quantity
        # only counts toward have_qty when its unit is convertible to the need's
        # unit; otherwise it's recorded as a same-name-but-uncomparable match and
        # surfaces as a CHECK (we never tell Will he's covered on a guess).
        matches = [m for m in on_hand_pool
                   if units.names_match(e["disp_name"], m["name"])]
        in_inventory = bool(matches)
        have_qty = 0.0          # on-hand, expressed in the recipe's unit
        unit_comparable = False  # at least one match was numerically nettable
        had_uncomparable = False  # matched by name but qty/unit not nettable
        match_srcs = set()
        match_units = []
        for m in matches:
            match_srcs.add(m["source"])
            if m["unit"]:
                match_units.append(m["unit"])
            conv = units.convert_qty(m["qty"], m["unit"], unit) if m["qty"] is not None else None
            if conv is not None:
                have_qty += conv
                unit_comparable = True
            else:
                had_uncomparable = True
        has_snapshot = "snapshot" in match_srcs

        # Blank-store / water flex items: no purchase needed (matches footer).
        is_water = "water" in name
        if (store in models.STORE_FLEX) and (is_water or unit == ""):
            status = "FLEX"
            line = f"{e['disp_name']} — flex/water, no purchase"
            by_store[store or "(unspecified)"].append((status, line, e["disp_name"]))
            continue

        if e["numeric"]:
            need = e["qty"]
            src = " (snapshot)" if has_snapshot else ""
            if unit_comparable:
                net = need - have_qty
                if net <= 1e-9:
                    # Fully covered by on-hand — struck, not a buy (bug #1).
                    status = "HAVE"
                    line = f"{e['disp_name']}: need {need:.2f} {unit}, have {have_qty:.2f}{src} — covered"
                else:
                    # Partially covered — show the GAP, don't strike (e.g. 6 buns
                    # on hand vs 8 needed -> buy ~2), don't re-buy the full need.
                    status = "BUY"
                    line = (f"{e['disp_name']}: need {need:.2f} {unit} "
                            f"(have {have_qty:.2f}{src}) -> buy ~{net:.2f} {unit}")
            elif in_inventory:
                # On hand by name but unit can't be netted (e.g. recipe "3 inches
                # ginger" vs snapshot in inches but as a powder sub) — confirm.
                status = "CHECK"
                iu = "/".join(sorted(set(u for u in match_units if u))) or "?"
                line = (f"{e['disp_name']}: need {need:.2f} {unit} — on hand{src} "
                        f"(unit {iu} not directly comparable); confirm coverage")
            else:
                status = "BUY"
                line = f"{e['disp_name']}: need {need:.2f} {unit} (not on hand) -> buy ~{need:.2f} {unit}"
        else:
            # non-numeric (to taste / flex) — always a CHECK, never assume
            status = "CHECK"
            seen = "; ".join(dict.fromkeys(e["raw"]))
            if has_snapshot:
                hav = " (on hand — snapshot)"
            elif in_inventory:
                hav = " (in inventory)"
            else:
                hav = " (NOT on hand — confirm)"
            line = f"{e['disp_name']} [{seen}]{hav}"

        by_store[store or "(unspecified)"].append((status, line, e["disp_name"]))

    # Output
    store_order = ["Costco", "Walmart", "Asian Mart", "(unspecified)"]
    stores = sorted(by_store, key=lambda s: store_order.index(s) if s in store_order else 99)
    order = {"BUY": 0, "CHECK": 1, "HAVE": 2, "FLEX": 3}
    mark_for = {"BUY": "[ ]", "CHECK": "[?]", "HAVE": "[x]", "FLEX": "[-]"}

    if as_json:
        import json
        out = {"cycle_date": cycle.date,
               "selections": [s.get("recipe_id", "?") for s in cycle.selections],
               "stores": {}, "n_buy": 0, "n_check": 0}
        for store in stores:
            items = []
            for status, line, disp in sorted(by_store[store], key=lambda r: order[r[0]]):
                items.append({"status": status, "item": disp, "detail": line})
                if status == "BUY":
                    out["n_buy"] += 1
                elif status == "CHECK":
                    out["n_check"] += 1
            out["stores"][store] = items
        print(json.dumps(out, indent=2))
        return

    print(f"Grocery list — cycle {cycle.date} ({Path(cycle_path).name})")
    print(f"Selections: {', '.join(s.get('recipe_id','?') for s in cycle.selections)}")
    print("Rule: every BUY/CHECK item is unconfirmed — never assume spices/sauces on hand.\n")
    n_buy = n_check = 0
    for store in stores:
        rows = sorted(by_store[store], key=lambda r: order[r[0]])
        print(f"== {store} ==")
        for status, line, _disp in rows:
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
