"""Regression tests for lib/units.py — the fuzzy-name + unit-scaling matcher that the
deplete<->grocery inventory-integrity guarantee hinges on.

Created 2026-06-26 from the adversarial review (task #100, finding #2: zero test coverage
on inventory-corrupting paths). Seeded with finding #1's additive-amount regression. These
are the load-bearing functions: a bad parse/match silently under-buys groceries or corrupts
inventory week over week, and `make validate` alone never exercises them.

Run: python -m pytest meal-planning/scripts/tests/test_units.py
"""
import sys
from pathlib import Path

# scripts/ is the import root (lib is a package under it)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.units import (
    parse_amount, is_to_taste, units_compatible, convert_qty, names_match,
)


# ── parse_amount: the quantity reader ───────────────────────────────────────────

def test_additive_amount_returns_none_not_leading_number():
    """REGRESSION (review #1): '1 Tbsp + 1 tsp' must NOT parse to 1.0 (dropping the
    '+ 1 tsp' silently under-buys + under-depletes). Returning None makes grocery flag
    it CHECK so Will confirms by hand."""
    assert parse_amount("1 Tbsp + 1 tsp") is None
    assert parse_amount("2 cups + 1 Tbsp") is None
    # and such an amount reads as 'to taste'/unmeasurable to the rest of the system
    assert is_to_taste("1 Tbsp + 1 tsp") is True

def test_parse_amount_core_forms():
    assert parse_amount("24oz") == 24.0          # glued unit
    assert parse_amount("32 oz (~4 thighs)") == 32.0  # trailing descriptive text
    assert parse_amount("2-3") == 2.5            # range -> midpoint
    assert parse_amount("12-18") == 15.0
    assert parse_amount("1 1/2") == 1.5          # mixed number
    assert parse_amount("3/4") == 0.75           # pure fraction
    assert parse_amount("1.25") == 1.25

def test_parse_amount_to_taste_and_empty():
    assert parse_amount(None) is None
    assert parse_amount("") is None
    assert parse_amount("to taste") is None
    assert is_to_taste("a pinch") is True


# ── convert_qty: the oz fluid-vs-weight resolver (the subtle one) ────────────────

def test_convert_within_volume_family():
    assert convert_qty(1, "tbsp", "tsp") == 3.0
    assert convert_qty(1, "cup", "tbsp") == 16.0

def test_convert_within_weight_family():
    assert convert_qty(1, "lb", "oz") == 16.0       # weight oz
    assert round(convert_qty(1000, "g", "kg"), 3) == 1.0

def test_convert_oz_resolves_by_partner_unit():
    """'oz' is ambiguous; the OTHER unit disambiguates. tbsp partner -> FLUID oz."""
    assert convert_qty(8, "oz", "tbsp") == 16.0     # 8 fl oz = 16 Tbsp
    # lb partner -> WEIGHT oz
    assert round(convert_qty(16, "oz", "lb"), 4) == 1.0

def test_convert_cross_family_is_none():
    """Volume vs weight has no shared family -> None (caller must CHECK, not subtract)."""
    assert convert_qty(1, "tsp", "lb") is None
    assert convert_qty(1, "cup", "g") is None

def test_convert_none_qty_and_blank():
    assert convert_qty(None, "tsp", "tbsp") is None
    assert convert_qty(1, "", "tsp") is None


# ── units_compatible: same-family gate (no scaling) ─────────────────────────────

def test_units_compatible_canonical_and_family():
    assert units_compatible("lbs", "lb") is True       # canonical spelling
    assert units_compatible("tbsp", "tablespoon") is True
    assert units_compatible("tsp", "cup") is True       # same volume family
    assert units_compatible("oz", "lb") is True         # same weight family

def test_units_incompatible_blank_or_cross_family():
    assert units_compatible("tsp", "packets") is False
    assert units_compatible("", "lb") is False
    assert units_compatible("tsp", None) is False


# ── names_match: fuzzy ingredient match + distinguisher guards ──────────────────

def test_names_match_descriptive_to_short():
    """Recipe descriptive name should match the short inventory name (subset containment)."""
    assert names_match("Olive oil (for roasting)", "Olive oil") is True
    assert names_match("Fat free Greek yogurt", "Greek yogurt") is True

def test_names_match_distinguishers_block_false_merge():
    """REGRESSION (audit 2026-06-14 #14): product-distinguishing modifiers must NOT match
    across — depleting 'Light soy sauce' must not draw down plain 'Soy sauce', and
    'Garlic powder' is not fresh 'Garlic'. A false on-hand is worse than a false buy."""
    assert names_match("Light soy sauce", "Soy sauce") is False
    assert names_match("Garlic powder", "Garlic") is False


def test_names_match_cream_is_a_distinguisher():
    """REGRESSION (2026-07-18 validate-cycle lesson): CREAM cheese must not cover a
    generic shredded-cheese need (one-sided 'cream' = different product), while
    same-product cream matches still hold."""
    assert names_match("Shredded cheese (cheddar or Mexican blend)", "Fat-free cream cheese") is False
    assert names_match("Fat free cream cheese", "Cream cheese") is True

def test_names_match_unrelated_is_false():
    assert names_match("Chicken thighs", "Olive oil") is False


# ── names_match singular/plural netting (2026-06-27 audit) ──────────────────────

def test_names_match_singular_plural_nets():
    """REGRESSION (2026-06-27): 'Raw chicken breast' vs 'Chicken breasts' was a false
    BUY — the plural-s blocked the subset test, so 5.5 lb of on-hand chicken read as
    'not on hand'. Equal-cardinality folded-equality nets singular/plural."""
    assert names_match("Raw chicken breast", "Chicken breasts") is True
    assert names_match("Chicken breast (poached/steamed, sliced)", "Chicken breasts") is True
    assert names_match("Chicken thighs", "Chicken thigh") is True
    assert names_match("Russet potatoes", "Russet potato") is True
    assert names_match("Russet potato, peeled + cubed", "Russet potatoes") is True  # 'peeled' now a stopword


def test_names_match_plural_fold_does_not_overmerge():
    """The fold is gated to EQUAL cardinality so 1-token-into-2 false merges are
    excluded (Greens != Green onion, Oats != Oat milk) — the adversarial-verify
    failures that killed the naive blanket-depluralize fix."""
    assert names_match("Greens", "Green onion") is False
    assert names_match("Oats", "Oat milk") is False
    assert names_match("Beans", "Bean sprouts") is False
    assert names_match("Peas", "Pea soup") is False
    assert names_match("Greens", "Green beans") is False
