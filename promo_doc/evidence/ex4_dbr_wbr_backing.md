<!-- Ex4 backing — 2026-07-13. Source: DBR Metric Review email thread (Mar 25 – May 31, 2025), pasted by Will.
     LOCAL. Fills the 3 [NEED FROM WILL] slots for the DBR/WBR/QBR business-review example. -->

# Example 4 backing — ICT Business-Review Metric Architecture (DBR/WBR/MBR/QBR)

**Window:** Mar 25 – May 31, 2025 (Will's first ~6–7 months; joined Oct 21 2024).
**Quip:** ICT Performance & Quality Metrics (quip-amazon.com/0iABA00h1mVD).
**Published to:** IPEX_ANALYTICS SharePoint (IPEX_WBR.html, "Redirects_execution"); DBR to
ipex-control-tower@ ("ICT - Summary, Quality & Performance DBR"); raw data to ipex-rdm@.

## What it is (the before-state / problem)
No codified daily/weekly/monthly/quarterly performance-measurement cadence existed for ICT
redirect execution. Will architected the full metric suite from scratch — DBR (daily) → WBR
(weekly) → MBR (monthly) → QBR (quarterly, reviewed with Cam) — and the ETL + IPEX Analytics
publishing behind it. DBR v1 launched 3/28/2025; iterated v1.1→v1.3 (through early May) and into
a v2 series; WBR v1→v1.2; MBR+QBR v1. Ran the definition/alignment reviews (3/26, 3/31) and drove
ICT-management sign-off.

## What the 49+ metric lines measure (from the line-by-line validation table)
- **Execution/topline (lines 3–12):** Created, Cancelled, Planned, Uncovered VRIDs, Picked Up,
  On-Time Pickup (OTP), Scheduled to Deliver, Delivered, On-Time Delivery (OTD), Cost.
- **Defect attribution by controllability (14–21):** IPEX+IM, Outside Org, FC-Controllable,
  IPEX-Controllable, Carrier-Controllable, Uncontrollable, uncategorized, TONU.
- **Network breakdowns (23–26, 33–36):** IXD-National, IXD-Regional, Sortable, Nonsortable.
- **Mode breakdowns (28–31, 38–41):** TL, 1P-IM, 3P-IM, 3P-LTL+SP.
- **Defect types (43–49):** VRID / Trailer / Manifest / ISA / Location defects.
- **WBR grain adds LTS components:** projected vs actual transit, dwell, pickup delay (v2 broke
  these out to isolate the projected↔actual gap); trailing-7-day / WTD / trailing-3-week views.

## The hard problem he drove (Dive Deep + cross-org)
**Data-dependency escalation (Apr 3–7 2025):** the `created_by` field in
`andes.ats-onestopshop.o_rr_schedule` stopped updating to D-1 — which broke ICT's ability to
separate IPEX redirects from non-IPEX aliases on the shared shipper account, i.e. it blocked
tracking redirect performance day-over-day (a core team function). Will wrote the problem
statement, escalated to IPEX Analytics, and drove the fix: IBWR (Terell McQueen) surfaced an
alternate table (`oss_loads.trid_create_user`) with D-1 creator visibility; Will drove the query
re-point and re-validation. Also personally: fixed OTP/OTD logic for prior-week-boundary pickups
(scheduled start-of-week, picked up end of prior week = on-time), excluded NCSL loads, excluded
3P-LTL/SP/IM and non-ICT-purview FCs where EDI gaps corrupted on-time metrics, and revamped the
transfer `fc2_dwell_to_receive` calc to align with vendor-redirect dwell at hourly grain.

## Cross-functional coordination (Will as driver/architect)
Set the roadmap and per-workstream owners; coordinated IPEX Analytics (ETL/query build, incl. HYD
shifts) and IBWR (creator-table workaround); drove ICT-management review + the QBR-with-Cam gate.
The ETL auto-publishes the DBR PDF into the WBR deck; management subscribed to the raw-data DL.

## Outcome
The DBR→QBR suite became ICT's performance/quality metric of record — automated ETL + IPEX
Analytics publishing, feeding the WBR deck and management/QBR reviews. It is the measurement
foundation the redirect-steering org reads from, and the judgment later encoded in Will's flash
automation (Example 3) was first structured in these reviews.

## Provenance / cautions
- 49+ lines, 6-week launch, first-six-months = Q1 PDF p2 + this thread (line table runs to 49).
- ALTITUDE: keep the v1.1→v1.3 version churn and specific meeting dates OUT of the body (backing only).
- NAMES: scrub L6+ internal names from the body (Matt Freza / Chris Wong / Cam Nelson). IPEX
  Analytics / IBWR as teams are fine; individual analyst names best left to backing.
