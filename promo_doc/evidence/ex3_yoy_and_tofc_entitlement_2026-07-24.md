# Ex3 — YoY redirect efficiency (Q1) + TOFC cost-avoidance entitlement (Q2)

**Built:** 2026-07-24 · **Owner:** William Zhou · **Status:** DRAFT — local only, no comms, no writeback.
Read-only investigation. All pulls are LIVE Quip / LIVE Redshift as of today unless noted.

---

## Q1 — YoY redirect efficiency: "are we redirecting more units/trailers at lower overall cost YoY?"

### Method used (source 1 succeeded — source 2 blocked, see below)

Used `all_team_slides/build_ytd_from_steering.py`'s own logic (2025 folder `UCF9OAFdxvE`, 2026 folder
`dKL9OAnfDIa`), re-run live today via a throwaway script (`C:\Users\zhouzw\_tmp_yoy_tofc_pull.py`,
**not committed, not in the repo** — respects the read-only constraint). No file in the repo was
written or modified for this pull; the existing `all_team_slides/ytd_rollup.json` (2026, WK1–29,
cached) was cross-checked and matches the fresh pull exactly.

Executed-row definition, dedup key, and "keep latest/most-complete week" logic are unchanged from
the tool (status in `{resolved, closed, ask met, in progress, completed, complete}`; dedup key =
`(date, giver, taker, sim, network)`).

### Critical data-quality finding: 2025 Quip folder has an 8-week gap

**2025 folder `UCF9OAFdxvE` contains weekly trackers for WK4, WK10–WK52. WK1–3 and WK5–9 do not
exist as discoverable docs in that folder** (checked live today — `enumerate_trackers()` returns
exactly `[4,10,11,...,52]`). That's **8 of the first 29 weeks missing (27.6%)**, concentrated in
Jan–Feb. This is a real gap, not a parsing miss — the folder simply has no thread matching those
week numbers. **A naive "2025 WK1–29 vs 2026 WK1–29" comparison is therefore biased** — 2026 gets
credit for 8 weeks 2025 structurally cannot report. I ran BOTH cuts below; use the matched-week
cut as the honest headline.

### Cut 1 — Unmatched (2025: 21 available weeks ≤WK29; 2026: full 29 weeks) — DO NOT USE AS HEADLINE, biased

| | 2025 (21 wks, WK4,10-29) | 2026 (29 wks, WK1-29) | YoY |
|---|---|---|---|
| Trailers | 11,355 | 14,039 | **+23.6%** |
| Units | 153,932,684 | 179,046,867 | **+16.3%** |
| Cost | $7,487,252 | $9,649,521 | **+28.9%** |
| Executed rows ("lanes") | 928 | 1,256 | **+35.3%** |
| $/row | $8,068 | $7,683 | −4.8% |
| $/unit | $0.0486 | $0.0539 | +10.9% |

This cut LOOKS like "more volume, more cost, roughly flat-to-better per-load unit cost" — but it's
comparing 21 weeks of 2025 against 29 weeks of 2026. Not defensible as-is.

### Cut 2 — Matched weeks (WK4, 10–29 = the 21 weeks BOTH years actually have) — USE THIS AS THE HEADLINE

| | 2025 | 2026 | YoY |
|---|---|---|---|
| Trailers | 11,355 | 11,316 | **−0.3%** (flat) |
| Units | 153,932,684 | 141,173,853 | **−8.3%** |
| Cost | $7,487,252 | $7,747,209 | **+3.5%** |
| Executed rows ("lanes") | 928 | 1,012 | **+9.1%** |
| $/row | $8,068 | $7,655 | −5.1% |
| $/unit | $0.0486 | $0.0549 | **+13.0%** |

**On the apples-to-apples 21-week window, the honest answer is NO, not on the primary axis Will
asked about.** Trailer count is flat. Unit volume is actually DOWN 8.3% YoY. Total cost is UP 3.5%
YoY. Cost-per-unit is UP 13.0% YoY. The one metric that improved is $/executed-row (−5.1%), and
that's driven by MORE, SMALLER redirect asks (+9.1% rows) rather than genuine per-unit efficiency —
diluting cost across more (smaller) lanes lowers the per-lane average even while $/unit rises.

**Do not use this as a "we're getting more efficient" data point in the promo doc.** If anything,
the matched-week comparison argues the opposite on unit-cost, though it's flat-to-slightly-worse
rather than dramatically worse. This is exactly the kind of anomalous-vs-expectation finding that
should be surfaced, not spot-fixed — see the caveats below on what could still be confounding it
(cost-field completeness, mix shift, network mix).

### Caveats on the steering-tracker cost basis (both cuts)

1. **The tracker's own `cost` field has a material zero-rate.** Sampling the TOFC-scope subset
   (below) alone shows 2 of 7 in-window rows carrying `cost=0` (28.6%) despite non-zero trailers/units
   — i.e., recorded cost undercounts true spend in both years' totals. Unless the zero-rate differs
   meaningfully by year (not checked at the full-dataset level — would need a row-by-row zero-cost
   audit across ~2,000 rows, out of scope for this pull), the YoY *direction* should be more robust
   than the absolute $ figures, but neither year's total $ should be read as a clean P&L number.
2. **Mix shift not decomposed.** The −0.3%/−8.3% trailers/units split (flat trailers, fewer units)
   implies average trailer density fell YoY — smaller loads per trailer. Whether that's freight-mix
   (more floor-loaded/lower-density SKUs) or a genuine change in what's being redirected isn't
   isolated here; flagging per the "surface anomalies, don't silently filter" rule rather than
   guessing at a cause.
3. **Network composition not isolated.** This is an all-network total (rIXD+NS+ARS+nIXD+AMXL_CA
   blended); a network-by-network YoY cut (e.g., is rIXD alone worse or better than the blend?)
   would sharpen this but wasn't run — deferred, flag if wanted.

### Q1 finance-query thread (source 2) — BLOCKED, confirmed absent from the scheduling cluster

Per Will's finance query: `andes.hydra_ib.D_HYDRA_IB_REPORT_NA_DAILY` joined to
`andes."ats-onestopshop".o_rr_schedule` on `report_id_vrid=load_number`, filtered on
`account_id IN ('TRANSFERSREDIRECTS','INBOUNDREDIRECTS','TRANSFERSINTERMODALREDIRECTS')`.

**Checked live today against `scheduling.cba7nbarlfx1.us-east-1.redshift.amazonaws.com:8197` /
db `scheduling`** (same connection `unified_flash/redshift_query.py get_connection()` uses):

- Enumerated all 88 schemas on the cluster (`information_schema.tables`, distinct `table_schema`).
  **No schema named `ats-onestopshop` or anything resembling `hydra_ib` exists.**
- Searched `table_name ilike '%hydra_ib_report%'` → **0 rows**.
- Searched `table_name ilike '%rr_schedule%'` and `'%o_rr%'` → **0 rows**.
- Searched `table_name ilike '%load_summary%'` → found `v_load_summary` under schemas `geller` and
  `andes_local` (not `ats-onestopshop` — that name doesn't exist here; `andes_local` is presumably
  a local datashare alias, distinct table). This is the SAME table `_notes/2026-07-14_azim_cost_avoidance.md`
  and the AZIM entitlement deep-dive pulled from — useful for AZIM midstream $, **not** a substitute
  for `D_HYDRA_IB_REPORT_NA_DAILY` (no evidence the two are the same underlying report).
- The `ibwr` schema (66 tables) DOES exist and has `atsb_redirect_mstr` / `atsb_redirect_raw` — but
  (a) per this project's own `CLAUDE.md`, that ledger uses a different methodology and does **not**
  reconcile to the steering trackers, and (b) checked its columns live — **no cost/dollar column at
  all** (`snapshot_date, redirect_week, redirect_date, redirect_year, fc1, fc1_type, fc1_region, arn,
  load_type, fc2, fc2_type, fc2_region, units, redirect_isa, fc2_receive_status`). It cannot answer
  the $/load or $/unit half of this question even as a fallback.

**Verdict: `D_HYDRA_IB_REPORT_NA_DAILY` and `o_rr_schedule` are not present on the scheduling
Redshift cluster under any schema.** This table pair almost certainly lives in DataCentral/Andes
proper (federated Andes access, not this cluster's datashares) — per your instruction, **not
attempted**. If you want this thread finished, it needs either (a) a DataCentral/QuickSight pull
against the real Andes tables, or (b) confirmation from Finance/Tobi on which local table (if any)
mirrors that report.

### Safe-to-claim lines (Q1)

- "2025 YTD steering-tracker discoverability has an 8-week gap (WK1–3, WK5–9); any 2025-vs-2026
  comparison spanning those weeks is biased toward 2026." — **LIVE-verified** (folder enumeration,
  today).
- "On the 21 weeks both years actually have data (WK4, WK10–29): trailers flat (−0.3%), units down
  8.3%, cost up 3.5%, $/unit up 13.0% YoY." — **derived** (live steering-tracker pull, today; executed-row
  dedup logic reused unmodified from `build_ytd_from_steering.py`).
- "We are not redirecting more units at lower cost YoY on the matched-week steering-tracker basis —
  the opposite is closer to true (fewer units, more total cost, worse $/unit)." — **derived**, with
  the caveats above (cost-field completeness, mix shift, network mix not isolated).
- "The Hydra/andes finance-query approach Will specified is blocked on this cluster — no
  `D_HYDRA_IB_REPORT_NA_DAILY` / `o_rr_schedule` schema exists here." — **LIVE-verified** (Redshift
  `information_schema` scan, today).
- **Recommendation:** do not use a YoY efficiency claim in the promo doc off this data. If a positive
  YoY story is needed, it would have to come from a different, narrower metric than aggregate
  steering-tracker $/unit (e.g., a specific lever's $/unit, like AZIM's or TOFC's own unit economics
  below) — not from "redirects overall."

---

## Q2 — TOFC cost-avoidance entitlement

### Program status (as documented in `las1_tofc_q2/tracker.md`, last updated 2026-06-07)

**The lever is on STANDBY, not active, as of 2026-06-07** — Will's own tracker: *"Kicked off WK17;
did NOT scale into sustained execution... intentionally not pulling TOFC right now — it adds
redirect spend, which runs against the current linehaul-reduction posture."* No steering-tracker row
tagged to this lane pattern appears after WK21 (5/20) through WK30 (checked live, full 2026 folder).
This materially changes the framing vs AZIM: **AZIM's $137K/$820K figures are a live, ongoing
run-rate. TOFC's numbers below are a closed historical window (5 weeks) plus a hypothetical
if-reactivated annualization — not a current run-rate.** State that distinction explicitly if this
goes in the same Summary line as AZIM.

### Unit economics (from `las1_tofc_q2/CLAUDE.md`, Will's own teardown — not re-derived here)

| Scenario | $/trailer |
|---|---|
| LAS1/VGT2 → Bernardino dray + Bernardino→ORD TOFC + ORD→dest dray ("via-LAS1-leg" tier) | $4.3K |
| nIXD-direct → Bernardino TOFC → ORD → dest (bypasses the LAS1/VGT2 leg entirely) | $2.6K |
| nIXD/LAS1/VGT2 → dest, over-the-road (OTR status quo) | $6.6K |

Two DIFFERENT savings claims live in this table and they should not be conflated:
- **vs OTR, via-LAS1/VGT2-leg tier:** $6.6K − $4.3K = **$2.3K/trailer**
- **vs OTR, nIXD-direct-bypass tier (the marketed "~$4K/trailer" headline):** $6.6K − $2.6K = **$4.0K/trailer**
- **Via-leg tier vs the direct-bypass tier (routing-efficiency delta, NOT a vs-OTR savings claim):**
  $4.3K − $2.6K = **$1.7K/trailer** — this is the number in the task prompt ("~$1.7K below incumbent
  LAS1 routing"). It compares TWO TOFC configurations against each other, not TOFC vs OTR.

**Important finding: every executed trailer found in the steering tracker (below) is LAS1- or
VGT2-origin — none of the nIXD-direct-bypass origins (MIT2/POC2/POC3/QXY8/XPH6/XSB2) show up as an
executed giver anywhere in the 2026 tracker.** That means the applicable, proven savings basis for
what actually ran is the **$2.3K/trailer (via-leg tier vs OTR)** figure, not the marketed $4.0K
best-case, which requires the nIXD-direct-bypass routing that has not been observed executing. I'm
flagging this because using $4.0K/trailer for the realized-to-date total would overstate it by ~74%.

### Realized-to-date: trailers actually moved (Q2 program, WK17–21, 4/23–5/20/2026)

Pulled live today from the full 2026 steering-tracker folder (all 30 weeks), filtering executed rows
where giver ∈ {LAS1, VGT2} and taker ∈ {RFD2, MDW2, FWA4} (dropped BJC1/SWF2 — see note below) and
cross-referencing each row's own notes field for the "TOFC SIM" tag:

| Week | Date | Lane | Trailers | Units | Cost (tracker) | SIM | TOFC-tagged? |
|---|---|---|---|---|---|---|---|
| WK17 | 4/24 | LAS1→RFD2 | 10 | 194,577 | $52,873 | V2188362329 | **Yes** ("TOFC SIM") |
| WK18 | 4/30 | LAS1→RFD2 | 30 | 374,698 | $108,172 | e2f47a92-... | Inferred (same lane, next week) |
| WK18 | 5/1 | VGT2→RFD2 | 4 | 107,661 | $9,947 | V2197693610 | **Yes** ("...to meet delta on LAS1→RFD2 TOFC SIM") |
| WK19 | 5/4 | VGT2→MDW2 | 75 | 1,402,584 | $183,471 | V2200998487 | **Yes** ("TOFC SIM") |
| WK20 | 5/12 | VGT2→MDW2 | 15 | 290,785 | $0 | V2212156490 | **Yes** ("TOFC SIM") |
| WK20 | 5/12 | VGT2→RFD2 | 5 | 84,542 | $48,774 | (blank) | Inferred (same lane/week) |
| WK21 | 5/20 | LAS1→RFD2 | 7 | 128,667 | $0 | (blank) | Inferred (same lane, tail end) |
| **TOTAL** | | | **146** | **2,583,514** | **$403,237** | | 4 explicit / 3 inferred |

**Note on scope:** I excluded LAS1→BJC1 and VGT2→BJC1 rows (WK24/25/29/30, totaling 51 more
"trailers" in the raw giver/taker filter) — those are tagged in their own notes as "BJC1 new launch
freight" / "MIDSTREAM ONLY SIM" / "HJBI and AZIM are unable to redirect on this lane via their ramp,"
which is BJC1-launch-support freight, not the rail-TOFC lever (`tracker.md`'s 5/14 decision log
explicitly says destination consolidated to **RFD2** only, dropping FWA4 — BJC1 was never in the
TOFC destination scope). Including them would inflate the count without basis.

**Note on the Feb 2026 run:** `las1_tofc_q2/CLAUDE.md` documents the prior (non-Q2) run as "~71
trailers across 4 days." I found candidate steering-tracker rows around WK6/WK7/WK9 (Feb 2026,
same LAS1/VGT2→RFD2/MDW2/FWA4 lane pattern) summing to ~130 trailers, but the SIM `V2100501621`
shows DIFFERENT dates (2/6 → 2/9) for what reads as the same evolving ask (3 trailers → 20
trailers), which the dedup key (`date,giver,taker,sim,network`) treats as two separate executions
because the date itself moved between snapshots — a likely double-count, not a real 130. **I am
using the documented "~71 trailers/4 days" from Will's own project doc as the Feb figure and NOT
the raw re-derived 130**, and flagging the discrepancy rather than picking a number silently. The
Feb run is also out of scope for the Q2 entitlement math below regardless.

### Cost avoidance — realized to date (146 trailers, WK17–21)

| Basis | $/trailer | Total (146 trailers) | Applicability |
|---|---|---|---|
| vs OTR, via-leg tier (proven — matches what actually executed) | $2.3K | **$335,800** | **Use this as the primary number** |
| vs OTR, nIXD-direct-bypass tier (marketed headline, NOT proven for these trailers) | $4.0K | $584,000 | Upper bound only — label as unproven for this population |

Tracker-recorded cost for the same 146 trailers is **$403,237** — this is NOT the same thing as
"cost avoided"; it's the redirect's OWN cost, which is already netted against the OTR/TOFC delta in
the $2.3K/$4.0K figures above. Also note 2 of 7 rows (28.6%) show tracker `cost=$0` despite non-zero
trailers/units, so even this recorded-cost figure is a likely undercount of the redirect's own spend
— it doesn't change the avoidance-basis calc (which uses the fixed $/trailer teardown figures, not
the tracker's cost column), but flag it as a tracker data-quality note consistent with the Q1 caveat.

**Cross-check against May 2026 Hydra finance data** (`redirect_budget_bridge/may_hydra_summary.json`,
a real Hydra/VLS-sourced lane-cost extract, already in the repo — built for the April/May budget
bridge, not re-derived today): for **May alone**, the 3 dominant TOFC-pattern lanes show:

| Lane | Loads (May only) | Cost (May only) | Avg miles |
|---|---|---|---|
| VGT2→MDW2 | 90 | $368,315 | 2,204 |
| LAS1→RFD2 | 47 | $203,349 | 2,229 |
| VGT2→RFD2 | 34 | $153,176 | 2,242 |
| **Total** | **171** | **$724,839** | |

The ~2,200-mile average is consistent with the Bernardino/ORD rail routing (a direct OTR LAS1↔RFD2
route is materially shorter), which is circumstantial support that these ARE TOFC-pattern moves. But
**this Hydra cut is lane-level, not SIM-tagged** — it can't distinguish a TOFC rail move from a plain
OTR redirect that happens to run the same FC-pair, so it may include non-TOFC volume. It is bigger
than my steering-tracker total for a SHORTER window (May alone > my full WK17–21 span), which is
directionally consistent with the Q1 finding that the steering tracker's own cost/volume fields
undercount realized activity — but I'm not merging the two into one number because their scope
isn't identical. Treat the steering-tracker 146/$403K as the SIM-attributable floor, and the Hydra
171/$725K (May only) as a lane-level ceiling-ish cross-check that the true executed volume in the
window was likely higher than 146.

### Annualized entitlement — hypothetical if-reactivated, NOT a live run-rate

The realized window is 5 weeks (WK17–21, 4/23–5/20) = **29.2 trailers/week**. If sustained for a
full 52-week year:

- Trailers/year (hypothetical): 29.2 × 52 ≈ **1,518 trailers**
- Cost avoidance/year, proven basis ($2.3K/trailer): 1,518 × $2,300 ≈ **$3.49M**
- Cost avoidance/year, upper-bound basis ($4.0K/trailer, unproven for this population): 1,518 × $4,000 ≈ **$6.07M**

**This is explicitly NOT comparable to the AZIM $137K YTD / ~$820K annualized framing without the
caveat spelled out.** AZIM's annualization projects an ACTIVE, currently-running weekly rate forward.
TOFC's lever has been on deliberate standby since 2026-06-07 (7 weeks as of today, 2026-07-24) —
the annualized figure above is "what it would be worth if reactivated and sustained," a policy
option, not a forecast of what will happen. If this goes in the promo doc Summary next to AZIM, it
should be labeled "entitlement if reactivated" or similar, not "run-rate."

### Safe-to-claim lines (Q2)

- "LAS1/VGT2 TOFC Q2 kicked off WK17 (4/23), scope-expanded 5/14, and was placed on deliberate
  standby 6/7 — it is not currently running." — **LIVE-verified** (`las1_tofc_q2/tracker.md`, cross-checked
  against the live 2026 steering tracker showing no TOFC-tagged execution after WK21).
- "146 trailers / 2,583,514 units moved via the TOFC lever during its active window (WK17–21),
  per the steering tracker, with 4 of 7 rows explicitly SIM-tagged 'TOFC SIM' and the remaining 3
  inferred from same-lane/same-week continuity." — **derived** (live steering-tracker pull, today;
  moderate confidence on the 3 inferred rows).
- "Realized cost avoidance to date: ~$336K on the proven $2.3K/trailer (via-leg tier vs OTR) basis;
  up to ~$584K on the marketed $4.0K/trailer basis, which is NOT proven for the LAS1/VGT2-origin
  trailers that actually executed." — **derived**, basis explicitly labeled.
- "Hypothetical annualized entitlement if reactivated and sustained at the WK17–21 rate: ~$3.49M
  (proven basis) to ~$6.07M (upper-bound basis)." — **derived**, explicitly hypothetical, not a
  run-rate — the lever is parked.
- "May 2026 Hydra finance data on the same 3 dominant lanes shows 171 loads / $724,839 for that
  month alone — higher than my steering-tracker total for a 5-week span, consistent with (not proof
  of) the tracker undercounting true execution." — **LIVE data, already in repo** (`may_hydra_summary.json`),
  cross-check only, not merged into the headline number.
- "The Feb 2026 prior run's '~71 trailers/4 days' figure is Will's own documented number; I did not
  independently reproduce it from steering-tracker rows (candidate rows summed to ~130 due to a
  likely SIM-date-drift double-count) and did not overwrite the documented figure." — **not
  independently re-derived; using the documented figure as-is.**

---

## Provenance

- **Q1 pull:** live Quip, today (2026-07-24), via `all_team_slides/build_ytd_from_steering.py`'s
  `_token()` / `enumerate_trackers()` / `fetch_records()` / `_is_executed()` / `_month()` functions,
  invoked from a throwaway script at `C:\Users\zhouzw\_tmp_yoy_tofc_pull.py` and
  `C:\Users\zhouzw\_tmp_yoy_matched.py` (outside the repo, not committed — delete when done). Raw
  dump also cached at `C:\Users\zhouzw\AppData\Local\Temp\_yoy_tofc_pull.json` (outside repo).
- **Q1 Redshift check:** live, today, against `scheduling.cba7nbarlfx1.us-east-1.redshift.amazonaws.com:8197`
  db `scheduling`, via `unified_flash/redshift_query.py get_connection()`. Read-only
  `information_schema` queries only — no data tables scanned in full.
- **Q2 tracker/program facts:** `las1_tofc_q2/tracker.md` (last updated 2026-06-07), `las1_tofc_q2/CLAUDE.md`.
- **Q2 executed-lane pull:** same live Quip pull as Q1, filtered to the TOFC-scope giver/taker set,
  full 2026 folder (WK1–30).
- **Q2 Hydra cross-check:** `redirect_budget_bridge/may_hydra_summary.json` (pre-existing file in
  repo, not modified, not re-pulled today — read only).
- **Methodology consistency reference:** `_notes/azim_entitlement_ytd_deepdive_2026-07-21.md` (the
  $137K YTD / $822K-$1.02M annualized AZIM figures already in the promo doc) — TOFC framing above
  mirrors its MEASURED/EST/inferred labeling discipline and its explicit "what would need to be true
  externally" caveats.
- Nothing in this file was posted anywhere or written back to any tracker/SIM/Quip doc. No repo file
  other than this one was created or modified during this investigation.
