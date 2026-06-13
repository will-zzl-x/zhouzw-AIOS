#!/usr/bin/env python3
"""defrost.py — DETERMINISTIC. No AI.

From the cycle's selected recipes + their proteins, emit a freezer->fridge
defrost-move schedule. Lead times from config.defrost_lead_hours:
  beef / thighs: 12-18h    breast: 18-24h
Move 2 nights before first cook (config.move_lead_nights), so the protein is
fully thawed with buffer. We don't have per-recipe cook dates in the schema, so
cook day = cycle start (Sat) by default unless a selection carries a cook_date.

Frozen-vs-fresh: only proteins that are typically frozen get a move line;
take-and-bake (Costco Salmon Milano) and rotisserie are skipped.

Usage: python defrost.py [cycles/<date>.yaml]
"""
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models

# proteins we keep frozen and must thaw (others bought fresh / take-and-bake)
THAW_PROTEINS = ("beef", "thigh", "breast", "steak", "salmon", "chicken")
SKIP_RECIPE_HINTS = ("rotisserie", "milano")  # take-and-bake / fresh same-day


def lead_hours_for(protein, config):
    table = config.get("defrost_lead_hours", {})
    p = protein.lower()
    for key, rng in table.items():
        if key.lower() in p:
            return tuple(rng)
    # default to the longer (breast) window if unknown but thawable
    return (18, 24)


def parse_iso(s, default):
    try:
        y, m, d = str(s).split("-")
        return date(int(y), int(m), int(d))
    except Exception:
        return default


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    cycle_path = Path(args[0]) if args else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Run `make new-cycle` or pass cycles/<date>.yaml."); sys.exit(1)

    config = models.load_config()
    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)
    cycle_start = parse_iso(cycle.date, date.today())
    move_nights = int(config.get("move_lead_nights", 2))

    rows = []
    for sel in cycle.selections:
        r = recipes.get(str(sel.get("recipe_id", "")))
        if not r:
            continue
        if any(h in r.name.lower() for h in SKIP_RECIPE_HINTS):
            continue
        if not any(p in r.protein.lower() for p in THAW_PROTEINS):
            continue
        cook_day = parse_iso(sel.get("cook_date"), cycle_start)
        lo, hi = lead_hours_for(r.protein, config)
        move_day = cook_day - timedelta(days=move_nights)
        rows.append((move_day, cook_day, r.name, r.protein, lo, hi))

    beef_rng = config.get("defrost_lead_hours", {}).get("beef", [12, 18])
    beef_str = "-".join(str(x) for x in beef_rng) if isinstance(beef_rng, (list, tuple)) else str(beef_rng)
    print(f"Defrost schedule — cycle {cycle.date} ({Path(cycle_path).name})")
    print(f"Rule: move freezer->fridge {move_nights} nights before first cook; "
          f"beef/thighs {beef_str}h, breast 18-24h.\n")
    if not rows:
        print("  No frozen proteins to thaw this cycle (take-and-bake / fresh / rotisserie only).")
        return
    rows.sort()
    for move_day, cook_day, name, protein, lo, hi in rows:
        print(f"  {move_day.isoformat()} (move) -> cook ~{cook_day.isoformat()}: "
              f"{protein} for '{name}' — thaws in {lo}-{hi}h, {move_nights}-night buffer")
    print(f"\n{len(rows)} protein(s) to stage. Move all on the earliest date if batching the freezer pull.")


if __name__ == "__main__":
    main()
