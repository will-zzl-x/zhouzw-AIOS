#!/usr/bin/env python3
"""deplete.py — DETERMINISTIC. No AI.

Subtract a completed cycle's consumed ingredients from data/inventory.json so the
next cycle starts from a true pantry state. Consumption = sum of selected recipes'
numeric ingredients scaled by planned servings (same math as grocery.py), matched
to inventory by normalized name + compatible unit.

Safe by default: prints the proposed depletion and writes nothing unless --apply
is passed. Never drops an item below zero; non-numeric (to-taste) ingredients are
not depleted (we can't quantify them) but are listed as "used some".

Usage:
  python deplete.py [cycles/<date>.yaml]            # dry-run (shows diff)
  python deplete.py [cycles/<date>.yaml] --apply    # writes data/inventory.json
"""
import sys
import json
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models
from lib import units


def norm_name(s):
    return " ".join(str(s).lower().split())


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # cp1252-safe (same fix as grocery.py)
    except (AttributeError, ValueError):
        pass
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    apply = "--apply" in sys.argv
    cycle_path = Path(args[0]) if args else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Pass cycles/<date>.yaml."); sys.exit(1)

    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)

    # consumed[(name, unit)] = qty
    consumed = defaultdict(float)
    soft_used = set()
    for sel in cycle.selections:
        r = recipes.get(str(sel.get("recipe_id", "")))
        if not r:
            continue
        planned = int(sel.get("planned_servings", r.servings))
        ratio = planned / r.servings if r.servings else 1.0
        for ing in r.ingredients:
            q = units.parse_amount(ing.amount)
            unit = units.normalize_unit(ing.unit)
            if q is None:
                soft_used.add(norm_name(ing.name))
            else:
                consumed[(norm_name(ing.name), unit)] += q * ratio

    # Load raw inventory (preserve unknown fields on write)
    inv_path = models.INVENTORY_PATH
    raw = json.load(open(inv_path, encoding="utf-8")) if inv_path.exists() else []

    print(f"Deplete — cycle {cycle.date} ({Path(cycle_path).name})  {'[APPLY]' if apply else '[dry-run]'}\n")
    changes = []
    unnetted = []   # consumed lines that matched a name but couldn't unit-convert
    for item in raw:
        inv_name = item.get("item", "")
        inv_unit = units.normalize_unit(item.get("unit", ""))
        # Match + net using the SAME logic grocery.py uses: fuzzy names_match +
        # scaling convert_qty. The old path (`cn == name` strict equality +
        # no-scaling units_compatible) matched almost nothing — recipe ingredient
        # names carry parentheticals ("Light soy sauce (sauce)") and needs are in
        # tsp/Tbsp vs oz inventory — so deplete decremented ~zero and inventory.json
        # inflated week over week while grocery reported items "covered" (audit
        # 2026-06-14, the system's core HAVE/USE invariant was broken).
        used = 0.0
        for (cn, cu), q in consumed.items():
            if not units.names_match(cn, inv_name):
                continue
            scaled = units.convert_qty(q, cu, inv_unit)
            if scaled is None:
                unnetted.append((item.get("item"), cn, q, cu, item.get("unit")))
            else:
                used += scaled    # consumed qty re-expressed in the item's own unit
        if used > 0:
            before = float(item.get("quantity", 0) or 0)
            after = max(0.0, before - used)
            changes.append((item.get("item"), before, used, after, item.get("unit")))
            item["quantity"] = round(after, 2)

    if changes:
        print("Depleted:")
        for nm, before, used, after, u in changes:
            print(f"  {nm}: {before:g} -> {after:g} {u}  (used ~{used:.2f})")
    else:
        print("  No numeric inventory items matched this cycle's consumption.")

    if unnetted:
        print("\nName-matched but unit not convertible (confirm + adjust by hand):")
        for nm, cn, q, cu, u in unnetted:
            print(f"  - {nm} ({u}): consumed {q:.2f} {cu} of '{cn}' — units not in same family")

    if soft_used:
        print("\nUsed some (to-taste / non-numeric — not auto-depleted, eyeball these):")
        for n in sorted(soft_used):
            print(f"  - {n}")

    if apply:
        json.dump(raw, open(inv_path, "w", encoding="utf-8"), indent=2)
        print(f"\nWrote {inv_path}")
    else:
        print("\nDry-run only. Re-run with --apply to write data/inventory.json.")


if __name__ == "__main__":
    main()
