#!/usr/bin/env python3
"""inventory_remove.py — DETERMINISTIC inventory editor. No AI.

CLI helper to safely remove an item from data/inventory.json by NAME, or
decrement its quantity, without hand-editing JSON (retro #11 — Will removed 2
stale items by hand last cycle). Matches the InventoryItem schema in lib/models.

Safety: DRY-RUN by default — prints the resulting JSON to stdout and writes
NOTHING. Pass --apply to actually write data/inventory.json.

Behavior:
  - match is by standardized name, case-insensitive ("chicken breast" finds the
    "Chicken breast" row). Ambiguous matches (e.g. multiple units) are listed and
    aborted unless you also pass --unit to disambiguate.
  - no quantity arg -> remove the whole row.
  - a numeric quantity arg -> decrement; row is dropped when it hits <= 0
    (never goes negative). A quantity larger than on-hand drops the row and warns.
  - output list stays sorted by item name (case-insensitive) for stable diffs.

Usage:
  python inventory_remove.py "Salsa"                  # remove whole row
  python inventory_remove.py "White rice" 2 lb        # decrement by 2 lb
  python inventory_remove.py "Salsa" --apply
  python inventory_remove.py "White rice" 2 --unit lb # disambiguate by unit
  positional: <item> [quantity] [unit]
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


def get_opt(flag):
    """Return the value following --flag in argv, or None."""
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return None


def main():
    apply = "--apply" in sys.argv
    opt_unit = get_opt("--unit")

    # Positional args: skip flags and the value consumed by --unit.
    pos = []
    skip = set()
    if opt_unit is not None:
        skip.add(sys.argv.index("--unit") + 1)
    for idx, a in enumerate(sys.argv[1:], start=1):
        if a.startswith("--"):
            continue
        if idx in skip:
            continue
        pos.append(a)

    if len(pos) < 1:
        print(__doc__.strip())
        print("\nERROR: need at least <item>.")
        sys.exit(2)

    raw_name = pos[0]
    name = standardize_name(raw_name)
    if not name:
        print("ERROR: item name is blank after standardization.")
        sys.exit(2)
    target_key = norm_name(name)

    dec_qty = None
    if len(pos) >= 2:
        dec_qty = parse_quantity(pos[1])
        if dec_qty is None:
            print(f"ERROR: quantity {pos[1]!r} is not a valid number.")
            sys.exit(2)
        if dec_qty <= 0:
            print(f"ERROR: decrement {dec_qty:g} must be positive.")
            sys.exit(2)

    # unit filter: explicit --unit wins; else a 3rd positional acts as unit.
    unit_filter = opt_unit if opt_unit is not None else (pos[2] if len(pos) >= 3 else None)
    if unit_filter is not None:
        unit_filter = str(unit_filter).strip()

    raw = load_raw_inventory()

    # Candidate rows by name (+ optional unit-compatibility filter).
    candidates = []
    for i, it in enumerate(raw):
        if norm_name(it.get("item", "")) != target_key:
            continue
        if unit_filter and not units.units_compatible(unit_filter, it.get("unit", "")):
            continue
        candidates.append(i)

    if not candidates:
        hint = f" with unit ~{unit_filter!r}" if unit_filter else ""
        print(f"No inventory row matches \"{name}\"{hint}. Nothing to remove.")
        # Show near names to help.
        near = sorted({it.get("item") for it in raw
                       if target_key.split()[0] in norm_name(it.get("item", ""))})
        if near:
            print("  did you mean: " + ", ".join(near))
        sys.exit(1)

    if len(candidates) > 1:
        print(f"AMBIGUOUS: {len(candidates)} rows match \"{name}\":")
        for i in candidates:
            it = raw[i]
            print(f"  - {it.get('item')}: {float(it.get('quantity', 0) or 0):g} "
                  f"{it.get('unit')} @ {it.get('location')}")
        print("Pass --unit <unit> to disambiguate, or remove rows one at a time.")
        sys.exit(2)

    idx = candidates[0]
    it = raw[idx]
    before = float(it.get("quantity", 0) or 0)

    mode = "[APPLY]" if apply else "[dry-run]"
    action_lines = []
    if dec_qty is None:
        action_lines.append(f"removed whole row: {it.get('item')} "
                            f"({before:g} {it.get('unit')} @ {it.get('location')})")
        del raw[idx]
    else:
        after = before - dec_qty
        if after <= 0:
            if after < 0:
                action_lines.append(
                    f"WARNING: decrement {dec_qty:g} exceeds on-hand {before:g} "
                    f"{it.get('unit')} — dropping row (not going negative).")
            action_lines.append(f"removed row (hit 0): {it.get('item')} "
                               f"{before:g} -> 0 {it.get('unit')}")
            del raw[idx]
        else:
            it["quantity"] = round(after, 4)
            action_lines.append(f"decremented: {it.get('item')} "
                               f"{before:g} -> {after:g} {it.get('unit')}")

    raw.sort(key=lambda d: norm_name(d.get("item", "")))

    print(f"inventory_remove {mode} — \"{name}\""
          + (f" by {dec_qty:g}" if dec_qty is not None else " (whole row)")
          + (f" [unit ~{unit_filter}]" if unit_filter else ""))
    for ln in action_lines:
        print(f"  {ln}")
    print()

    out = dump_inventory(raw)
    print(out)
    json.loads(out)  # confirm valid JSON

    if apply:
        write_inventory(raw)
        print(f"\nWrote {models.INVENTORY_PATH}")
    else:
        print("\nDry-run only. JSON above is VALID. Re-run with --apply to write "
              "data/inventory.json.")


if __name__ == "__main__":
    main()
