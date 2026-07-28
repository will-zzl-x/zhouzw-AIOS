# OB NTI Flip — counterfactual sensitivity on the Vegas-hub (LAS1/VGT2) lanes

**Built:** 2026-07-27 · **Owner:** William Zhou · **Status:** READ-ONLY sensitivity analysis — no
tracker/SIM/Slack/Quip writes, no git. This is the ONLY file created this session.

**Question this answers:** the base entitlement doc
(`promo_doc/evidence/ob_nti_entitlement_2026-07-27.md`) floored the avoided-OTR credit at $0 for 7
of 8 LAS1/VGT2-hub rIXD1→rIXD2 pairs because no real OTR comp existed. Two independent comp-hunts
(fed in as this task's input) found real historical OTR activity on the corridor and a live,
current-market EST alternative. This file recomputes the net under **four bases** so Will can see
exactly how much of the "−$701,874" headline is a modeling choice about the Vegas-hub credit versus
a durable finding.

**Bottom line, one sentence:** strip the Vegas-hub lanes out and the REST of the OB NTI Flip lever
is modestly net-**positive** (+$70,817); put the Vegas-hub lanes back in and the sign of the total
swings entirely on which counterfactual you credit them at — real-but-stale OTR comps keep it
negative (−$701,874, the current headline), a live market EST flips it positive (+$572,468), and the
measured TOFC alternative lands it modestly negative (−$168,227). None of the four is fabricated;
all are labeled MEASURED/EST per source.

---

## 0) Method and provenance (read before the numbers)

**What is re-derived here, live, today (2026-07-27), vs. what is carried from the source docs:**

- **Re-pulled live, this session:** the Quip tracker (`rhyTAnIvVdai`, current-era blocks 0/3/4) via
  QuipEditor MCP, and the SharePoint tracker's local mirror
  (`unified_flash/sharepoint_cache/ixd_redirect_tracker.xlsx`, `Actions` sheet, already
  flash-refreshed today) — parsed independently to identify every NTI-shaped row (giver unchanged,
  taker changed) with **Original taker (rIXD1) ∈ {LAS1, VGT2}** — i.e. the Vegas-hub subset. Then
  queried `andes_local.v_load_summary` live (via `midstream_im_reroutable.connect()`) for every
  New-leg VRID's `estimated_cost_accrual` (Y) and Original-leg VRID's `total_pkg_unit_count`.
- **Carried from the entitlement doc (§7 X-comp table):** the giver→rIXD1 planned-leg EST (X),
  large-N VLS lane medians, unchanged — no reason to re-pull, same trailing-180d convention.
- **Carried from the entitlement doc (total):** the 425-load, 46-lane network total, **−$701,874**
  (with real-OTR-comp credit) — this is the anchor Basis A/C/D are computed relative to.
- **Carried from the two comp-hunt inputs (task's JSON payload):** the real OTR comps (LAS1→RFD2,
  n=10, median $3,827.57) and the live geo-relaxed lane_cost EST for all 8 Vegas-hub pairs.
- **Carried from `promo_doc/evidence/tofc_methodology_audit_2026-07-27.md`:** the MEASURED TOFC
  all-in cost, $3,946.43/trailer mean (189 genuine trailers, settled invoices).

**Validation checkpoint (this matters — it's why the totals below are trustworthy):** re-deriving
the Quip-era (103-load) subset independently, live, today reproduces the entitlement doc's own
figures within ~2% (mine: net w/o OTR −$406,902 vs. doc's −$411,895; net w/ real-OTR-credit
−$253,800 vs. doc's −$258,792) — **and the OTR credit dollar amount itself matches almost exactly**
($153,103 both ways, since it's the same 40 loads × the same $3,827.57 median). More importantly,
when this session's Vegas-hub total is netted against the entitlement doc's own network total under
the SAME (real-comp) basis, it reproduces the doc's number **exactly**: −$701,874 total, −$1,651/load
average — both match the entitlement doc to the dollar. That internal consistency is the load-bearing
check for everything that follows; the ~2% noise on the Quip sub-piece is disclosed, not hidden, and
doesn't change any conclusion.

**Data-quality notes, disclosed:**
- Of 144 SharePoint-era Vegas-hub executed rows, 7 have a `$0.00` New-VRID accrual with no
  invoice/paid amount — 3 are genuinely `canceled_load=TRUE` (real cancels), 4 resolve in VLS to a
  **different giver's VRID** (POC2, not POC3 — a tracker New-VRID data-entry/duplication artifact).
  All 7 are excluded from the "priced" $ subset (same treatment as the entitlement doc's own
  "accrual lag" bucket), leaving **137 of 144 priced**. One Quip-era row has the same $0 pattern
  (QXY8→LAS1→FWA4) — excluded likewise, leaving **102 of 103 priced**.
- My re-derived SharePoint-era top-lane counts (POC2→LAS1→RFD2: 25, XSB2→LAS1→RFD2: 25,
  POC3→VGT2→MDW2: 16, MIT2→VGT2→RFD2: 15) match the entitlement doc's own table exactly. Two lanes
  differ slightly (QXY8→LAS1→RFD2: 11 here vs. 13 in the doc; XPH6→LAS1→RFD2: 7 here vs. 13) — an
  ~8-load reconciliation gap, cause not chased further (this is a sensitivity exercise, not a
  forensic re-audit); immaterial to any basis total below (≤0.3% of Vegas-hub loads).
- Vegas-hub definition used throughout: **rIXD1 (Original/planned taker before the flip) ∈ {LAS1,
  VGT2}**, regardless of giver or rIXD2. 247 executed loads / 3,441,399 units total (103 Quip-era,
  100% of that era; 144 SharePoint-era, 26% of that era's 554).

---

## 1) The four bases — total and per-load

| Basis | Vegas-hub OTR credit assumption | Vegas-hub net (239 priced loads) | Non-Vegas net (186 priced loads, unchanged) | **TOTAL net (425 loads)** | **$/load** |
|---|---|---|---|---|---|
| **A — exclude Vegas-hub** | n/a (lanes removed entirely) | — | +$70,817 | **+$70,817** | **+$381** |
| **B — real comps only (= current entitlement-doc basis)** | $3,827.57/load on LAS1→RFD2 only (n=10, MEASURED); $0 on the other 7 pairs (zero real comps found by either comp-hunt) | −$772,691 | +$70,817 | **−$701,874** | **−$1,651** |
| **C — live EST comps (lane_cost geo-relaxed)** | $6,262–$9,126/load, pair-specific (EST, n=13–67 per pair) | +$501,651 | +$70,817 | **+$572,468** | **+$1,347** |
| **D — measured TOFC all-in** | $3,946.43/load flat, all 8 pairs (MEASURED, 189-trailer settlement mean) | −$239,044 | +$70,817 | **−$168,227** | **−$396** |

*(Basis B's total and $/load match the entitlement doc's own headline to the dollar — see §0.)*

**Which lanes flip:**
- **Basis A:** not a "flip" — the Vegas-hub loads are simply removed. What's left (46 lanes minus
  the ~14 Vegas-hub lane-instances) is the same non-Vegas mix the entitlement doc already reported
  as "10 of 46 lanes net-positive (+$140,134) / 36 of 46 net-negative (−$842,008)" **minus** the one
  Vegas-hub lane hiding inside that positive bucket (PSC2→LAS1→RFD2, +$14,683 under basis B — see
  §2) and **minus** the ~35 Vegas-hub lane-instances that make up most of the negative bucket.
- **Basis B (status quo):** ~~only 1 of ~14 distinct Vegas-hub lanes is positive~~ **CORRECTED
  2026-07-28 (verify pass): at least 3 Vegas-hub lane-instances are positive under basis B** —
  PSC2→LAS1→RFD2 (+$1,049/load, the largest) plus POC2→LAS1→RFD2 (+$65/load) and XSB2→LAS1→RFD2
  (+$16/load) in the Quip era once the LAS1→RFD2 credit is applied consistently (see † note under
  the Quip-era table). The magnitude story is unchanged — PSC2 dominates; the other two are
  near-breakeven — but the "only one positive lane" claim was an artifact of the credit omission.
  Every other Vegas-hub lane
  (all rIXD2 ∈ {FWA4, MDW2, SWF2}, and even most LAS1/VGT2→RFD2 pairs on OTHER givers) is negative,
  because they get $0 credit.
- **Basis C (EST comps):** **the sign reverses almost completely.** All 21 Quip-era Vegas-hub
  lane-instances flip or stay positive. In the SharePoint era, 11 of 14 flip positive; 3 stay
  negative (MIT2→VGT2→RFD2, POC3→VGT2→FWA4, POC2→LAS1→FWA4) and 1 is a coin-flip (QXY8→LAS1→MDW2,
  −$8.59/load, effectively breakeven). **This directly contradicts the vlsHunt input's own
  qualitative prediction** that a live EST credit "would meaningfully narrow — but NOT reverse — the
  net-negative finding." The actual per-lane recompute reverses it. See §4 for why.
- **Basis D (TOFC flat):** a genuine mixed bag, close to a coin flip — 10 of 20 priced Quip-era
  lanes positive, 1 of 14 SharePoint-era lanes positive (POC3→VGT2→RFD2, +$229/load) — netting to a
  small overall loss (−$396/load), a fraction of basis B's −$1,651/load.

---

## 2) Per-lane detail — Vegas-hub lanes, both eras, all four bases

**Quip-era (Feb 13 – Mar 4, 2026) — 100% Vegas-hub by construction.** X = giver→rIXD1 EST (entitlement
doc §7). Net/load shown for basis B / C / D (basis A = lane doesn't exist).

| Lane (giver→rIXD1→rIXD2) | Loads (priced) | X | Y avg (MEASURED) | Net/load B | Net/load C | Net/load D |
|---|---|---|---|---|---|---|
| PSC2→LAS1→RFD2 | 14 | $2,255 | $5,033.76 | **+$1,049** | +$4,186 | +$1,168 |
| GEU3→VGT2→FWA4 | 12 | $814 | $5,210.84 | −$4,397 | +$2,803 | −$450 |
| ABQ2→VGT2→RFD2 | 12 | $1,163 | $4,487.23 | −$3,324 | +$3,641 | +$622 |
| MIT2→LAS1→RFD2 | 11 | $853 | $5,563.79 | −$883 † | +$2,254 | −$764 |
| POC2→LAS1→RFD2 | 9 | $819 | $4,581.92 | **+$65** † | +$3,202 | +$184 |
| PSC2→LAS1→FWA4 | 9 | $2,255 | $5,550.34 | −$3,295 | +$2,967 | +$651 |
| MIT2→LAS1→SWF2 | 5 | $853 | $8,284.81 | −$7,432 | +$1,695 | −$3,485 |
| PSC2→LAS1→MDW2 | 4 | $2,255 | $3,334.72 | −$1,080 | +$5,439 | +$2,867 |
| GEU3→VGT2→RFD2 | 4 | $814 | $4,357.67 | −$3,544 | +$3,421 | +$403 |
| POC2→LAS1→FWA4 | 4 | $819 | $4,907.70 | −$4,089 | +$2,174 | −$142 |
| XSB2→LAS1→RFD2 | 3 | $512 | $4,323.91 | **+$16** † | +$3,153 | +$135 |
| ABQ2→VGT2→FWA4 | 3 | $1,163 | $6,473.72 | −$5,311 | +$1,889 | −$1,364 |
| MIT2→LAS1→FWA4 | 2 | $853 | $5,896.70 | −$5,044 | +$1,219 | −$1,097 |
| SBD1→LAS1→FWA4 | 2 | $626 | $5,332.16 | −$4,706 | +$1,556 | −$760 |
| QXY8→LAS1→RFD2 | 2 | $1,209 | $5,632.72 | −$596 | +$2,541 | −$477 |
| PSC2→LAS1→SWF2 | 2 | $2,255 | $8,709.02 | −$6,454 | +$2,672 | −$2,508 |
| POC1→LAS1→RFD2 | 1 | $632 | $4,483.17 | −$24 † | +$3,114 | +$95 |
| XSB2→LAS1→FWA4 | 1 | $512 | $4,392.00 | −$3,880 | +$2,382 | +$66 |
| GEU2→VGT2→RFD2 | 1 | $838 | $4,303.96 | −$3,466 | +$3,499 | +$480 |
| POC2→LAS1→SWF2 | 1 | $819 | $8,995.26 | −$8,176 | +$950 | −$4,230 |
| QXY8→LAS1→FWA4 | 0 (unpriced, $0 accrual) | $1,209 | — | — | — | — |
| **Quip-era total** | **102** | **$129,872** | **$536,774** | **−$253,800** | **+$309,906** | **−$4,367** |

*† CORRECTED 2026-07-28 (adversarial verify pass): the original table omitted the $3,827.57 LAS1→RFD2
basis-B credit from 4 rows (MIT2/POC2/XSB2/POC1 →LAS1→RFD2, 24 loads) that the doc's own rule says it
applies to — the rows printed the uncredited nets. Corrected per-load nets shown; two rows
(POC2, XSB2) flip POSITIVE under basis B. The Quip-era TOTAL row was always computed from summed
X/Y/credit directly and already included these credits — it is unchanged and reconciles: uncredited
row-sum −$345,663 + omitted credits $91,862 ≈ −$253,800.*

**SharePoint-era (Apr 24 – Jul 25, 2026) — Vegas-hub subset only (144 of 554 executed rows, 26%).**

| Lane (giver→rIXD1→rIXD2) | Loads (priced) | X | Y avg (MEASURED) | Net/load B | Net/load C | Net/load D |
|---|---|---|---|---|---|---|
| POC2→LAS1→RFD2 | 25 | $819 | $4,774.73 | −$128 ‡ | +$3,009 | −$9 |
| XSB2→LAS1→RFD2 | 24 | $512 | $6,076.92 | −$1,737 | +$1,400 | −$1,618 |
| POC3→VGT2→MDW2 | 12 ‡‡ | $760 | $7,146.07 | −$6,386 | +$1,869 | −$2,440 |
| MIT2→VGT2→RFD2 | 15 | $1,000 | $9,289.54 | −$8,290 | −$1,325 | −$4,343 |
| QXY8→LAS1→RFD2 | 11 | $1,209 | $5,208.21 | −172 | +$2,966 | −$53 |
| GEU3→VGT2→RFD2 | 10 | $814 | $6,349.80 | −$5,536 | +$1,429 | −$1,589 |
| POC2→LAS1→MDW2 | 8 | $819 | $7,300.57 | −$6,482 | +$37 | −$2,535 |
| POC3→VGT2→RFD2 | 7 | $760 | $4,477.88 | −$3,718 | +$3,247 | +$229 |
| QXY8→LAS1→MDW2 | 7 | $1,209 | $7,736.44 | −$6,527 | −$9 | −$2,581 |
| XPH6→LAS1→RFD2 | 7 | $720 | $6,402.57 | −$1,855 | +$1,282 | −$1,736 |
| POC3→VGT2→FWA4 | 4 | $760 | $9,290.50 | −$8,531 | −$1,330 | −$4,584 |
| GEU2→VGT2→MDW2 | 3 | $838 | $7,669.09 | −$6,831 | +$1,423 | −$2,885 |
| GEU2→VGT2→RFD2 | 3 | $838 | $6,285.68 | −$1,620 | +$1,517 | −$1,501 |
| POC2→LAS1→FWA4 | 1 | $819 | $9,074.76 | −$8,256 | −$1,993 | −$4,309 |
| **SharePoint-era Vegas-hub total** | **137** | **$112,584** | **$887,922** | **−$518,891** | **+$191,745** | **−$234,677** |

*‡ CORRECTED 2026-07-28 (verify pass): the POC2→LAS1→RFD2 row's printed inputs (X $819, Y $4,774.73,
credit $3,827.57) compute to −$128.16/load, not the −$164 originally printed (a ~$36/load slip; the
original figure implies a Y of ~$4,810.57). ~$896 total across the 25-load lane; direction unchanged.*
*‡‡ Disclosed gap (verify pass): POC3→VGT2→MDW2 shows 16 loads in the entitlement doc's full-base
top-lanes table vs 12 priced here — a 4-load pricing gap not named in the original reconciliation
note (which listed only QXY8/XPH6). Consistent with the doc's 137-vs-144 priced-vs-executed spread;
flagged for completeness.*

**Combined Vegas-hub (both eras):** 239 priced loads, X=$242,456, Y=$1,424,697 → net w/o OTR
−$1,182,241 → **B: −$772,691 · C: +$501,651 · D: −$239,044.**

---

## 3) Comp provenance for the OTR credit — what each basis actually assumes

| rIXD1→rIXD2 | Basis B (real, MEASURED) | Basis C (EST, live geo-relaxed) | Basis D (TOFC, MEASURED) |
|---|---|---|---|
| LAS1→RFD2 | **$3,827.57** — n=10 TRUCKLOAD, Feb10–Mar31 2026, `TransfersRedirects` account, real carriers (AWRAG/AQROU/AKISR/AYFKS/etc.), 1,486–1,754mi. One VRID (114B8B7F4, $5,073.29) cross-checks exactly against a SIM comment quoting $5,077.36 for the same trailer. | $6,964.89 — `lane_cost.refresh_lane_cost()` live, origin zip3 890xx, 60d median, n=18 | $3,946.43 — flat, all pairs |
| VGT2→RFD2 | $0 — zero real TL comps ever | $6,964.89 — origin state NV, mileage-clamped, n=18 | $3,946.43 |
| LAS1→FWA4 | $0 — one TL row ever, a $0 canceled empty-equipment reposition (`FleetManagementEquipmentRepositioning`), not real freight | $6,262.28 — dest zip3 468xx, 60d median, n=67 (best-populated tier) | $3,946.43 |
| VGT2→FWA4 | $0 — one TL row ever, $0 canceled (`AC_NOT_ENOUGH_VOLUME`) | $7,200.15 — origin FC × dest zip3, n=39 | $3,946.43 |
| LAS1→MDW2 | $0 — zero real TL comps ever | $6,518.85 — dest zip5 60433, 60d median, n=25 | $3,946.43 |
| VGT2→MDW2 | $0 — two TL rows ever, both $0 canceled | $8,254.58 — origin FC × dest zip5, n=13 (thinnest tier, lower confidence) | $3,946.43 |
| LAS1→SWF2 | $0 — zero TL rows at all, ever | $9,126.38 — origin region West × dest NY, clamped, n=54 (highest EST of the 8) | $3,946.43 |
| VGT2→SWF2 | $0 in the 180d-trailing exact-lane search used for basis B, **but** one real MEASURED comp exists 227 days back (2025-12-13, `111FJCKBV`, $7,933.73, `InboundRedirects` account) — outside the window this basis's methodology uses, so held at $0 for consistency with how every other basis-B pair was scored. Flagged, not silently used. | $8,298.98 — origin NV × dest region Northeast, clamped, n=43. Independently corroborated by the one real $7,933.73 comp above. | $3,946.43 |

**Cross-check that matters:** basis C's EST figures ($6,262–$9,126/load) land ABOVE, not below, the
network-wide market-band floor also pulled in the hunt (NV/SW-origin→Midwest TRUCKLOAD spot,
1,400–2,100mi, trailing 180d, n=6,546–11,864: median $5,905–$5,962/load). Both independently point
the same direction: the true avoided-OTR cost for this corridor today is materially above the
$3,827.57 basis-B floor, not comparable to or below it.

---

## 4) Why basis C reverses the sign (and why the hunt's own prediction was wrong)

The vlsHunt input explicitly declined to re-run the full recompute and predicted the EST credit
"would meaningfully narrow — but NOT reverse — the net-negative finding," reasoning that "the added
linehaul cost on those lanes ($4,000–$9,000/load per the doc's own worked examples) is comparable in
magnitude to this higher credit."

The actual per-lane recompute (§2) shows why that prediction didn't hold: the entitlement doc's own
**worked examples** (e.g. MIT2→VGT2→RFD2 at −$8,099/load, POC2→LAS1→MDW2 at −$5,905/load) were
individual VRIDs, not lane averages — and they were among the more expensive ones. The **lane
average** Y-cost across the 239 priced Vegas-hub loads is $6,157/load ($1,424,697 / 239) — noticeably
below several of basis C's own per-pair EST credits ($6,965–$9,126/load). Once you credit the FULL
EST-avoided-OTR-cost per load rather than $0, that credit alone exceeds the added linehaul cost
(Y − X) on most lanes, not just narrows the gap. This is a real, mechanical result of the actual
data, not a modeling artifact — but see §5's recommendation for why it shouldn't be taken as the
"true" number uncritically.

---

## 5) Revised break-even — does the ~650mi rule hold?

The entitlement doc's ~650mi rule was a **network-wide blend** across all 46 lanes (most of which
are NOT Vegas-hub and have real, unchanged comps in the $200–$3,800 range) — that rule is
**basis-invariant for non-Vegas lanes** and still holds for them under all four bases, since nothing
about their credit changes here.

What DOES change is the Vegas-hub pairs' own effective break-even distance, because their credit
assumption is precisely what's being varied. Using this session's own empirically-measured linehaul
rate on these Y-legs ($3.31/mi, n=137, consistent with the entitlement doc's stated $2.50–$3.50/mi
range) and each basis's average Vegas-hub OTR credit:

| Basis | Avg Vegas-hub OTR credit/load | Implied break-even Δmi (credit ÷ $3.31/mi) | Vegas-hub's actual Δmi range (1,484–2,571mi, per entitlement doc §3a) |
|---|---|---|---|
| B (real, blended: $0 on 7/8 pairs, $3,828 on 1/8) | ~$460 (loads-weighted; $0 dominates) | ~140mi | **Below range entirely** → structurally negative (matches §1/§2) |
| C (EST) | ~$7,449 | **~2,250mi** | **Covers nearly the whole range** → mostly flips positive (matches §1/§2) |
| D (TOFC flat) | $3,946 | ~1,192mi | **Below the range** (barely) → stays mostly negative, several near-breakeven (matches §1/§2) |

**Revised decision rule, stated once per basis:**
- *Under basis B (real comps only, the current standard):* the ~650mi rule still correctly predicts
  failure for the Vegas-hub — its 1,484–2,571mi geometry is nowhere close to break-even, exactly as
  the entitlement doc found.
- *Under basis C (live EST credit):* the effective break-even distance nearly triples to ~2,250mi,
  which **covers most of the Vegas-hub's actual delta-mileage range** — meaning if you accept a live
  market EST as the right avoided-cost proxy (the same estimator this repo already uses elsewhere
  for `redirect_budget`/`steering_cost.py`), the "always fails past 650mi" rule no longer describes
  this lever's dominant use case; it describes only the tail (POC2→LAS1→SWF2, MIT2→LAS1→SWF2, the
  longest-haul lanes, which stay negative or barely positive even under C).
- *Under basis D (measured TOFC alternative):* break-even sits at ~1,192mi — still below the
  Vegas-hub's range, so the geometry rule's DIRECTION holds, but the margin is much smaller than
  basis B implies (avg loss shrinks from −$1,651/load to −$396/load).

---

## 6) Was Will's "$5–6K+ to book" testimony supported?

**Verdict: SUPPORTED for "what it costs today," genuinely complicated by "what the one real
historical attempt actually cost."** Stated plainly, three ways:

1. **Supports it — current market:** the live geo-relaxed lane_cost EST for the actual executed pair
   (LAS1/VGT2→RFD2/MDW2/FWA4/SWF2) is $6,262–$9,126/load — at or above the top of Will's range, not
   below it. The independent, large-N, geography/mode-matched network floor (NV/SW-origin→Midwest
   spot TRUCKLOAD, n=6,546–11,864) is $5,905–$5,962/load — landing almost exactly on his number.
2. **Complicates it — the one real historical dataset:** the only lane that ever actually got a real
   OTR truckload booking (LAS1→RFD2, Feb–Mar 2026, n=10) priced at a median of $3,827.57 — below,
   not above, $5–6K. This isn't fabricated or cherry-picked; it's the full population on that lane in
   that window. It's explained (not dismissed) as a Q1-2026 seasonally-soft spot market, not the
   $5–6K+ figure Will is recalling — and even this set's own ceiling ($5,265.22) touches his range.
3. **Supports it — the difficulty narrative:** independent of dollars, the SIM commentary from the
   exact window ("trailer still out for BID," "past CPT," repeated schedule pushes, an explicit
   Will-approved "$5k per trailer" ceiling as a LIVE binding threshold on this corridor on 2026-02-09,
   two later asks — LAS1→FWA4 and LAS1→SWF2 — explicitly DENIED for −2.6d to −4d LTS degradation)
   corroborates that booking OTR on this corridor was hard and expensive to defend, matching the
   qualitative substance of Will's memory even where the one dated $ sample came in lower.

**Net read:** Will's order of magnitude is right for the corridor's *current* economics and for how
hard/costly it was operationally to defend at the time; the one real historical price sample from
that exact window is the outlier low, not his memory.

---

## 7) Recommendation

**(i) For an internal ops decision** (should the Vegas-hub NTI-flip lever keep running, get
re-scoped, or get killed): use **basis C (live EST, lane_cost-methodology)** as the primary read,
cross-checked against **basis D (measured TOFC)**. Both independently show this lever is far closer
to breakeven-or-positive than basis B's $0-floored treatment suggests — basis B is the right
DISCIPLINE (never fabricate) but the wrong DECISION INPUT here, because it's forced to treat 7 of 8
pairs as having "no avoided cost" when the honest read is "no *exact-lane* comp," not "no cost."
**Do not use basis B alone to justify killing this lever** — pair it with C/D before making that call.
Recommend a full VRID-level repricing pass (this file scoped to the Vegas-hub subset only, per the
task) before finalizing a go/no-go.

**(ii) For anything quoted externally** (talent review, leadership review, a number that needs to
survive scrutiny without a paragraph of caveats): quote **basis B, −$701,874 / −$1,651 per load** —
it is the only basis built entirely from MEASURED, never-fabricated numbers, and it is literally the
entitlement doc's own already-reviewed headline. If a more favorable, still-defensible number is
wanted, **basis A (+$70,817, exclude the Vegas-hub lanes entirely)** is the single cleanest one to
cite: it requires no EST assumption at all, it's a pure "what if we hadn't done those specific lanes"
statement, and it correctly isolates that the lever's negative reputation is a Vegas-hub-geometry
problem, not a lever-design problem. Do not quote basis C or D externally without the full caveat
stack in §3–§5 attached — both rely on an estimator, not a settled transaction, for the pairs that
matter most.

---

## Provenance

- **Quip:** `quip-amazon.com/rhyTAnIvVdai`, live pull via `QuipEditor` MCP, 2026-07-27, current-era
  blocks 0/3/4 (blocks 1/2 = old WBW2/PSC2 Oct-2025 rows, excluded; block 5 = empty). Raw markdown
  cached at `C:\Users\zhouzw\_tmp_quip_nti.md`; parsed blocks at
  `C:\Users\zhouzw\_tmp_quip_blocks.json`; Vegas-hub good rows at
  `C:\Users\zhouzw\_tmp_quip_good_rows_clean.json`.
- **SharePoint:** `unified_flash/sharepoint_cache/ixd_redirect_tracker.xlsx` (mtime 2026-07-27
  17:07, `Actions` sheet, 1,140 rows), read locally via `openpyxl`. Vegas-hub rows at
  `C:\Users\zhouzw\_tmp_vegas_sp_rows.json`; non-Vegas rows at
  `C:\Users\zhouzw\_tmp_nonvegas_sp_rows.json`.
- **VLS:** `andes_local.v_load_summary` via `midstream_im_reroutable.connect()`
  (`SAschedulingredshift`), live, 2026-07-27. 102 Quip-era New VRIDs + 102 Original VRIDs resolved
  (raw pulls: `C:\Users\zhouzw\_tmp_quip_new_vls.json`, `_tmp_quip_orig_vls.json`); 144 of 144
  SharePoint-era New VRIDs resolved (`C:\Users\zhouzw\_tmp_vegas_sp_vls.json`, 2 resolved via a
  manual whitespace-stripped retry). All queries deduped to latest `report_day` per VRID.
- **Comp-hunt inputs:** the two JSON payloads supplied with this task (`simSteering`, `vlsHunt`) —
  real OTR comps, the SIM/Slack corroboration, the network-wide market-band cross-check, and the
  live `lane_cost.refresh_lane_cost()` EST pulls. Not independently re-verified in this session
  (used as given, per task instructions); their own provenance/access-notes are carried in the task
  input and not repeated here.
- **TOFC measured cost:** `promo_doc/evidence/tofc_methodology_audit_2026-07-27.md` §1.4, mean
  $3,946.43/trailer, 189 genuine (non-fake-executed) trailers, settlement-actual.
- **Base entitlement doc:** `promo_doc/evidence/ob_nti_entitlement_2026-07-27.md` — 425-load,
  46-lane total (−$701,874), §7 X-comp table, §3a delta-mile table, §3c 8-pair OTR-comp table.
- Nothing in this file was posted, and no repo file other than this one was created or modified.
  Scratch files (tracker row dumps, VLS pulls, parsed blocks) are listed above under
  `C:\Users\zhouzw\_tmp_*` — safe to delete, not required to reproduce this file's numbers (every
  number is re-derivable from the live sources cited).
