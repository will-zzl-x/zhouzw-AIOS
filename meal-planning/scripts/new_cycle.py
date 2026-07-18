#!/usr/bin/env python3
"""new_cycle.py — interactive cycle creator. No AI.

Prompts for dates / exceptions / carryover / selected recipes, then writes
cycles/<YYYY-MM-DD>.yaml in the schema the other scripts read. Interactive by
default; supports --noninteractive to emit a skeleton (used by tests / Makefile
demo so the loop never blocks on stdin).

Always writes to the TOP LEVEL of cycles/ (the current-cycle spot) and then
auto-archives any older top-level cycle (yaml + its <date>-*.md artifacts) into
cycles/archive/ — so the top level only ever holds the cycle you're living in
(see cycles/README.md). Pass --keep-old to skip the auto-archive.

Usage:
  python new_cycle.py                 # interactive prompts
  python new_cycle.py --noninteractive [--date YYYY-MM-DD]   # skeleton cycle
  python new_cycle.py --keep-old      # don't auto-archive the prior cycle
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
    # grocery list. grocery.py nets these out via the fuzzy matcher, so populating
    # it here prevents the false-positive BUYs flagged in retro #1/#12
    # (the 2026-06-06 cycle had 20+ hand-struck buys because this was left empty).
    #
    # ⚠ ADD SEMANTICS: snapshot entries ADD to the on-hand pool ON TOP OF
    # data/inventory.json — they do NOT override or replace it. Re-listing an
    # item that's already in inventory.json DOUBLE-COUNTS it (this caused real
    # double-counting earlier). Correct pattern: run `deplete --apply` for the
    # finished cycle FIRST so inventory.json is true, then use the snapshot ONLY
    # for genuinely new purchases / items not tracked in inventory.json.
    inventory_snapshot = []
    print("\nItems already on hand for this cycle (reduce the grocery list). Blank name to finish.")
    print("  NOTE: these ADD to data/inventory.json (not override) — don't re-list items")
    print("  already tracked there, or they double-count. New/untracked purchases only.")
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


def archive_prior_cycles(new_stem):
    """Move every OTHER top-level cycle (yaml + its <date>-*.md artifacts:
    cook-plan, grocery, retro, ...) into cycles/archive/, so the top level only
    holds the new current cycle. Non-destructive: files are MOVED, never
    deleted; an existing archive file of the same name is left alone (the
    top-level copy stays put and is reported for manual review)."""
    moved, skipped = [], []
    models.CYCLES_ARCHIVE.mkdir(exist_ok=True)
    for p in sorted(models.CYCLES.glob("*.yaml")):
        if p.stem == new_stem:
            continue
        for f in [p] + sorted(models.CYCLES.glob(f"{p.stem}-*.md")):
            dest = models.CYCLES_ARCHIVE / f.name
            if dest.exists():
                skipped.append(f.name)
                continue
            f.rename(dest)
            moved.append(f.name)
    return moved, skipped


def main():
    noninteractive = "--noninteractive" in sys.argv
    keep_old = "--keep-old" in sys.argv
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

    if not keep_old:
        moved, skipped = archive_prior_cycles(cdate)
        if moved:
            print(f"Archived prior cycle file(s) -> cycles/archive/: {', '.join(moved)}")
            print("  -> update cycles/README.md (new row on top + move the CURRENT pointer)")
        if skipped:
            print(f"  ⚠ left at top level (same name already in archive/): {', '.join(skipped)}")

    print("Next: make week   (preflight will nudge if the prior cycle was never depleted)")
    print("Then: make validate-cycle   (per-ingredient inventory check before shopping)")


if __name__ == "__main__":
    main()
