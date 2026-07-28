# TOFC methodology audit — LAS1/VGT2 Q2 2026 cost-avoidance ($336K headline)

**Built:** 2026-07-27 · **Owner:** William Zhou · **Status:** READ-ONLY audit — no edits to any
tracker/SIM/Slack/repo file except this one. All pulls LIVE today unless noted.

**Mandate:** stress-test the ~$336K / 146-trailer / $2.3K-per-trailer TOFC cost-avoidance figure in
`promo_doc/evidence/ex3_yoy_and_tofc_entitlement_2026-07-24.md` with the same rigor the AZIM audit
applied (corridor-comp EST → measured leg VRIDs, 2.7x correction, fake-executed removal, settlement
actuals). Unlike AZIM, **this audit finds the original number is UNDER-, not OVER-stated on the
execution side, but the counterfactual (OTR) side is weaker evidence than assumed.** Read the whole
thing before quoting a number — the "right" headline depends on a judgment call about the
counterfactual that I cannot make for Will.

---

## TL;DR

| | Value | Confidence |
|---|---|---|
| Trailers, ground-truth SharePoint/VRID tracker (WK17–21) | **190** | MEASURED |
| Of which confirmed fake-executed (manifest flipped, never moved) | **1** (0.5%) | MEASURED |
| **Corrected executed population** | **189** | MEASURED |
| Units, 189 genuine trailers | **3,197,654** | MEASURED |
| MEASURED TOFC actual cost (settlement, mean/trailer) | **$3,946** (median $3,797) | MEASURED (183/189 rail legs + most dray legs = settled invoice; 6/189 partly rest on a MANIFEST/TONU estimate) |
| OTR counterfactual | **UNRESOLVED** — zero exact-lane OTR truckload moves exist in VLS on any of the 4 lanes, the entire program window | EST only, either basis below |
| — desk-assumption basis ($6.6K/trailer, unchanged) | savings $2,654/trailer → **$501,524 total** | EST (unimproved) |
| — live geo-relaxed VLS basis (lane-specific) | savings $3,621/trailer avg → **$684,330 total** | EST (better sourced, still no exact-lane comp) |
| **Recommended headline** (conservative: fixes only what I can measure) | **~$502K** (189 trailers × ($6,600 desk-OTR − $3,946 measured-TOFC)) | see caveat below |
| Original ex3 headline | $335,800 (146 × $2.3K, both sides assumed) | superseded by this pull |

**The single biggest open question this audit could NOT close:** was OTR really the counterfactual,
or would these floor trailers otherwise have just dwelled at LAS1/VGT2 (the exact problem the lever
exists to fix)? Zero exact-lane OTR moves in VLS is consistent with either "OTR essentially never
runs this pair, so the $6.6K figure is a pure model, not an observed price" or "correct — nobody
does this OTR because TOFC is what enabled the redirect at all, so it's the right counterfactual
policy question, if not an observed transaction." I can't resolve this from transportation data
alone — see §3.

---

## 1. What actually executed — ground truth vs. the steering-tracker proxy ex3 used

### 1.1 Source and verification

Ex3's 146-trailer figure came from the **Quip steering tracker** (weekly redirect-ask/approval
doc), filtered to giver∈{LAS1,VGT2}, taker∈{RFD2,MDW2,FWA4}, with 4 of 7 rows explicitly "TOFC SIM"
tagged and 3 inferred. That is a **proxy** for execution — it's an ask/approval record, not a
transportation record.

This audit instead pulled the **actual execution artifact**: the pinned SharePoint tracker AZIM and
ICT worked off of live in-channel, `LAS1 TOFC Redirects WK17-20.xlsx` (despite the filename, tabs
run WK 17 / WK18 / WK 19 / WK 20 / WK 21), which has one row per physical trailer with **Original
VRID, Original FC, Trailer #, Original Manifest ID, Units, Redirect FC, First Leg Redirect VRID,
Last Leg Redirect VRID, NEW MANIFEST ID**.

- **Local OneDrive copy:** `C:\Users\zhouzw\OneDrive - amazon.com\LAS1 TOFC Redirects WK17-20.xlsx`
  (mtime 2026-05-22, matches the program's last activity date before standby).
- **Verified current:** resolved the pinned Slack link
  (`https://amazon-my.sharepoint.com/:x:/p/zhouzw/IQC31MyrYtc9RL8XyhGvRv3GASMhYyM-XdYPc_eVXM1OVpQ`)
  via `sharepoint_resolve_url` → same server-relative path
  (`/personal/zhouzw_amazon_com/Documents/LAS1 TOFC Redirects WK17-20.xlsx`). Fetched a fresh copy
  live today — identical byte size (52,256 bytes) to the local OneDrive copy. Treated as current.

### 1.2 Row count reconciliation — 190, not 146

After stripping embedded repeat-header rows, the tracker has **190 unique trailer rows** across
WK17–21 (4/24–5/22/2026), **every one with NEW MANIFEST ID populated** (100% "executed" under the
same rule Ex6 used for the AZIM tracker). No duplicate `Original VRID`, `Trailer`, or
`First Leg Redirect VRID` values — no double-counting in the raw tracker.

| Week | Dates | Lane(s) | Trailers |
|---|---|---|---|
| WK 17 | 4/24 | LAS1→RFD2 (10), LAS1→MDW2 (5) | 15 |
| WK18 | 4/30–5/1 | LAS1→RFD2 (41), VGT2→RFD2 (4) | 45 |
| WK 19 | 5/4–5/11 | VGT2→MDW2 (75) | 75 |
| WK 20 | 5/14–5/15 | VGT2→MDW2 (15), VGT2→RFD2 (5) | 20 |
| WK 21 | 5/19–5/22 | VGT2→RFD2 (25), LAS1→RFD2 (10) | 35 |
| **Total** | 4/24–5/22 | | **190** |

**Where ex3's 146 undercounts:** ex3's steering-tracker pull is missing WK17's 5-trailer LAS1→MDW2
lane entirely, is short ~11 trailers on WK18's LAS1→RFD2 leg (30 captured vs 45 actual), and misses
WK21 almost completely (7 captured vs 35 actual — ex3 only picked up a same-lane blank-cost row, not
the 25 VGT2→RFD2 + 10 LAS1→RFD2 that the ground-truth tracker shows). **This corroborates, with hard
VRID-level evidence, the caveat ex3 itself already flagged** ("the steering tracker's own cost/volume
fields undercount realized activity") — the correction here runs the *opposite* direction from
AZIM's (AZIM's proxy overstated; this proxy understated).

### 1.3 Finding the actual leg-level cost — the tracker's 2 VRID columns are dray-only

Querying `andes_local.v_load_summary` for the 380 First/Last Leg VRIDs in the tracker returns **555
rows, 100% `shipment_mode = TRUCKLOAD`.** There is no rail-mode VRID in the tracker's own two VRID
columns — meaning the tracker literally only names the **origin dray** (giver→BNSF-Bernardino) and
**destination dray** (BNSF-Willowsprings/Corwith→taker) legs. **The rail leg itself is a third,
separately-priced VRID that AZIM creates under the same `run_structure_id` but never surfaces in the
tracker.**

Pivoting through `run_structure_id` (query VLS for every run structure that contains a tracker
First/Last-Leg VRID) recovers the full picture: **189 of 190 run structures resolve to a clean
3-leg chain** — `[giver]→BNSF-Bernardino-TE` (TRUCKLOAD dray) → `BNSF-Bernardino-TE→BNSF-
Willowsprings-TE or BNSF-Corwith-TE` (**INTERMODAL**, ~1,967–1,978mi, BNSF) →
`BNSF-Willowsprings/Corwith-TE→[taker]` (TRUCKLOAD dray). 3 of 190 have a 4th leg (a retry — see
§1.5). All 190 run structures were found 100% (555/555 known VRIDs, 589/589 rows under the 198
run-structure IDs pulled).

### 1.4 Measured cost distribution (189 genuine trailers — excludes the 1 fake, §2)

| Stat | Value |
|---|---|
| Sum, `total_paid_amount` | **$745,876.11** |
| Mean / trailer | **$3,946.43** |
| Median / trailer | $3,797.27 |
| Std dev | $610.49 |
| Min / Max | $1,514.15 / $8,533.76 |
| Sum, `total_accrual` (if unsettled legs land at their accrual estimate) | $757,701.55 |

By lane:

| Lane | n | Mean TOFC cost/trailer |
|---|---|---|
| LAS1→MDW2 | 5 | $4,692.94 |
| LAS1→RFD2 | 60 | $3,932.82 |
| VGT2→MDW2 | 90 | $3,963.97 |
| VGT2→RFD2 | 34 | $3,814.26 |

**Accrual/settlement gap:** 6 of 189 trailers (3.2%) have at least one leg priced off `accrual_cost_
source = MANIFEST` or `TONU` (an estimate) rather than a settled `INVOICE`. The gap ranges $154–
$2,940/trailer on those 6 — small in aggregate ($11,825 total, 1.6% of the $745,876 sum) but the same
species of measurement hole the AZIM review flagged on RDU2→TOL3 (53% of that number resting on an
estimated leg). Here it's contained to a handful of trailers, not the majority.

**Positive, verified finding — rate-parity worked:** the intermodal (rail) leg price dropped from a
**uniform $3,596.72/leg across all 15 WK17 trailers** to a **$2,313.00 flat floor covering 155 of 188
priced rail legs (82%) from WK18 onward** — a ~36% real cost reduction, consistent with
`tracker.md`'s risk log ("Procurement engaged upfront this time" on rate parity). $2,313/1,967mi =
**$1.18/mi**, comfortably under the ~$2.50/mi container-parity ceiling Procurement was targeting — the
negotiated rate beat its own target. Residual outliers: 13 WK19 legs at $3,515.76 and 1 WK19 leg at
$7,031.52 (3x the modal rate) never cleared to the $2,313 floor — worth a follow-up with Procurement/
Intermodal on why, but immaterial to the headline (14 of 188 legs, <1% of total $).

**Data-quality anomaly (immaterial, flagged not fixed):** 3 of ~570 dray legs are priced at exactly
$2,313.00 — the flat RAIL rate — posted against what should be a $130–$330 short local dray leg
(2 on VGT2→Bernardino, 1 on Willowsprings→MDW2). Looks like a VRID/leg-mapping data-entry artifact,
not a real $2,313 dray. $6,939 total exposure (<1% of the $745,876 sum) — flagged, not adjusted, per
the no-silent-filtering rule.

### 1.5 Worked examples (2 clean + 1 failed — see §2 for the failed one)

**Example 1 — clean, VGT2→MDW2, WK19 (ask 5/6, moved 5/7).** Trailer `AZNG-HV2201816`, orig manifest
`POC3_VGT2_...`, 30,961 units, run structure `R-1111936YY`:

| Leg | Origin→Dest | Mode | Miles | Carrier | Invoice=Paid |
|---|---|---|---|---|---|
| 1 | VGT2 → BNSF-Bernardino-TE | TRUCKLOAD | 236 | NexGen Trucking | $1,284.95 |
| 2 | BNSF-Bernardino-TE → BNSF-Corwith-TE | INTERMODAL | 1,978 | BNSF | $3,515.76 |
| 3 | BNSF-Willowsprings-TE → MDW2 | TRUCKLOAD | 22 | (unlisted) | $190.64 |
| **Total** | | | | | **$4,991.35** |

Geo-relaxed OTR EST for VGT2→MDW2: $8,254.58 (n=13). Implied avoided (if OTR holds): **$3,263.23**.

**Example 2 — clean, LAS1→RFD2, WK21 (ask 5/21, moved 5/22).** Trailer `AZNG-HV2203065`, orig
manifest `QXY8_LAS1_...`, 11,568 units, run structure `R-113YWD43Z`:

| Leg | Origin→Dest | Mode | Miles | Carrier | Invoice=Paid |
|---|---|---|---|---|---|
| 1 | LAS1 → BNSF-Bernardino-TE | TRUCKLOAD | 213 | NexGen Trucking | $1,176.92 |
| 2 | BNSF-Bernardino-TE → BNSF-Willowsprings-TE | INTERMODAL | 1,967 | BNSF | $2,313.00 |
| 3 | BNSF-Willowsprings-TE → RFD2 | TRUCKLOAD | 41 | (unlisted) | $333.17 |
| **Total** | | | | | **$3,823.09** |

Geo-relaxed OTR EST for LAS1→RFD2: $6,964.89 (n=18). Implied avoided (if OTR holds): **$3,141.80**.

**The 3-leg retry cases (4 of 190, not counted as failures):** `R-113SBPZVJ`, `R-116KZKKWS`,
`R-11353JPQK` each show a 4th leg — a canceled first attempt at the destination dray (once corroborated
in-channel: the 4/25 "mech issue" trailer `115G3ZRF6` in Slack is the exact origin-dray VRID inside
`R-116KZKKWS`) — followed by a successful, paid second attempt. These are genuine executions with a
small extra wasted-attempt cost layered in ($154–$175 on 2 of the 3); already included in §1.4's totals.
One more (`R-113B77JSH`) has its rail leg mode-labeled TRUCKLOAD with a stray `canceled_load=TRUE` flag
despite being fully invoiced/paid at a rail-tier price — ambiguous data labeling, included as measured
since the $ was paid.

---

## 2. Execution-integrity check — one confirmed fake-executed load

Applying the AZIM audit's manifest-ID discipline, ALL 190 tracker rows show `NEW MANIFEST ID`
populated (100% "executed" by that rule alone). Going one step further — checking VLS for actual
departure/arrival timestamps on all three legs of every run structure — surfaces **exactly one
fake-executed load:**

**Run structure `R-111TW6JFR` — LAS1→RFD2, WK18, trailer `TT608401`, orig manifest
`POC1_LAS1_...`, 10,215 units.**

| Leg | VRID | Status | Paid | Timestamps |
|---|---|---|---|---|
| 1 (LAS1→Bernardino) | `112BFXS56` | **canceled**, reason `AC_SCHEDULING_ERROR`, canceled 1.2h *after* scheduled depart | $0.00 | no calc-depart, no calc-arrival |
| 2 (Bernardino→Willowsprings) | `116RNV3LJ` | **canceled**, same reason | $0.00 (accrual source=MANIFEST, not invoice) | none |
| 3 (Willowsprings→RFD2) | `114V7MCYG` | **canceled**, same reason | $0.00 (accrual source=MANIFEST) | none |

**Slack corroboration (exact match, VRID for VRID):** Jamie Dougan, 2026-05-04 18:59 in
`vegas-tofc-redirects-q2-2026`: *"VGT2→MDW2 15 trailers/295980 units added to tracker. Also, there
was a cancelled LAS1→RFD2 VRID **112BFXS56**. Trailer is still at LAS1. Should I flip everything back
to face LAS1 to work?"* — three independent sources (VLS cancellation flags + zero settlement + no
movement timestamps; Slack ground truth stating the trailer never left LAS1; and the tracker still
showing `NEW MANIFEST ID` = `LAS1-RFD2-11d1d5a4-...` as if it executed) agree this load **never
physically moved.** It should be excluded from any headline trailer/unit/$ count.

**Verdict: 189 of 190 tracker rows (99.5%) are genuinely executed** — all 189 have a non-canceled
final-destination leg with a real `dest_calc_arrival` timestamp at the taker FC (188 also have a
`dest_finish_unloading_time`; the 189th has calc-arrival but the finish-unload field is null, likely
just unload-record timing lag, not a red flag on its own). **This is a materially cleaner execution
rate than the AZIM precedent** — the mechanism largely did what it claimed.

---

## 3. The counterfactual verdict — OTR is not a measured fact for this lane pair

### 3.1 Zero exact-lane comps

Queried `andes_local.v_load_summary` for genuine direct TRUCKLOAD moves — `origin` = LAS1 or VGT2,
`final_destination` = RFD2 or MDW2, non-canceled, `report_day` between 2026-04-01 and 2026-07-27
(the whole program window plus lead-in and lag):

**Zero rows on all four lane pairs.** Amazon did not run a single direct OTR truckload move on
LAS1→RFD2, LAS1→MDW2, VGT2→RFD2, or VGT2→MDW2 in this entire window, TOFC-adjacent or otherwise.
There is no A/B control group.

### 3.2 Where the $6.6K figure actually came from

Traced to source: Will's own message in-channel, 2026-05-15 17:14, proposing a process change to
AZIM (skip the LAS1/VGT2 leg, flip nIXDs direct):

> Scenario 1 (current vegas TOFC routing): $0.7K POC2→LAS1 + $1.1K LAS1→Bernardino + $2.3K
> Bernardino→Willowsprings + $0.2K Willowsprings→RFD2 = **$4.3K/trailer**
> Scenario 2 (nIXD-direct TOFC): $0.1K POC2→Bernardino + $2.3K + $0.2K = **$2.6K/trailer**
> Scenario 3 (nIXD OTR direct): **$6.6K/trailer POCs→RFD2**

**This confirms ex3's reading exactly, from primary source, and resolves an ambiguity ex3 could not:**
the $6.6K figure was modeled for **POC(nIXD)→RFD2 OTR**, not for LAS1/VGT2→RFD2/MDW2 OTR — the pair
that actually executed. `las1_tofc_q2/CLAUDE.md`'s unit-economics table bundles both under one row
("nIXD/LAS1/VGT2 → dest, over-the-road (OTR status quo for some lanes): $6.6K") without ever
confirming the two lanes price the same. Given LAS1/VGT2 (Las Vegas) sit ~250–350 fewer miles from
Chicago than the SoCal nIXDs, a naive prior would expect LAS1/VGT2→RFD2 OTR to run *cheaper* than
$6.6K, not the same or higher.

### 3.3 Live geo-relaxed EST (best available, still not exact-lane)

Ran `lane_cost.refresh_lane_cost()` live against VLS today (temp cache only —
`%TEMP%\_tofc_audit_lane_cache.json`; the repo's real `redirect_budget/cache/lane_cost_60d.json`
was never touched):

| Lane | Cost | Basis | n |
|---|---|---|---|
| LAS1→RFD2 | $6,964.89 | origin zip3 890xx, 60d median | 18 |
| LAS1→MDW2 | $6,518.85 | dest zip5 60433, 60d median | 25 |
| VGT2→RFD2 | $6,964.89 | origin state NV, mileage-clamped 1,393–2,090mi | 18 |
| VGT2→MDW2 | $8,254.58 | origin FC × dest zip5 60433, 60d median | 13 |

All four resolve through **geographic relaxation tiers 2–3** of the estimator (no exact-lane comp
exists at any tier) — same honesty-contract discipline as Ex6, just with a worse starting point
(Ex6 had exact-lane hits on all 9 lanes; this population has none). These land 5–25% *above* the
desk's flat $6.6K assumption, not below — contrary to the AZIM-style expectation that a live re-pull
would shrink an inflated estimate.

### 3.4 The unresolved question: OTR, or dwell?

The program exists **because** LAS1/VGT2 floor trailers were degrading NVF push at 10+ days —
i.e., the underlying problem is dwell. Zero observed OTR moves on this exact pair is consistent with
either:

- **(a)** OTR genuinely never runs this pair because it's uneconomical/rare at this distance, and TOFC
  was invented specifically because there was no other live redirect lever — meaning the "$6.6K OTR"
  figure is a legitimate policy counterfactual ("what we'd have had to pay to force relief by truck")
  even though it's never been observed, or
- **(b)** the true no-TOFC alternative for at least some of these 189 trailers was **continued dwell**
  at LAS1/VGT2, not a paid OTR move — in which case the "vs OTR" transport-savings framing is the
  wrong lens entirely, and the real value driver is dwell/NVF relief (unquantified in dollars in any
  evidence I could find), **exactly the AZIM methodology review's finding #1** ("the value is the
  avoided re-handle + avoided dwell/gridlock relief... on a different basis, not transport").

I found no evidence in the tracker, Slack, or VLS that lets me pick between (a) and (b) with
confidence — this is a genuine floor, not a gap I failed to look hard enough for. **Flagging for
Will's judgment call, not resolving it myself.**

---

## 4. Reconciling the numbers floating around

| Figure | What it actually measures | Status after this audit |
|---|---|---|
| **$2.3K/trailer** ("as-executed" savings, ex3) | Desk-assumed $6.6K OTR − desk-assumed $4.3K TOFC, both EST | Superseded — TOFC side is now MEASURED ($3,946 mean, ~8% below the $4.3K assumption); OTR side still EST |
| **$4.0K/trailer** ("marketed"/direct-bypass headline) | $6.6K OTR − $2.6K nIXD-direct-bypass TOFC | **Confirmed never executed** — no nIXD-direct-bypass origin (MIT2/POC2/POC3/QXY8/XPH6/XSB2) appears as a *giver* anywhere in the 190-row ground-truth tracker; they only appear embedded in `Original Manifest ID` as the far-upstream node that already transited LAS1/VGT2 before redirect. Not applicable to the executed population — same conclusion ex3 reached, now confirmed at VRID level, not steering-tracker inference. |
| **$4.3K/trailer** (teardown "via-LAS1-leg" tier) | Will's 5/15 Slack model: $0.7K (POC→LAS1) + $1.1K + $2.3K + $0.2K | Includes a sunk upstream leg (POC→LAS1) that isn't part of the redirect's incremental cost. The **redirect-only** portion of this model ($1.1K+$2.3K+$0.2K≈$3.6K) is close to, and now superseded by, the MEASURED $3,946 mean. |
| **$2.6K/trailer** (teardown "nIXD-direct-bypass" tier) | Never executed (see $4.0K row) | Same — n/a for the realized population |
| **$6.6K/trailer** (teardown OTR tier) | Modeled for POC(nIXD)→RFD2, per source Slack message — **never separately validated for LAS1/VGT2→RFD2/MDW2**, the pair that actually ran | EST, unresolved; live geo-EST for the *actual* executed pair comes in $6.5K–$8.3K, higher not lower |
| **$3,946/trailer** (this audit, MEASURED) | Settlement-actual sum of the 3-leg run structure (dray+rail+dray), 189 genuine trailers | **New MEASURED basis — use this for the TOFC-cost side of any future calc.** |

---

## 5. Recomputed headline — waterfall

| Step | Trailers | $/trailer basis | Total | Δ vs prior |
|---|---|---|---|---|
| Ex3 original | 146 | $2.3K (both sides EST, desk) | $335,800 | — |
| + execution-integrity correction (ground-truth SharePoint/VRID tracker vs steering-tracker undercount) | 189 | $2.3K (unchanged) | $434,700 | +$98,900 |
| + TOFC-cost correction (desk $4.3K assumption → MEASURED mean $3,946, netted against the unchanged $6.6K OTR desk assumption) | 189 | $6,600 − $3,946 = $2,654 | **$501,524** | +$66,824 |
| + OTR-counterfactual correction (desk $6.6K flat → live geo-relaxed, lane-specific EST) | 189 | weighted avg $3,621 | $684,330 | +$182,806 (EST-only, not recommended as headline) |

**Recommended headline: ~$502K** ($501,524) — the row that fixes only what this audit could
actually *measure* (execution integrity + real settlement cost) while leaving the OTR assumption at
its original, institutionally-used value rather than substituting a still-EST, unvalidated-for-this-
lane number that happens to be more favorable. State the $684K row as an **upper alternate**, clearly
labeled EST, if a more favorable comp is wanted — but see §3.4: **both rows share the same
unresolved OTR-vs-dwell risk**, so neither is a "clean" AZIM-style fully-measured figure the way the
transport-only floor was for AZIM.

**If Will wants the single most conservative, "populate-only" fix** (change nothing about the
$/trailer basis, only correct the trailer count to ground truth): **$434,700** (189 × $2,300).

---

## 6. When TOFC beats OTR vs. when it doesn't

**TOFC wins when, simultaneously:**
1. The rail leg clears its negotiated flat rate (realized $2,313/leg, ~$1.18/mi — beat the $2.50/mi
   container-parity target after Procurement's rate-parity push, WK18 onward).
2. Dray capacity is available **without** starving container RTD dray at the origin ramp — Hunter
   Knowlton flagged this exact risk in-channel 4/23: *"this splits our dray capacity for containers
   and trailers so could see a rise in RTDs dwelling as a result (like last time)"* — mitigated only
   by a **dedicated carrier**, which the tracker.md risk log notes is an accepted incremental cost.
3. The **taker** has open dock/receiving capacity — this is the actual, documented trigger that ended
   the live run: Will, 2026-05-26, in-channel: *"Not yet, I don't see the taker capacity in our
   typical destinations."* (The tracker.md's 6/7 "standby, conflicts with linehaul-reduction posture"
   note formalizes this a couple weeks later as the durable policy reason; taker-capacity exhaustion
   was the immediate, practical trigger.)
4. The giver has enough **eligible** trailers (AZNG floor only — not AZNU, not pallet, not 3P) to hit
   the daily ask — repeatedly the actual constraint in the back half of the run (5/15, 5/19, 5/21
   messages all report falling short of the 15/day ask for lack of eligible trailers).
5. The destination rail ramp sits a short, cheap final dray from the taker — RFD2/MDW2 sit 22–53mi
   from Willowsprings/Corwith ($126–$333/leg observed); this lever would not pencil for a taker far
   from a BNSF Chicago-area ramp.

**TOFC loses (or the lever gets parked) when:** taker capacity dries up, dray capacity can't be
split without dwell risk, giver can't produce enough eligible floor trailers, or — the actual,
official reason it's parked as of 2026-06-07 — **even the cheapest available redirect still adds
incremental redirect spend against a network posture actively trying to reduce linehaul spend.**
TOFC was never "free" or "profit-generating" in this program's own framing; it was the *least-bad*
paid relief lever, held in reserve for when LAS1/VGT2 dwell forces the trade-off again.

**Minor aside (out of scope for the Q2 headline, flagged for completeness):** the Feb 2026 prior run
tracker files (`LAS1 TOFC Redirects WK8.xlsx` / `WK9.xlsx`) show 11 + 70 = **81 rows**, vs.
`las1_tofc_q2/CLAUDE.md`'s documented "~71 trailers across 4 days." A ~14% discrepancy — not
re-derived further since ex3 already scoped the Feb run out of the Q2 entitlement math.

---

## Provenance

- **Ground-truth execution tracker:** `LAS1 TOFC Redirects WK17-20.xlsx`, tabs WK 17/WK18/WK 19/
  WK 20/WK 21. Local copy `C:\Users\zhouzw\OneDrive - amazon.com\LAS1 TOFC Redirects WK17-20.xlsx`
  (mtime 2026-05-22); verified against a fresh live SharePoint fetch today via
  `sharepoint_resolve_url` + `sharepoint_read_file` (identical 52,256-byte size). 190 unique trailer
  rows, no duplicates.
- **VLS leg-level pricing:** `andes_local.v_load_summary`, live via `midstream_im_reroutable.connect()`
  (ada `SAschedulingredshift`), today. 555/555 tracker-named VRIDs found; 589 rows recovered across
  198 `run_structure_id`s; 190/190 tracker rows resolved to a run structure (189 clean, 1 fully
  canceled).
- **OTR counterfactual EST:** `lane_cost.refresh_lane_cost()`, live VLS pull today, written to a
  **temp cache only** (`%TEMP%\_tofc_audit_lane_cache.json`) — the repo's real
  `redirect_budget/cache/lane_cost_60d.json` was never opened for write.
  Also confirmed **zero** exact-lane OTR TRUCKLOAD rows exist on any of the 4 lanes,
  2026-04-01–2026-07-27, direct `v_load_summary` query.
  Also confirmed **exact-lane exhaustive search** returned 0 rows.
- **Slack ground truth:** channel `C0AVAR06T4H` (`vegas-tofc-redirects-q2-2026`, created 2026-04-23,
  renamed from `las1-tofc-redirects-q2-2026` 2026-05-14), full history pulled today (143 messages,
  4/23–5/26/2026, `has_more: false` — nothing after 5/26). Key posters identified via
  `batch_get_user_info`: William Zhou (`U07S244PV63`), Lee Swaim/AZIM (`U03N0QC9XJ9` — note:
  project docs spell this "Lex Swaim," Slack profile reads "Lee Swaim"), Jamie Dougan/ICT
  (`U03BAHT6ZEH`), Hunter Knowlton/Intermodal Ops (`U020M6KUARK`), Varun Anantharaman/Procurement
  (`U03GGTSBVUL`).
- **Feb 2026 cross-check:** `LAS1 TOFC Redirects WK8.xlsx` / `WK9.xlsx` (same OneDrive folder).
- **Prior-audit methodology reference:** `_notes/azim_entitlement_methodology_review_2026-07-21.md`,
  `promo_doc/evidence/ex6_vs_otr_reconstruction_2026-07-19.md` (mirrored discipline: MEASURED/EST/
  UNRESOLVED labeling, worked per-load examples, explicit counterfactual-proxy caveats).
- **Original basis under audit:** `promo_doc/evidence/ex3_yoy_and_tofc_entitlement_2026-07-24.md`
  (Q2 section), `las1_tofc_q2/CLAUDE.md`, `las1_tofc_q2/tracker.md`.
- Nothing in this file was posted anywhere or written back to any tracker/SIM/Slack/Quip doc. No
  repo file other than this one was created or modified during this investigation. All working
  scratch files (tracker row dumps, VLS pulls, temp lane-cost cache) were written outside the repo
  under `C:\Users\zhouzw\` / `%TEMP%`, not committed, and not required to reproduce this file's
  claims (every number here is cited back to its live source and can be re-pulled).
