"""Tests for validate_cycle.py's four-gate coverage rule (2026-07-18 lesson):
covered = name match AND qty > 0 AND unit-convertible AND enough. The earlier
ad-hoc validation FALSE-OK'd (a) name matches whose file qty was 0 ("Lettuce
0 head" shown as covered) and (b) name-only hits with no real unit-compatible
quantity. These tests pin each gate.

Run: python -m pytest scripts/tests/test_validate_cycle.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.models import Cycle, Ingredient, InventoryItem, Recipe
from validate_cycle import build_pool, check_cycle_inventory, check_ingredient


def _inv(item, qty, unit, loc="fridge"):
    return InventoryItem(item=item, quantity=qty, unit=unit, location=loc)


def _recipe(rid, name, ingredients, servings=4):
    return Recipe(id=rid, name=name, tier=None, meal_slots=[4], servings=servings,
                  protein="", ingredients=ingredients)


# ── gate: qty must be > 0 (the "lettuce 0 head" false-OK) ─────────────────────

def test_zero_qty_match_is_flagged_not_covered():
    pool = build_pool([_inv("Lettuce (romaine/iceberg)", 0, "head")], [])
    res = check_ingredient(Ingredient(name="Lettuce", amount="1", unit="head"), 1.0, pool)
    assert res["status"] == "ZERO"
    assert res["flag"] is True


# ── gate: a name hit alone (unit not convertible) is NEVER covered ────────────

def test_name_hit_without_unit_compatibility_is_flagged():
    # name matches, qty > 0, but 'jar' cannot convert to 'tbsp' -> UNIT?, never OK
    pool = build_pool([_inv("Chicken bouillon", 1, "jar")], [])
    res = check_ingredient(Ingredient(name="Chicken bouillon", amount="2", unit="tbsp"), 1.0, pool)
    assert res["status"] == "UNIT?"
    assert res["flag"] is True


def test_different_product_does_not_match_at_all():
    # the cream-cheese lesson: a different cheese must not name-match -> MISSING
    pool = build_pool([_inv("Shredded Mexican cheese", 8, "oz")], [])
    res = check_ingredient(Ingredient(name="Fat-free cream cheese", amount="4", unit="oz"), 1.0, pool)
    assert res["status"] == "MISSING"
    assert res["flag"] is True


# ── happy path + short ────────────────────────────────────────────────────────

def test_covered_when_all_four_gates_pass():
    pool = build_pool([_inv("Ground beef (90/10)", 6.25, "lbs", "freezer")], [])
    res = check_ingredient(Ingredient(name="Ground beef", amount="20", unit="oz"), 1.0, pool)
    assert res["status"] == "OK"
    assert res["flag"] is False
    assert res["have"] == 100.0  # 6.25 lb = 100 oz, converted into the recipe's unit


def test_short_shows_gap():
    pool = build_pool([_inv("Coleslaw mix", 1.0, "lb")], [])
    res = check_ingredient(Ingredient(name="Coleslaw mix", amount="28", unit="oz"), 1.0, pool)
    assert res["status"] == "SHORT"
    assert res["flag"] is True


def test_non_numeric_need_is_confirm():
    pool = build_pool([_inv("Salt", 25, "oz", "pantry")], [])
    res = check_ingredient(Ingredient(name="Salt", amount="to taste", unit=""), 1.0, pool)
    assert res["status"] == "CONFIRM"
    assert res["flag"] is True


# ── snapshot ADD semantics + cross-recipe contention ─────────────────────────

def test_snapshot_adds_on_top_of_inventory_and_gets_flagged_multi():
    """Snapshot ADDS to inventory.json (the documented double-count hazard): the
    same item in both places SUMS (6+6=12) — and because coverage came from
    summing 2 different rows, validate-cycle demotes it to ⚠ MULTI so the
    double-count is surfaced instead of silently OK'd."""
    pool = build_pool([_inv("Honey", 6, "oz", "pantry")],
                      [{"name": "Honey", "amount": "6", "unit": "oz"}])
    res = check_ingredient(Ingredient(name="Honey", amount="10", unit="oz"), 1.0, pool)
    assert res["status"] == "MULTI"
    assert res["flag"] is True
    assert res["have"] == 12.0


def test_multi_product_sum_never_auto_oks():
    """The cheese lesson, second form: a generic need numerically 'covered' only by
    summing several DIFFERENT cheeses must be flagged MULTI, never ✓ OK."""
    pool = build_pool([_inv("Asiago cheese", 4, "oz"),
                       _inv("Cottage cheese", 16, "oz"),
                       _inv("Ricotta cheese", 15, "oz")], [])
    res = check_ingredient(Ingredient(name="Shredded cheese (cheddar or Mexican blend)",
                                      amount="2", unit="cup"), 1.0, pool)
    assert res["status"] == "MULTI"
    assert res["flag"] is True


def test_single_row_coverage_is_ok():
    pool = build_pool([_inv("Sriracha", 17, "oz", "pantry")], [])
    res = check_ingredient(Ingredient(name="Sriracha", amount="1", unit="tbsp"), 1.0, pool)
    assert res["status"] == "OK"
    assert res["flag"] is False


def test_contention_flags_combined_overdraw():
    """Two recipes each individually covered by one bag, jointly over it -> CONTENTION."""
    recipes = {
        "1": _recipe("1", "Bowls A", [Ingredient(name="Mixed frozen veggies", amount="10", unit="oz")], 4),
        "2": _recipe("2", "Fried rice B", [Ingredient(name="Mixed frozen veggies", amount="12", unit="oz")], 4),
    }
    cycle = Cycle(date="2026-07-18", selections=[
        {"recipe_id": "1", "planned_servings": 4, "slot_assignments": []},
        {"recipe_id": "2", "planned_servings": 4, "slot_assignments": []},
    ])
    pool = build_pool([_inv("Mixed frozen veggies", 16, "oz", "freezer")], [])
    result = check_cycle_inventory(cycle, recipes, pool)
    per_recipe = [row["status"] for b in result["recipes"] for row in b["rows"]]
    assert per_recipe == ["OK", "OK"]          # each alone looks covered...
    assert len(result["contention"]) == 1      # ...but combined 22 oz > 16 oz is flagged
    assert result["contention"][0]["total_need"] == 22.0


def test_serving_ratio_scales_need():
    recipes = {"1": _recipe("1", "Scaled", [Ingredient(name="Rice", amount="8", unit="oz")], servings=4)}
    cycle = Cycle(date="2026-07-18", selections=[
        {"recipe_id": "1", "planned_servings": 8, "slot_assignments": []},   # 2x
    ])
    pool = build_pool([_inv("Rice", 12, "oz", "pantry")], [])
    result = check_cycle_inventory(cycle, recipes, pool)
    row = result["recipes"][0]["rows"][0]
    assert row["need"] == 16.0                  # 8 oz * 2
    assert row["status"] == "SHORT"             # 12 on hand < 16 needed
