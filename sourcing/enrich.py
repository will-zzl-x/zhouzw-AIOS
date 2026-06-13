#!/usr/bin/env python3
"""enrich.py — dedupe + filter + score Apify Google Maps output into a ranked
acquisition lead list. Stdlib only. No AI, no tokens.

Pipeline: raw Apify export (CSV or JSON) -> dedupe -> filter to relevant
categories + drop chains -> score on acquisition-fit heuristics (Maps-only
signals; financials come later via outreach) -> write ranked CSV + markdown.

This produces the TOP of the 100/50/10/1 funnel: a prioritized contact list of
likely owner-operated, established bookkeeping/accounting firms in Phoenix metro.
It does NOT qualify deals — that's /deal-eval after you've made contact.

Usage:
  python enrich.py dataset.json                  # or dataset.csv
  python enrich.py dataset.json --out leads      # custom output prefix
  python enrich.py dataset.json --min-reviews 3  # tune the floor
"""
import argparse, csv, json, re, sys
from pathlib import Path

# Categories we keep (substring match, lowercased).
KEEP_CATEGORIES = [
    "bookkeep", "account", "tax prepar", "tax consult", "tax service",
    "payroll", "cpa", "financial", "auditor",
]

# National chains / franchises to drop — not owner-operated acquisition targets.
CHAIN_BLOCKLIST = [
    "h&r block", "hr block", "jackson hewitt", "liberty tax", "turbotax",
    "intuit", "adp", "paychex", "h & r block",
]

# CPA-flagged title hints (AZ ownership law: 51% must be CPA-licensed — bookkeeping
# / non-CPA firms dodge that constraint, so they score a touch higher).
CPA_HINTS = ["cpa", "certified public account"]


def load(path):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".json":
        data = json.loads(text)
        return data if isinstance(data, list) else data.get("items", [data])
    # CSV
    return list(csv.DictReader(text.splitlines()))


def g(row, *keys, default=""):
    """Get first present key (Apify field names vary across actor versions)."""
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return row[k]
    return default


def to_int(v, default=0):
    try:
        return int(float(str(v).replace(",", "")))
    except (ValueError, TypeError):
        return default


def to_float(v, default=0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return default


def norm_key(name, addr):
    s = (str(name) + "|" + str(addr)).lower()
    return re.sub(r"[^a-z0-9]+", "", s)


def is_chain(name):
    n = name.lower()
    return any(c in n for c in CHAIN_BLOCKLIST)


def category_ok(cat, name):
    blob = (str(cat) + " " + str(name)).lower()
    return any(c in blob for c in KEEP_CATEGORIES)


def score(row, mode="solo"):
    """Acquisition-fit heuristic, 0-100. Maps-only proxies for 'established but
    owner-operated' — the profile most likely to be a motivated, buyable firm.

    Mode:
      - "solo"  → target $300-500k deals. Smaller owner-operated firms.
                  Sweet spot: 10-80 reviews (real biz, not big firm).
      - "dan"   → target $500k-$1M deals (Dan-partnered bookkeeping/accounting).
                  Sweet spot: 30-150 reviews (more established, more SDE)."""
    name = g(row, "title", "name")
    reviews = to_int(g(row, "reviewsCount", "reviews", "totalReviews"))
    rating = to_float(g(row, "totalScore", "rating", "stars"))
    website = g(row, "website", "url", "website")
    phone = g(row, "phone", "phoneUnformatted", "phoneNumber")
    cat = g(row, "categoryName", "category")

    s, flags = 0, []

    # Review-count sweet spot is mode-dependent — smaller deal targets want
    # smaller firms (10-80 reviews); larger deal targets (Dan-partnered) want
    # mid-sized established firms (30-150 reviews).
    if mode == "dan":
        if 30 <= reviews <= 150:
            s += 35
        elif 15 <= reviews < 30 or 150 < reviews <= 250:
            s += 22
        elif reviews > 250:
            s += 8; flags.append("very large — may exceed $1M cap")
        else:  # <15
            s += 8; flags.append("thin reviews for Dan-track size")
    else:  # solo mode (default)
        if 10 <= reviews <= 80:
            s += 35
        elif 5 <= reviews < 10 or 80 < reviews <= 150:
            s += 22
        elif reviews > 150:
            s += 8; flags.append("large/established — may exceed $500k solo cap")
        else:  # <5
            s += 8; flags.append("thin reviews — verify it's real")

    # Healthy reputation.
    if rating >= 4.5:
        s += 20
    elif rating >= 4.0:
        s += 14
    elif rating >= 3.0:
        s += 6

    # Contactability.
    if website:
        s += 15
    else:
        flags.append("no website")
    if phone:
        s += 10
    else:
        flags.append("no phone")

    # Non-CPA bookkeeping dodges the AZ 51%-CPA-ownership rule -> structurally simpler.
    blob = (str(name) + " " + str(cat)).lower()
    if any(h in blob for h in CPA_HINTS):
        flags.append("CPA — AZ 51% ownership rule applies")
    else:
        s += 10  # bookkeeping / non-CPA firm: cleaner ownership path

    # Recurring-revenue likelihood by type (bookkeeping/payroll = recurring;
    # tax-prep = seasonal one-time).
    if "bookkeep" in blob or "payroll" in blob:
        s += 10; flags.append("likely recurring rev")
    elif "tax prepar" in blob or "tax service" in blob:
        flags.append("tax-prep — seasonal/one-time, verify recurring %")

    return min(s, 100), flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Apify export (.json or .csv)")
    ap.add_argument("--out", default="leads-ranked", help="output file prefix")
    ap.add_argument("--min-reviews", type=int, default=0, help="drop below this review count")
    ap.add_argument("--mode", choices=["solo", "dan"], default="solo",
                    help="solo = target $300-500k owner-op (10-80 review sweet spot); "
                         "dan = target $500k-$1M Dan-partnered bookkeeping (30-150 review sweet spot)")
    args = ap.parse_args()
    print(f"Scoring mode: {args.mode} ({'$500k-$1M Dan-partnered' if args.mode == 'dan' else '$300-500k solo'})")

    rows = load(args.input)
    print(f"Loaded {len(rows)} raw rows")

    seen, kept = set(), []
    dropped_chain = dropped_cat = dropped_dupe = dropped_rev = 0
    for r in rows:
        name = g(r, "title", "name")
        addr = g(r, "address", "street", "formattedAddress")
        cat = g(r, "categoryName", "category")
        if not name:
            continue
        k = norm_key(name, addr)
        if k in seen:
            dropped_dupe += 1; continue
        seen.add(k)
        if is_chain(name):
            dropped_chain += 1; continue
        if not category_ok(cat, name):
            dropped_cat += 1; continue
        if to_int(g(r, "reviewsCount", "reviews", "totalReviews")) < args.min_reviews:
            dropped_rev += 1; continue
        sc, flags = score(r, mode=args.mode)
        kept.append({
            "score": sc,
            "name": name,
            "category": cat,
            "reviews": to_int(g(r, "reviewsCount", "reviews", "totalReviews")),
            "rating": to_float(g(r, "totalScore", "rating", "stars")),
            "phone": g(r, "phone", "phoneUnformatted", "phoneNumber"),
            "website": g(r, "website", "url", "website"),
            "email": g(r, "email", "emails"),
            "address": addr,
            "flags": "; ".join(flags),
        })

    kept.sort(key=lambda x: x["score"], reverse=True)

    print(f"Dropped: {dropped_dupe} dupes, {dropped_chain} chains, "
          f"{dropped_cat} off-category, {dropped_rev} below min-reviews")
    print(f"Kept {len(kept)} ranked leads")

    # CSV
    csv_path = Path(f"{args.out}.csv")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(kept[0].keys()) if kept else
                           ["score","name","category","reviews","rating","phone","website","email","address","flags"])
        w.writeheader(); w.writerows(kept)

    # Markdown top 50 for quick eyeballing
    md_path = Path(f"{args.out}.md")
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# Ranked acquisition leads — {len(kept)} firms\n\n")
        f.write("Bookkeeping/accounting, Phoenix metro. Top of the 100/50/10/1 funnel.\n")
        f.write("Score = Maps-only acquisition-fit heuristic (see enrich.py). Next: contact top tier, then `/deal-eval`.\n\n")
        f.write("| # | Score | Name | Reviews | Rating | Phone | Website | Flags |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for i, r in enumerate(kept[:50], 1):
            web = "✓" if r["website"] else "—"
            f.write(f"| {i} | {r['score']} | {r['name']} | {r['reviews']} | "
                    f"{r['rating']} | {r['phone']} | {web} | {r['flags']} |\n")

    print(f"Wrote {csv_path} (full) + {md_path} (top 50)")


if __name__ == "__main__":
    main()
