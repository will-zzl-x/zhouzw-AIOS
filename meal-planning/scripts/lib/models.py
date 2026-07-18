"""Dataclasses for the meal-planning system — DETERMINISTIC, no AI.

Schema matches data/recipes.json EXACTLY (source of truth, never mutated):
  Recipe: id, name, tier, meal_slots, servings, protein, ingredients[],
          notes, recipe_available, recipe_steps[], on_break
  Ingredient: name, amount (free text), unit (free text), store

Cycle / InventoryItem / Member are local to this system (config + cycle yaml).

Loaders are pure stdlib + PyYAML. `amount` stays a STRING on the dataclass
(faithful to the file); use lib/units.parse_amount() when you need a number.
"""
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any

# Repo paths — resolve relative to this file so scripts work from any cwd.
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
ROOT = SCRIPTS_DIR.parent                      # meal-planning/
DATA = ROOT / "data"
CYCLES = ROOT / "cycles"
CYCLES_ARCHIVE = CYCLES / "archive"            # past cycles live here (preserved, never deleted)
DEPLETE_LOG_PATH = DATA / "deplete_log.json"   # cycles whose consumption was drawn down (deplete --apply)
RECIPES_PATH = DATA / "recipes.json"
CONFIG_PATH = DATA / "config.yaml"
INVENTORY_PATH = DATA / "inventory.json"
TIER_LIST_PATH = DATA / "tier_list.yaml"
SEASONAL_PATH = DATA / "seasonal.yaml"

VALID_SLOTS = {1, 2, 3, 4}  # M1 added 2026-06-13: batch-cooked M1 (e.g. pork loin + veg) now allowed, not just freeform eggs/bar
VALID_STORES = {"Costco", "Walmart", "Asian Mart"}
STORE_FLEX = {"", "varies"}  # allowed for water / flex sides


@dataclass
class Ingredient:
    name: str
    amount: str            # free text, verbatim from recipes.json
    unit: str              # free text, verbatim
    store: str = ""

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Ingredient":
        return cls(
            name=str(d.get("name", "")),
            amount=str(d.get("amount", "")),
            unit=str(d.get("unit", "")),
            store=str(d.get("store", "")),
        )


@dataclass
class Recipe:
    id: str
    name: str
    tier: Optional[str]
    meal_slots: List[int]
    servings: int
    protein: str
    ingredients: List[Ingredient]
    notes: str = ""
    recipe_available: bool = True
    recipe_steps: List[str] = field(default_factory=list)
    on_break: bool = False

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Recipe":
        # Null/shape guards (InventoryItem.quantity was already guarded with `or 0`;
        # Recipe was not — so a single malformed paste from ai/vet_recipe.md, e.g.
        # "servings": null or "meal_slots": 3, used to crash int()/the comprehension
        # and brick validate/coverage/grocery/deplete all at once). Coerce defensively;
        # validate.py is the place that REPORTS bad data — loaders shouldn't die on it.
        raw_slots = d.get("meal_slots") or []
        if not isinstance(raw_slots, list):
            raw_slots = [raw_slots]
        slots = []
        for s in raw_slots:
            try:
                slots.append(int(s))
            except (TypeError, ValueError):
                pass  # non-int slot is reported by validate.py, not fatal here
        try:
            servings = int(d.get("servings") or 0)
        except (TypeError, ValueError):
            servings = 0
        return cls(
            id=str(d.get("id", "")),
            name=str(d.get("name", "")),
            tier=d.get("tier"),
            meal_slots=slots,
            servings=servings,
            protein=str(d.get("protein", "")),
            ingredients=[Ingredient.from_dict(i) for i in (d.get("ingredients") or []) if isinstance(i, dict)],
            notes=str(d.get("notes", "")),
            recipe_available=bool(d.get("recipe_available", True)),
            recipe_steps=list(d.get("recipe_steps", [])),
            on_break=bool(d.get("on_break", False)),
        )

    @property
    def active(self) -> bool:
        """Selectable this cycle: available and not benched."""
        return self.recipe_available and not self.on_break


@dataclass
class InventoryItem:
    item: str
    quantity: float
    unit: str
    location: str = "pantry"          # fridge | freezer | pantry
    freshness_date: Optional[str] = None  # ISO date string

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "InventoryItem":
        return cls(
            item=str(d.get("item", "")),
            quantity=float(d.get("quantity", 0) or 0),
            unit=str(d.get("unit", "")),
            location=str(d.get("location", "pantry")),
            freshness_date=d.get("freshness_date"),
        )


@dataclass
class Member:
    id: str          # "Will" | "Elena"
    slots: Dict[str, str]  # e.g. {"M2": "microwave lunch", "M4": "dinner"}


@dataclass
class Cycle:
    date: str                      # cycle start (Sat), ISO
    grocery_day: str = ""
    exceptions: List[Dict[str, Any]] = field(default_factory=list)   # dining-out / covered meals
    carryover: List[Dict[str, Any]] = field(default_factory=list)    # leftover servings from last cycle
    selections: List[Dict[str, Any]] = field(default_factory=list)   # {recipe_id, planned_servings, slot_assignments}
    # ⚠ ADD semantics: inventory_snapshot ADDS to data/inventory.json (never
    # overrides). Listing an item that's already in inventory.json double-counts
    # it in grocery/validate-cycle. Deplete the prior cycle first; snapshot only
    # genuinely NEW purchases. See README "inventory_snapshot".
    inventory_snapshot: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Cycle":
        return cls(
            date=str(d.get("date", "")),
            grocery_day=str(d.get("grocery_day", "")),
            exceptions=list(d.get("exceptions", [])),
            carryover=list(d.get("carryover", [])),
            selections=list(d.get("selections", [])),
            inventory_snapshot=list(d.get("inventory_snapshot", [])),
        )


# ---- Loaders (pure I/O) ----

def load_recipes(path: Path = RECIPES_PATH) -> List[Recipe]:
    with open(path, encoding="utf-8") as f:
        return [Recipe.from_dict(r) for r in json.load(f)]


def load_recipes_raw(path: Path = RECIPES_PATH) -> List[Dict[str, Any]]:
    """Raw dicts — for validate.py, which inspects fields the dataclass coerces."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_inventory(path: Path = INVENTORY_PATH) -> List[InventoryItem]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [InventoryItem.from_dict(i) for i in json.load(f)]


def _load_yaml(path: Path) -> Any:
    import yaml
    import sys as _sys
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # A file that EXISTS but parses to None is malformed/truncated — coercing it to {}
    # silently runs all-defaults (review #4). Warn loudly; still return {} so the caller
    # doesn't crash, but Will sees the config didn't load.
    if data is None:
        print(f"  ⚠ {path.name} exists but loaded as empty (None) — malformed/truncated YAML? "
              f"running with DEFAULTS for this file.", file=_sys.stderr)
        return {}
    return data


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    return _load_yaml(path)


def load_tier_list(path: Path = TIER_LIST_PATH) -> Dict[str, Any]:
    return _load_yaml(path)


def load_seasonal(path: Path = SEASONAL_PATH) -> Dict[str, Any]:
    return _load_yaml(path)


def load_cycle(path: Path) -> Cycle:
    return Cycle.from_dict(_load_yaml(Path(path)))


def latest_cycle_path() -> Optional[Path]:
    """Newest TOP-LEVEL cycle yaml. Deliberately non-recursive: past cycles are
    moved to cycles/archive/ (see cycles/README.md) and must NOT be picked up
    here — the top level holds only the current cycle, so `make week` with no
    CYCLE arg always runs the current one. Filenames are ISO dates, so
    lexicographic sort == chronological."""
    files = sorted(CYCLES.glob("*.yaml"))
    return files[-1] if files else None


def all_cycle_paths() -> List[Path]:
    """Every cycle yaml — top-level (current) plus cycles/archive/ (past),
    sorted chronologically by filename date. For history-aware checks (e.g. the
    run_week deplete-nudge) that need to see archived cycles too."""
    files = list(CYCLES.glob("*.yaml"))
    if CYCLES_ARCHIVE.exists():
        files += list(CYCLES_ARCHIVE.glob("*.yaml"))
    return sorted(files, key=lambda p: p.stem)


def prior_cycle_path(current) -> Optional[Path]:
    """The cycle immediately BEFORE `current` (by filename date), searching both
    the top level and cycles/archive/. None if `current` is the oldest."""
    cur_stem = Path(current).stem
    older = [p for p in all_cycle_paths() if p.stem < cur_stem]
    return older[-1] if older else None


def load_deplete_log(path: Path = None) -> Dict[str, Any]:
    """The deplete log: which cycles have had `deplete --apply` run (inventory
    drawn down). Written by deplete.py, read by run_week.py's preflight nudge.
    Shape: {"applied": [{"cycle": "<stem>", "applied_at": "...", ...}, ...]}."""
    p = Path(path or DEPLETE_LOG_PATH)
    if not p.exists():
        return {"applied": []}
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not isinstance(data.get("applied"), list):
        return {"applied": []}
    return data
