#!/usr/bin/env python3
"""cook_schedule.py — DETERMINISTIC. No AI.

Order the cycle's cooks by:
  1. freshness urgency  — recipes with most-perishable ingredients first
                          (greens medley, fresh fish, herbs) per recipe notes
  2. marinade lead      — needs overnight marinade -> stage the night before
  3. slow-cooker / long-simmer first  — long unattended cooks start early in the day
  4. rotisserie Saturday — rotisserie breakdown is the Saturday anchor
  5. parallelizable / standard — everything else

Priority weights come from config.cook_priority. Signals are read from each
recipe's notes + steps with simple keyword matching (no AI). Also surfaces the
relevant cooking_rules from config as reminders.

Usage: python cook_schedule.py [cycles/<date>.yaml]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models

PERISHABLE = ("greens medley", "salmon", "poke", "fish", "most perishable",
              "use greens", "fresh", "avocado", "herbs", "cilantro")
MARINADE = ("marinate", "marinade", "overnight", "dry brine", "dry-brine")
SLOW_LONG = ("slow cooker", "slow-cooker", "simmer", "braise", "dutch oven",
             "45-60 min", "instant pot", "low 4 hour", "low 3-4")
ROTISSERIE = ("rotisserie",)


def classify(r, weights):
    """Return (weight, reason) — lower weight cooks earlier.

    Checks run in SPEC PRIORITY ORDER (perishable -> marinade -> slow/long ->
    rotisserie -> standard) and return on first hit, so a recipe matching multiple
    buckets is assigned to its HIGHEST-priority one. (A salmon dish whose glaze
    'simmers' must still be cooked first for freshness, not demoted to the slow bucket.)"""
    text = (r.notes + " " + " ".join(r.recipe_steps)).lower()
    if any(k in text for k in PERISHABLE):
        return weights.get("freshness_urgency", 0), "perishable ingredients — cook first"
    if any(k in text for k in MARINADE):
        return weights.get("marinade_lead", 1), "needs marinade — stage night before"
    if any(k in text for k in SLOW_LONG):
        return weights.get("slow_or_long_simmer", 2), "slow-cooker / long simmer — start early"
    if any(k in text for k in ROTISSERIE):
        return weights.get("rotisserie_saturday", 3), "rotisserie — Saturday breakdown anchor"
    return weights.get("standard", 4), "standard — parallelizable / flexible"


def relevant_rules(r, rules):
    text = (r.notes + " " + " ".join(r.recipe_steps)).lower()
    hits = []
    for rule in rules:
        rl = rule.lower()
        # surface a rule if a distinctive keyword from it appears in the recipe
        for kw in ("dutch oven", "rotisserie", "dry-brine", "dry brine", "bouillon",
                   "day-old", "kale", "avocado oil", "olive oil"):
            if kw in rl and kw in text:
                hits.append(rule)
                break
    return hits


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # cp1252-safe glyphs (em-dash etc.)
    except (AttributeError, ValueError):
        pass
    as_json = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    cycle_path = Path(args[0]) if args else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Run `make new-cycle` or pass cycles/<date>.yaml."); sys.exit(1)

    config = models.load_config()
    weights = config.get("cook_priority", {})
    rules = config.get("cooking_rules", [])
    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)

    ordered = []
    for sel in cycle.selections:
        r = recipes.get(str(sel.get("recipe_id", "")))
        if not r:
            continue
        w, reason = classify(r, weights)
        ordered.append((w, r, reason, int(sel.get("planned_servings", r.servings))))
    ordered.sort(key=lambda x: (x[0], x[1].name))

    if as_json:
        import json
        print(json.dumps({
            "cycle_date": cycle.date,
            "cooks": [
                {"order": i, "recipe_id": r.id, "recipe": r.name, "servings": servings,
                 "meal_slots": r.meal_slots, "why": reason,
                 "rules": relevant_rules(r, rules)}
                for i, (w, r, reason, servings) in enumerate(ordered, 1)
            ],
        }, indent=2))
        return

    print(f"Cook schedule — cycle {cycle.date} ({Path(cycle_path).name})")
    print("Order: perishable -> marinade-lead -> slow/long -> rotisserie(Sat) -> standard\n")
    for i, (w, r, reason, servings) in enumerate(ordered, 1):
        print(f"  {i}. [{r.id}] {r.name}  ({servings} servings, M{'/'.join(map(str,r.meal_slots))})")
        print(f"       why: {reason}")
        for rule in relevant_rules(r, rules):
            print(f"       rule: {rule}")
    print(f"\n{len(ordered)} cook(s) scheduled. Marinade-lead items: stage the night before per defrost.py.")


if __name__ == "__main__":
    main()
