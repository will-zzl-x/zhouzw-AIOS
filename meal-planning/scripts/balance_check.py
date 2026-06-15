#!/usr/bin/env python3
"""balance_check.py — DETERMINISTIC nutrition/variety guard. No AI.

Surfaces variety risks in a cycle's SELECTED recipes BEFORE you commit to a
grocery run (retro #10). Reads a cycle file (default latest, or arg path) +
recipes.json (source of truth, never modified). Looks at each selection's
Recipe.protein field and the recipe name to flag:

  (a) PROTEIN MONOTONY — a single protein used by >=3 selected recipes, OR
      >50% of selections sharing one protein. (We caught chicken-heavy weeks by
      hand mid-conversation last cycle; this makes it automatic.)
  (b) CUISINE CONCENTRATION — best-effort cuisine tag inferred from recipe name
      keywords (Mexican/Italian/Korean/Chinese/...). Warn when one cuisine is
      >=50% of selections (only when most selections are confidently tagged).
  (c) OMEGA-3 / FISH GAP — warn when NO selected recipe has a fish/salmon
      protein (the reason #26 salmon was added last cycle).

Counting is per SELECTED recipe (one vote per recipe in cycle.selections),
not per serving — variety is about how many distinct dishes lean on a thing.
Carryover leftovers are shown for context but don't drive the warnings (they're
last cycle's cooking, not this cycle's selection variety).

Usage: python balance_check.py [cycles/<date>.yaml]   (defaults to latest cycle)
"""
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models

# Proteins that count as fish / omega-3 sources (substring match on the
# Recipe.protein field, lowercased). Conservative: only real seafood tokens.
FISH_TOKENS = (
    "fish", "salmon", "tuna", "trout", "sardine", "mackerel", "cod",
    "tilapia", "shrimp", "prawn", "halibut", "anchov", "seafood",
)

# Best-effort cuisine inference from recipe-name keywords. First match wins,
# checked in list order. Deterministic + conservative: a name with no keyword
# is left UNTAGGED rather than guessed (untagged rows don't drive the warning).
CUISINE_KEYWORDS = [
    ("Mexican", ("crunchwrap", "taco", "burrito", "chipotle", "quesadilla",
                 "enchilada", "fajita", "carnitas", "mexican", "pico")),
    ("Korean", ("korean", "gochujang", "bibimbap", "bulgogi", "kimchi")),
    ("Chinese", ("chinese", "fried rice", "lo mein", "kung pao", "szechuan",
                 "sichuan", "hoisin", "ginger-scallion", "scallion sauce",
                 "poached chicken", "five spice")),
    ("Japanese", ("japanese", "teriyaki", "katsu", "sushi", "ramen", "udon",
                  "onigiri", "yakitori")),
    ("Thai", ("thai", "pad thai", "curry", "satay")),
    ("Mediterranean", ("hummus", "mediterranean", "greek", "falafel",
                       "tzatziki", "pita")),
    ("Italian", ("alfredo", "pasta", "fettuccine", "spaghetti", "marinara",
                 "parmesan", "italian", "lasagna", "pesto", "risotto")),
    ("American", ("burger", "sandwich", "bbq", "meatloaf", "mac and cheese",
                  "grilled cheese", "sloppy joe", "wings")),
]


def infer_cuisine(name):
    """Return a cuisine label or None (untagged) from a recipe name. First match
    wins in CUISINE_KEYWORDS order; American is intentionally last so 'BBQ
    chicken sandwich' isn't out-prioritized but specific cuisines win."""
    n = str(name).lower()
    for label, kws in CUISINE_KEYWORDS:
        if any(kw in n for kw in kws):
            return label
    return None


def norm_protein(p):
    """Display-normalize a protein label; '' / None -> 'Unspecified'."""
    p = str(p or "").strip()
    return p if p else "Unspecified"


def is_fish(protein):
    return any(tok in str(protein or "").lower() for tok in FISH_TOKENS)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    cycle_path = Path(args[0]) if args else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Run `make new-cycle` or pass cycles/<date>.yaml.")
        sys.exit(1)

    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)

    # One row per selected recipe (dedupe on recipe_id — a recipe selected once
    # but split across slots is still one dish for variety purposes).
    selected = []  # list of (rid, recipe)
    seen = set()
    unknown = []
    for sel in cycle.selections:
        rid = str(sel.get("recipe_id", ""))
        if rid in seen:
            continue
        seen.add(rid)
        r = recipes.get(rid)
        if not r:
            unknown.append(rid)
            continue
        selected.append((rid, r))

    n = len(selected)

    print(f"Balance check — cycle {cycle.date} ({Path(cycle_path).name})")
    print(f"{n} selected recipe(s): "
          f"{', '.join('#' + rid for rid, _ in selected) or '(none)'}")
    if unknown:
        print(f"  ! cycle references unknown recipe id(s): {', '.join(unknown)}",
              file=sys.stderr)
    print()

    if n == 0:
        print("No resolvable selections — nothing to balance-check.")
        sys.exit(0)

    # --- Protein tally (per selected recipe) ---
    prot_counts = defaultdict(int)
    prot_recipes = defaultdict(list)
    for rid, r in selected:
        p = norm_protein(r.protein)
        prot_counts[p] += 1
        prot_recipes[p].append(f"#{rid}")

    print("Protein spread (per selected recipe):")
    print(f"  {'Protein':18} {'Recipes':>7}  {'Share':>6}")
    print("  " + "-" * 38)
    # Sort by count desc, then name for determinism.
    for p in sorted(prot_counts, key=lambda k: (-prot_counts[k], k)):
        c = prot_counts[p]
        share = c / n
        print(f"  {p:18} {c:>7}  {share*100:>5.0f}%   ({', '.join(prot_recipes[p])})")
    print()

    # --- Cuisine tally (per selected recipe; untagged tracked separately) ---
    cuisine_counts = defaultdict(int)
    cuisine_recipes = defaultdict(list)
    untagged = 0
    for rid, r in selected:
        c = infer_cuisine(r.name)
        if c is None:
            untagged += 1
        else:
            cuisine_counts[c] += 1
            cuisine_recipes[c].append(f"#{rid}")

    if cuisine_counts:
        print("Cuisine spread (best-effort, inferred from recipe name):")
        for c in sorted(cuisine_counts, key=lambda k: (-cuisine_counts[k], k)):
            cnt = cuisine_counts[c]
            print(f"  {c:18} {cnt:>7}  ({', '.join(cuisine_recipes[c])})")
        if untagged:
            print(f"  {'(untagged)':18} {untagged:>7}")
        print()

    # --- Warnings ---
    warnings = []

    # (a) Protein monotony.
    for p in sorted(prot_counts, key=lambda k: (-prot_counts[k], k)):
        if p == "Unspecified":
            continue
        c = prot_counts[p]
        share = c / n
        if c >= 3:
            warnings.append(
                f"PROTEIN MONOTONY: {c} selected recipes use {p} "
                f"({', '.join(prot_recipes[p])}). Aim for more variety.")
        elif share > 0.5 and c >= 2:
            warnings.append(
                f"PROTEIN MONOTONY: {p} is {share*100:.0f}% of selections "
                f"({c}/{n}: {', '.join(prot_recipes[p])}). >50% share — diversify.")

    # (b) Cuisine concentration — only when most selections are confidently
    # tagged (untagged < half), so we don't cry wolf on a thin signal.
    tagged_total = sum(cuisine_counts.values())
    if tagged_total >= 2 and untagged < (n / 2.0):
        for c in sorted(cuisine_counts, key=lambda k: (-cuisine_counts[k], k)):
            cnt = cuisine_counts[c]
            if cnt / n > 0.5 and cnt >= 2:
                warnings.append(
                    f"CUISINE CONCENTRATION: {cnt}/{n} selections are {c} "
                    f"({', '.join(cuisine_recipes[c])}). Mix in another cuisine.")

    # (c) Omega-3 / fish gap.
    fish_recipes = [f"#{rid}" for rid, r in selected if is_fish(r.protein)]
    if not fish_recipes:
        warnings.append(
            "OMEGA-3 GAP: no selected recipe has a fish/seafood protein. "
            "Consider adding a salmon/fish dish (omega-3s) — last cycle this was "
            "closed by adding a salmon recipe.")

    if warnings:
        print(f"{len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  ! {w}")
    else:
        print("No balance warnings — protein/cuisine spread looks varied, "
              "fish present. (no AI needed)")

    # Carryover context (informational; doesn't drive warnings).
    if cycle.carryover:
        print("\nCarryover (last cycle's leftovers — context only, not counted):")
        for c in cycle.carryover:
            rid = str(c.get("recipe_id", ""))
            r = recipes.get(rid)
            label = f"{norm_protein(r.protein)} — {r.name}" if r else "unknown recipe"
            print(f"  - #{rid}: {label}")


if __name__ == "__main__":
    main()
