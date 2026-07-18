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

CYCLE_DAYS = 7  # Sat -> Fri, 7 days (all cooking Sat+Sun; week eats leftovers)


def build_need(config):
    """needed[(member, slot)] = servings for the cycle (1/day * 7), per member's
    configured slots. M1 is counted ONLY when it's a real cooked meal (e.g. Will's
    'lean protein + veg'); a freeform 'protein bar'/'shake' M1 is grab-and-go and
    not part of cook-prep coverage (added 2026-06-13 when batch-cooked M1 became a
    valid recipe slot). Work-only slots (M2/M3) that don't apply on weekend/travel
    days are reconciled via cycle exceptions, not here."""
    need = defaultdict(int)
    for m in config.get("members", []):
        mid = m["id"]
        slots = m.get("slots", {})
        for slot in slots:
            if slot == "M1":
                val = str(slots.get("M1", "")).lower()
                if "bar" in val or "shake" in val:
                    continue  # freeform grab-and-go — not cooked-prep coverage
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


def compute_coverage(config, recipes, cycle):
    """Pure compute: returns a structured coverage result (no I/O, no printing).
    This is the app-portable core — main() just renders it as text or JSON.

    Returns: {
      'cycle_date', 'rows': [{member, slot, need, planned, gap}],
      'gaps': [{member, slot, short}], 'total_short', 'covered' (bool)
    }
    """
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

    # COVER-FIRST ordering (Will 2026-07-18: "I need to make sure her meals are
    # covered with things she likes and then I'll fill in mine"). The member in
    # config.planning.cover_first (default Elena) sorts FIRST in rows/gaps, and
    # the text render leads with that member's gap analysis — plan their
    # coverage first, then fill the other member's meals around it.
    cover_first = str((config.get("planning", {}) or {}).get("cover_first", "Elena"))

    rows, gaps = [], []
    for (mid, slot) in sorted(need, key=lambda k: (k[0] != cover_first, k)):
        nd = need[(mid, slot)]
        pl = dist.get((mid, slot), 0)
        gap = nd - pl
        rows.append({"member": mid, "slot": slot, "need": nd, "planned": pl, "gap": gap})
        if gap > 0:
            gaps.append({"member": mid, "slot": slot, "short": gap})

    return {
        "cycle_date": cycle.date,
        "cover_first": cover_first,
        "rows": rows,
        "gaps": gaps,
        "total_short": sum(g["short"] for g in gaps),
        "covered": not gaps,
    }


def render_text(result, cycle_path):
    lines = [f"Coverage — cycle {result['cycle_date']} ({Path(cycle_path).name})"]

    # Lead with the cover-first member's gap analysis (plan her coverage first —
    # only meals she likes, per data/tier_list.yaml — THEN fill Will's around it).
    cf = result.get("cover_first")
    if cf:
        cf_rows = [r for r in result["rows"] if r["member"] == cf]
        cf_gaps = [g for g in result["gaps"] if g["member"] == cf]
        lines.append(f"\n== COVER FIRST: {cf} — lock her meals (tier list) before filling the rest ==")
        for r in cf_rows:
            mark = f"  <-- GAP: short {r['gap']}" if r["gap"] > 0 else "  ✓"
            lines.append(f"  {cf} {r['slot']}: need {r['need']}, planned {r['planned']}{mark}")
        if cf_gaps:
            lines.append(f"  -> FILL {cf}'s gaps FIRST (things she likes — data/tier_list.yaml), then Will's.")
        else:
            lines.append(f"  {cf} fully covered — now fill the remaining meals around her.")
        lines.append("")

    lines += [f"{'Member':6} {'Slot':4} {'Need':>5} {'Planned':>8} {'Gap':>5}",
              "-" * 32]
    for r in result["rows"]:
        flag = "  <-- GAP" if r["gap"] > 0 else ("  (over)" if r["gap"] < 0 else "")
        lines.append(f"{r['member']:6} {r['slot']:4} {r['need']:>5} {r['planned']:>8} {r['gap']:>5}{flag}")
    lines.append("")
    if result["gaps"]:
        lines.append(f"{len(result['gaps'])} gap(s), {result['total_short']} serving(s) short:")
        for g in result["gaps"]:
            lines.append(f"  - {g['member']} {g['slot']}: short {g['short']}")
        lines.append("\n-> Optionally run ai/suggest_recipes.md to fill these gaps (TOKENS).")
    else:
        lines.append("No gaps — cycle is fully covered. (no AI needed)")
    return "\n".join(lines)


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
    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)

    result = compute_coverage(config, recipes, cycle)
    if as_json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print(render_text(result, cycle_path))


if __name__ == "__main__":
    main()
