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
RECIPES_PATH = DATA / "recipes.json"
CONFIG_PATH = DATA / "config.yaml"
INVENTORY_PATH = DATA / "inventory.json"
TIER_LIST_PATH = DATA / "tier_list.yaml"
SEASONAL_PATH = DATA / "seasonal.yaml"

VALID_SLOTS = {2, 3, 4}
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
        return cls(
            id=str(d.get("id", "")),
            name=str(d.get("name", "")),
            tier=d.get("tier"),
            meal_slots=[int(s) for s in d.get("meal_slots", [])],
            servings=int(d.get("servings", 0)),
            protein=str(d.get("protein", "")),
            ingredients=[Ingredient.from_dict(i) for i in d.get("ingredients", [])],
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
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    return _load_yaml(path)


def load_tier_list(path: Path = TIER_LIST_PATH) -> Dict[str, Any]:
    return _load_yaml(path)


def load_seasonal(path: Path = SEASONAL_PATH) -> Dict[str, Any]:
    return _load_yaml(path)


def load_cycle(path: Path) -> Cycle:
    return Cycle.from_dict(_load_yaml(Path(path)))


def latest_cycle_path() -> Optional[Path]:
    files = sorted(CYCLES.glob("*.yaml"))
    return files[-1] if files else None
