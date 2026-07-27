# AZIM 1P-IM midstream reroute — defensible annualized cost avoidance

**Built:** 2026-07-24 · **Owner:** William Zhou · **Status:** READ-ONLY analysis. Only this file was written.
**Replaces:** the `$144,739 ÷ 16.7%` ≈ **$0.85–0.87M** method (share of 2025 full-year redirect *units*
in the WK24–30 window, from `all_team_slides/ytd_rollup.json`). That method is **retired** — it
assumes the AZIM midstream lever ran at its WK24–30 rate for the other 45 weeks of the year, which
is false: the lever's tracked history starts WK24 (2026-06-08); there is no earlier data because it
didn't durably exist yet. `ytd_rollup.json` was **not used** as a basis anywhere below.

---

## 0) Bottom line

| # | Method | Result | Status |
|---|---|---|---|
| 1 | **Pure run-rate**, durable weeks only (excl. WK24 launch burst + WK27's one-time rail-crosstown windfall) | **~$754K/yr** | primary, most defensible |
| 1 | Pure run-rate, naive flat mean (all 7 weeks) | ~$1.08M/yr | upper bound / what the task's own naive check produces |
| 1 | Pure run-rate, recent-3-weeks (WK28–30) | ~$1.13M/yr | recency-weighted, still carries RDU2→TOL3 tail |
| 1 | Pure run-rate, median week ×52 | ~$0.735M/yr | robust-to-outlier cross-check, agrees with the durable-weeks cut |
| 1 | Floor: strip the one-time RDU2→TOL3 lane entirely from every week | ~$0.485M/yr | conservative floor if that lane never recurs |
| 2 | **Volume-grounded** (task's formula) | **not independently computable this session** | Source A reachable but not AZIM-attributable at VRID level within scope; Source B has no 1P-IM-specific annual denominator. Self-referential version reproduces ~$1.07M (not new information — see §5). |

**Safe-to-claim line for the promo doc:**
> "AZIM 1P-IM midstream reroute is on a **$750K–$1.1M/year run-rate** as a durable weekly lever
> (WK24–30 2026 realized: $144,739 / 307 loads / ~5.17M units), replacing the retired
> ÷16.7%-seasonality method (~$0.85M). Point estimate if one number is required: **~$900K/yr**."

Caveat in one sentence: **this is a forward run-rate extrapolation off 7 weeks of real data, one of
which (WK27) is dominated by a single non-recurring lane (RDU2→TOL3, a Chicago-crosstown rail
interception) — the range exists because that lane's recurrence is unknown, not because of
measurement noise.**

---

## 1) Fixed inputs (given by the task; NOT recomputed)

- Realized net transport avoidance, WK24–30 2026: **$144,739**.
- ~307 executed loads / ~5.05M units.
- Source: `_notes/azim_entitlement_ytd_deepdive_2026-07-21.md` (+ its 2026-07-24 correction removing
  the CLT2→MCI4 lane, which had no new-manifest-ID / was never independently re-approved at the
  escalated scale — see `promo_doc/evidence/clt2_mci4_verification_2026-07-24.md`).

**One flagged discrepancy (surfacing, not silently fixing):** re-deriving the corrected total
directly from `_notes/azim_entitlement_ytd_loads.tsv` (533-row per-VRID ledger, already carries the
SIM-disproof / reversal / rail-firming flags from the 07-21 re-pulls) — excluding the CLT2→MCI4 lane
entirely and summing `net` over the executed flags (`EXEC-SIM-CONFIRMED`, `EXEC-TRACKER-ONLY`,
`EXEC-UNVERIFIED-IN-VLS`) — reproduces the dollar total **exactly**: **$144,739.03**, 307 loads, but
**5,173,975 units**, not ~5.05M. The gap (≈124K units, 2.4%) traces to the correction note's own
"-0.34M units" line, which was a rough approximation for the CLT2→MCI4 removal, not a recomputation
(actual units removed = 216,069, not ~340,000). MEASURED from the TSV, 2026-07-24. Using **5,173,975
units** below since it is the figure that ties to the $ total to the cent; flagging the ~5.05M figure
in the task brief as a minor rounding artifact, not a contradiction of the $144,739 anchor.

---

## 2) Per-week detail (MEASURED, reconciled to $144,739.03 exactly)

Reconstructed from `_notes/azim_entitlement_ytd_loads.tsv`, excluding the CLT2→MCI4 lane (24 rows:
14 confirmed + 2 unverified + 8 disproven, per the 07-24 correction), keeping the three executed
flags. Every row traces to a VRID; sums verified against the deep-dive's own rollups.

| Week | Loads | Units | Net $ | Dominant lane(s) |
|---|---|---|---|---|
| WK24 (w/o 6/8) | 126 | 2,154,884 | $6,337 | CLT2→RDU2 (60), FTW1→IAH3 (66) |
| WK25 (w/o 6/15) | 5 | 132,106 | **−$83** | FTW1→IAH3 only — CLT2→MCI4 (removed) and RFD2→MDW2 (disproven-by-SIM) both zeroed out |
| WK26 (w/o 6/22) | 15 | 315,324 | $7,382 | RMN3→ABE8 |
| WK27 (w/o 6/29) | 31 | 443,162 | **$65,875** | RDU2→TOL3 (22 loads, $61,536 — the Chicago-crosstown rail-credit lane) + PSP3→LAX9 (9, $4,339) |
| WK28 (w/o 7/6) | 56 | 906,898 | $27,754 | MDW2→RFD2 (45, $8,190) + RDU2→TOL3 tail (6, $17,980) + RFD4→MDW8 (5, $1,585) |
| WK29 (w/o 7/13) | 55 | 953,644 | $14,142 | MDW2→RFD2 (39, $6,377) + RMN3→ABE8 (16, $7,765) |
| WK30 (w/o 7/20) | 19 | 267,957 | $23,332 EST | FWA4→RFD2 (all 19 — accrual-lag EST, VRIDs still faced FWA4 at last VLS pull) |
| **TOTAL** | **307** | **5,173,975** | **$144,739** | |

Loads/week ranged **5–126** (not 15–126 — WK25 drops to 5 once CLT2→MCI4 and the disproven
RFD2→MDW2 rows are removed per the 07-24 correction; the task brief's "~15–126" reflects the
pre-correction tracker-convention count). $/week ranged **−$83 to $65,875**.

### Requested-vs-executed (available pool → captured), same window, tracker convention

| Week | Requested loads | Requested units | (Verified-)executed units | Load exec rate |
|---|---|---|---|---|
| WK24 | 126 | 2,154,884 | 2,154,884 | 100% |
| WK25 | 98 | 2,112,423 | 132,106 | 5% (verified) |
| WK26 | 15 | 315,324 | 315,324 | 100% |
| WK27 | 32 | 453,336 | 443,162 | 97% |
| WK28 | 79 | 1,377,591 | 906,898 | 71% |
| WK29 | 137 | 2,327,050 | 953,644 | 41% |
| WK30 | 46 | 776,270 | 267,957 | 41% (in-flight) |
| **TOTAL** | 533 | 9,516,878 | 5,173,975 | **54.4%** (verified) / 63% (tracker-raw manifest-flip convention) |

WK25's near-zero verified net is **not** the lever pausing — it's an execution-integrity event: its
two largest asks (CLT2→MCI4, 332K units; RFD2→MDW2, 429K units) both failed verification (no
manifest ID / disproven-by-SIM respectively), leaving only 5 FTW1→IAH3 loads standing. Flagging
this because it changes how WK25 should be read in the cadence: it is a **data-quality low**, not
necessarily a **demand low**.

---

## 3) Durable-cadence read

Two non-representative weeks, for different reasons:

- **WK24 (126 loads)** — the tracker's first week; plausibly a backlog dump of everything already
  identified before the tracker existed, not a repeatable weekly load count. Every other week is
  5–56 loads.
- **WK27 ($65,875, of which $61,536 is RDU2→TOL3)** — RDU2→TOL3 is a **one-time rail-crosstown
  interception**: 28 loads total, all in WK27–28, tied to a specific PSC2-origin rail flow that
  happened to route through Chicago en route to a Charlotte-bound lane. The deep-dive itself frames
  it as a narrow window ("23/28 RDU2 loads never had [a similar] crosstown [opportunity] booked");
  nothing in the record establishes it as a standing, repeatable weekly capability. It never
  recurred after WK28.

Excluding both (WK25, 26, 28, 29, 30 = 5 weeks) gives the **durable weekly cadence**: mean
**$14,505/wk**, loads 5–56/wk (mean ~29/wk). This is method 1's primary recommendation (§4).

---

## 4) Method 1 — pure run-rate (primary)

All cuts computed directly off the reconciled per-week table in §2:

| Cut | Weekly $ | ×52 | Note |
|---|---|---|---|
| Naive flat mean (all 7 wks) — the task's own baseline check | $20,677 | **$1,075,204** | = $144,739.03 / 7. Matches the task's own "$144,739/7×52≈$1.08M" naive line. |
| Recent-3-weeks mean (WK28–30) | $21,743 | **$1,130,626** | Still carries WK28's RDU2→TOL3 tail ($17,980 of $27,754). |
| Median week (WK29, $14,142) | $14,142 | **$735,388** | Outlier-robust; agrees closely with the durable-cadence cut. |
| **Durable-cadence (excl. WK24 + WK27)** | **$14,505** | **$754,284** | **Recommended primary** — excludes the launch-burst week and the one-time-lane week, keeps everything else including RDU2→TOL3's WK28 tail. |
| Floor: strip RDU2→TOL3 entirely from all weeks ($79,516 removed) | $9,318 | **$484,917** | Conservative floor if that lane structurally never recurs. |
| Range (min wk → max wk, illustrative only) | −$83 → $65,875 | −$4,322 → $3,425,488 | Not usable directly — shows the volatility a single-week extrapolation would produce; included per the task's ask for "the range." |

**Recommended range: $750K–$1.1M/year.** The spread is driven almost entirely by one question:
*does a RDU2→TOL3-style crosstown interception recur?* If yes (or something like it does, at
similar scale), the recent-weeks/naive end (~$1.0–1.1M) is defensible. If it was genuinely one-time,
the durable-cadence/median figure (~$735–754K) is the honest run-rate, with the fully-stripped
$485K as a hard floor.

---

## 5) Method 2 — volume-grounded

### Source A (Hydra) — status: **REACHABLE** (correcting the task brief's stated blocker)

The task brief stated `hydra_ib` + `o_rr_schedule` are not on the scheduling Redshift cluster. That
was checked fresh this session and is **not correct**: both are queryable directly, live, via the
same `SAschedulingredshift` profile / `scheduling.cba7nbarlfx1...` cluster already used by
`midstream_im_reroutable.connect()` — Redshift datashare cross-database syntax
(`andes.hydra_ib.d_hydra_ib_report_na_daily`, `"andes"."ats-onestopshop".o_rr_schedule`) resolves
and returns real rows. Confirmed via `svv_all_tables` (`database_name='andes'`) and direct
`SELECT * ... LIMIT 1` on both tables, 2026-07-24. andes-mcp being disconnected this session did not
block this path — it went through the existing Redshift connector instead.

**What Source A actually gave, and why it does NOT close out the volume-grounded formula:**

- `account_id = 'TRANSFERSINTERMODALREDIRECTS'`, 2026 YTD (through ~7/27, last 1–2 weeks visibly
  lagged/incomplete): **18,277,373 units / 2,918 loads** — MEASURED, live pull 2026-07-24.
- This account_id is **company-wide** — every team/region's 1P/3P intermodal redirects, not
  AZIM-exclusive. It shows real, material volume every week back to at least Dec 2025 (e.g.,
  1.7M units/wk in mid-Feb 2026), i.e., the *mechanism* pre-dates AZIM's WK24 tracker start by
  months — AZIM is a specific initiative layered onto (and, per below, apparently a large
  contributor to) an already-existing account category, not the sole occupant of it.
- Calendar weeks matching WK24–30 sum to **~5,158,695 units** company-wide under this account —
  same order of magnitude as AZIM's own reconciled 5,173,975 (§2), a reassuring aggregate-level
  cross-check, but the **per-week shapes don't line up** (Hydra's peak is the week of 6/15; AZIM's
  peak week is WK24/6/8). Most likely explained by accrual/invoice-date lag between Hydra's
  `report_date` (a cost-recognition date) and the tracker's flip date — the same lag pattern
  already documented for WK30 FWA4→RFD2 in VLS. **Not treated as a precise per-week validation.**
- Attempted a lane-level join to isolate AZIM specifically: AZIM's true rail *origins* (PSC2, XSB2,
  TCY2/CORWITH) don't match the Hydra `origin` field the way the tracker's giver-FC interception
  points would (origin in Hydra is the upstream rail/vendor origin, not the interception FC), and
  many `origin`/`scac` values are masked/abbreviated (`"P!"`, `"K!"`, `"IR"`, `"C+"`), so a clean
  VRID-level attribution of Hydra $ to AZIM specifically was **not achievable within this session's
  scope**. Filtering by AZIM's **taker** FCs (`final_destination`) does surface real, lane-consistent
  volume (`"P!"→MCI4`/`→TOL3`, `"K!"→ABE8`, `RFD4→MDW8` — all real AZIM lanes) confirming AZIM is
  *directionally* a major driver of this account's taker-side volume in these weeks, but not a
  reconciled dollar figure.
- Contextual finding (not used in the calc): 2026 YTD (partial year, ~30 wks) = 18.28M units already
  exceeds full-year 2025's 15.73M under this account; full-year 2024 was 39.56M. Network-wide
  intermodal-redirect activity is trending up in 2026 vs 2025 — supports that AZIM's ramp rides a
  genuinely growing mechanism, not a shrinking one, but this is directional context, not a number
  that feeds the formula.

**Verdict on Source A: reachable, real data pulled, but does not yield an independent
"annual redirectable 1P-IM volume available to the lever" denominator distinct from AZIM's own
tracker** — because the account isn't AZIM-exclusive and per-VRID attribution wasn't achievable
here. No number was fabricated to force a fit.

### Source B (steering trackers) — status: reachable, used for context only

Live-pulled per-week totals (all mechanisms, all networks) for WK24–30 2026 via
`build_ytd_from_steering.enumerate_trackers`/`fetch_records` (Quip folder `dKL9OAnfDIa`), 2026-07-24:

| Week | Total tracker units (all redirect mechanisms) | AZIM units (§2) | AZIM share |
|---|---|---|---|
| WK24 | 7,086,152 | 2,154,884 | 30.4% |
| WK25 | 8,401,677 | 132,106 | 1.6% |
| WK26 | 6,375,570 | 315,324 | 4.9% |
| WK27 | 7,456,624 | 443,162 | 5.9% |
| WK28 | 6,510,308 | 906,898 | 13.9% |
| WK29 | 4,173,526 | 953,644 | 22.8% |
| WK30 | 4,843,433 | 267,957 | 5.5% |

This confirms AZIM is a real, meaningful (1.6–30%), but minority share of total ICT redirect volume
in its own active weeks. It is **not** a 1P-IM-specific denominator (the tracker mixes NS floor
loads, ARS, rIXD/nIXD non-IM redirects, etc.) — same limitation the retired ÷16.7% method had, just
without the false full-year-seasonality assumption. Included for context, not used to scale the
headline number.

### The self-referential version (shown for completeness, flagged as not independent)

Using AZIM's **own** requested (candidate) volume as the "available pool" — the only pool actually
measured — produces:
```
pool (annualized)   = 9,184,455 requested units (excl. CLT2→MCI4) / 7 wks × 52 = 68,227,380 units/yr
penetration          = 5,173,975 / 9,184,455 = 56.3%
$/unit                = $144,739.03 / 5,173,975 = $0.02797/unit
annual value          = 68,227,380 × 0.563 × $0.02797 ≈ $1,074,690/yr
```
This lands within rounding of Method 1's naive flat-mean ($1,075,204) — **expected, not
confirmatory**: extrapolating the pool linearly by 52/7 and multiplying by the realized penetration
and $/unit is mathematically the same operation as extrapolating realized $ by 52/7 directly. It is
shown for transparency (the task asked for this formula to be attempted) but should **not** be cited
as independent corroboration of the $1.07–1.1M figure — it's the same number, decomposed.

**Bottom line for Method 2:** a genuinely independent volume-grounded annual figure is **not
obtainable this session** even with Source A reachable, because (a) the Hydra account isn't
AZIM-exclusive and (b) VRID-level attribution needs origin/scac decoding work beyond this task's
scope. Method 1 (run-rate) is the basis for the safe-to-claim figure; Method 2's Source-A pull is
retained here as supporting/context evidence (reachability + rough magnitude + trend direction),
not as an alternate calculation.

---

## 6) Safe-to-claim line + honest caveats

> **Safe to claim: AZIM 1P-IM midstream reroute runs at a $750K–$1.1M/year durable cost-avoidance
> rate (point estimate ~$900K/yr if one number is required), based on WK24–30 2026 realized
> performance ($144,739 / 307 loads / ~5.17M units) extrapolated forward as a run-rate — not the
> retired $0.85M ÷16.7%-seasonality figure.**

What this assumes, spelled out:

1. **The lever keeps running at something close to its WK24–30 average weekly $ for the rest of the
   year.** It has 7 weeks of history; this is a forward extrapolation, not a measurement of 52
   weeks.
2. **The RDU2→TOL3-style rail-crosstown interception is the single biggest swing factor** — one
   26–28-load event contributed ~$79.5K (>50% of one week's total) and hasn't recurred since WK28.
   Whether that pattern is a standing capability (→ top of range, ~$1.1M) or a one-off (→ bottom of
   range / floor, ~$750K–$485K) is unconfirmed and would need AZIM/rail-ops input, not something
   derivable from the data pulled here.
3. **WK30's $23,332 is entirely EST** (accrual lag — VRIDs still showed $0 VLS accrual at last pull)
   and WK25's near-zero total reflects two failed/disproven asks, not necessarily lower demand — so
   the "durable cadence" itself still carries some estimation and some execution-integrity noise.
4. **This does not scale with total company redirect volume** — Source B shows AZIM was 1.6–30% of
   total ICT redirect volume in its own active weeks; Source A shows the broader "intermodal
   redirects" account is a multi-hundred-team-wide, multi-year-old mechanism running well beyond
   AZIM's own book. Neither gives a clean independent ceiling on how much MORE volume AZIM could
   capture if scaled up — that would need the VRID-level Hydra attribution this session couldn't
   complete, or a fresh systemwide 1P_IM_TRANSFERS ARRIVAL_SCHEDULED pull (not attempted here; would
   be a new query, not a byproduct of what's already been pulled).
5. **Units basis note:** the $ total ($144,739) is fixed and exact; the units figure used here
   (5,173,975) is 2.4% above the task brief's ~5.05M due to a rounding artifact in the correction
   note (§1) — doesn't affect any $ figure above, flagged for completeness.

---

## Sources

- `_notes/azim_entitlement_ytd_deepdive_2026-07-21.md` (+ 2026-07-24 correction) — realized $144,739
  basis, taken as given per task instruction, not recomputed.
- `_notes/azim_entitlement_ytd_loads.tsv` (533-row per-VRID ledger, MEASURED/EST-tagged) — direct
  Python aggregation 2026-07-24 (`csv.DictReader`, grouped by week/lane, executed-flag filter,
  CLT2→MCI4 excluded) to produce §2's per-week table. Reproduces $144,739.03 / 307 loads exactly.
- `promo_doc/evidence/clt2_mci4_verification_2026-07-24.md` — basis for excluding CLT2→MCI4.
- **Source A, live 2026-07-24:** `andes.hydra_ib.d_hydra_ib_report_na_daily` +
  `"andes"."ats-onestopshop".o_rr_schedule`, queried via `midstream_im_reroutable.connect()`
  (`SAschedulingredshift` / `scheduling.cba7nbarlfx1...`). Confirmed reachable (contrary to task
  brief); queries run: account_id totals by year, weekly totals for
  `TRANSFERSINTERMODALREDIRECTS`/`TRANSFERSREDIRECTS`, origin/destination filters against AZIM
  giver/taker FC lists. Raw result sets are in this session's tool transcript, not persisted to
  disk (read-only task; no exports made).
- **Source B, live 2026-07-24:** `all_team_slides/build_ytd_from_steering.py`
  (`enumerate_trackers`/`fetch_records`/`_is_executed`), Quip folder `dKL9OAnfDIa`, WK24–30 2026
  trackers, re-pulled fresh this session (not from the stale `all_team_slides/ytd_rollup.json`,
  which is monthly-only and was explicitly excluded from the basis per the task instruction).
- `all_team_slides/ytd_rollup.json` / `ytd_rollup_2025.json` — read ONLY to confirm what the retired
  method used and why it doesn't apply; not used as a basis for any number in §4–6.
