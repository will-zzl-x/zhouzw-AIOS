#!/usr/bin/env python3
"""validate_cycle.py — DETERMINISTIC per-ingredient inventory check for a cycle. No AI.

For a given cycle file, validates EVERY ingredient of EVERY selected recipe
against data/inventory.json (plus the cycle's inventory_snapshot, labeled) using
the same lib/units fuzzy matcher grocery/deplete use, and prints a PER-RECIPE
checklist: file value vs. need, with a ⚠ flag on anything short / zero / missing
/ unverifiable.

WHY THIS EXISTS (lesson from the 2026-07-18 cycle): an earlier ad-hoc validation
FALSE-OK'd items — a fuzzy NAME hit alone was treated as "covered" even when the
matched row's quantity was 0 ("Lettuce 0 head" shown as covered) or the match was
a different product ("cream cheese" ~ "shredded Mexican cheese"). So the rule
here is hard:

    covered  =  fuzzy-name match
                AND matched quantity > 0
                AND a real unit-compatible conversion (lib/units.convert_qty)
                AND converted on-hand >= scaled need

A name hit alone is NEVER covered. Anything that can't clear all four gates is
flagged ⚠ and surfaced for Will to confirm by hand — the script never assumes.

Statuses:
  ✓ OK       — all four gates pass via ONE matched row (shows have vs need + file row)
  ⚠ MULTI    — numerically covered, but only by SUMMING 2+ different fuzzy-matched
               rows — they may be different products (four cheeses "covering" one
               shredded-cheese need). Confirm they're really the same item.
  ⚠ SHORT    — matched + convertible but on-hand < need (shows the gap)
  ⚠ ZERO     — name matched, but every matched row has qty == 0 (the lettuce bug)
  ⚠ UNIT?    — name matched with qty > 0, but units not convertible (never auto-OK)
  ⚠ MISSING  — no inventory/snapshot row fuzzy-matches at all
  ⚠ CONFIRM  — the NEED is non-numeric ("to taste"/flex) — unverifiable, eyeball it

Also prints a CONTENTION section: inventory rows whose quantity is exceeded by
the COMBINED need across all selected recipes, even if each recipe individually
passed (e.g. two recipes both drawing on one frozen-veg bag). Conservative: a
need matched by several rows is charged to each, so contention can over-flag —
by design, it surfaces rather than assumes.

Usage:
  python validate_cycle.py [cycles/<date>.yaml] [--json]   (defaults to latest cycle)
  make validate-cycle [CYCLE=cycles/<date>.yaml]

Exit 0 = every ingredient ✓ OK; exit 1 = at least one ⚠ (or no cycle/selections).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models
from lib import units

EPS = 1e-9


def build_pool(inventory, snapshot):
    """On-hand pool = data/inventory.json rows PLUS the cycle's
    inventory_snapshot entries (labeled 'snapshot').

    ⚠ ADD SEMANTICS: the snapshot ADDS to inventory.json — it never overrides.
    An item listed in both is counted twice (that's the double-count bug the
    README documents); the snapshot is for genuinely NEW purchases only.

    Unlike grocery.py's pool, qty==0 rows are KEPT here — not to cover anything
    (they can't; the qty>0 gate excludes them) but so a zero row is REPORTED as
    ⚠ ZERO instead of blending into MISSING. That's the whole point of this
    script: show the file value, don't hide it."""
    pool = []
    for it in inventory:
        pool.append({
            "name": it.item,
            "qty": float(it.quantity or 0),
            "unit": units.normalize_unit(it.unit),
            "raw_unit": it.unit,
            "source": "inventory",
            "loc": it.location,
        })
    for snap in snapshot or []:
        q = units.parse_amount(snap.get("amount"))
        pool.append({
            "name": str(snap.get("name", "")),
            "qty": float(q) if q is not None else None,  # None = present-but-unmeasured
            "unit": units.normalize_unit(snap.get("unit", "")),
            "raw_unit": str(snap.get("unit", "")),
            "source": "snapshot",
            "loc": "snapshot",
        })
    return pool


def check_ingredient(ing, ratio, pool):
    """One ingredient vs. the on-hand pool. Returns a result dict with:
    status, need (float|None), unit, matches (file rows), have (converted), note.
    """
    unit = units.normalize_unit(ing.unit)
    raw_need = units.parse_amount(ing.amount)
    need = raw_need * ratio if raw_need is not None else None

    matches = [m for m in pool if units.names_match(ing.name, m["name"])]
    match_desc = [
        {"item": m["name"], "qty": m["qty"], "unit": m["raw_unit"],
         "source": m["source"], "loc": m["loc"]}
        for m in matches
    ]

    # have = only qty>0 AND unit-convertible rows count (the four-gate rule)
    have = 0.0
    convertible = False
    positive_unconvertible = False
    contributors = []   # distinct file rows whose quantity actually counted
    for m in matches:
        if m["qty"] is None or m["qty"] <= 0:
            continue
        conv = units.convert_qty(m["qty"], m["unit"], unit)
        if conv is None:
            positive_unconvertible = True
        else:
            have += conv
            convertible = True
            contributors.append(m["name"])

    base = {"ingredient": ing.name, "amount": ing.amount, "unit": ing.unit,
            "need": round(need, 2) if need is not None else None,
            "have": round(have, 2) if convertible else None,
            "matches": match_desc}

    if not matches:
        return {**base, "status": "MISSING", "flag": True,
                "note": "no inventory/snapshot row matches — buy or add to inventory"}
    if all((m["qty"] is not None and m["qty"] <= 0) for m in matches):
        return {**base, "status": "ZERO", "flag": True,
                "note": "matched row(s) have qty 0 — NOT covered (file says none on hand)"}
    if need is None:
        return {**base, "status": "CONFIRM", "flag": True,
                "note": f"need is non-numeric ({ing.amount!r}) — can't verify, eyeball it"}
    if not convertible:
        note = ("name-matched with qty > 0 but units not convertible — confirm by hand"
                if positive_unconvertible else
                "matched only unmeasured row(s) — confirm by hand")
        return {**base, "status": "UNIT?", "flag": True, "note": note}
    if have + EPS < need:
        return {**base, "status": "SHORT", "flag": True,
                "note": f"short {need - have:.2f} {unit}"}
    if len(contributors) > 1:
        # Numerically covered — but only by SUMMING different fuzzy-matched rows,
        # which may be different products (2026-07-18 lesson: four cheeses "covered"
        # one shredded-cheese need). Never auto-OK a summed multi-product match.
        return {**base, "status": "MULTI", "flag": True,
                "note": f"covered only by summing {len(contributors)} rows "
                        f"({' + '.join(contributors)}) — confirm same product"}
    return {**base, "status": "OK", "flag": False, "note": ""}


def check_cycle_inventory(cycle, recipes, pool):
    """Pure core (testable): per-recipe rows + cross-recipe contention.
    Returns {"recipes": [...], "contention": [...], "n_ok": int, "n_flag": int}."""
    blocks = []
    charged = {}  # id(pool row) -> {"row": m, "total": float(converted), "by": [(rid, qty)]}
    for sel in cycle.selections:
        rid = str(sel.get("recipe_id", ""))
        r = recipes.get(rid)
        if not r:
            blocks.append({"recipe_id": rid, "recipe": "(unknown recipe id)",
                           "ratio": None, "rows": [], "unknown": True})
            continue
        planned = int(sel.get("planned_servings", r.servings))
        ratio = planned / r.servings if r.servings else 1.0
        rows = []
        for ing in r.ingredients:
            res = check_ingredient(ing, ratio, pool)
            rows.append(res)
            # contention bookkeeping: charge this need to every convertible match
            raw_need = units.parse_amount(ing.amount)
            if raw_need is None:
                continue
            need = raw_need * ratio
            unit = units.normalize_unit(ing.unit)
            for m in pool:
                if m["qty"] is None or m["qty"] <= 0:
                    continue
                if not units.names_match(ing.name, m["name"]):
                    continue
                conv_need = units.convert_qty(need, unit, m["unit"])
                if conv_need is None:
                    continue
                slot = charged.setdefault(id(m), {"row": m, "total": 0.0, "by": []})
                slot["total"] += conv_need
                slot["by"].append((rid, round(conv_need, 2)))
        blocks.append({"recipe_id": rid, "recipe": r.name,
                       "planned_servings": planned, "ratio": round(ratio, 2),
                       "rows": rows, "unknown": False})

    contention = []
    for slot in charged.values():
        m, total = slot["row"], slot["total"]
        if total > m["qty"] + EPS and len(slot["by"]) > 1:
            contention.append({
                "item": m["name"], "have": m["qty"], "unit": m["raw_unit"],
                "total_need": round(total, 2),
                "recipes": [f"#{rid} ({q} {m['raw_unit']})" for rid, q in slot["by"]],
            })

    all_rows = [row for b in blocks for row in b["rows"]]
    return {
        "recipes": blocks,
        "contention": contention,
        "n_ok": sum(1 for r in all_rows if not r["flag"]),
        "n_flag": sum(1 for r in all_rows if r["flag"]),
    }


MARK = {"OK": "✓", "MULTI": "⚠ MULTI", "SHORT": "⚠ SHORT", "ZERO": "⚠ ZERO",
        "UNIT?": "⚠ UNIT?", "MISSING": "⚠ MISSING", "CONFIRM": "⚠ CONFIRM"}


def render_text(result, cycle, cycle_path):
    out = [f"Validate-cycle — {cycle.date} ({Path(cycle_path).name})",
           "Rule: covered = name match AND qty > 0 AND unit-convertible AND enough.",
           "      A fuzzy name hit alone is NEVER covered — ⚠ items are for Will to confirm.", ""]
    for b in result["recipes"]:
        if b.get("unknown"):
            out.append(f"[#{b['recipe_id']}] ⚠ UNKNOWN RECIPE ID — fix the cycle file")
            out.append("")
            continue
        out.append(f"[#{b['recipe_id']}] {b['recipe']} — {b['planned_servings']} srv (x{b['ratio']})")
        for r in b["rows"]:
            mark = MARK[r["status"]]
            need_s = f"{r['need']:g} {units.normalize_unit(r['unit'])}" if r["need"] is not None else f"'{r['amount']}'"
            file_s = "; ".join(
                f"{m['item']}: {('%g' % m['qty']) if m['qty'] is not None else '?'} {m['unit']}"
                f" ({m['source']}{'/' + m['loc'] if m['source'] == 'inventory' else ''})"
                for m in r["matches"]) or "no match"
            have_s = f" — have {r['have']:g}" if r["have"] is not None else ""
            note_s = f"  [{r['note']}]" if r["note"] else ""
            out.append(f"  {mark:10} {r['ingredient']}: need {need_s}{have_s}  <- file: {file_s}{note_s}")
        out.append("")

    if result["contention"]:
        out.append("== CONTENTION (combined across recipes — each alone may look covered) ==")
        for c in result["contention"]:
            out.append(f"  ⚠ {c['item']}: {c['have']:g} {c['unit']} on hand vs "
                       f"{c['total_need']:g} {c['unit']} total need — {', '.join(c['recipes'])}")
        out.append("")

    n_ok, n_flag = result["n_ok"], result["n_flag"]
    out.append(f"Summary: {n_ok} ✓ ok · {n_flag} ⚠ flagged"
               + (f" · {len(result['contention'])} contention" if result["contention"] else ""))
    if n_flag or result["contention"]:
        out.append("⚠ items are UNCONFIRMED — verify on hand, add to the buy list, or fix inventory.json.")
    else:
        out.append("Every ingredient verifiably covered by file quantities.")
    return "\n".join(out)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    as_json = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    cycle_path = Path(args[0]) if args else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Run `make new-cycle` or pass cycles/<date>.yaml."); sys.exit(1)

    recipes = {r.id: r for r in models.load_recipes()}
    cycle = models.load_cycle(cycle_path)
    if not cycle.selections:
        print(f"Cycle {cycle.date} has no selections — nothing to validate."); sys.exit(1)

    pool = build_pool(models.load_inventory(), cycle.inventory_snapshot)
    result = check_cycle_inventory(cycle, recipes, pool)

    if as_json:
        import json
        print(json.dumps({"cycle_date": cycle.date, "cycle_file": Path(cycle_path).name,
                          **result}, indent=2))
    else:
        print(render_text(result, cycle, cycle_path))
    sys.exit(1 if (result["n_flag"] or result["contention"]) else 0)


if __name__ == "__main__":
    main()
