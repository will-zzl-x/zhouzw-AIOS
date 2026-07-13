# Backlog — Completed / Archived

Rows moved here from `backlog.md` at Sunday reflections. Newest batch on top.

## Archived 2026-07-12

| id | Title | Area | Quest | Notes | Completed |
|---|---|---|---|---|---|
| dan-fill-numbers | Fill the 3 load-bearing numbers in Frame B before sending | Money | work-main | (a) Elena's $50K + timing locked, signed off 6/18; (b) hours/week = full-time-early → taper Year 1, signed off 6/18; (c) Dan CPA-licensure framed as open call question. Send-channel question retired — `dan-reachout` pivoted to in-person 6/18. | 2026-06-18 (archived 7/12) |
| meal-grocery-fix | meal-planning grocery.py: read cycle.inventory_snapshot + fuzzy/unit match | AIOS-Infra | not-quest | Shipped 6/14 PM weekly-run-confident commit (+ `run_week.py` orchestrator, inventory_add/remove, balance_check). Validated across 2026-06-20 + 2026-06-27 (Banff-split) cycles incl. zero-qty coverage fix. | 2026-06-14 (archived 7/12) |
| meal-defrost-fix | meal-planning defrost.py: skip fresh-buy cycles | AIOS-Infra | not-quest | Same weekly-run-confident commit; validated over subsequent cycles. | 2026-06-14 (archived 7/12) |
| brief-description-fix | Morning-brief: propagate Daily Consistent / gate descriptions into Todoist | AIOS-Infra | not-quest | Shipped 2026-06-15 (brief_generator.py Rule 10, todoist_client description passthrough, archiver-safe `sm:<id>` format, unit-tested). Live on 7am GitHub Action. | 2026-06-15 (archived 7/12) |

## Archived 2026-06-14

| id | Title | Area | Quest | Notes | Completed |
|---|---|---|---|---|---|
| apify-scrape-dan | Run scrape (Dan track — bookkeeping/accounting $500k-$1M) + enrich | Money | work-main | Pivoted off Apify → Google Places API (free $200/mo GCP credit, see `sourcing/places_scrape.py`). 505 ranked viable bookkeeping/accounting firms in `sourcing/leads-ranked-dan.md`. Closed readiness-gate #2 for `dan-reachout`. | 2026-06-14 |
| apify-scrape-solo | Run scrape (Solo track — 12-sector broad menu, $300-500k) + enrich | Money | work-main | Architecture pivot: scrape-broad-first, narrow-after. 620 ranked viable leads across 8 sourceable sectors in `sourcing/leads-ranked-solo.md`. Per-sector yields are the dimension-5 input for the now-demoted Solo sector-pick. | 2026-06-14 |
| hotel-block-chase | Hotel block: sign Element + land premium block | Wedding | side | Courtyard Marriott 10 ✅ (5/28) + Element SkySong 9 ✅ (6/10) = 19 rooms × 3 nights = 57 room nights locked. Premium-tier chase (The Remi / Valley Ho) split into its own lower-priority row. | 2026-06-14 |
| digital-minimalism-tier1 | Digital Minimalism Tier 1 — done; monitor screen-time end of June | Life | life-main | Resolved 6/7; YouTube Shorts feed → 0 min structurally killed. Tier 3 escalation criterion folded into post-cut review queue. | 2026-06-07 (archived 6/14) |

## Archived 2026-06-07

| id | Title | Area | Quest | Notes | Completed |
|---|---|---|---|---|---|
| frazier-script-v2 | Roland Frazier YouTube + outreach script v2 | Money | work-main | Frazier transcript ingested, full v2 outreach script + first-conversation flow → `context/frazier-outreach-script.md`. Closed 13-mo-old action item. Unblocked apify-scrape. | 2026-06-04 |
| dan-thesis-verify | Verify Dan thesis files | Money | work-main | Re-dumped from Google Doc, extracted to journals/dan-thesis-history.md + context/dan-thesis.md; gaps flagged. | 2026-06-03 |
| socal-trip-book | Book SoCal weekend (Sonesta + dinners) | Relationships | side | Sonesta Select HB Fountain Valley booked; Thai District Sat dinner; Brodard Fri dinner. Full itinerary on calendar. | 2026-06-04 |
| socal-trip-confirm-elena | Confirm Reggie end-time + studio | Relationships | side | Reggie Sat 4pm+ at 5235 Pacific Ave #A, Long Beach. Allergy heads-up logged. | 2026-06-03 |
| test-plan-elena | Test-plan close-the-loop with Elena | Relationships | side | Home test negative at 11 days late; thread closed. (Reopen trigger noted in archive only.) | 2026-06-01 |
| escalation-scraper | Escalation scraper threshold logic | Career | not-quest | Closed without AIOS action — coverage absorbed by ICT automation on work laptop / deprioritized. | 2026-06-04 |
| pre-cana-schedule | Schedule Pre-Cana process | Wedding | side | Initial reach-out to St. Andrew done, Pre-Cana date booked. | 2026-06-07 |
