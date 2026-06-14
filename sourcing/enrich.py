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

# Categories we keep, by mode. Substring match, lowercased — matched against
# the place's category string AND name. Apify Google Maps + Google Places API
# (New) both expose a category-ish field (categoryName / primaryTypeDisplayName).
KEEP_CATEGORIES_DAN = [
    "bookkeep", "account", "tax prepar", "tax consult", "tax service",
    "payroll", "cpa", "financial", "auditor",
]

# Solo-track 12-sector menu (context/acquisition.md, 2026-06-10).
KEEP_CATEGORIES_SOLO = [
    # 1. HOA management
    "hoa", "homeowners association", "community management", "community association",
    "property management",  # often overlaps HOA
    # 2. Water treatment / softener
    "water softener", "water treatment", "water filtration", "water conditioning",
    # 3. MSP / IT managed services
    "managed service", "it service", "it support", "it consultant",
    "computer support", "computer service", "tech support", "information technology",
    # 4. Specialty distribution (B2B niche)
    "distributor", "wholesale", "industrial supply", "supply company",
    # 5. Office plant care / interior landscaping
    "interior plant", "plant service", "plantscape", "interior landscap",
    "office plant",
    # 6. Mat rental
    "mat rental", "mat service", "uniform rental", "uniform service",
    "floor mat", "linen service",
    # 7. Document destruction / shredding
    "shredding", "document destruction", "paper shred", "data destruction",
    # 8. Window cleaning commercial
    "window clean", "window wash",
    # 9. Pool service
    "pool service", "pool clean", "pool maintenance", "swimming pool",
    # 10. Pest control
    "pest control", "exterminator", "termite", "pest management",
    # 11. Vending / micro-market
    "vending", "micro market", "micro-market", "break room service",
    # 12. Coffee / water service
    "coffee service", "water delivery", "office coffee", "office water",
    "bottled water",
]

# National chains / franchises to drop — not owner-operated acquisition targets.
CHAIN_BLOCKLIST_DAN = [
    "h&r block", "hr block", "jackson hewitt", "liberty tax", "turbotax",
    "intuit", "adp", "paychex", "h & r block",
]

CHAIN_BLOCKLIST_SOLO = [
    # Pest
    "orkin", "terminix", "aptive", "truly nolen", "ehrlich", "western exterminator",
    # Pool / aquatics retail (not service)
    "leslie's pool", "leslies pool", "pinch a penny",
    # Janitorial / mat (national franchises)
    "cintas", "aramark", "g&k services", "unifirst", "alsco", "vestis",
    "servicemaster", "jan-pro", "stratus building", "vanguard cleaning",
    "coverall", "jani-king", "jani king",
    # Shredding
    "iron mountain", "shred-it", "shred it", "proshred",
    # Window clean franchise
    "fish window cleaning", "window genie",
    # Water / coffee (national)
    "culligan", "primo water", "ds services", "ready refresh", "readyrefresh",
    "kinetico",  # softener manufacturer/dealers — too brand-driven
    # IT / MSP nationals
    "geek squad", "office depot", "best buy",
    # Vending nationals
    "canteen", "five star food service", "compass group",
]


def keep_categories(mode):
    return KEEP_CATEGORIES_DAN if mode == "dan" else KEEP_CATEGORIES_SOLO


def chain_blocklist(mode):
    # Solo mode also keeps the Dan list as a safety net (no harm), and vice versa
    # is rarely triggered (Dan-mode results wouldn't match pool franchises).
    if mode == "dan":
        return CHAIN_BLOCKLIST_DAN
    return CHAIN_BLOCKLIST_SOLO + CHAIN_BLOCKLIST_DAN

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


def is_chain(name, mode="solo"):
    n = name.lower()
    return any(c in n for c in chain_blocklist(mode))


def category_ok(cat, name, mode="solo"):
    blob = (str(cat) + " " + str(name)).lower()
    return any(c in blob for c in keep_categories(mode))


def sector_tag(cat, name, mode="solo"):
    """Tag a kept row with which sector family it matched. Solo mode only —
    helps Will + Elena see per-sector yields during the scoring exercise."""
    if mode != "solo":
        return ""
    blob = (str(cat) + " " + str(name)).lower()
    SECTORS = [
        ("hoa-management", ["hoa", "homeowners association", "community management", "community association", "property management"]),
        ("water-treatment", ["water softener", "water treatment", "water filtration", "water conditioning"]),
        ("msp-it", ["managed service", "it service", "it support", "it consultant", "computer support", "computer service", "tech support", "information technology"]),
        ("specialty-distribution", ["distributor", "wholesale", "industrial supply", "supply company"]),
        ("office-plant-care", ["interior plant", "plant service", "plantscape", "interior landscap", "office plant"]),
        ("mat-rental", ["mat rental", "mat service", "uniform rental", "uniform service", "floor mat", "linen service"]),
        ("document-destruction", ["shredding", "document destruction", "paper shred", "data destruction"]),
        ("window-cleaning", ["window clean", "window wash"]),
        ("pool-service", ["pool service", "pool clean", "pool maintenance", "swimming pool"]),
        ("pest-control", ["pest control", "exterminator", "termite", "pest management"]),
        ("vending-micromarket", ["vending", "micro market", "micro-market", "break room service"]),
        ("coffee-water-service", ["coffee service", "water delivery", "office coffee", "office water", "bottled water"]),
    ]
    for tag, terms in SECTORS:
        if any(t in blob for t in terms):
            return tag
    return "other"


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

    blob = (str(name) + " " + str(cat)).lower()

    if mode == "dan":
        # AZ 51%-CPA-ownership: non-CPA bookkeeping is structurally cleaner.
        if any(h in blob for h in CPA_HINTS):
            flags.append("CPA — AZ 51% ownership rule applies")
        else:
            s += 10  # bookkeeping / non-CPA firm: cleaner ownership path

        # Recurring vs seasonal revenue type signal.
        if "bookkeep" in blob or "payroll" in blob:
            s += 10; flags.append("likely recurring rev")
        elif "tax prepar" in blob or "tax service" in blob:
            flags.append("tax-prep — seasonal/one-time, verify recurring %")
    else:
        # Solo mode: recurring-revenue bonus for route/contract sectors.
        ROUTE_TERMS = ["pest control", "pool service", "pool clean", "vending",
                       "shredding", "document destruction", "mat rental",
                       "uniform rental", "linen", "managed service", "msp",
                       "office coffee", "water delivery", "interior plant",
                       "plantscape", "hoa", "community management",
                       "window clean", "window wash"]
        if any(t in blob for t in ROUTE_TERMS):
            s += 10; flags.append("recurring/route sector")

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
        if is_chain(name, mode=args.mode):
            dropped_chain += 1; continue
        if not category_ok(cat, name, mode=args.mode):
            dropped_cat += 1; continue
        if to_int(g(r, "reviewsCount", "reviews", "totalReviews")) < args.min_reviews:
            dropped_rev += 1; continue
        sc, flags = score(r, mode=args.mode)
        row_out = {
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
        }
        if args.mode == "solo":
            row_out["sector"] = sector_tag(cat, name, mode="solo")
        kept.append(row_out)

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
        track_label = ("Bookkeeping/accounting (Dan track, $500k-$1M)" if args.mode == "dan"
                       else "Solo track ($300-500k, 12-sector menu)")
        f.write(f"# Ranked acquisition leads — {len(kept)} firms\n\n")
        f.write(f"{track_label}, Phoenix metro. Top of the 100/50/10/1 funnel.\n")
        f.write("Score = Maps-only acquisition-fit heuristic (see enrich.py). Next: contact top tier, then `/deal-eval`.\n\n")

        # Solo mode: per-sector yield summary — feeds dimension-5 ("sourcing
        # reality") of the sector-evaluation-framework scoring.
        if args.mode == "solo":
            from collections import Counter
            sector_yields = Counter(r.get("sector", "other") for r in kept)
            f.write("## Per-sector yield (dimension-5 sourcing-reality input)\n\n")
            f.write("| Sector | Viable leads | Sourcing-reality score band |\n")
            f.write("|---|---|---|\n")
            for sector, count in sector_yields.most_common():
                if count >= 100:
                    band = "**5** (100+) — strong sourcing"
                elif count >= 60:
                    band = "**4** (60-99) — solid"
                elif count >= 30:
                    band = "**3** (30-59) — workable"
                elif count >= 15:
                    band = "**2** (15-29) — thin"
                else:
                    band = "**1** (<15) — DROP (hard filter)"
                f.write(f"| {sector} | {count} | {band} |\n")
            f.write("\n")

        f.write("## Top 50 leads\n\n")
        if args.mode == "solo":
            f.write("| # | Score | Sector | Name | Reviews | Rating | Phone | Website | Flags |\n")
            f.write("|---|---|---|---|---|---|---|---|---|\n")
        else:
            f.write("| # | Score | Name | Reviews | Rating | Phone | Website | Flags |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
        for i, r in enumerate(kept[:50], 1):
            web = "✓" if r["website"] else "—"
            if args.mode == "solo":
                f.write(f"| {i} | {r['score']} | {r.get('sector','-')} | {r['name']} | "
                        f"{r['reviews']} | {r['rating']} | {r['phone']} | {web} | {r['flags']} |\n")
            else:
                f.write(f"| {i} | {r['score']} | {r['name']} | {r['reviews']} | "
                        f"{r['rating']} | {r['phone']} | {web} | {r['flags']} |\n")

    print(f"Wrote {csv_path} (full) + {md_path} (top 50)")


if __name__ == "__main__":
    main()
