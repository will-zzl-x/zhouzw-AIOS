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

## Run the scrape
1. Open the actor → **JSON input editor** (toggle from the form view).
2. Paste the contents of `apify-input.json` (delete the `_comment` / `_field_note`
   / `_alternative_*` helper keys first — they're just notes, Apify ignores
   underscore keys but cleaner to strip).
3. **Start**. Wait for it to finish (a few min to ~30 min depending on volume).
4. **Export** the dataset as **JSON** (preferred) or CSV → save into `sourcing/leads/`.

## Enrich + rank (local, zero tokens)
```
cd sourcing
python enrich.py leads/dataset.json
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
