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
    leading numbers with trailing text ("24oz", "32 oz (~4 thighs)").

    Additive amounts ("1 Tbsp + 1 tsp") return None on purpose (2026-06-26 review #1):
    taking only the leading number silently DROPPED the "+ 1 tsp", under-buying in
    grocery AND under-depleting inventory the same way (drift every cycle). Returning
    None makes grocery flag it a CHECK item — Will confirms by hand rather than the
    system guessing low. (Full additive summing needs unit conversion; not worth the
    risk for the handful of additive entries.)

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

    # Additive amount ("1 Tbsp + 1 tsp"): a '+' joining two quantities. Don't guess the
    # leading number — return None so grocery marks it CHECK (review #1). Guard placed
    # before the leading-number regex below, which would otherwise grab just the "1".
    if "+" in s:
        return None

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


# ---- Unit conversion (for inventory netting) ----------------------------------
#
# grocery.py needs to net an on-hand quantity (e.g. inventory "Olive oil: 8 oz")
# against a recipe need in a different unit ("Olive oil: 1.5 Tbsp"). units_compatible()
# only answers "same dimensional family?" — it does NOT scale. These tables let
# convert_qty() rescale within a family so the subtraction is correct.
#
# Volume base = teaspoon (tsp). Cooking-standard US conversions. `oz` here is the
# FLUID ounce (1 fl oz = 6 tsp) — appropriate because the items that ship in oz
# and get measured in tsp/Tbsp/cup are liquids (oils, soy sauce, vinegar, yogurt).
_VOLUME_TO_TSP = {
    "tsp": 1.0,
    "tbsp": 3.0,            # 1 Tbsp = 3 tsp
    "cup": 48.0,            # 1 cup  = 48 tsp = 16 Tbsp
    "oz": 6.0,             # 1 fl oz = 6 tsp = 2 Tbsp
    "ml": 1.0 / 4.92892,   # 1 tsp ~= 4.92892 ml
    "l": 1000.0 / 4.92892,
    "pint": 96.0,
    "quart": 192.0,
}

# Weight base = gram (g). `oz`/`lb` here are weight (avoirdupois) ounces/pounds.
_WEIGHT_TO_G = {
    "g": 1.0,
    "kg": 1000.0,
    "oz": 28.3495,
    "lb": 453.592,
}

_VOLUME_UNITS = set(_VOLUME_TO_TSP)
_WEIGHT_UNITS = set(_WEIGHT_TO_G)


def _unit_token(u):
    """Leading canonical token of a (possibly descriptive) unit string."""
    n = normalize_unit(u)
    return n.split()[0] if n.split() else n


def convert_qty(qty, from_unit, to_unit):
    """Convert `qty` expressed in from_unit into to_unit. Returns a float, or None
    when the units are not in the SAME measurable family (volume or weight) — the
    caller must then fall back to a confirm/CHECK rather than a blind subtraction.

    `oz` is ambiguous (fluid vs weight). It is resolved by the OTHER unit: when one
    side is a pure-volume unit (tsp/Tbsp/cup/ml/l) oz is treated as fluid oz; when
    the other side is a pure-weight unit (lb/g/kg) oz is treated as weight oz. If
    both sides are oz it's an identity (returns qty unchanged)."""
    if qty is None:
        return None
    a = _unit_token(from_unit)
    b = _unit_token(to_unit)
    if not a or not b:
        return None
    if a == b:
        return float(qty)

    a_vol, a_wt = a in _VOLUME_TO_TSP, a in _WEIGHT_TO_G
    b_vol, b_wt = b in _VOLUME_TO_TSP, b in _WEIGHT_TO_G

    # Pick the family that BOTH units can satisfy. `oz` is in both tables, so it
    # adapts to its partner; a pure-volume vs pure-weight pair has no shared family.
    if a_vol and b_vol and not (a == "oz" and b == "oz"):
        return float(qty) * _VOLUME_TO_TSP[a] / _VOLUME_TO_TSP[b]
    if a_wt and b_wt:
        return float(qty) * _WEIGHT_TO_G[a] / _WEIGHT_TO_G[b]
    if a_vol and b_vol:
        return float(qty)
    return None


# ---- Fuzzy ingredient-name matching (for inventory netting) --------------------
#
# Recipe ingredient names are descriptive ("Olive oil (for roasting)", "Salsa or
# pico de gallo", "Fat free Greek yogurt"); inventory/snapshot names are short
# ("Olive oil", "Salsa", "Greek yogurt"). Strict equality misses these, causing
# the false buys retro bug #2 calls out. names_match() does conservative
# token-overlap matching: lowercase, drop parenthetical notes + punctuation +
# stopwords, then require that ALL content tokens of the SHORTER name appear in
# the longer name (subset containment). This keeps it safe — a false on-hand
# (telling Will he has something he doesn't) is worse than a false buy, so we
# never match on a single weak token alone.

# Words that carry no identity — prep/packaging/role descriptors. Dropped before
# matching. NOTE: deliberately does NOT include product-distinguishing modifiers
# like "powder", "flakes", "juice", "whites", "spray" — those change WHAT the item
# is (garlic powder != fresh garlic, egg whites != eggs) and are guarded separately
# by _DISTINGUISHERS below.
_NAME_STOPWORDS = {
    "fresh", "raw", "cooked", "pre-cooked", "precooked", "dry",
    "sliced", "diced", "chopped", "minced", "grated", "crushed", "shredded",
    "smashed", "trimmed", "thinly", "finely", "halved", "wedged", "cubed", "peeled",
    "the", "a", "an", "of", "or", "and", "for", "with", "per", "each", "to",
    "any", "color", "colour", "low-cal", "lite", "fat", "free",
    "fatfree", "fat-free", "skinless", "boneless", "lean", "extra", "large",
    "medium", "small", "whole", "half", "optional", "base", "topping",
    "salad", "rub", "seasoning", "sub", "station", "from", "into",
    "as", "needed", "taste", "garnish", "florets", "pack", "bag", "fork",
    # "light"/"dark"/"reduced" deliberately NOT stopwords — they distinguish
    # products (Light vs Dark vs plain Soy sauce = 3 bottles). Live in
    # _DISTINGUISHERS below. (audit 2026-06-14 #14: one "Light soy sauce"
    # consumption was depleting all three soy bottles.)
}

# Product-distinguishing tokens: if ONE name carries one of these and the other
# does not, the two are DIFFERENT products and must NOT fuzzy-match — even if the
# rest of the tokens line up. This is the guardrail that keeps "Garlic powder"
# (pantry) from covering a "Fresh garlic" (produce) need, "Corn flakes" from
# covering "corn", "Egg whites" from "Eggs", etc. A false on-hand is worse than a
# false buy, so we err toward NOT matching when a distinguisher is one-sided.
_DISTINGUISHERS = {
    "powder", "flakes", "flake", "juice", "whites", "white", "spray",
    "seeds", "seed", "frozen", "dried", "ground", "shells", "shell",
    "sauce", "vinegar", "oil", "paste", "fillet", "canned",
    # Product-grade modifiers that pick out one bottle among siblings
    # (Light/Dark/plain soy; reduced-sodium variants). One-sided presence ->
    # different product -> no match (audit 2026-06-14 #14).
    "light", "dark", "reduced",
    # "cream" distinguishes dairy products (cream cheese != shredded/other cheese,
    # sour cream != cream). Added 2026-07-18: a generic "Shredded cheese" need was
    # reading fat-free CREAM cheese as coverage (validate-cycle false-OK lesson).
    "cream",
}

# A few aliases where the short name uses a different head noun than the recipe.
# Kept tiny + explicit (conservative): each entry maps an alias token to the
# canonical token the recipe is likely to use.
_NAME_ALIASES = {
    "scallion": "scallions",
    "scallions": "scallions",
    "greenonion": "scallions",
    "pepper": "peppers",     # "bell pepper" snapshot vs "bell peppers" recipe
}


def _name_tokens(name):
    """Content tokens of an ingredient name: lowercased, parentheticals removed,
    punctuation stripped, stopwords + pure-number tokens dropped, aliases applied."""
    s = str(name).lower()
    s = re.sub(r"\([^)]*\)", " ", s)          # drop parenthetical notes
    s = re.sub(r"[^a-z0-9\s-]", " ", s)        # punctuation -> space
    toks = []
    for t in s.split():
        t = t.strip("-")
        if not t or t in _NAME_STOPWORDS:
            continue
        if t.replace(".", "").isdigit():       # pure number ("12oz" already split)
            continue
        toks.append(_NAME_ALIASES.get(t, t))
    return toks


def _depluralize_nondistinguisher(toks):
    """Fold a trailing plural on NON-distinguisher tokens so 'breast'/'breasts'
    and 'potato'/'potatoes' collapse to the same form. Distinguisher tokens
    (powder/whites/seeds/flakes/...) are left verbatim — their singular/plural
    identity is load-bearing and is judged by the _DISTINGUISHERS guard, not here.
    Length-guarded + -ss excluded so mass nouns ('molasses') and short tokens
    aren't mangled. Used ONLY for the equal-cardinality folded-equality path in
    names_match (added 2026-06-27 — 'Raw chicken breast' vs 'Chicken breasts' was
    a false BUY because the plural-s blocked the subset test)."""
    out = set()
    for t in toks:
        if t in _DISTINGUISHERS:
            out.add(t)
        elif t.endswith("ies") and len(t) > 4:
            out.add(t[:-3] + "y")               # berries->berry
        elif (t.endswith("oes") and len(t) > 4) or (t.endswith("es") and len(t) > 4 and t[-3] in "shx"):
            out.add(t[:-2])                       # potatoes->potato, dishes->dish
        elif t.endswith("s") and not t.endswith("ss") and len(t) > 3:
            out.add(t[:-1])                       # breasts->breast, eggs->egg
        else:
            out.add(t)
    return out


def names_match(recipe_name, inv_name):
    """Conservative fuzzy match between a recipe ingredient name and an on-hand
    (inventory or snapshot) name. True when, after normalization, every content
    token of the shorter token-set is contained in the longer set AND at least one
    of those shared tokens is >2 chars (avoids matching on noise like 'oil' alone
    being too generic — we still require full subset, so 'olive oil' won't match
    'avocado oil'). Returns False if either name has no content tokens."""
    a = _name_tokens(recipe_name)
    b = _name_tokens(inv_name)
    if not a or not b:
        return False
    sa, sb = set(a), set(b)
    # Guardrail: a one-sided product-distinguishing token means different products
    # (garlic powder vs fresh garlic, egg whites vs eggs). Runs on RAW tokens so the
    # distinguisher's own plurality (white/whites, seed/seeds) is judged before folding.
    if (sa & _DISTINGUISHERS) != (sb & _DISTINGUISHERS):
        return False
    if sa == sb:
        return True
    shorter, longer = (sa, sb) if len(sa) <= len(sb) else (sb, sa)
    if shorter.issubset(longer) and any(len(t) > 2 for t in shorter):
        return True
    # Singular/plural net — ONLY at EQUAL cardinality. Every false-merge risk from
    # blanket depluralization (Greens->green ⊂ {green,onion}; Oats->oat ⊂ {oat,milk})
    # is a 1-token-into-2 subset; requiring len(sa)==len(sb) admits 'chicken breast'~
    # 'chicken breasts' while excluding those. (Adversarially verified 2026-06-27.)
    if len(sa) == len(sb):
        fa, fb = _depluralize_nondistinguisher(sa), _depluralize_nondistinguisher(sb)
        if fa == fb and any(len(t) > 2 for t in fa):
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
