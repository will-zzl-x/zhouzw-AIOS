#!/usr/bin/env python3
"""defrost.py — DETERMINISTIC. No AI.

From the cycle's selected recipes + their proteins, emit a freezer->fridge
defrost-move schedule. Lead times from config.defrost_lead_hours:
  beef / thighs: 12-18h    breast: 18-24h
Move 2 nights before first cook (config.move_lead_nights), so the protein is
fully thawed with buffer. We don't have per-recipe cook dates in the schema, so
cook day = cycle start (Sat) by default unless a selection carries a cook_date.

Frozen-vs-fresh: only proteins that are typically frozen get a move line;
take-and-bake (Costco Salmon Milano) and rotisserie are skipped.

Staging source of truth = THE FREEZER (data/inventory.json items with
location == 'freezer'). A protein needs a thaw move ONLY if it's actually frozen
on hand. Three cases per selected thawable protein:
  1. In the freezer  -> emit a move line (this is the real staging job).
  2. On hand fresh/fridge (in cycle.inventory_snapshot, not freezer) -> skip,
     labeled "on hand fresh" — no staging needed.
  3. Neither -> fresh raw buy this cycle's grocery run -> skip, labeled "fresh buy".
We must NOT emit a (past-dated) move line for cases 2/3.

Bug fix (2026-06-14): the prior version checked ONLY cycle.inventory_snapshot for
"on hand", so frozen proteins recorded in data/inventory.json (e.g. 2 lb ground
beef, 8 chicken thighs) were wrongly called "fresh buy" and never got a thaw line.
The freezer is now the staging truth; the snapshot only distinguishes fresh on-hand
from a fresh buy for labeling.

Usage: python defrost.py [cycles/<date>.yaml]
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models
from lib import units  # noqa: F401 — kept for parity w/ deplete/grocery snapshot reads

# proteins we keep frozen and must thaw (others bought fresh / take-and-bake)
THAW_PROTEINS = ("beef", "thigh", "breast", "steak", "salmon", "chicken")
SKIP_RECIPE_HINTS = ("rotisserie", "milano")  # take-and-bake / fresh same-day

# Core protein nouns used to match a recipe.protein against an on-hand item name.
# Token match, not substring, so "chicken broth"/"beef bouillon" don't read as raw protein.
PROTEIN_TOKENS = ("beef", "chicken", "thigh", "thighs", "breast", "breasts",
                  "steak", "salmon", "pork", "turkey", "shrimp", "fish")

# SPECIES vs CUT: "chicken" alone is generic; "breast"/"thigh" specify the cut.
# When a recipe protein and an on-hand item share a species (chicken) BUT each
# names a DIFFERENT cut (breast vs thigh), they are NOT the same item — frozen
# chicken thighs must not satisfy a chicken-breast recipe. Cut-aware matching
# prevents that false positive (defrost staging the wrong protein).
SPECIES_TOKENS = ("beef", "chicken", "pork", "turkey", "salmon", "shrimp", "fish")
CUT_TOKENS = ("breast", "breasts", "thigh", "thighs", "steak", "steaks", "ground",
              "loin", "tenderloin", "wing", "wings", "drumstick", "drumsticks",
              # broaden so a freezer cut not in the recipe's vocabulary still
              # registers as A cut (else the guard silently no-fires — verifier
              # 2026-06-14: 'pork loin' wrongly matched 'pork shoulder'):
              "shoulder", "belly", "brisket", "chuck", "butt", "leg", "quarter",
              "ribs", "rib", "shank", "fillet", "filet", "round", "flank", "chop",
              "chops", "sirloin", "ribeye", "tenderloins", "breasts")

# Snapshot names carrying any of these are pantry derivatives (broth, seasoning,
# etc.), NOT raw protein to thaw — they share a protein word but aren't a freezer
# stage. e.g. "Chicken broth", "Beef bouillon", "Pork seasoning".
NON_RAW_QUALIFIERS = ("broth", "stock", "bouillon", "base", "seasoning",
                      "rub", "powder", "sauce", "gravy", "marinade", "paste")


def lead_hours_for(protein, config):
    table = config.get("defrost_lead_hours", {})
    p = protein.lower()
    for key, rng in table.items():
        if key.lower() in p:
            return tuple(rng)
    # default to the longer (breast) window if unknown but thawable
    return (18, 24)


def parse_iso(s, default):
    try:
        y, m, d = str(s).split("-")
        return date(int(y), int(m), int(d))
    except Exception:
        return default


def _protein_tokens(text):
    """Core protein nouns present in a free-text string (lowercased word match)."""
    words = set(re.findall(r"[a-z]+", str(text).lower()))
    return {t for t in PROTEIN_TOKENS if t in words}


def _cut_tokens(text):
    words = set(re.findall(r"[a-z]+", str(text).lower()))
    return {t for t in CUT_TOKENS if t in words}


def _species_tokens(text):
    words = set(re.findall(r"[a-z]+", str(text).lower()))
    return {t for t in SPECIES_TOKENS if t in words}


def _name_matches_protein(protein, name):
    """True when a recipe protein and an on-hand item name are the SAME raw protein.
    Cut-aware: requires a shared protein token, skips pantry derivatives, and rejects
    a same-species/different-cut collision (frozen chicken THIGHS must NOT satisfy a
    chicken BREAST recipe). If both sides name a specific cut and the cuts are
    disjoint, it's not a match even though the species agrees."""
    low = str(name).lower()
    if any(q in low for q in NON_RAW_QUALIFIERS):
        return False  # pantry derivative (broth/seasoning), not raw protein to thaw
    want = _protein_tokens(protein)
    if not (want and (want & _protein_tokens(name))):
        return False

    # Cut guard. Same species can still be a DIFFERENT product if the cuts differ
    # (frozen chicken THIGHS must not satisfy a chicken BREAST recipe; pork LOIN
    # must not satisfy pork SHOULDER). Two ways the cuts can be "explicitly different":
    p_cuts, n_cuts = _cut_tokens(protein), _cut_tokens(name)
    p_norm = {c.rstrip("s") for c in p_cuts}
    n_norm = {c.rstrip("s") for c in n_cuts}

    # (a) Both sides name a known cut, and they don't overlap -> different product.
    if p_norm and n_norm and not (p_norm & n_norm):
        return False

    # (b) The RECIPE names a known cut but the freezer item does not contain that
    # cut word at all (its descriptive words differ) -> can't confirm it's the same
    # cut, so reject. This catches the case where the freezer cut word isn't in our
    # vocabulary (e.g. recipe 'pork loin' vs freezer 'pork shoulder' when 'shoulder'
    # weren't listed). We only reject when the item HAS other content words that
    # aren't the recipe's cut — a bare 'pork' freezer item (no cut named) still
    # matches a 'pork loin' recipe (generic on-hand, give it the benefit).
    if p_norm and not n_norm:
        species = _species_tokens(protein) & _species_tokens(name)
        item_words = {w.rstrip("s") for w in re.findall(r"[a-z]+", str(name).lower())}
        # words on the item that are neither the shared species nor a recipe cut
        extra = item_words - species - p_norm - {"and", "the", "of"}
        if extra:
            return False
    return True


def protein_frozen_on_hand(protein, frozen_items):
    """True when this recipe's protein is actually IN THE FREEZER — matches a
    data/inventory.json item with location == 'freezer'. THIS is what needs a thaw
    move. `frozen_items` is a list of InventoryItem pre-filtered to freezer."""
    if not _protein_tokens(protein):
        return False
    return any(_name_matches_protein(protein, it.item) for it in frozen_items)


def protein_fresh_on_hand(protein, snapshot):
    """True when this recipe's protein appears in cycle.inventory_snapshot (fresh /
    fridge on-hand Will flagged for THIS week). Used only to LABEL a skip as 'on
    hand fresh' vs 'fresh buy' — fresh on-hand needs no freezer move either way."""
    if not _protein_tokens(protein):
        return False
    for item in snapshot or []:
        name = item.get("name", "") if isinstance(item, dict) else getattr(item, "name", "")
        if _name_matches_protein(protein, name):
            return True
    return False


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    cycle_path = Path(args[0]) if args else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Run `make new-cycle` or pass cycles/<date>.yaml."); sys.exit(1)

    config = models.load_config()
    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)
    cycle_start = parse_iso(cycle.date, date.today())
    move_nights = int(config.get("move_lead_nights", 2))

    # Staging source of truth: items physically in the freezer (data/inventory.json).
    frozen_items = [it for it in models.load_inventory()
                    if str(it.location).lower() == "freezer"]

    rows = []
    fresh_buys = []     # (recipe name, protein) — fresh raw buy this cycle's grocery run
    fresh_on_hand = []  # (recipe name, protein) — already on hand fresh/fridge (snapshot)
    for sel in cycle.selections:
        r = recipes.get(str(sel.get("recipe_id", "")))
        if not r:
            continue
        if any(h in r.name.lower() for h in SKIP_RECIPE_HINTS):
            continue
        if not any(p in r.protein.lower() for p in THAW_PROTEINS):
            continue
        # Staging decision: a thaw move is needed ONLY if the protein is in the
        # freezer. Otherwise it's fresh on hand (snapshot) or a fresh buy — both
        # skip staging, but we label them differently for the report.
        if not protein_frozen_on_hand(r.protein, frozen_items):
            if protein_fresh_on_hand(r.protein, cycle.inventory_snapshot):
                fresh_on_hand.append((r.name, r.protein))
            else:
                fresh_buys.append((r.name, r.protein))
            continue
        cook_day = parse_iso(sel.get("cook_date"), cycle_start)
        lo, hi = lead_hours_for(r.protein, config)
        move_day = cook_day - timedelta(days=move_nights)
        rows.append((move_day, cook_day, r.name, r.protein, lo, hi))

    beef_rng = config.get("defrost_lead_hours", {}).get("beef", [12, 18])
    beef_str = "-".join(str(x) for x in beef_rng) if isinstance(beef_rng, (list, tuple)) else str(beef_rng)
    print(f"Defrost schedule — cycle {cycle.date} ({Path(cycle_path).name})")
    print(f"Rule: move freezer->fridge {move_nights} nights before first cook; "
          f"beef/thighs {beef_str}h, breast 18-24h.\n")
    if not rows:
        if fresh_buys or fresh_on_hand:
            # Nothing frozen to stage. Do NOT print a (past-dated) move schedule.
            print("  No freezer staging needed this cycle.")
            if fresh_on_hand:
                print(f"  {len(fresh_on_hand)} protein(s) already on hand fresh (no thaw):")
                for name, protein in fresh_on_hand:
                    print(f"    - {protein} for '{name}' — on hand fresh")
            if fresh_buys:
                print(f"  {len(fresh_buys)} fresh-buy protein(s); buy raw on the {cycle.grocery_day or cycle.date} grocery run, cook within the week:")
                for name, protein in fresh_buys:
                    print(f"    - {protein} for '{name}' — fresh buy (not in freezer)")
        else:
            print("  No frozen proteins to thaw this cycle (take-and-bake / fresh / rotisserie only).")
        return
    rows.sort()
    for move_day, cook_day, name, protein, lo, hi in rows:
        print(f"  {move_day.isoformat()} (move) -> cook ~{cook_day.isoformat()}: "
              f"{protein} for '{name}' — thaws in {lo}-{hi}h, {move_nights}-night buffer")
    print(f"\n{len(rows)} protein(s) to stage from the freezer. Move all on the earliest date if batching the freezer pull.")
    if fresh_on_hand:
        print(f"\nAlready on hand fresh ({len(fresh_on_hand)}, no thaw needed):")
        for name, protein in fresh_on_hand:
            print(f"  - {protein} for '{name}'")
    if fresh_buys:
        print(f"\nFresh-buy this cycle ({len(fresh_buys)}, not in freezer — buy raw, no staging):")
        for name, protein in fresh_buys:
            print(f"  - {protein} for '{name}'")


if __name__ == "__main__":
    main()
