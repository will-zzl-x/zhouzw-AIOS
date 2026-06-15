#!/usr/bin/env python3
"""run_week.py — the single weekly entrypoint. DETERMINISTIC, no AI, no tokens.

One command to run the read-only half of the loop for a cycle, with a PREFLIGHT
healthcheck that fails fast BEFORE any step crashes mid-output. Replaces running
coverage -> grocery -> defrost -> schedule by hand four times.

  python run_week.py [cycles/<date>.yaml]      # defaults to latest cycle
  make week CYCLE=cycles/2026-06-13.yaml

What it does:
  0. PREFLIGHT (fail fast) — UTF-8 stdout; recipes valid; inventory finite/parseable;
     cycle parseable + recipe_ids exist + slots in M1-M4 + members valid + servings ok.
     Any FAIL -> print red summary, exit 2, run NOTHING. WARN -> note + continue.
  1. coverage   — servings need vs planned, gaps
  2. grocery    — buy/check/have by store
  3. defrost    — freezer staging vs fresh-buy
  4. schedule   — ordered cook plan
  Then STOP. deplete is NOT chained — it MUTATES data/inventory.json, so it stays an
  explicit `make deplete` after you've actually cooked the week.

This orchestrates the existing scripts as subprocesses (zero behavior change to them)
and prints one clean section per step. Exit codes: 0 clean · 1 gaps/warnings · 2 preflight fail.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import models

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

SCRIPTS = Path(__file__).resolve().parent
VALID_SLOTS = models.VALID_SLOTS
VALID_MEMBERS = {"Will", "Elena", "Both"}


# ---------------------------------------------------------------------------
# PREFLIGHT — the safety net the loop lacks today. Each check returns
# (fails, warns): lists of strings. A non-empty `fails` aborts the run.
# ---------------------------------------------------------------------------
def check_recipes():
    fails, warns = [], []
    try:
        raw = models.load_recipes_raw()
    except Exception as e:
        return [f"recipes.json unreadable: {e}"], []
    ids = [r.get("id") for r in raw]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        fails.append(f"duplicate recipe id(s): {sorted(dupes)}")
    for r in raw:
        ms = r.get("meal_slots")
        if ms is not None and not isinstance(ms, list):
            fails.append(f"recipe {r.get('id')}: meal_slots is not a list ({ms!r})")
        if r.get("servings") in (None, 0):
            warns.append(f"recipe {r.get('id')} '{r.get('name','')}': servings missing/zero")
    return fails, warns


def check_inventory():
    fails, warns = [], []
    p = models.INVENTORY_PATH
    if not p.exists():
        return [], ["inventory.json missing — every item will read as a BUY"]
    try:
        raw = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return [f"inventory.json invalid JSON: {e}"], []
    import math
    for it in raw:
        q = it.get("quantity")
        try:
            qf = float(q)
            if not math.isfinite(qf):
                fails.append(f"inventory '{it.get('item')}': non-finite quantity {q!r}")
            elif qf < 0:
                fails.append(f"inventory '{it.get('item')}': negative quantity {q!r}")
        except (TypeError, ValueError):
            fails.append(f"inventory '{it.get('item')}': non-numeric quantity {q!r}")
    return fails, warns


def check_cycle(cycle_path):
    """The validation the system has NO equivalent of today (audit P2 #7)."""
    fails, warns = [], []
    try:
        cycle = models.load_cycle(cycle_path)
    except Exception as e:
        return [f"cycle unreadable: {e}"], [], None
    if not cycle.date:
        fails.append("cycle has no date")
    recipes = {r.id: r for r in models.load_recipes()}
    for sel in cycle.selections:
        rid = str(sel.get("recipe_id", ""))
        if rid not in recipes:
            fails.append(f"selection references unknown recipe_id {rid!r}")
        for sa in sel.get("slot_assignments", []):
            mem = sa.get("member")
            if mem not in VALID_MEMBERS:
                fails.append(f"recipe {rid}: invalid member {mem!r} (want {sorted(VALID_MEMBERS)})")
            slot = str(sa.get("slot", "")).upper().lstrip("M")
            if slot.isdigit() and int(slot) not in VALID_SLOTS:
                fails.append(f"recipe {rid}: slot M{slot} not in {sorted(VALID_SLOTS)}")
            srv = sa.get("servings")
            if srv is not None:
                try:
                    if float(srv) < 0:
                        fails.append(f"recipe {rid}: negative servings {srv!r}")
                except (TypeError, ValueError):
                    fails.append(f"recipe {rid}: non-numeric servings {srv!r}")
    # Soft: un-netted planned_servings warning (audit P1 #6)
    if cycle.exceptions and cycle.selections:
        warns.append("cycle has exceptions — confirm planned_servings are pre-netted "
                     "(grocery/deplete read planned_servings, not exceptions)")
    return fails, warns, cycle


def preflight(cycle_path):
    print("== PREFLIGHT ==")
    all_fails, all_warns = [], []
    rf, rw = check_recipes(); all_fails += rf; all_warns += rw
    inf, inw = check_inventory(); all_fails += inf; all_warns += inw
    cf, cw, _ = check_cycle(cycle_path); all_fails += cf; all_warns += cw
    for f in all_fails:
        print(f"  ⛔ FAIL: {f}")
    for w in all_warns:
        print(f"  🟡 warn: {w}")
    if not all_fails and not all_warns:
        print("  ✅ all checks passed")
    print()
    return all_fails, all_warns


# ---------------------------------------------------------------------------
# STEP RUNNER
# ---------------------------------------------------------------------------
def run_step(title, script, cycle_path):
    print(f"== {title} ==")
    # Force the child's stdout to UTF-8 (some scripts emit em-dash/arrow glyphs) and
    # decode with errors="replace" so one stray cp1252 byte can't blow up the reader
    # thread and swallow the whole step's output (observed on coverage.py 2026-06-14).
    import os
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / script), str(cycle_path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
    )
    out = (r.stdout or "").rstrip()
    if out:
        print(out)
    if r.returncode != 0:
        err = (r.stderr or "").rstrip()
        print(f"  ⛔ {script} exited {r.returncode}" + (f"\n{err}" if err else ""))
    print()
    return r.returncode


def run_step_json(script, cycle_path):
    """Run a step with --json and return its parsed result (or {'error': ...})."""
    import json
    import os
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / script), str(cycle_path), "--json"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
    )
    try:
        return json.loads(r.stdout)
    except (ValueError, TypeError):
        return {"error": f"{script} did not emit valid JSON", "stderr": (r.stderr or "")[:500]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cycle", nargs="?", default=None)
    ap.add_argument("--json", action="store_true",
                    help="emit the whole WeekReport as one JSON object (the app's week endpoint)")
    args = ap.parse_args()

    cycle_path = Path(args.cycle) if args.cycle else models.latest_cycle_path()
    if not cycle_path or not Path(cycle_path).exists():
        print("No cycle file. Run `make new-cycle` or pass cycles/<date>.yaml.")
        sys.exit(2)

    cycle = models.load_cycle(cycle_path)

    # --json mode: preflight + every step as ONE structured WeekReport. This object
    # IS the future app's "plan my week" endpoint — no CLI scraping.
    if args.json:
        import json
        pf_fails, pf_warns = [], []
        rf, rw = check_recipes(); pf_fails += rf; pf_warns += rw
        inf, inw = check_inventory(); pf_fails += inf; pf_warns += inw
        cf, cw, _ = check_cycle(cycle_path); pf_fails += cf; pf_warns += cw
        report = {
            "cycle_date": cycle.date,
            "cycle_file": Path(cycle_path).name,
            "grocery_day": cycle.grocery_day,
            "preflight": {"ok": not pf_fails, "fails": pf_fails, "warnings": pf_warns},
        }
        if not pf_fails:
            report["coverage"] = run_step_json("coverage.py", cycle_path)
            report["grocery"] = run_step_json("grocery.py", cycle_path)
            report["defrost"] = run_step_json("defrost.py", cycle_path)
            report["schedule"] = run_step_json("cook_schedule.py", cycle_path)
        print(json.dumps(report, indent=2))
        sys.exit(0 if not pf_fails else 2)

    print(f"WEEK {cycle.date}  ({Path(cycle_path).name})  grocery_day {cycle.grocery_day or '?'}\n")

    fails, warns = preflight(cycle_path)
    if fails:
        print(f"PREFLIGHT FAILED ({len(fails)} issue(s)) — ran nothing. Fix the above and re-run.")
        sys.exit(2)

    rc = 0
    for title, script in [("COVERAGE", "coverage.py"), ("GROCERY", "grocery.py"),
                          ("DEFROST", "defrost.py"), ("SCHEDULE", "cook_schedule.py")]:
        if run_step(title, script, cycle_path) != 0:
            rc = 1

    print("== NEXT ==")
    print("  Cook the week. When done, deplete inventory explicitly (it mutates state):")
    print(f"    make deplete CYCLE={cycle_path}            # dry-run")
    print(f"    make deplete CYCLE={cycle_path} APPLY=1    # write data/inventory.json")
    if warns:
        rc = max(rc, 1)
        print(f"\n  ({len(warns)} preflight warning(s) above — review before shopping.)")
    sys.exit(rc)


if __name__ == "__main__":
    main()
