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
    """Validate + parse a quantity to float. Returns None if not a plain FINITE
    number. Stricter than units.parse_amount: rejects ranges/fractions/trailing
    text so a fat-fingered '8lb' or '2-3' is caught instead of silently coerced —
    AND rejects inf/nan, which float() happily accepts ('inf'<=0 and 'nan'<=0 are
    both False, so they slipped past the add guard and wrote literal Infinity/NaN
    into inventory.json — invalid JSON for any strict/JS parser, i.e. a future app)."""
    import math
    try:
        v = float(str(s).strip())
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


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
    """Atomically write the inventory list to disk (2-space indent + trailing
    newline). Writes to a temp file in the SAME directory, then os.replace() —
    so a crash or full disk mid-write can't truncate/corrupt inventory.json (the
    one non-regenerable file in the system). All inventory writers should route
    through here rather than truncate-in-place."""
    import os
    import tempfile
    path = Path(path or models.INVENTORY_PATH)
    payload = dump_inventory(raw) + "\n"
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".inv_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)   # atomic on the same filesystem
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
