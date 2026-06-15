#!/usr/bin/env python3
"""inventory_add.py — DETERMINISTIC inventory editor. No AI.

CLI helper to safely add (or merge) an item in data/inventory.json without
hand-editing JSON (retro #11 — Will added 16 items last cycle by hand and wanted
typo-proof name standardization). Matches the InventoryItem schema in lib/models
(item, quantity, unit, location, freshness_date).

Safety: DRY-RUN by default — prints the resulting JSON to stdout and writes
NOTHING. Pass --apply to actually write data/inventory.json.

Behavior:
  - quantity must parse to a number (float); errors out otherwise.
  - item name is standardized (whitespace collapsed, first letter capitalized;
    the rest is left as typed so proper nouns like "G Hughes BBQ" survive).
  - if an item with the SAME standardized name AND a compatible unit already
    exists, quantities are SUMMED (merge) rather than duplicated.
  - if the name matches but the unit is incompatible, a SECOND row is added and
    a note is printed (we never silently merge oz into tbsp).
  - output list is sorted by item name (case-insensitive) for stable diffs.

Usage:
  python inventory_add.py "Chicken breast" 8 lb freezer
  python inventory_add.py "Chicken breast" 8 lb freezer 2026-08-01
  python inventory_add.py "Chicken breast" 8 lb freezer --apply
  positional: <item> <quantity> <unit> [location] [freshness_date]
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models
from lib import units
from lib.inv_io import (
    standardize_name, parse_quantity, load_raw_inventory, write_inventory,
    dump_inventory, norm_name,
)

VALID_LOCATIONS = {"fridge", "freezer", "pantry"}


def main():
    apply = "--apply" in sys.argv
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]

    if len(pos) < 3:
        print(__doc__.strip())
        print("\nERROR: need at least <item> <quantity> <unit>.")
        sys.exit(2)

    raw_name, raw_qty, unit = pos[0], pos[1], pos[2]
    location = pos[3] if len(pos) >= 4 else "pantry"
    freshness_date = pos[4] if len(pos) >= 5 else None

    name = standardize_name(raw_name)
    if not name:
        print("ERROR: item name is blank after standardization.")
        sys.exit(2)

    qty = parse_quantity(raw_qty)
    if qty is None:
        print(f"ERROR: quantity {raw_qty!r} is not a valid number.")
        sys.exit(2)
    if qty <= 0:
        print(f"ERROR: quantity {qty:g} must be positive for an add.")
        sys.exit(2)

    unit = str(unit).strip()
    location = str(location).strip().lower() or "pantry"
    if location not in VALID_LOCATIONS:
        print(f"WARNING: location {location!r} not in {sorted(VALID_LOCATIONS)} "
              f"(allowed but unusual).", file=sys.stderr)

    raw = load_raw_inventory()

    # Try to merge into an existing row: same standardized name + compatible unit.
    target_key = norm_name(name)
    merged_into = None
    for it in raw:
        if norm_name(it.get("item", "")) == target_key and \
                units.units_compatible(unit, it.get("unit", "")):
            before = float(it.get("quantity", 0) or 0)
            it["quantity"] = round(before + qty, 4)
            # Keep the existing canonical name; backfill missing fields.
            if location != "pantry" and it.get("location", "pantry") == "pantry":
                it["location"] = location
            if freshness_date and not it.get("freshness_date"):
                it["freshness_date"] = freshness_date
            merged_into = (it.get("item"), before, it["quantity"], it.get("unit"))
            break

    if merged_into is None:
        new_item = {
            "item": name,
            "quantity": round(qty, 4),
            "unit": unit,
            "location": location,
            "freshness_date": freshness_date,
        }
        raw.append(new_item)

    # Stable sort for clean diffs.
    raw.sort(key=lambda d: norm_name(d.get("item", "")))

    mode = "[APPLY]" if apply else "[dry-run]"
    print(f"inventory_add {mode} — \"{name}\" {qty:g} {unit} @ {location}"
          + (f" (fresh {freshness_date})" if freshness_date else ""))
    if merged_into:
        nm, b, a, u = merged_into
        print(f"  merged into existing row: {nm} {b:g} -> {a:g} {u}")
    else:
        print(f"  added new row: {name} {qty:g} {unit} @ {location}")
    print()

    out = dump_inventory(raw)
    print(out)
    # Confirm the produced text is valid JSON (re-parse round-trip).
    json.loads(out)

    if apply:
        write_inventory(raw)
        print(f"\nWrote {models.INVENTORY_PATH}")
    else:
        print("\nDry-run only. JSON above is VALID. Re-run with --apply to write "
              "data/inventory.json.")


if __name__ == "__main__":
    main()
