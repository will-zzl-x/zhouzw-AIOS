#!/usr/bin/env python3
"""coverage.py — DETERMINISTIC. No AI.

Servings NEEDED per slot per person, minus carryover and dining-out/covered
exceptions, vs. servings PLANNED in the cycle. Prints gaps. Gaps are the cue to
optionally run ai/suggest_recipes.md (the only AI step in this loop).

Need model: each member's active slots (from config) need 1 serving per day for
the 7-day Sat->Sat cycle. Exceptions (dining out / covered) subtract a serving
from that member+slot+day. Carryover subtracts ready servings. Planned servings
come from the cycle's slot_assignments.

Usage: python coverage.py [cycles/<date>.yaml]   (defaults to latest cycle)
"""
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models

CYCLE_DAYS = 7  # Sat -> Sat


def build_need(config):
    """needed[(member, slot)] = servings for the cycle (1/day * 7), per member's
    configured slots. M1 (protein bar / light) is not a cooked-prep slot — skip it."""
    need = defaultdict(int)
    for m in config.get("members", []):
        mid = m["id"]
        for slot in m.get("slots", {}):
            if slot == "M1":
                continue  # protein bar / light — not part of cook-prep coverage
            need[(mid, slot)] = CYCLE_DAYS
    return need


def apply_exceptions(need, cycle):
    """Each dining-out / covered meal removes one needed serving for that member+slot.
    member 'Both' applies to every member configured for that slot."""
    members = {k[0] for k in need}
    for ex in cycle.exceptions:
        slot = ex.get("slot")
        who = ex.get("member", "Both")
        targets = members if who == "Both" else {who}
        for mid in targets:
            if (mid, slot) in need and need[(mid, slot)] > 0:
                need[(mid, slot)] -= 1


def apply_carryover(planned, cycle, recipes_by_id):
    """Carryover servings act like already-planned servings for the recipe's slot.
    Assign them to the recipe's first listed meal_slot, member 'Both' bucket."""
    for c in cycle.carryover:
        rid = str(c.get("recipe_id", ""))
        servings = int(c.get("servings", 0))
        r = recipes_by_id.get(rid)
        if not r or not r.meal_slots:
            continue
        slot = f"M{r.meal_slots[0]}"
        planned[("_carryover", slot)] += servings


def build_planned(cycle):
    """planned[(member, slot)] = sum of planned servings from slot_assignments.
    'Both' is split evenly across members at print time; track raw here."""
    planned = defaultdict(int)
    for sel in cycle.selections:
        for a in sel.get("slot_assignments", []):
            planned[(a.get("member", "Both"), a.get("slot"))] += int(a.get("servings", 0))
    return planned


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    cycle_path = Path(args[0]) if args else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Run `make new-cycle` or pass cycles/<date>.yaml."); sys.exit(1)

    config = models.load_config()
    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)

    need = build_need(config)
    apply_exceptions(need, cycle)
    planned = build_planned(cycle)
    apply_carryover(planned, cycle, recipes)

    # Members configured per slot, to fan out 'Both'.
    slot_members = defaultdict(list)
    for (mid, slot) in need:
        slot_members[slot].append(mid)

    # Distribute 'Both' + '_carryover' planned servings across that slot's members.
    dist = defaultdict(int)
    for (who, slot), n in planned.items():
        if who in ("Both", "_carryover"):
            ms = slot_members.get(slot, [])
            if not ms:
                continue
            base, extra = divmod(n, len(ms))
            for i, mid in enumerate(sorted(ms)):
                dist[(mid, slot)] += base + (1 if i < extra else 0)
        else:
            dist[(who, slot)] += n

    print(f"Coverage — cycle {cycle.date} ({Path(cycle_path).name})")
    print(f"{'Member':6} {'Slot':4} {'Need':>5} {'Planned':>8} {'Gap':>5}")
    print("-" * 32)
    gaps = []
    for (mid, slot) in sorted(need):
        nd = need[(mid, slot)]
        pl = dist.get((mid, slot), 0)
        gap = nd - pl
        flag = "  <-- GAP" if gap > 0 else ("  (over)" if gap < 0 else "")
        print(f"{mid:6} {slot:4} {nd:>5} {pl:>8} {gap:>5}{flag}")
        if gap > 0:
            gaps.append((mid, slot, gap))

    print()
    if gaps:
        total = sum(g[2] for g in gaps)
        print(f"{len(gaps)} gap(s), {total} serving(s) short:")
        for mid, slot, g in gaps:
            print(f"  - {mid} {slot}: short {g}")
        print("\n-> Optionally run ai/suggest_recipes.md to fill these gaps (TOKENS).")
    else:
        print("No gaps — cycle is fully covered. (no AI needed)")


if __name__ == "__main__":
    main()
