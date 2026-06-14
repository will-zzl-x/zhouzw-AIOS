#!/usr/bin/env python3
"""places_scrape.py — Google Places API (New) replacement for the Apify Google
Maps Scraper. Same input config shape, same output JSON shape (enrich.py-
compatible). Stdlib + requests only.

Pipeline: read Apify-style config -> run Text Search (New) for each search
string with pagination -> dedupe by place_id -> emit JSON array of place dicts
shaped to match the Apify output enrich.py reads (title, address, categoryName,
reviewsCount, totalScore, website, phone).

Free tier: Google gives $200/mo Maps Platform credit. Our usage:
  - Text Search Pro (ID-only is free tier; basic data tier): ~$0.005/place
  - Solo full run (~180 strings, max ~60 results each, ~10,800 places before
    dedupe; ~3-5k after) -> ~$15-25 -> well under $200 free credit.

Usage:
  python places_scrape.py --config apify-input-dan-bookkeeping.RUN.json \
                          --out leads/dan-2026-06-14.json

  python places_scrape.py --config apify-input-solo.RUN.json \
                          --out leads/solo-2026-06-14.json
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib import request, error

API_URL = "https://places.googleapis.com/v1/places:searchText"

# Field mask — what the API returns. Each named field is "basic" or "advanced"
# pricing tier. We're using mostly basic + a couple advanced (rating, reviewCount).
# Cost stays low because we DON'T pull reviews body, photos, or contributor info.
FIELD_MASK = ",".join([
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.types",
    "places.primaryType",
    "places.primaryTypeDisplayName",
    "places.rating",
    "places.userRatingCount",
    "places.websiteUri",
    "places.nationalPhoneNumber",
    "places.internationalPhoneNumber",
    "places.businessStatus",
    "places.googleMapsUri",
    "nextPageToken",
])


def load_env(repo_root: Path):
    """Load .env from sourcing/ — simple KEY=VALUE parser, stdlib only."""
    env_path = repo_root / ".env"
    if not env_path.exists():
        return {}
    out = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def text_search(query: str, api_key: str, max_results: int = 60,
                page_size: int = 20) -> list[dict]:
    """Call Text Search (New) with pagination. Returns list of place dicts in
    the API's response shape. max_results capped by API at ~60 (3 pages × 20)."""
    collected = []
    page_token = None

    for page_num in range(3):  # API allows up to 3 pages
        if len(collected) >= max_results:
            break

        body = {
            "textQuery": query,
            "pageSize": min(page_size, max_results - len(collected)),
        }
        if page_token:
            body["pageToken"] = page_token

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": FIELD_MASK,
        }

        req = request.Request(
            API_URL,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f"    HTTP {e.code} on query '{query}' page {page_num}: {err_body[:200]}",
                  file=sys.stderr)
            break
        except error.URLError as e:
            print(f"    URLError on query '{query}' page {page_num}: {e}",
                  file=sys.stderr)
            break

        places = data.get("places", [])
        collected.extend(places)

        page_token = data.get("nextPageToken")
        if not page_token:
            break
        # Google requires a brief wait before pageToken becomes valid.
        time.sleep(2)

    return collected[:max_results]


def to_apify_shape(p: dict) -> dict:
    """Convert Places API (New) response to the field names enrich.py reads.

    enrich.py's g() helper tries multiple field names, so we populate the
    primary ones it expects (title, address, categoryName, reviewsCount,
    totalScore, website, phone). Also includes 'placeId' for dedup."""
    display_name = p.get("displayName", {})
    name = display_name.get("text", "") if isinstance(display_name, dict) else str(display_name)

    primary_disp = p.get("primaryTypeDisplayName", {})
    category = primary_disp.get("text", "") if isinstance(primary_disp, dict) else str(primary_disp)
    # Backup: combine primary_type + types into a category-ish string
    if not category:
        category = p.get("primaryType", "") or " / ".join(p.get("types", [])[:3])

    return {
        "title": name,
        "name": name,
        "address": p.get("formattedAddress", ""),
        "categoryName": category,
        "category": category,
        "categories": p.get("types", []),
        "reviewsCount": p.get("userRatingCount", 0),
        "totalScore": p.get("rating", 0.0),
        "website": p.get("websiteUri", ""),
        "phone": p.get("nationalPhoneNumber", "") or p.get("internationalPhoneNumber", ""),
        "phoneUnformatted": p.get("nationalPhoneNumber", ""),
        "url": p.get("googleMapsUri", ""),
        "placeId": p.get("id", ""),
        "businessStatus": p.get("businessStatus", ""),
        # Carry the raw display strings so enrich.py's substring matcher gets
        # the richest possible blob to match on (sector type variants).
        "primaryType": p.get("primaryType", ""),
        "primaryTypeDisplayName": category,
    }


def run(config_path: Path, out_path: Path, api_key: str,
        max_per_search: int = 60, sleep_between: float = 0.3):
    config = json.loads(config_path.read_text())
    queries = config.get("searchStringsArray", [])
    if not queries:
        print(f"No searchStringsArray in {config_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Config: {config_path}")
    print(f"Queries: {len(queries)}")
    print(f"Max results per query: {max_per_search}")
    print(f"Output: {out_path}\n")

    seen_ids: set[str] = set()
    all_places: list[dict] = []
    started = time.time()

    for i, query in enumerate(queries, 1):
        print(f"  [{i:3d}/{len(queries)}] {query}", end="", flush=True)
        results = text_search(query, api_key, max_results=max_per_search)
        new_count = 0
        for p in results:
            pid = p.get("id")
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)
            all_places.append(to_apify_shape(p))
            new_count += 1
        elapsed = time.time() - started
        print(f"  → +{new_count} new ({len(results)} raw)  [{elapsed:.0f}s total]")
        time.sleep(sleep_between)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(all_places, indent=2))

    print(f"\n✓ Saved {len(all_places)} unique places to {out_path}")
    print(f"  ({len(seen_ids)} total unique place IDs seen; "
          f"{sum(len(q) for q in queries)} chars of query)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True,
                    help="Apify-shape JSON config (apify-input-*.RUN.json)")
    ap.add_argument("--out", required=True,
                    help="Output JSON path (typically leads/<track>-<date>.json)")
    ap.add_argument("--max-per-search", type=int, default=60,
                    help="Max results per query (cap = 60 due to API pagination)")
    ap.add_argument("--api-key", default=None,
                    help="Google Maps Platform API key (else reads sourcing/.env)")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent  # sourcing/
    env = load_env(repo_root)
    api_key = args.api_key or env.get("GOOGLE_PLACES_API_KEY") or os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key:
        print("ERROR: no API key. Set GOOGLE_PLACES_API_KEY in sourcing/.env "
              "or pass --api-key", file=sys.stderr)
        sys.exit(2)

    config_path = Path(args.config)
    if not config_path.is_absolute() and not config_path.exists():
        # Try relative to sourcing/
        config_path = repo_root / args.config
    if not config_path.exists():
        print(f"Config not found: {args.config}", file=sys.stderr)
        sys.exit(2)

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = repo_root / args.out

    run(config_path, out_path, api_key, max_per_search=args.max_per_search)


if __name__ == "__main__":
    main()
