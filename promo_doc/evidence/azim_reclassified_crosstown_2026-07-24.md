# AZIM entitlement — corrected crosstown/standard reclassification (run-structure join)

**Built:** 2026-07-24 · **Owner:** William Zhou · **Status:** READ-ONLY reclassification. This is
the only file written; `_notes/azim_entitlement_ytd_loads.tsv` and all code were read but not
edited. No SIM/tracker writeback, no posting.

**Access stated plainly:** VPN + `ada` (`SAschedulingredshift`) confirmed live this session via
`midstream_im_reroutable.connect()`. `andes_local.v_load_summary` queried directly (same-database
alias, no cross-db federation needed) — full leg-level pulls for all 316 loads in the reclassified
base, plus targeted lane-comp queries for WK30 MCI4→IND9. All raw pulls in this session's
transcript; nothing exported to disk beyond this file.

---

## 0) TL;DR

| Question | Answer |
|---|---|
| Corrected realized $ (existing 307-load base) | **$144,739.03 — UNCHANGED.** The reclassification confirms the deep-dive's own classification (RDU2→TOL3 = the only crosstown lane in that base) was already correct. |
| Corrected realized $ (incl. newly-discovered WK30 MCI4→IND9) | **$148,841–$151,565** (partial; avoided-OTR term unresolved — likely understated further) |
| Corrected annualized (naive/52) | **~$1.11M–$1.13M/yr** (was ~$1.075M) |
| Corrected annualized (durable-cadence, primary) | **~$797K–$825K/yr** (was ~$754K) |
| Corrected annualized (median-week, floor) | **~$735K/yr — unchanged** (WK30's bump doesn't cross WK29's median rank) |
| Crosstown vs standard split, full 316-load base | **37 loads / 553,855 units CROSSTOWN** (28 RDU2→TOL3 + 9 MCI4→IND9) vs **279 loads / 4,737,682 units STANDARD** (0 additional crosstowns found anywhere else) |
| Was WK30 MCI4→IND9 crosstown? | **YES — confirmed, all 9 executed loads.** Structurally identical signature to RDU2→TOL3 (disconnected giver-bound dead branch + carrier switch), even though invoice/paid is still null on every leg (accrual lag, loads are 2–4 days old). |
| Is crosstown recurring or one-off? | **Weakens toward "recurring."** Confirmed in 2 of 7 tracked weeks (WK27–28 AND WK30) via 2 structurally distinct origin-hub/carrier pairs (PSC2-hub BNSF/UPRR→NSRR at Chicago-Calumet, and HEA2-hub NSRR→BNSF at Chicago-Croxton). Still only n=2 occurrences — not proven durable, but no longer a single isolated lane. |
| Parse-correction check (mid-run addition) | **Zero VRIDs miscounted** in the existing 307-load base under a proper per-block, header-name-aware parse. The only gap found is a **timing gap, not a parse bug**: 9 WK30 MCI4→IND9 loads were manifested 2026-07-22, one day after the deep-dive's 2026-07-21 TSV snapshot — they simply didn't exist in the tracker yet when the TSV was built. |

---

## 1) Parse-correction verification (per Will's mid-run addition)

**Why this section exists:** Will flagged that the tracker's header blocks have inconsistent
column layout even within one tab, and that the 7/21 deep-dive's "block-aware parse" claim might
have mis-extracted the new-manifest-ID column (which defines "executed"), silently miscounting the
TSV's executed flags.

**Method:** Re-parsed the live tracker (`AZIM Midstream Redirect Requests 2026.xlsx`, mtime
2026-07-24 15:33) independently, tab by tab, detecting every header row by locating a cell equal to
`VRID` (case-insensitive) rather than assuming one header per tab or a fixed column index. For each
detected header block, located the VRID and "new manifest ID" columns **by header name** (tolerant
of case/spacing variants), then extracted every data row until the next header row. 601 data rows
parsed across 29 distinct header blocks.

**Confirmed column drift exists** (this part of Will's concern is real): the new-manifest-ID column
is NOT at a fixed index — it moves between column 8 and column 14 depending on the block:

| Sheet | Header row(s) | New-Manifest-ID column | VRID col | Orig-FC col | Redirect-FC col |
|---|---|---|---|---|---|
| WK24 | 1, 70 | 8 ("New/NEW MANIFEST ID") | 2 | 3 | 7 |
| WK25 | 1, 10, 36, 73, 93 | 9 | 2 | 3 | 7 |
| WK 26 | 1, 18 | 9 | 2 | 3 | 7 |
| WK 27 | 1, 13 | 8 | 2 | 3 | 6 |
| WK 28 | 1, 22, 42, 55, 71, 79 | 8 | 2 | 3 | 6 |
| WK29 | 1, 32, 56, 84, 108, 131 | 9 | 3 | 2 | 7 |
| WK30 | 1, 30 | 9 | 3 | 2 | 7 |
| WK30 | 44, 66 | **13** | 3 | 2 | 8 |
| WK30 | 83 | **13** | 3 | 2 | 6 |
| WK30 | 117 | **14** | 3 | 2 | 6 |

**Result of the cross-check** (per-block-header parse's manifest-shaped VRIDs vs the TSV's
`executed_flag`, after excluding known placeholder text — `Pending`, `IOG Validation PASSED`,
`unable to flip OG manifest`, any `VRID CANCELLED...` variant, `#N/A`):

- **Undercounted** (TSV says not-executed, my parse found a real manifest ID): **0** (2 false
  positives from `VRID CANCELLED: TPC freight not ready` / `...AC continuous scheduling` resolved
  once the placeholder matcher was widened from exact-match to prefix-match).
- **Overcounted** (TSV says tracker-executed, my parse found NO manifest ID anywhere for that
  VRID): **0**.
- **TSV VRIDs not found anywhere in the tracker parse:** 0 (all 533 resolve).
- **Tracker-executed VRIDs (real manifest ID) missing from the TSV entirely: 9** — all 9 are the
  WK30 MCI4→IND9 loads (see §4). Dated 2026-07-22 in the tracker; the TSV was built 2026-07-21
  evening. **This is a snapshot-timing gap, not a column-parse error** — the 7/21 deep-dive's
  block-aware parse was correct for every row that existed when it ran.

**Conclusion: Will's suspected parse bug did not materialize in the existing 307-load executed
base.** The $144,739 / 307-load / 5,173,975-unit total needs no parse correction. The only base
correction needed is additive (§4): 9 more executed loads that postdate the TSV's build.

---

## 2) Method — the run-structure join, and the refinement this task required

Started from the proven method (`_notes/crosstown_gate_scoping_2026-07-24.md`): join
`andes_local.v_load_summary` on `run_structure_id`, filter to `shipment_mode='INTERMODAL'` legs,
and flag a carrier change between consecutive INTERMODAL legs as "crosstown."

**Applying that method naively across the full 316-load base surfaced a real complication that the
single-load proof-of-concept didn't hit:** `run_structure_id` is not always a clean single-container
key. In many runs it groups legs from what appears to be a shared scheduling/interchange window
(duplicate parallel dray legs between the same two nodes, or a small unlogged interchange move),
and sorting strictly by `cpt` breaks ties arbitrarily (alphabetically by VRID) when two legs share
an identical timestamp — which produced spurious "crosstown" and "ambiguous" verdicts on lanes that
are actually fully-executed same-route journeys (e.g., every `CLT2→RDU2` and `RMN3→ABE8` load
initially misclassified this way).

**The fix, arrived at in three iterations and validated against the confirmed RDU2→TOL3 case at
each step:**

1. Reconstruct each run's legs into a **topologically-ordered chain** by matching
   `final_destination` → next leg's `origin` (not by `cpt`, which ties). Duplicate parallel legs
   are resolved by preferring the invoiced/paid one.
2. **A carrier-switch alone is not sufficient evidence of a crosstown interception.** Checked every
   run where 2+ INTERMODAL legs exist: in the large majority (`CLT2→RDU2` 58/60, `FTW1→IAH3` 69/71,
   `RMN3→ABE8` 20/31), **both** rail legs are invoiced+paid — the freight rode the *entire*
   multi-carrier rail path to its normal ramp, and only the final dray target changed. That is
   economically identical to the already-documented `CLT2→MCI4` pattern ("ramp did not change...
   rail was NOT truncated") — no rail leg was avoided, so no credit applies, **even though the
   underlying network topology happens to pass through a carrier interchange.** Labeled
   `STANDARD-RODE-THROUGH` to keep this visible without conflating it with the outright single-carrier
   `STANDARD` cases.
3. **The genuine crosstown signature** is: the run splits into two chains that do NOT connect to
   each other (the connecting interchange leg was never even booked, because the load was
   physically intercepted before it needed to be) — one chain is a **dead branch terminating at the
   historical giver FC with a zeroed/never-invoiced terminal dray**, the other chain **terminates at
   the actual taker FC**, and **the rail leg on the dead-branch side carries a different carrier and
   was never invoiced/paid.** This is exactly RDU2→TOL3's already-documented pattern
   (`_notes/azim_entitlement_ytd_deepdive_2026-07-21.md` "RAIL LEGS FIRMED" section), generalized
   into a repeatable test: identify the chain ending at the taker FC and the chain (if any) ending
   at the giver FC by FC-name match (not by invoice status, since accrual-lag loads can have every
   leg null); if a giver-bound chain exists, has a null-invoice INTERMODAL leg, and that leg's
   carrier differs from the taker chain's rail leg → **CROSSTOWN**, credit = that leg's
   `manifest_total` (a booked planned cost that never got invoiced because the leg never ran — the
   same "canceled-in-practice" signal the deep-dive already established and later confirmed as
   MEASURED once RDU2→TOL3's accruals firmed).

This is NOT the "invoice/paid null vs populated" gate alone (`canceled_load` was already proven
unreliable in the prior scoping doc; a naive "any null leg = crosstown" gate is *also* unreliable,
because accrual-lag loads have null legs on the side that DID execute, per §4). The gate used here
is: **does a genuinely disconnected, FC-identity-confirmed dead branch exist, with a carrier switch
on it** — structure first, invoice-status second (for pricing, not for classification, when
accrual-lag is present).

**Full-base coverage, not sampling:** every one of the 316 loads' `run_structure_id` was resolved
(0 unresolved lookups) and every run's full leg set was pulled and classified individually — this is
not a lane-level extrapolation from a handful of examples.

---

## 3) Corrected crosstown-vs-standard split — full 316-load base

| Lane | Loads | Units | Verdict |
|---|---|---|---|
| CLT2→RDU2 | 60 | — | 55 STANDARD-RODE-THROUGH, 3 STANDARD, 2 accrual-pending (structurally standard) |
| FTW1→IAH3 | 71 | — | 47 STANDARD-RODE-THROUGH, 22 STANDARD, 2 accrual-pending |
| RMN3→ABE8 | 31 | — | 20 STANDARD-RODE-THROUGH, 11 accrual-pending (structurally standard) |
| PSP3→LAX9 | 9 | 90,561 | 9 STANDARD |
| **RDU2→TOL3** | **28** | **436,293** | **28 CROSSTOWN** (confirmed — matches deep-dive) |
| MDW2→RFD2 | 84 | — | 84 STANDARD |
| RFD4→MDW8 | 5 | 1,633 | 5 STANDARD |
| FWA4→RFD2 | 19 | 267,957 | 19 STANDARD |
| **MCI4→IND9 (new, WK30)** | **9** | **117,562** | **9 CROSSTOWN** (new finding — §4) |
| **TOTAL** | **316** | **5,291,537** | **37 CROSSTOWN / 5,555 accrual-pending-but-standard / 264 confirmed-standard, incl. 122 STANDARD-RODE-THROUGH** |

Rollup:

```
                        loads   units
CROSSTOWN                  37   553,855
STANDARD (all shades)     279  4,737,682
  of which STANDARD-RODE-THROUGH   122  2,381,545  (carrier switch present, but leg ran -- no credit)
  of which STANDARD (single-carrier or no switch)  142  2,105,716
  of which accrual-pending (structurally standard, too recent to fully invoice)  15   250,421
```

**Answer to the deep-dive's core assumption:** "RDU2→TOL3's 28 loads as the ONLY crosstown,
everything else same-ramp/standard" is **CONFIRMED CORRECT for the 307-load base that existed on
2026-07-21.** Zero additional crosstowns were found anywhere in `CLT2→RDU2`, `FTW1→IAH3`,
`RMN3→ABE8`, `PSP3→LAX9`, `MDW2→RFD2`, `RFD4→MDW8`, or `FWA4→RFD2` — despite several of those lanes
(`CLT2→RDU2`, `FTW1→IAH3`, `RMN3→ABE8`) structurally passing through a carrier interchange on
nearly every load. The ONLY correction is additive: a 9th crosstown-shaped lane (`MCI4→IND9`) that
didn't exist in the ledger yet.

One steel-wheel-ramp load found in passing (`1148G2SDB`, RMN3→ABE8, WK29 — `BNSF-LOSANGELES-SW` /
`CSXT-CHICAGO59TH-SW` / `CSXT-CHAMBERSBURG-SW`); already executed and fully invoiced end-to-end
(STANDARD-RODE-THROUGH), so the never-redirectable flag is informational only here, not a
reclassification.

---

## 4) WK30 MCI4→IND9 — Will's specific question, tested explicitly

**Finding: YES, all 9 executed WK30 MCI4→IND9 loads are genuinely CROSSTOWN.**

These loads are **not in `_notes/azim_entitlement_ytd_loads.tsv` at all** — the tracker's `WK30` tab
carries a 14-row MCI4→IND9 block dated 2026-07-22 (§1), one day after the TSV's 2026-07-21 build.
Of the 14: **9 have a real `NEW Manifest ID`** (executed, 117,562 units); **5 show `#N/A`** for
`Run Structure` / `Leg3 VRID` / `NEW Manifest ID` (never executed, 62,585 units) — correctly
excludable, same convention the TSV already uses elsewhere.

**Structural evidence, identical shape across all 9 (MEASURED from `v_load_summary`, live
2026-07-24):**

```
GIVER-BOUND DEAD BRANCH (never ran, terminal dray zeroed):
  BNSF-WILLOWSPRINGS-CS --[rail, BNSF, invoice/paid NULL, manifest_total $746-$762]--> BNSF-LOGPARKAN-CS
  BNSF-LOGPARKAN-CS --[dray, invoice/paid NULL, manifest_total $0]--> MCI4  (the ORIGINAL tracked VRID)

TAKER-BOUND EXECUTED CHAIN (the actual redirect):
  HEA2 --[dray]--> NSRR-CROXTON --[rail, NORFOLK SOUTHERN, invoice/paid NULL, manifest_total $469-$493]--> NSRR-CHICAGO47TH
  NSRR-CHICAGO47TH --[dray]--> IND9  (the tracker's own "Leg3 VRID" -- confirmed new taker leg)
```

Carrier switch: **BNSF (avoided) → NSRR (executed)**, at Chicago (Willowsprings/Logparkan vs
Croxton/Chicago-47th) — the same generic "PSC2/HEA2-hub freight interchanges carriers at Chicago"
topology as RDU2→TOL3, just a different hub and a reversed carrier order. The giver-side dray's
`manifest_total = $0` on every one of the 9 loads is the identical "canceled-in-practice, zeroed"
signature already established for RDU2→TOL3's avoided drays.

**Why invoice/paid is null on the EXECUTED side too (not a disqualifier):** these loads are 2–4
days old (tracker dates 2026-07-20 to 2026-07-22; pull date 2026-07-24) — this is the same
accrual-lag pattern already documented for WK30 FWA4→RFD2 in the deep-dive ("all VRIDs still face
FWA4 with $0 accrual... VLS hasn't caught up"). Classification here rests on chain structure and FC
identity (§2), which is available now; pricing (below) is partially blocked by the same lag.

**$ impact — MEASURED piece:**

| Component | Value | Source |
|---|---|---|
| Avoided rail leg (BNSF Willowsprings→Logparkan) manifest_total, per load | $746–$762 (avg $758.44) | MEASURED, per-VRID manifest record |
| **Rail-delta credit, 9 loads** | **$6,826.00** | MEASURED (manifest accrual; not yet invoice-confirmed — same pending-firm status the deep-dive gave RDU2→TOL3 before its accruals posted) |

**$ impact — EST/partial piece (Will's formula additionally needs X, Y, avoided_OTR):**

| Term | Value | Basis |
|---|---|---|
| X (planned MCI4-bound dray, Logparkan→MCI4) | $302.47 EST | lane-median, 120d, n=200 invoiced TRUCKLOAD legs (the specific canceled leg itself shows $0, never priced) |
| Y (actual taker-bound dray, Chicago47th→IND9) | $605.13 EST | lane-median, 120d, n=585 invoiced TRUCKLOAD legs (actual per-load Y is $0 accrued — accrual lag, per above) |
| avoided_OTR (MCI4→IND9 direct spot) | **UNRESOLVED** | The only 29 `MCI4→IND9`-direct rows in VLS are dated entirely within this same WK30 redirect window (07-16 to 07-25) — they are artifacts of this redirect, not an independent pre-existing spot lane. No non-circular comp exists. Not fabricated. |
| Partial net (rail credit + X−Y, **excl. OTR**) | **$4,102.06 EST**, 9 loads | $6,826.00 + 9×(302.47−605.13) |

**The $ delta, stated plainly:** if MCI4→IND9 had defaulted to the ledger's usual STANDARD/no-credit
treatment (as every non-RDU2→TOL3 lane does), it would contribute **$0** in rail credit. Correctly
recognizing it as crosstown adds a **MEASURED $6,826** rail credit, and a **partial EST net of
$4,102** once the (thin, EST) dray-delta terms are included — with the avoided-OTR term (typically
the single largest positive term in every other lane's net — $2,242 on RDU2→TOL3, $823 on
RMN3→ABE8, $671 on FTW1→IAH3) still excluded and UNRESOLVED. **The true net for this lane is very
likely higher than $4,102 once OTR is priced** — this is a floor, not a ceiling, and should not be
read as "this lane is barely worth anything."

---

## 5) Corrected realized total — reconciliation

```
                                          loads   units       net $
Existing 307-load base (TSV, unchanged)    307   5,173,975   $144,739.03   MEASURED (reproduces exactly)
+ WK30 MCI4->IND9 (new, this session)        9     117,562   $4,102.06 EST (partial, OTR excl.) to $6,826.00 (rail-credit-only view)
= CORRECTED TOTAL                          316   5,291,537   $148,841.09 to $151,565.03
```

Both figures for the MCI4→IND9 addition are shown because there are two defensible ways to present
a partially-priced lane: the conservative "just the proven rail credit" ($151,565 all-in) or the
"best-effort full formula minus the unresolved term" ($148,841 all-in, which nets a small negative
EST dray-delta against the measured rail credit). **Neither should be quoted as final** — avoided_OTR
is missing from both and would only add, not subtract.

**Everything else in the deep-dive's $144,739 realized total stands unchanged** — the 7-lane,
307-load, pre-existing base needed no correction (§3).

**Flagged per task item 5 (loads where `v_load_summary` couldn't cleanly resolve):**
- 0 of 316 loads failed `run_structure_id` lookup entirely.
- 1 load (`116R53MQT`, RDU2→TOL3) was mis-flagged `STANDARD` by this session's first automated
  batch pull because its avoided leg (`114LX9F3R`) didn't come back in that specific batch query
  for an undetermined reason (chunking artifact, not a data gap) — a direct single-VRID re-query
  confirmed the leg exists under the same `run_structure_id` with the expected `CROSSTOWN` signature
  (NSRR-CALUMET→NSRR-CHARLOTTE, null invoice, $996 manifest_total). Corrected manually; already
  folded into all totals above and into the deep-dive's own $144,739 (this load was already
  correctly priced there from its dedicated, non-batched verification).
- 15 loads (2 CLT2→RDU2, 2 FTW1→IAH3, 11 RMN3→ABE8) are structurally confirmed STANDARD
  (single connected chain to the taker FC) but have not yet fully invoiced — these are recent WK29
  loads and were already carrying EST-Y flags in the TSV; no reclassification needed, just noting
  they're not yet fully MEASURED.

---

## 6) Corrected annualized figure — method from `promo_doc/evidence/azim_annualization_2026-07-24.md`

Re-running that doc's own methods with the corrected realized base ($148,841–$151,565 / 7 weeks,
MCI4→IND9 attributed to WK30):

| Method | Prior (that doc) | Corrected | Change |
|---|---|---|---|
| Naive flat mean ×52 | $1,075,204 | **$1,105,590–$1,125,911** | +$30K to +$51K |
| Recent-3-weeks (WK28–30) ×52 | $1,130,626 | **~$1,143K–$1,167K** | modest bump (WK30 term rises) |
| Median week (WK29) ×52 | $735,388 | **$735,388 — unchanged** | WK30's bump doesn't overtake WK29's rank |
| **Durable-cadence (excl. WK24, WK27) — primary** | $754,284 | **$796,921–$825,250** | +$43K to +$71K |
| Floor (strip RDU2→TOL3 entirely) | $484,917 | **$484,917 — unchanged** (MCI4→IND9 not stripped in this view) | — |

**Revised range: ~$795K–$1.13M/yr, point estimate ~$920K/yr if one number is required** (was
$750K–$1.1M / ~$900K). The dollar shift is small (WK30 MCI4→IND9's own $ contribution is a few
thousand dollars against a $150K base) — **this is not the headline finding.**

**The headline finding is qualitative, and it directly addresses the annualization doc's central
open question ("does a RDU2→TOL3-style crosstown interception recur, or was it one-time?"):**

- Crosstown interception has now been confirmed in **2 of the 7 tracked weeks** (WK27–28 for
  RDU2→TOL3, WK30 for MCI4→IND9) — not one isolated week/lane.
- The two occurrences are **structurally distinct**: different origin hub (PSC2 vs HEA2), different
  avoided/executed carrier pair (BNSF/UPRR→NSRR at the Chicago-Calumet/Cicero interchange, vs
  NSRR→BNSF at the Chicago-Croxton/Willowsprings interchange), different taker FC (TOL3 vs IND9).
  This is evidence of a **general network mechanism** (multi-carrier PSC2/HEA2-hub-style long-haul
  runs interchange at Chicago; an AZIM redirect that intercepts before that interchange avoids a
  rail leg, wherever in the network it happens) rather than one specific lane's quirk.
- **This weakens — but does not eliminate — the "one-time RDU2→TOL3 windfall" concern.** n=2
  occurrences in 7 weeks is still a thin sample; it is not proof of a standing weekly capability.
  But "it happened once, in one lane, and never again" is no longer an accurate characterization of
  the data — it happened in a second, different lane three weeks later. The honest updated framing:
  **crosstown interception looks like a recurring feature of this network topology that surfaces
  opportunistically wherever a PSC2/HEA2-hub-style redirect happens to be requested before the
  Chicago carrier interchange, not a one-off event tied to the RDU2→TOL3 pairing specifically.**
  Confirming whether it recurs at a similar cadence going forward still needs more weeks of data —
  not asserted here.

---

## 7) Sources / provenance

- `_notes/azim_entitlement_ytd_loads.tsv` — 533-row ledger, read only; 307-load executed base
  reproduced by filtering `executed_flag` in (`EXEC-SIM-CONFIRMED`, `EXEC-TRACKER-ONLY*`,
  `EXEC-UNVERIFIED-IN-VLS`) and excluding the `CLT2->MCI4` lane per Will's 2026-07-24 ruling. Sums to
  $144,739.03 / 307 loads / 5,173,975 units exactly.
- `_notes/azim_entitlement_ytd_deepdive_2026-07-21.md` (+ 2026-07-24 correction) — prior methodology,
  the $144,739 figure, and the RDU2→TOL3 "RAIL LEGS FIRMED" section whose method this reclassification
  generalizes.
- `_notes/crosstown_gate_scoping_2026-07-24.md` — the proven run-structure-join method this task
  was scoped to use; extended here (§2) to handle full-base batch reclassification, which the
  original single-load proof-of-concept didn't need to handle.
- `promo_doc/evidence/azim_annualization_2026-07-24.md` — annualization methods reused in §6.
- `C:/Users/zhouzw/OneDrive - amazon.com/AZIM Midstream Redirect Requests 2026.xlsx` — live tracker,
  mtime 2026-07-24 15:33, tabs WK24–WK30, re-parsed per-block by header name (§1); source of the 9
  WK30 MCI4→IND9 executed VRIDs and their `run_structure_id`s (not present in the TSV).
- **Live Redshift, 2026-07-24**, `andes_local.v_load_summary` via `midstream_im_reroutable.connect()`
  (`SAschedulingredshift`): VRID→`run_structure_id` resolution for all 316 loads (2 batched queries,
  150/query); full leg pull for all 316 distinct `run_structure_id`s (1,325 leg-snapshot rows, latest
  `report_day` per leg kept); targeted lane-median queries for MCI4→IND9's X/Y/avoided-OTR comps
  (BNSF-LOGPARKAN-CS→MCI4, NSRR-CHICAGO47TH→IND9, MCI4→IND9 direct, BNSF-WILLOWSPRINGS-CS→
  BNSF-LOGPARKAN-CS). Raw pulls in this session's transcript only; nothing exported.
- Every number above is tagged MEASURED, EST, or UNRESOLVED inline. Nothing was fabricated to force
  a complete formula where the data (avoided_OTR for MCI4→IND9) doesn't yet support one.
