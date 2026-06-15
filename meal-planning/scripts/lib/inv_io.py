"""inv_io.py — shared inventory-edit helpers for inventory_add / inventory_remove.

DETERMINISTIC, no AI. Centralizes name standardization, numeric validation, and
JSON read/write so the two CLI helpers stay consistent (retro #11). All I/O goes
through models.INVENTORY_PATH so the data/inventory.json schema (item, quantity,
unit, location, freshness_date) is the single source of truth.
"""
import json
from pathlib import Path

from . import models


def norm_name(s):
    """Case/whitespace-insensitive key for matching item names."""
    return " ".join(str(s).lower().split())


def standardize_name(s):
    """Collapse whitespace and capitalize the FIRST character only, leaving the
    rest as typed. This matches the existing inventory style ("White rice",
    "Chicken thighs") while preserving proper-noun casing the user typed
    ("G Hughes BBQ", "Parmigiano Reggiano"). Deterministic; never lowercases
    interior capitals."""
    s = " ".join(str(s).split())
    if not s:
        return ""
    return s[0].upper() + s[1:]


def parse_quantity(s):
    """Validate + parse a quantity to float. Returns None if not a plain number.
    Stricter than units.parse_amount: rejects ranges/fractions/trailing text so a
    fat-fingered '8lb' or '2-3' is caught instead of silently coerced."""
    try:
        return float(str(s).strip())
    except (TypeError, ValueError):
        return None


def load_raw_inventory(path: Path = None):
    """Load inventory.json as raw dicts (preserves any unknown fields on write).
    Returns [] when the file is missing."""
    path = path or models.INVENTORY_PATH
    if not Path(path).exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dump_inventory(raw):
    """Serialize the inventory list to the same 2-space-indented JSON the file
    already uses (so diffs stay minimal). Returns a string; does NOT write."""
    return json.dumps(raw, indent=2)


def write_inventory(raw, path: Path = None):
    """Write the inventory list back to disk (2-space indent + trailing newline)."""
    path = path or models.INVENTORY_PATH
    with open(path, "w", encoding="utf-8") as f:
        f.write(dump_inventory(raw))
        f.write("\n")
