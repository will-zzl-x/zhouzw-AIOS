# Acquisition Sourcing — Apify Google Maps → ranked leads

Top-of-funnel lead generation for the bookkeeping/accounting acquisition search
(Scenario B, 20mi Phoenix metro). Produces the "100" in Codie's 100/50/10/1 ratio
— a prioritized contact list. Qualification happens later via `/deal-eval` once
you've made contact.

Connects to: `context/acquisition.md` (deal box), `references/sanchez.md`
(100/50/10/1), `journals/acquisition-log.md` (where chosen leads get logged),
Dan/solo outreach.

---

## One-time setup
1. Make an Apify account (apify.com) — free tier has starter credits; this run
   costs a few dollars of credits at most.
2. Find the **"Google Maps Scraper"** actor (by Compass / `compass/crawler-google-places`).

## Dual-track configuration

There are now TWO scrape configs because the dual-track strategy targets different deal sizes:

| File | Track | Target deal size | Review sweet spot in scoring |
|---|---|---|---|
| `apify-input-dan-bookkeeping.json` | Dan-partnered bookkeeping/accounting | $500k–$1M | 30-150 reviews (more established) |
| `apify-input-solo-template.json` | Solo, Zone of Genius sector | $300–$500k | 10-80 reviews (smaller owner-op) |
| `apify-input.json` | (legacy — same as Dan-bookkeeping) | $500k–$1M | (default) |

For the SOLO track, the template needs you to fill in search terms after picking
a sector. See `context/sector-evaluation-framework.md` for the Zone-of-Genius
sector-picking exercise that needs to happen first.

## Run the scrape (either track)
1. Open the actor → **JSON input editor** (toggle from the form view).
2. Paste the appropriate config (`apify-input-dan-bookkeeping.json` for Dan
   track OR your filled-in solo template). Delete the `_comment` / `_field_note`
   / `_alternative_*` / `_*_status` helper keys first — Apify ignores underscore
   keys but cleaner to strip.
3. **Start**. Wait for it to finish (a few min to ~30 min depending on volume).
4. **Export** the dataset as **JSON** (preferred) or CSV → save into `sourcing/leads/`
   with a track-identifying name (e.g., `leads/dan-2026-06-08.json` or
   `leads/solo-hvac-2026-06-08.json`).

## Enrich + rank (local, zero tokens)
Specify the matching mode:
```
cd sourcing
# Dan-partnered $500k-$1M target:
python enrich.py leads/dan-2026-06-08.json --mode dan --out leads-ranked-dan

# Solo $300-500k target:
python enrich.py leads/solo-hvac-2026-06-08.json --mode solo --out leads-ranked-solo-hvac
```
Outputs:
- `leads-ranked.csv` — full ranked list (all kept leads)
- `leads-ranked.md` — top 50 as a readable table

Tuning:
- `--min-reviews 3` drops near-empty listings
- `--out batch1` changes the output filename prefix

## What the scoring does (Maps-only heuristics)
The score (0–100) proxies "established but owner-operated" — the buyable profile:
- **Review sweet spot 10–80** = real business, not a chain (peak score)
- **Rating ≥4.0** = healthy
- **Has website + phone** = contactable + legit
- **Non-CPA bookkeeping** scores higher (dodges AZ's 51%-CPA-ownership rule)
- **Bookkeeping/payroll** flagged as likely-recurring; **tax-prep** flagged seasonal
- **National chains dropped** (H&R Block, Jackson Hewitt, ADP, Paychex, etc.)

It does NOT know financials, owner age, or staff count — those come from contact +
`/deal-eval`. This is sorting, not qualifying.

## Workflow into the funnel
1. Run scrape → enrich → eyeball `leads-ranked.md`
2. Pull the top ~20–30 into active outreach (Frame B / Frazier script v2)
3. Log contacted leads in `journals/acquisition-log.md`
4. Qualified responders → `/deal-eval`

## Notes
- `leads/` is gitignored (raw scrape data can be large + churny). The ranked
  outputs are small — commit those if you want them shared with Elena.
- Re-run monthly or when expanding search terms/cities to refresh the funnel.
