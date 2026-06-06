"""Unit + amount-string helpers — DETERMINISTIC, no AI.

recipes.json stores `amount` as FREE TEXT ("4", "2-3", "~1/3", "1.25", "24oz",
"to taste", "1 Tbsp + 1 tsp"). These helpers parse that into numbers when
possible and normalize units, so grocery aggregation and serving math can run
without ever calling a model.

Whole-item rounding (onion=8oz, garlic clove=0.1oz, bell pepper=6oz, shallot=2oz)
mirrors the will-zzl-x/meal-planner UnitConverter so the two systems agree if the
data is ever migrated. See README "Relationship to the meal-planner app".
"""
import re
from fractions import Fraction

# Phrases that mean "no measurable quantity" — used by validate.py's seasoning
# allowlist and by grocery.py to flag (not sum) the item.
TO_TASTE_TOKENS = {
    "to taste", "as needed", "flex", "light coat", "pinch", "varies",
    "for garnish", "garnish", "optional",
}

# Units that are volume/weight measurable vs. count/pack (informational; the
# grocery aggregator groups by exact (name, unit) string like the app does).
MEASURABLE_UNITS = {"tsp", "tbsp", "cup", "cups", "oz", "lb", "lbs", "g", "ml", "l"}

# Whole-item oz conversions (from the meal-planner app's UnitConverter.whole_items).
WHOLE_ITEM_OZ = {
    "onion": 8.0, "garlic": 0.1, "bell pepper": 6.0, "shallot": 2.0,
}


def parse_amount(amount):
    """Best-effort parse of a free-text amount string to a float.

    Returns None when the amount is non-numeric ("to taste", "as needed", etc.).
    Handles: plain ints/decimals ("4", "1.25"), fractions ("1/2", "3/4"),
    mixed ("1 1/2"), ranges ("2-3" -> midpoint), tilde/approx ("~1/3"),
    leading numbers with trailing text ("24oz", "32 oz (~4 thighs)"),
    and additive amounts ("1 Tbsp + 1 tsp" -> 1, the leading number).

    Deterministic and conservative: when in doubt, return None rather than guess.
    """
    if amount is None:
        return None
    s = str(amount).strip().lower()
    if not s:
        return None
    if any(tok in s for tok in TO_TASTE_TOKENS):
        return None

    s = s.replace("~", "").replace("about", "").strip()

    # Range "2-3" or "12-18" -> midpoint. Only when it's number-dash-number.
    m = re.match(r"^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", s)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2.0

    # Mixed number "1 1/2"
    m = re.match(r"^(\d+)\s+(\d+)/(\d+)", s)
    if m:
        return float(m.group(1)) + float(Fraction(int(m.group(2)), int(m.group(3))))

    # Pure fraction "3/4"
    m = re.match(r"^(\d+)/(\d+)", s)
    if m:
        return float(Fraction(int(m.group(1)), int(m.group(2))))

    # Leading decimal/int, optionally glued to a unit ("24oz", "1.25", "32 oz")
    m = re.match(r"^(\d+(?:\.\d+)?)", s)
    if m:
        return float(m.group(1))

    return None


def is_to_taste(amount):
    """True when the amount carries no measurable quantity."""
    return parse_amount(amount) is None


def normalize_unit(unit):
    """Lowercase + collapse common unit spellings for grouping. Non-destructive:
    returns a canonical token for measurable units, else the stripped original."""
    if not unit:
        return ""
    u = str(unit).strip().lower()
    canon = {
        "tablespoon": "tbsp", "tablespoons": "tbsp", "tbsp.": "tbsp",
        "teaspoon": "tsp", "teaspoons": "tsp", "tsp.": "tsp",
        "pound": "lb", "pounds": "lb", "lbs": "lb",
        "ounce": "oz", "ounces": "oz", "oz.": "oz",
        "cups": "cup",
    }
    # Only normalize when the WHOLE unit string is a known measurable token;
    # recipes.json units are often descriptive ("thighs (1 Costco pack)") and
    # must stay verbatim so aggregation keys don't wrongly merge.
    first = u.split()[0] if u.split() else u
    return canon.get(u, canon.get(first, u))


def units_compatible(recipe_unit, inv_unit):
    """True when an inventory quantity in inv_unit can be directly compared to a
    need expressed in recipe_unit (for subtraction). Handles:
      - exact / canonical-token match ("lbs" ~ "lb", "tbsp" ~ "tablespoon")
      - descriptive recipe units: leading token match ("thighs (1 costco pack)"
        ~ "thighs", "eggs (1 per serving, fried)" ~ "eggs")
      - same dimensional family (both volume tsp/tbsp/cup, or both weight oz/lb)
    Conservative: returns False when either side is blank (caller handles flex),
    or when the families differ (e.g. recipe "tsp" vs inventory "packets")."""
    r = normalize_unit(recipe_unit)
    i = normalize_unit(inv_unit)
    if not r or not i:
        return False
    if r == i:
        return True
    rt = r.split()[0] if r.split() else r
    it = i.split()[0] if i.split() else i
    if rt == it:
        return True
    VOLUME = {"tsp", "tbsp", "cup"}
    WEIGHT = {"oz", "lb", "g"}
    if rt in VOLUME and it in VOLUME:
        return True
    if rt in WEIGHT and it in WEIGHT:
        return True
    return False


def whole_item_count(name, oz_quantity):
    """For onion/garlic/bell pepper/shallot given a total oz, return the rounded-up
    whole-item count (mirrors the app). Returns None if not a whole-item or no oz."""
    if oz_quantity is None:
        return None
    key = next((k for k in WHOLE_ITEM_OZ if k in name.lower()), None)
    if not key:
        return None
    import math
    return math.ceil(oz_quantity / WHOLE_ITEM_OZ[key])
