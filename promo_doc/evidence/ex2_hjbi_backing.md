# Example 2 backing — HJBI Drop-to-Live (stripped from v3 body per DNA #1/#5, ARC1 items 9–10)

## Debugging episode (v1 L56 — relocated whole; methodology detail banned in body)

When the candidate-load selector disagreed with the operational SKED UI on slot availability, William refused the spot-fix and traced the discrepancy through three Redshift sources — `sked_constraints_daily`, `ipex.site_scheduled_capacity`, `ground_control_inbound_view_main_page_v2` — found a per-ISA capacity-counting bug (script counted 6 live pallets vs actual ISA count of 12; table cap 13 vs UI cap 12 — corrected figures per REVIEW 6/28 #4; the earlier "7 open vs 0 open" numbers were unsourced), restructured the SQL from correlated subqueries into proper joins, and held the weekly candidate list until the source matched the UI ceiling. Body keeps a one-clause version.

## Script / artifact names (banned in body)

- `pilot_site_selection.py` — Redshift-backed weekly site selector; per-shift live capacity vs HJBI pushed loads on drop constraints. Repo: `hjbi_pilot/`.
- HJBL SCAC provisioned **5/1/2026** (body says "May 2026").
- First pilot load XMI3 5/11; WK20 launch; second load HIA1 arrived 5/29 (WK22 — REVIEW 6/28 #3 correction).
- Pilot plan: 4 weeks (not 6 — REVIEW 6/28 #6). KPIs: FPY, Driver Detention (DTU) cost, NCNS rate, MDP benefit (REVIEW 6/28 #7).

## Color cut as unverifiable (ARC1 §3 #11 — do not restore without artifacts)

- "sitting for four months" — no artifact; body now says "stalled since its November 2025 identification."
- "original January 2026 launch had slipped" — no artifact for the Jan target.
- "replied within 24 hours" to the pilot lead's four concerns — the concerns email (4/24 10:33) exists; Will's reply timestamp was not retrievable.

## Consciously trimmed from v3 (ARC2 LOW-2a — restore if wanted)

v1 close: "At pilot conclusion, William is drafting a Lessons-Learned doc for scalability, sized to unlock up to $22.5M in annual cost/speed savings if the model holds." Partially covered by v3's "pending scalability read-out"; the Lessons-Learned-doc artifact claim itself was dropped as forward-looking filler.

## Own-OOTO claim (restored in body — DECISION 4)

Will's OOTO 5/7–5/11; teammate covered; pilot kept moving and recarped the first ISA without Will on point (a4de771 text + REVIEW 6/28 #5 — the v1 "Colton's OOTO" attribution was backwards). Will to confirm dates/facts before ship.

## Partner-name key (names banned in body prose)

HJBI pilot lead = John Calcote; Amazon GL Prepaid Trans pilot owner = Robin Thomas. Peer endorsement on handoff: Shelby King, 4/22 — verbatim in `evidence/targeted_thread_pulls.md` (restored to disk from a4de771 on 2026-07-12; ARC2 LOW-5).
