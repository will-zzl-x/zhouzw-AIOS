#!/usr/bin/env python3
"""rank_dan.py — Dan-thesis-aligned RE-RANK of the Maps-only Dan lead list.

Stdlib only. No AI, no tokens. Same spirit as enrich.py — it just changes the
scoring lens.

WHY THIS EXISTS
---------------
sourcing/leads-ranked-dan.csv was scored Maps-only (review count + rating +
contactability). For the DAN thesis specifically that score has a blind spot:
the firms it ranks highest are heavily TAX-PREP firms flagged
"tax-prep — seasonal/one-time". But the Dan thesis (context/dan-thesis.md +
context/acquisition.md) is about acquiring a RECURRING-REVENUE back office to
modernize with AI. The headline acquisition criterion is recurring revenue
>= 70%. Seasonal tax-prep is the WRONG profile — a firm whose revenue lands in
a Jan-Apr spike can't be run on quarterly check-ins, which is the whole
absentee-ownership end state.

So this re-rank computes a `dan_fit_score` that:
  - UP-weights recurring-revenue signals (bookkeeping, payroll, ongoing
    accounting, CFO / fractional CFO / controller / advisory).
  - DOWN-weights pure-seasonal signals (tax / tax service / income tax /
    tax prep) when there is NO bookkeeping/payroll/accounting co-signal.
  - Keeps the established-but-owner-operated review sweet spot (30-150 per the
    Dan track in enrich.py).
  - Keeps the rating + contactability components.
  - FLAGS "CPA" firms (AZ 51%-CPA-ownership constraint — a deal-structure note
    per context/acquisition.md, NOT a drop).

It preserves all original columns and ADDS:
  - dan_fit_score          (0-100, the new sort key)
  - revenue_class          (recurring | mixed | seasonal-tax | unknown)
  - dan_reason             (human-readable why)

The Maps-only `score` column is preserved untouched so you can see the shift.

This re-rank still does NOT qualify deals (no financials) — it just re-orders
the top of the 100/50/10/1 funnel toward the recurring-revenue profile the Dan
thesis actually wants. Verification of recurring-% still happens via outreach.

Usage:
  python rank_dan.py                      # uses default in/out paths below
  python rank_dan.py --in leads-ranked-dan.csv --out-prefix leads-dan-reranked
"""
import argparse
import csv
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --- Signal vocabularies (substring match, lowercased; matched against the
#     firm's name AND category, which is where the revenue-type signal lives) ---

# STRONG recurring-revenue signals — unambiguous ongoing back-office work, the
# profile the Dan thesis wants. These are revenue models that bill a recurring
# monthly client book, not a seasonal spike or an AUM/commission model.
STRONG_RECURRING_TERMS = [
    "bookkeep", "book keeping", "payroll",
    "fractional cfo", "fractional controller", "outsourced cfo",
    "outsourced accounting", "outsourced controller",
    "cfo", "controller",
    # ongoing-accounting phrasings
    "monthly", "client accounting", "accounting services", "full charge",
    "full-charge", "quickbooks", "qbo",
]

# WEAK recurring signals — "advisory"/"advisor" CAN capture fractional-CFO /
# accounting advisory (recurring), but they also ride along on AUM-based wealth-
# management / financial-advisor firms, which are a DIFFERENT revenue model (assets-
# under-management / commission, not a recurring bookkeeping back office). These
# only count as recurring when the firm is NOT a wealth-management shop (see
# WEALTH_MGMT_TERMS) — otherwise a wealth advisor gets falsely promoted on one token.
WEAK_RECURRING_TERMS = ["advisory", "advisor"]

# Wealth-management / investment-advisory signals — wrong sector for the Dan
# bookkeeping thesis. When present with NO strong-recurring co-signal, the weak
# "advisor"/"advisory" match must NOT promote the firm to recurring.
WEALTH_MGMT_TERMS = [
    "wealth", "cfp", "financial advisor", "wealth management",
    "investment advis", "aum", "retirement planning", "private wealth",
    "asset management", "financial planning",
]

# "accounting" alone is a soft recurring signal: ongoing accounting work tends
# to be recurring, but the word also rides along on seasonal "tax & accounting"
# storefronts. Handled separately so it can't outweigh a strong tax-only signal.
SOFT_ACCOUNTING_TERMS = ["account"]

# Tax-STRATEGY / advisory signals — ONGOING, high-margin tax advisory and the
# fractional-CFO / consulting upgrade path. This is Dan's NAMED high-conviction
# target (dan-thesis.md "Why Dan": "accounting / tax strategy firms with an
# upgrade path to fractional CFO / consulting"). These bill an ongoing advisory
# relationship, NOT a Jan-Apr filing spike — so they are recurring-tier, and the
# seasonal screen below must NOT catch them just because they contain "tax".
TAX_STRATEGY_TERMS = [
    "tax strateg", "tax advisory", "tax advisor", "tax planning",
    "tax consult", "tax resolution", "fractional cfo",
]

# Seasonal tax-PREP signals — Jan-Apr commodity revenue spike, one-time filing
# work, no ongoing book to modernize. DISTINCT from tax-strategy above:
# "tax prep" / "income tax" / "tax service" is filing-season commodity work.
SEASONAL_TERMS = [
    "tax prepar", "tax prep", "income tax", "tax service", "tax services",
    "tax relief", "tax & ", "tax and ", "tax,", "taxes", " tax", "tax ",
]

# Tax word-STEM — catches coined/brand names where "tax" carries no whitespace
# boundary and so slips the substring SEASONAL_TERMS list (e.g. "Taxanista",
# "TaxPro", "Taxworks"). \btax\w* matches a word that STARTS with "tax", so it
# won't false-fire on mid-word matches like "syntax". Used as an additional
# seasonal signal only.
_TAX_STEM = re.compile(r"\btax\w*")

# CPA ownership flag (AZ 51% rule — note, not a drop).
CPA_HINTS = ["cpa", "certified public account"]

# Dan-track review sweet spot (established but still owner-operated).
SWEET_LO, SWEET_HI = 30, 150


def _to_int(v, default=0):
    try:
        return int(float(str(v).replace(",", "")))
    except (ValueError, TypeError):
        return default


def _to_float(v, default=0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


def _has(blob, terms):
    return any(t in blob for t in terms)


def classify_revenue(blob):
    """Return (revenue_class, signals).

    `signals` is a dict of booleans used to build the human-readable reason:
      strong, soft_acct, weak_advisor, wealth_mgmt, tax_strategy, seasonal.

    Classes:
      recurring     — strong recurring (bookkeeping/payroll/CFO/controller),
                      OR tax-STRATEGY / tax-advisory / fractional-CFO (Dan's NAMED
                      high-conviction target per dan-thesis.md — ongoing advisory,
                      NOT a filing-season spike), OR a non-wealth-mgmt advisory
                      firm, OR ongoing-accounting phrasing.
      mixed         — a seasonal tax-PREP signal AND a recurring/accounting co-signal
                      (e.g. "Tax & Accounting", "Tax & Bookkeeping").
      seasonal-tax  — a seasonal tax-PREP signal with NO recurring/accounting
                      co-signal (pure filing-season prep — wrong profile).
      unknown       — no clear revenue-type signal. NOTE: a wealth-management /
                      AUM firm whose only recurring-ish token was "advisor" lands
                      here (its 'advisor' match is disqualified) — off-thesis
                      revenue model, correctly demoted out of the top tier.
    """
    strong = _has(blob, STRONG_RECURRING_TERMS)
    soft_acct = _has(blob, SOFT_ACCOUNTING_TERMS)
    wealth_mgmt = _has(blob, WEALTH_MGMT_TERMS)
    # "advisor"/"advisory" counts as recurring ONLY when this is not a wealth-
    # management firm — otherwise an AUM/CFP shop gets falsely promoted on one token.
    weak_advisor = _has(blob, WEAK_RECURRING_TERMS) and not wealth_mgmt
    tax_strategy = _has(blob, TAX_STRATEGY_TERMS)
    # Seasonal = explicit tax-PREP phrasing OR a coined "tax..."-stem brand name
    # (catches "Taxanista" etc. that slip the whitespace-bounded substring list).
    # But tax-STRATEGY work is ongoing advisory, so it is NEVER seasonal.
    seasonal = (_has(blob, SEASONAL_TERMS) or bool(_TAX_STEM.search(blob))) \
        and not tax_strategy

    signals = {
        "strong": strong, "soft_acct": soft_acct, "weak_advisor": weak_advisor,
        "wealth_mgmt": wealth_mgmt, "tax_strategy": tax_strategy, "seasonal": seasonal,
    }

    recurring_hit = strong or weak_advisor or tax_strategy
    co_signal = recurring_hit or soft_acct

    if tax_strategy:
        # Dan's explicitly named target: accounting / tax-strategy firm with a
        # fractional-CFO / consulting upgrade path. Recurring advisory, not prep.
        return "recurring", signals
    if seasonal and co_signal:
        return "mixed", signals
    if seasonal and not co_signal:
        return "seasonal-tax", signals
    if recurring_hit or soft_acct:
        return "recurring", signals
    return "unknown", signals


def dan_fit(row):
    """Dan-thesis fit score, 0-100, + revenue_class + reason. Re-derived from
    the firm's name + category (the Maps fields that carry the revenue-type
    signal), so this function is self-contained and does not trust the prior
    `flags` column."""
    name = str(row.get("name", ""))
    cat = str(row.get("category", ""))
    blob = (name + " " + cat).lower()

    reviews = _to_int(row.get("reviews"))
    rating = _to_float(row.get("rating"))
    website = str(row.get("website", "")).strip()
    phone = str(row.get("phone", "")).strip()

    revenue_class, sig = classify_revenue(blob)

    s = 0
    reasons = []

    # --- Revenue-type component (the heart of the Dan re-rank): up to 40 pts.
    # This is what moves recurring firms above seasonal tax-prep firms.
    if revenue_class == "recurring":
        if sig["strong"]:
            s += 40
            reasons.append("recurring-rev signal (bookkeeping/payroll/CFO/controller)")
        elif sig["tax_strategy"]:
            # Dan's explicitly named high-conviction target (dan-thesis.md).
            s += 40
            reasons.append("tax-strategy / advisory — Dan's named target (ongoing, not seasonal)")
        elif sig["weak_advisor"]:
            s += 32
            reasons.append("advisory firm (non-wealth-mgmt) — likely recurring")
        else:
            s += 30
            reasons.append("ongoing-accounting signal (soft recurring)")
    elif revenue_class == "mixed":
        s += 22
        reasons.append("mixed tax + recurring/accounting co-signal")
    elif revenue_class == "seasonal-tax":
        s += 4
        reasons.append("pure tax-prep — seasonal/one-time (wrong profile for Dan thesis)")
    else:  # unknown
        s += 12
        if sig["wealth_mgmt"]:
            reasons.append("wealth-mgmt/AUM — off-thesis revenue model (advisor token disqualified)")
        else:
            reasons.append("no clear revenue-type signal — verify")

    # --- Established-but-owner-operated review sweet spot: up to 30 pts. ---
    if SWEET_LO <= reviews <= SWEET_HI:
        s += 30
    elif 15 <= reviews < SWEET_LO or SWEET_HI < reviews <= 250:
        s += 18
    elif reviews > 250:
        s += 6
        reasons.append("very large — may exceed $1M cap")
    else:  # < 15
        s += 6
        reasons.append("thin reviews for Dan-track size")

    # --- Reputation: up to 18 pts. ---
    if rating >= 4.5:
        s += 18
    elif rating >= 4.0:
        s += 12
    elif rating >= 3.0:
        s += 5

    # --- Contactability: up to 12 pts. ---
    if website:
        s += 8
    else:
        reasons.append("no website")
    if phone:
        s += 4
    else:
        reasons.append("no phone")

    # --- CPA flag (AZ 51% ownership rule applies — note, NOT a drop). ---
    if _has(blob, CPA_HINTS):
        reasons.append("CPA — AZ 51% ownership rule applies (deal-structure note)")

    return min(s, 100), revenue_class, "; ".join(reasons)


def is_recurring_profile(revenue_class):
    """Top-25-composition bucketing: recurring/mixed/unknown count as
    'recurring-leaning'; only 'seasonal-tax' counts as seasonal."""
    return revenue_class != "seasonal-tax"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile",
                    default=str(HERE / "leads-ranked-dan.csv"),
                    help="input ranked CSV (from enrich.py --mode dan)")
    ap.add_argument("--out-prefix", default="leads-dan-reranked",
                    help="output prefix; writes <prefix>.csv + leads-dan-shortlist.md")
    args = ap.parse_args()

    in_path = Path(args.infile)
    if not in_path.is_absolute():
        in_path = HERE / in_path

    # --- Load. Read as UTF-8 (enrich.py wrote UTF-8). ---
    with in_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        orig_fields = list(reader.fieldnames or [])
        rows = []
        malformed = 0
        for r in reader:
            # csv.DictReader puts overflow columns under None; flag & skip those.
            if None in r and r[None]:
                malformed += 1
            if not str(r.get("name", "")).strip():
                malformed += 1
                continue
            rows.append(r)

    print(f"Loaded {len(rows)} rows from {in_path.name}")

    # --- Capture the ORIGINAL (Maps-only) top-25 composition before re-rank. ---
    # Input is already sorted by the Maps `score`, but sort defensively.
    by_orig = sorted(rows, key=lambda r: _to_int(r.get("score")), reverse=True)
    pre_top25 = by_orig[:25]
    pre_classes = [classify_revenue(
        (str(r.get("name", "")) + " " + str(r.get("category", ""))).lower())[0]
        for r in pre_top25]  # [0] = revenue_class (classify_revenue returns (class, signals))
    pre_recurring = sum(1 for c in pre_classes if is_recurring_profile(c))
    pre_seasonal = sum(1 for c in pre_classes if not is_recurring_profile(c))

    # --- Score + classify on the Dan-fit lens. ---
    blank_email = 0
    for r in rows:
        score, rev_class, reason = dan_fit(r)
        r["dan_fit_score"] = score
        r["revenue_class"] = rev_class
        r["dan_reason"] = reason
        if not str(r.get("email", "")).strip():
            blank_email += 1

    rows.sort(key=lambda r: r["dan_fit_score"], reverse=True)

    # --- Post-rerank top-25 composition. ---
    post_top25 = rows[:25]
    post_recurring = sum(1 for r in post_top25 if is_recurring_profile(r["revenue_class"]))
    post_seasonal = sum(1 for r in post_top25 if not is_recurring_profile(r["revenue_class"]))

    # --- Write full re-ranked CSV (preserve original cols + new cols). ---
    out_fields = orig_fields + [c for c in ("dan_fit_score", "revenue_class", "dan_reason")
                                if c not in orig_fields]
    csv_path = HERE / f"{args.out_prefix}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    # --- Write shortlist markdown (top 25 + composition shift). ---
    md_path = HERE / "leads-dan-shortlist.md"
    overall_class_mix = Counter(r["revenue_class"] for r in rows)
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Dan-thesis re-ranked shortlist — top 25\n\n")
        f.write("Re-ranked by `dan_fit_score` (recurring-revenue-weighted), "
                "from `rank_dan.py`.\n")
        f.write("Source: `leads-ranked-dan.csv` (Maps-only score). "
                "Sector LOCKED bookkeeping/accounting, Phoenix metro, $500k-$1M Dan track.\n\n")
        f.write("The Dan thesis wants a RECURRING-REVENUE back office (acquisition.md: "
                "recurring revenue >= 70%) to modernize with AI — NOT seasonal tax-prep.\n")
        f.write("This re-rank up-weights bookkeeping / payroll / ongoing accounting / "
                "CFO / controller / advisory and down-weights pure tax-prep.\n\n")

        f.write("## Top-25 composition shift (recurring-leaning vs. seasonal-tax)\n\n")
        f.write(f"- **Before re-rank (Maps-only score):** {pre_recurring} recurring-leaning, "
                f"{pre_seasonal} seasonal-tax in the top 25.\n")
        f.write(f"- **After re-rank (Dan-fit score):** {post_recurring} recurring-leaning, "
                f"{post_seasonal} seasonal-tax in the top 25.\n")
        f.write("- (recurring-leaning = recurring + mixed + unknown; seasonal-tax = "
                "pure tax-prep with no bookkeeping/payroll/accounting co-signal.)\n\n")
        f.write("Overall list revenue-class mix: "
                + ", ".join(f"{k}={v}" for k, v in overall_class_mix.most_common())
                + ".\n\n")

        f.write("## Top 25 leads\n\n")
        f.write("| # | Dan fit | Maps | Class | Name | Reviews | Rating | Phone | Web | Reason |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        for i, r in enumerate(post_top25, 1):
            web = "yes" if str(r.get("website", "")).strip() else "no"
            # sanitize pipe chars in free-text so the table doesn't break
            name = str(r.get("name", "")).replace("|", "/")
            reason = str(r.get("dan_reason", "")).replace("|", "/")
            f.write(f"| {i} | {r['dan_fit_score']} | {r.get('score','')} | "
                    f"{r['revenue_class']} | {name} | {r.get('reviews','')} | "
                    f"{r.get('rating','')} | {r.get('phone','')} | {web} | {reason} |\n")

    # --- Console verification. ---
    print(f"Wrote {csv_path.name} (full, {len(rows)} rows, sorted by dan_fit_score) "
          f"+ {md_path.name} (top 25)")
    print(f"Top-25 composition: BEFORE {pre_recurring} recurring / {pre_seasonal} seasonal "
          f"-> AFTER {post_recurring} recurring / {post_seasonal} seasonal")
    print("Overall revenue-class mix: "
          + ", ".join(f"{k}={v}" for k, v in overall_class_mix.most_common()))
    if blank_email:
        print(f"Data note: {blank_email}/{len(rows)} rows have blank email (Maps rarely exposes email).")
    if malformed:
        print(f"Data note: {malformed} malformed/nameless rows skipped or flagged.")
    print("\nNew top 10 (Dan-fit):")
    for i, r in enumerate(rows[:10], 1):
        print(f"  {i:2d}. [{r['dan_fit_score']}] {r['revenue_class']:12} {r.get('name','')}")


if __name__ == "__main__":
    main()
