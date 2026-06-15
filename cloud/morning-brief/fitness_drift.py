"""fitness_drift.py — DETERMINISTIC drift detector for the cut. No AI, no tokens.

WHY THIS EXISTS (task #74, the half that needs NO new data source)
------------------------------------------------------------------
The cut got re-baselined TWICE because nobody saw that steps were averaging 9,165
(target 12,500) and Zone-2 was under-firing for weeks. The manual Sunday-paste habit
logged the data but nothing *watched the rolling average against target* — so the
miss only surfaced after it had already cost lead time.

The full pipeline (fitness_logger.DRAFT.py) auto-INGESTS workouts/weight/steps and is
blocked on 5 source-auth questions for Will. This module is the OTHER half: given the
data already in the repo (journals/health-log.md + journals/workout-log.md), compute
rolling averages vs. the cut targets and emit a DRIFT REPORT. It needs no new source,
no auth, no deploy — so it's useful today and gets sharper for free once the ingester
lands and the logs fill in automatically.

It is READ-ONLY on the journals. It prints a report (and returns a dict). It never
writes to the logs or state.md — surfacing the drift is the job; acting on it is Will's.

TARGETS (from context/daily-standard.md + dashboard.md Daily Consistents, NYC Cut):
  - Steps   >= 12,500/day  (raised from 10k on 6/7 — now the PRIMARY cut lever)
  - Protein >= 150 g/day
  - Calories ~1,820/day    (BMR floor; deficit phase — flag BOTH under-eating and creep)
  - Training >= 3 sessions/week (Ravage)
  - Zone-2  >= 1 Sunday 60-90 min keystone + 1 weekday 20-min (scenario C)
  - Weight  7-day rolling avg; refeed trigger at <= 176 lb (don't react to single days)

WINDOW: default 7-day rolling (the cut reads the rolling avg, never spot values).

Usage:
  python fitness_drift.py                       # parse repo logs, 7-day window, print report
  python fitness_drift.py --days 14             # 14-day window
  python fitness_drift.py --asof 2026-06-14     # pretend "today" is this date (testing/backfill)
  python fitness_drift.py --health PATH --workout PATH   # override log paths
"""
import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ---- Targets (single source of truth for the thresholds; edit here if the cut changes) ----
STEPS_TARGET = 12_500
PROTEIN_TARGET = 150          # grams
CAL_TARGET = 1_820            # BMR floor
CAL_CREEP_BAND = 250          # cals over target before we call it "creep" (rolling)
TRAIN_PER_WEEK = 3
Z2_WEEKDAY_MIN = 20           # one weekday Z2 session, minutes
Z2_SUNDAY_MIN = 60           # the Sunday keystone, minutes
WEIGHT_REFEED_AT = 176.0      # 7-day rolling avg at/under this -> add a refeed day

# A drift is "amber" within this fraction of target, "red" past it.
AMBER_FRACTION = 0.90         # >=90% of target = amber, <90% = red (for "more is better" metrics)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent   # zhouzw-AIOS/
HEALTH_LOG = REPO_ROOT / "journals" / "health-log.md"
WORKOUT_LOG = REPO_ROOT / "journals" / "workout-log.md"

ISO = "%Y-%m-%d"


def _today(asof):
    if asof:
        return datetime.strptime(asof, ISO).date()
    # Date.today() is fine in a normal CLI run; the --asof flag exists for
    # deterministic testing/backfill so we never depend on the wall clock there.
    return date.today()


# ---------------------------------------------------------------------------
# PARSERS — tolerant, line-based. The logs are hand-written markdown, so we
# extract date + metric pairs wherever they appear, rather than assuming a
# rigid schema. Every metric is OPTIONAL on any given day.
# ---------------------------------------------------------------------------
_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
_STEPS_RE = re.compile(r"steps?\D{0,4}([\d,]{3,7})", re.IGNORECASE)
_PROTEIN_RE = re.compile(r"protein\D{0,4}(\d{2,3})\s*g", re.IGNORECASE)
_CAL_RE = re.compile(r"cal(?:orie)?s?\D{0,4}([\d,]{3,5})", re.IGNORECASE)
_WEIGHT_RE = re.compile(r"(\d{2,3}\.?\d?)\s*lb", re.IGNORECASE)
_Z2_RE = re.compile(r"(?:zone[\s-]?2|z2)\D{0,8}(\d{1,3})\s*min", re.IGNORECASE)


def _to_int(s):
    try:
        return int(str(s).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _to_float(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


# Markdown weekly-table rows: '| Steps | 10,675/day (…) | 10k | … |'. The cut's
# health-log.md is written as WEEKLY SUMMARY TABLES (one block per week, source =
# Cronometer/steps screenshots), not per-day lines. A '| Metric | value | … |' row
# carries a week average; we attribute it to that week's 7 days so rolling windows
# work on the data that actually exists. (This dual format is itself the finding:
# until the ingester lands, daily granularity doesn't exist — only weekly prose.)
_TBL_ROW_RE = re.compile(r"^\s*\|\s*([A-Za-z][\w /]+?)\s*\|\s*([^|]+)\|", re.MULTILINE)


def _metric_from_row(label, value):
    """Map a weekly-table row (label, raw value cell) to (key, number)."""
    lab = label.strip().lower()
    if lab.startswith("step"):
        m = re.search(r"([\d,]{3,7})", value)
        return ("steps", _to_int(m.group(1))) if m else (None, None)
    if lab.startswith("protein"):
        m = re.search(r"(\d{2,3})\s*g", value)
        return ("protein", _to_int(m.group(1))) if m else (None, None)
    if lab.startswith("cal"):
        m = re.search(r"([\d,]{3,5})", value)
        return ("calories", _to_int(m.group(1))) if m else (None, None)
    if lab.startswith("weight"):
        m = re.search(r"(\d{2,3}\.?\d?)", value)
        return ("weight", _to_float(m.group(1))) if m else (None, None)
    return (None, None)


def parse_health_log(path):
    """Return {date: {steps, protein, calories, weight, z2_min}} from health-log.md.

    Handles BOTH formats present in the file:
      1. Per-day lines (what health_logger.py / the future ingester writes):
         'Steps: 9,165 ✗  |  Protein: 169g ✓' on a dated line.
      2. Weekly summary tables (the current hand-written format): a dated section
         header ('## 2026-05-24 — NYC Cut Week 1 baseline (May 17–23)') followed by
         '| Metric | weekly-avg | target | note |' rows. The week's avg is spread
         across the 7 days the section covers, so rolling windows have data to read.
    A day with no entry under either format is absent (low coverage = the headline)."""
    out = {}
    if not Path(path).exists():
        return out
    text = Path(path).read_text(encoding="utf-8")

    # --- Format 1: per-day metric lines ---
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            continue  # table rows handled below, not as per-day lines
        m = _DATE_RE.search(line)
        if not m:
            continue
        d = m.group(1)
        rec = out.setdefault(d, {})
        if (sm := _STEPS_RE.search(line)):
            v = _to_int(sm.group(1))
            if v and 1000 <= v <= 60000:
                rec["steps"] = v
        if (pm := _PROTEIN_RE.search(line)):
            rec["protein"] = _to_int(pm.group(1))
        if (cm := _CAL_RE.search(line)):
            v = _to_int(cm.group(1))
            if v and 800 <= v <= 6000:
                rec["calories"] = v
        if (zm := _Z2_RE.search(line)):
            rec["z2_min"] = _to_int(zm.group(1))
        if (wm := _WEIGHT_RE.search(line)):
            v = _to_float(wm.group(1))
            if v and 140 <= v <= 230:
                rec["weight"] = v

    # --- Format 2: weekly summary tables under a dated section header ---
    # Split on '## ' section headers; the first ISO date in a section anchors it,
    # and the section's table rows fill that week's 7 days (header date back 6 days).
    for section in re.split(r"\n##\s+", text):
        dm = _DATE_RE.search(section)
        if not dm:
            continue
        anchor = datetime.strptime(dm.group(1), ISO).date()
        week_metrics = {}
        for label, value in _TBL_ROW_RE.findall(section):
            key, num = _metric_from_row(label, value)
            if key and num is not None:
                week_metrics[key] = num
        if not week_metrics:
            continue
        # Spread the weekly avg across the 7 days ending at the anchor date. Only
        # FILL days that have no per-day (format-1) data — never overwrite a real day.
        for i in range(7):
            d = (anchor - timedelta(days=i)).strftime(ISO)
            rec = out.setdefault(d, {})
            for k, v in week_metrics.items():
                rec.setdefault(k, v)
    return out


def parse_workout_log(path):
    """Return {date: session_count} — count of dated training-session headers.

    workout-log.md uses '**Thu May 15 — W4 D2 Torso A**' style headers (and the
    pipeline's '<!--[liftosaur:YYYY-MM-DD]-->' markers). We count one session per
    dated header line. Month-name dates are resolved against the nearest plausible
    year from any ISO date context, defaulting to the file's ISO markers when present."""
    out = {}
    if not Path(path).exists():
        return out
    text = Path(path).read_text(encoding="utf-8")
    # Prefer explicit ISO markers if the ingester has started writing them.
    for m in re.finditer(r"\[liftosaur:(\d{4}-\d{2}-\d{2})\]", text):
        out[m.group(1)] = out.get(m.group(1), 0) + 1
    if out:
        return out
    # Fallback: count '**<Weekday> <Mon> <DD>**' headers. Without an explicit year
    # we can't ISO-stamp these reliably, so we return them keyed by raw header for
    # the report to note "N sessions found, dates not ISO — enable ingester markers."
    headers = re.findall(r"^\*\*([A-Z][a-z]{2}\s+[A-Z][a-z]{2}\s+\d{1,2})\b", text, re.MULTILINE)
    for h in headers:
        out[f"raw:{h}"] = out.get(f"raw:{h}", 0) + 1
    return out


# ---------------------------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------------------------
def _window_dates(today, days):
    return {(today - timedelta(days=i)).strftime(ISO) for i in range(days)}


def _avg(vals):
    vals = [v for v in vals if v is not None]
    return (sum(vals) / len(vals)) if vals else None


def _status(avg, target, more_is_better=True):
    """green/amber/red vs target. For 'more is better' (steps/protein), amber is
    90-100% of target, red is <90%. Returns (label, emoji)."""
    if avg is None:
        return ("no-data", "—")
    ratio = avg / target if target else 1
    if more_is_better:
        if ratio >= 1.0:
            return ("on-target", "✅")
        if ratio >= AMBER_FRACTION:
            return ("amber", "🟡")
        return ("red", "⛔")
    return ("info", "ℹ️")


def analyze(health, workouts, today, days):
    win = _window_dates(today, days)
    in_win = {d: r for d, r in health.items() if d in win}

    steps_vals = [r.get("steps") for r in in_win.values()]
    prot_vals = [r.get("protein") for r in in_win.values()]
    cal_vals = [r.get("calories") for r in in_win.values()]
    z2_vals = [(d, r.get("z2_min")) for d, r in in_win.items() if r.get("z2_min")]

    # Weight: 7-day rolling avg from the most recent up-to-7 weight readings in window.
    weight_series = sorted((d, r["weight"]) for d, r in in_win.items() if r.get("weight"))
    weight_avg = _avg([w for _, w in weight_series][-7:])

    steps_avg = _avg(steps_vals)
    prot_avg = _avg(prot_vals)
    cal_avg = _avg(cal_vals)

    # Training: count ISO-dated sessions in window; raw-dated fall back to a count note.
    iso_sessions = sum(c for k, c in workouts.items() if not k.startswith("raw:") and k in win)
    raw_session_total = sum(c for k, c in workouts.items() if k.startswith("raw:"))
    weeks_in_win = max(1, days / 7)
    train_per_week = iso_sessions / weeks_in_win if iso_sessions else None

    # Z2: did we hit >=1 weekday 20-min AND a Sunday 60+ in the window?
    z2_weekday = [m for d, m in z2_vals
                  if m and m >= Z2_WEEKDAY_MIN and datetime.strptime(d, ISO).weekday() != 6]
    z2_sunday = [m for d, m in z2_vals
                 if m and m >= Z2_SUNDAY_MIN and datetime.strptime(d, ISO).weekday() == 6]

    # Coverage: how many of the window days actually have any log entry? Low
    # coverage is itself the headline drift — it's why misses went unseen.
    logged_days = len([d for d in win if d in health])

    findings = []

    def add(metric, avg, target, more_is_better=True, fmt="{:.0f}"):
        label, emoji = _status(avg, target, more_is_better)
        shown = fmt.format(avg) if avg is not None else "no data"
        findings.append({
            "metric": metric, "avg": avg, "target": target,
            "status": label, "emoji": emoji, "shown": shown,
        })
        return label

    steps_status = add("Steps/day", steps_avg, STEPS_TARGET)
    add("Protein g/day", prot_avg, PROTEIN_TARGET)

    # Calories: two-sided — flag under-eating (below floor) AND creep (over band).
    cal_label = "no-data"
    if cal_avg is not None:
        if cal_avg < CAL_TARGET - CAL_CREEP_BAND:
            cal_label = "under-floor"
            cal_emoji = "🟡"
        elif cal_avg > CAL_TARGET + CAL_CREEP_BAND:
            cal_label = "creep"
            cal_emoji = "⛔"
        else:
            cal_label = "on-target"
            cal_emoji = "✅"
        findings.append({"metric": "Calories/day", "avg": cal_avg, "target": CAL_TARGET,
                         "status": cal_label, "emoji": cal_emoji, "shown": f"{cal_avg:.0f}"})
    else:
        findings.append({"metric": "Calories/day", "avg": None, "target": CAL_TARGET,
                         "status": "no-data", "emoji": "—", "shown": "no data"})

    return {
        "today": today.strftime(ISO),
        "window_days": days,
        "logged_days": logged_days,
        "coverage_pct": round(100 * logged_days / days),
        "steps_avg": steps_avg, "steps_status": steps_status,
        "protein_avg": prot_avg,
        "calories_avg": cal_avg, "calories_status": cal_label,
        "weight_avg": weight_avg,
        "weight_refeed_trigger": (weight_avg is not None and weight_avg <= WEIGHT_REFEED_AT),
        "train_sessions_iso": iso_sessions,
        "train_per_week": train_per_week,
        "raw_session_total": raw_session_total,
        "z2_weekday_hits": len(z2_weekday),
        "z2_sunday_hits": len(z2_sunday),
        "findings": findings,
    }


# ---------------------------------------------------------------------------
# REPORT
# ---------------------------------------------------------------------------
def render(a):
    L = []
    L.append(f"Fitness drift — {a['window_days']}-day window ending {a['today']}")
    L.append(f"Log coverage: {a['logged_days']}/{a['window_days']} days ({a['coverage_pct']}%)"
             + ("  ⛔ LOW — missed days hide drift; this is the #1 thing the pipeline fixes"
                if a['coverage_pct'] < 60 else ""))
    L.append("")
    for f in a["findings"]:
        tgt = f"(target {f['target']:,})" if isinstance(f['target'], int) else f"(target {f['target']})"
        L.append(f"  {f['emoji']} {f['metric']:<16} {f['shown']:>8}  {tgt}  [{f['status']}]")

    # Weight
    if a["weight_avg"] is not None:
        wflag = "⬇️ refeed trigger hit" if a["weight_refeed_trigger"] else ""
        L.append(f"  📉 Weight 7d avg     {a['weight_avg']:>7.1f} lb  (refeed at <= {WEIGHT_REFEED_AT}) {wflag}")
    else:
        L.append("  📉 Weight 7d avg       no data")

    # Training
    if a["train_sessions_iso"]:
        tflag = "✅" if (a["train_per_week"] or 0) >= TRAIN_PER_WEEK else "🟡"
        L.append(f"  {tflag} Training          {a['train_per_week']:.1f}/wk  (target {TRAIN_PER_WEEK}/wk, {a['train_sessions_iso']} sessions in window)")
    elif a["raw_session_total"]:
        L.append(f"  ℹ️ Training          {a['raw_session_total']} sessions found, dates not ISO — enable ingester [liftosaur:DATE] markers for accurate weekly rate")
    else:
        L.append("  — Training            no sessions parsed")

    # Z2
    z2flag = "✅" if (a["z2_weekday_hits"] >= 1 and a["z2_sunday_hits"] >= 1) else "🟡"
    L.append(f"  {z2flag} Zone-2            weekday {a['z2_weekday_hits']} (need >=1), Sunday keystone {a['z2_sunday_hits']} (need >=1)")

    # Headline
    L.append("")
    reds = [f["metric"] for f in a["findings"] if f["status"] in ("red", "creep")]
    if a["coverage_pct"] < 60:
        L.append("HEADLINE: log coverage too low to trust the averages — fix logging first (the exact gap that hid the steps/Z2 miss).")
    elif reds:
        L.append(f"HEADLINE: ⛔ drift on {', '.join(reds)} — act before the rolling avg re-baselines the cut again.")
    elif any(f["status"] == "amber" for f in a["findings"]):
        L.append("HEADLINE: 🟡 within 90% on at least one lever — nudge it back this week.")
    else:
        L.append("HEADLINE: ✅ all tracked levers on target over the window.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--asof", default=None, help="YYYY-MM-DD; pretend today is this (testing/backfill)")
    ap.add_argument("--health", default=str(HEALTH_LOG))
    ap.add_argument("--workout", default=str(WORKOUT_LOG))
    args = ap.parse_args()

    today = _today(args.asof)
    health = parse_health_log(args.health)
    workouts = parse_workout_log(args.workout)
    a = analyze(health, workouts, today, args.days)
    print(render(a))
    return a


if __name__ == "__main__":
    main()
