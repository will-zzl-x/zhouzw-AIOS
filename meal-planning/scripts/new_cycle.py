#!/usr/bin/env python3
"""new_cycle.py — interactive cycle creator. No AI.

Prompts for dates / exceptions / carryover / selected recipes, then writes
cycles/<YYYY-MM-DD>.yaml in the schema the other scripts read. Interactive by
default; supports --noninteractive to emit a skeleton (used by tests / Makefile
demo so the loop never blocks on stdin).

Usage:
  python new_cycle.py                 # interactive prompts
  python new_cycle.py --noninteractive [--date YYYY-MM-DD]   # skeleton cycle
"""
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models


def next_saturday(d=None):
    d = d or date.today()
    # Saturday = weekday 5. Use NEXT Saturday even when run ON a Saturday — a new cycle
    # is always for the upcoming week, never today (review #6: the bare %7 returned 0 on
    # Saturdays, defaulting the cycle to today instead of +7).
    return d + timedelta(((5 - d.weekday() + 7) % 7) or 7)


def to_yaml(cycle_dict):
    import yaml
    return yaml.safe_dump(cycle_dict, sort_keys=False, allow_unicode=True)


def ask(prompt, default=""):
    try:
        v = input(f"{prompt}" + (f" [{default}]" if default else "") + ": ").strip()
    except EOFError:
        v = ""
    return v or default


def interactive():
    recipes = {r.id: r for r in models.load_recipes()}
    sat = next_saturday()
    cdate = ask("Cycle start (Saturday, YYYY-MM-DD)", sat.isoformat())
    gday = ask("Grocery day (Walmart Fri order)", (date.fromisoformat(cdate) - timedelta(days=1)).isoformat())

    print("\nActive recipes (not on_break):")
    for r in sorted(recipes.values(), key=lambda x: int(x.id)):
        if r.active:
            print(f"  {r.id:>3}  {r.name}  (tier {r.tier or '-'}, M{'/'.join(map(str,r.meal_slots))}, {r.servings} srv)")

    print("\nEnter selections. Blank recipe id to finish.")
    selections = []
    while True:
        rid = ask("  recipe id")
        if not rid:
            break
        if rid not in recipes:
            print(f"    unknown id {rid}; skipping")
            continue
        r = recipes[rid]
        pserv = ask(f"    planned servings for {r.name}", str(r.servings))
        member = ask("    member (Will/Elena/Both)", "Both")
        slot = ask(f"    slot (M{'/M'.join(map(str,r.meal_slots))})", f"M{r.meal_slots[0]}")
        selections.append({
            "recipe_id": rid,
            "planned_servings": int(pserv),
            "slot_assignments": [{"member": member, "slot": slot, "servings": int(pserv)}],
        })

    exceptions = []
    print("\nDining-out / covered meals. Blank date to finish.")
    while True:
        d = ask("  exception date (YYYY-MM-DD)")
        if not d:
            break
        exceptions.append({
            "date": d,
            "member": ask("    member (Will/Elena/Both)", "Both"),
            "slot": ask("    slot", "M4"),
            "reason": ask("    reason", "dining out"),
        })

    carryover = []
    print("\nCarryover servings from last cycle. Blank recipe id to finish.")
    while True:
        rid = ask("  carryover recipe id")
        if not rid:
            break
        carryover.append({"recipe_id": rid, "servings": int(ask("    servings", "0"))})

    # inventory_snapshot — items already on hand for THIS cycle that reduce the
    # grocery list. grocery.py + deplete.py net these out by (name, amount, unit),
    # so populating it here prevents the false-positive BUYs flagged in retro #1/#12
    # (the 2026-06-06 cycle had 20+ hand-struck buys because this was left empty).
    inventory_snapshot = []
    print("\nItems already on hand for this cycle (reduce the grocery list). Blank name to finish.")
    while True:
        nm = ask("  on-hand item name")
        if not nm:
            break
        inventory_snapshot.append({
            "name": nm,
            "amount": ask("    amount", "1"),
            "unit": ask("    unit (oz/lb/cup/slices/each...)", "each"),
            "note": ask("    note (which recipe / why)", ""),
        })

    return cdate, {
        "date": cdate, "grocery_day": gday,
        "exceptions": exceptions, "carryover": carryover,
        "selections": selections, "inventory_snapshot": inventory_snapshot,
    }


def skeleton(d=None):
    cdate = (d or next_saturday()).isoformat() if not isinstance(d, str) else d
    return cdate, {
        "date": cdate,
        "grocery_day": (date.fromisoformat(cdate) - timedelta(days=1)).isoformat(),
        "exceptions": [], "carryover": [], "selections": [], "inventory_snapshot": [],
    }


def main():
    noninteractive = "--noninteractive" in sys.argv
    dval = None
    if "--date" in sys.argv:
        dval = sys.argv[sys.argv.index("--date") + 1]
    if noninteractive:
        cdate, cyc = skeleton(dval)
    else:
        cdate, cyc = interactive()

    out = models.CYCLES / f"{cdate}.yaml"
    if out.exists():
        ans = "" if noninteractive else input(f"{out.name} exists. Overwrite? [y/N] ").strip().lower()
        if ans != "y":
            print("Aborted — existing cycle kept."); return
    models.CYCLES.mkdir(exist_ok=True)
    out.write_text(to_yaml(cyc), encoding="utf-8")
    print(f"Wrote {out}")
    print("Next: make coverage   (then grocery / defrost / schedule)")


if __name__ == "__main__":
    main()
