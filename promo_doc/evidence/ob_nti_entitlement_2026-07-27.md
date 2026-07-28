# OB NTI Flip entitlement — validating Will's formula against real VLS pricing

**Built:** 2026-07-27 · **Owner:** William Zhou · **Status:** DRAFT — local only, no comms, no
tracker/SIM writes. This is the ONLY file written this session.

**Headline finding (read this first):** Will's formula (`X − Y + avoided_OTR`) is structurally
correct, but **the dominant real-world application of this lever is net-NEGATIVE under measured
VLS pricing**, not net-positive. Of 425 fully-priced executed loads (Feb–Jul 2026), **275 loads /
3.92M units are net-negative (−$842,008)** and only **150 loads / 2.71M units are net-positive
(+$140,134)** — netting to **−$701,874** across the priced sample. The failure mode is
geometric and systematic, not a handful of outliers: it concentrates in the LAS1/VGT2-hub flips,
which are also this lever's highest-volume, most historically-established use case. See §3 for the
decision rule and §2 for the honest number, stated multiple ways.

---

## 0) Access status (state this plainly, per instruction)

- **Quip** (`quip-amazon.com/rhyTAnIvVdai`, "nIXD Outbound -> rIXD NTI Redirect Tracker"): LIVE via
  the QuipEditor MCP tool. **The file-based API token (`~/.ees-interactive-repl/quip.json`) is
  INVALID for direct `requests` calls** — a raw `GET /1/threads/{id}` with that token returned
  HTTP 400 `"OAuth token is invalid or expired"` even though the token's own embedded expiry
  decodes to 2027-07-23. The MCP tool's session auth is independent of that file and worked fine.
  **Large-doc caveat hit and worked around:** calling QuipEditor with `analyzeStructure=true`
  balloons the response to 3×~1MB chunks (per-cell `sectionId` HTML-comment bloat) and only chunk
  1 is retrievable through this tool — no chunk-2/3 parameter is exposed. Re-calling with
  `analyzeStructure` OMITTED returned the full document cleanly at ~62KB (the real content is
  small; the bloat was 100% structural metadata).
- **SharePoint** (`sites/IXDRedirects/Shared Documents/IXD Redirect Tracker.xlsx`): LIVE, read from
  the local `unified_flash/sharepoint_cache/ixd_redirect_tracker.xlsx` mirror, which the flash
  pipeline had already refreshed **today (2026-07-27 17:07)** — no new SharePoint MCP pull needed.
  This turned out to be **the more important source**: see §5.
- **Slack** `#nti-ob-flips-nixd2rixd-ib` (channel `C097KRGDJRF`): LIVE via ai-community-slack-mcp.
  1,195 total messages, 2025-08-05 → 2026-07-27 (today). Full history usable.
- **VLS** (`andes."ats-onestopshop".v_load_summary` via `SAschedulingredshift`): LIVE. Queried
  ~1,350 distinct VRIDs across both executed-base pulls plus ~35 lane-comp queries. This is the
  workhorse source for every dollar figure below.
- **Nothing was blocked.** The only real friction was the Quip chunking bug (worked around) and the
  stale file-token (irrelevant once routed through the MCP tool).

---

## 1) Executed base — three eras, one lever

**Convention:** "executed" = the tracker's own completion checkbox (Quip: `Manifest Flipped`=☑;
SharePoint: `Completed`=`Done`) AND a real New VRID present. Giver is required to be UNCHANGED
between Original Lane and New Lane (only the taker changes) — that's the NTI-flip signature per
`ob_nti_flip/CLAUDE.md` and confirmed structurally in both trackers (0 mismatches found across
739 rows where a giver was parseable).

### 1a. Break-glass era (Oct 2025) — EXCLUDED from the entitlement base, used only for §6

| Block | Lane | Rows | Executed (Manifest Flipped=☑) | Completion |
|---|---|---|---|---|
| WBW2→MDW2 | Oct 1, 2025 | 30 | 8 | 27% |
| PSC2→MDW2 | Oct 1, 2025 | 30 | 1 | 3% |

No `Units` column existed yet in this era's tracker schema — the process was too immature to even
track volume, let alone price it. **MEASURED** (raw tracker rows), excluded from all $ totals below
per task instruction (task explicitly named these as the "(old)" pre-transformation tabs, and they
are — see the Notes-field/date/owner evidence in §6).

### 1b. Current era, Quip tracker (Feb 13 – Mar 4, 2026)

The dedicated Quip doc's blocks 0/3/4 (block1/2 are the WBW2/PSC2 old blocks above; block5 is an
empty unused continuation sheet).

| | Rows | Executed | Completion |
|---|---|---|---|
| Total | 151 | **121** | 80% |

**121 executed loads / 1,553,036 units** (units MEASURED off the Original VRID's own
`total_pkg_unit_count` field in VLS — the tracker itself carries no Units column in this era for
17 of 121 rows; VLS supplied it for all 121). Givers: POC1, POC2, POC3, PSC2, XSB2, GEU2, GEU3,
MIT2, ABQ2, SBD1, QXY8. Original takers (rIXD1): **exclusively LAS1 or VGT2**. New takers (rIXD2):
RFD2, FWA4, MDW2, SWF2 — all MW_GL region.

**17 of 121 rows had blank Original-Lane/New-Lane cells** (tracker data-entry gap, owners
`[hunterjn]`/RHOADELL/`dabhaska@`/`patralid@`). Resolved via the VRID's own `origin`/
`final_destination` fields in VLS (not guessed) — 15 of 17 fit the LAS1/VGT2 pattern exactly, **2
resolve to BOI2** (an unexpected destination, flagged not force-fit). 10 of these 17 were
additionally priceable and are consistent with the same negative-net pattern (§2); held OUT of the
headline 425-load priced set to keep the primary audit trail simple, detailed in `_notes` appendix
data, not fabricated into the totals.

### 1c. Current era, SharePoint tracker (Apr 24 – Jul 25, 2026) — the ACTUAL current record of truth

**This is the load-bearing discovery of this session.** The Quip tracker's last real dated entry
is 2026-03-04. It was NOT abandoned in the sense of the lever dying — the team migrated
record-keeping onto the SAME general-purpose SharePoint `IXD Redirect Tracker.xlsx` already used
for the broader IXD redirect program (see §6 for the dated Slack evidence — Will personally drove
this). Filtering that tracker's `Actions` sheet (1,140 rows) to NTI-flip-shaped rows (giver
unchanged, taker changed):

| Month | Requested | Rows | | Month | Requested rows |
|---|---|---|---|---|---|
| Apr 2026 | 96 | | Jun 2026 | 191 |
| May 2026 | 148 | | Jul 2026 (through 7/25) | 108 |

**588 NTI-shaped rows, 554 marked `Completed=Done` (94%)** — **554 executed loads / 8,910,396
units** (Units column present natively in this tracker era — MEASURED, no VLS lookup needed for
volume). Givers expand well beyond the LAS1/VGT2 corridor: LBE1, POC2/3, XSB2, POC3, HLI2, XLA4,
QXY8, XPH6, PSC2, ABQ2, GEU3, FWA4, TCY2, MEM1, MIT2, plus a long tail. Top lanes by volume:

| Lane (giver→rIXD1→rIXD2) | Loads |
|---|---|
| LBE1→ORF2→RMN3 | 36 |
| LBE1→ORF2→AVP1 | 32 |
| POC2→LAS1→RFD2 | 25 |
| XSB2→LAS1→RFD2 | 25 |
| POC3→VGT2→MDW2 | 16 |
| MIT2→VGT2→RFD2 | 15 |
| HLI2→MDW2→BJC1 | 15 |
| XLA4→MDW2→IMO1 | 14 |
| QXY8→LAS1→RFD2 / XPH6→LAS1→RFD2 | 13 each |

### 1d. Combined current-era executed base

**675 executed loads / 10,463,432 units, Feb–Jul 2026 (~5.5 months).** **425 of 675 (63%) were
fully priced end-to-end** (both legs resolved to a real dollar figure) — the rest are held out for
one of: (a) the giver→rIXD1 lane wasn't in this session's comp-pull scope (220 SharePoint-era rows —
listed in §7, not zero-comp, just not pulled this pass — **this understates both the realized $ and
the run-rate below, direction unknown**), (b) the New-leg VRID hadn't billed yet at pull time
(accrual lag, 17+18 rows), (c) the 7 blank-lane Quip rows not folded into the headline set (§1b).

---

## 2) Realized cost avoidance — the honest number, three ways

Every row below prices as `net = X_planned − Y_executed + OTR_avoided`. X is EST (large-N VLS lane
median on the giver→rIXD1 corridor — see §7 for why this is NOT the AZIM-style thin n=3 comp
problem: every X comp here carries n≥235, most n>500). Y is MEASURED (VLS `estimated_cost_accrual`,
confirmed by `total_invoice_amount`/`total_paid_amount` matching on the large majority — see
per-row tags). OTR is MEASURED-where-a-real-comp-exists, **$0/EXCLUDED where it doesn't** (never
fabricated — same discipline as the AZIM MCI4→IND9 precedent).

| | Loads | Units | net WITHOUT OTR credit | net WITH OTR credit (real comps only) |
|---|---|---|---|---|
| Quip-era (Feb–Mar 2026) | 103 | 1,436,208 | **−$411,895** | **−$258,792** |
| SharePoint-era (Apr–Jul 2026) | 322 | ~5.6M* | **−$812,507** | **−$443,081** |
| **TOTAL priced** | **425** | **~7.0M*** | **−$1,224,402** | **−$701,874** |

*(SharePoint-era unit total for the priced subset only; full-base 8.91M units is §1c.)*

**Per-load average: −$1,651/load** (with-OTR-credit basis, both eras blended).

**By lane sign** (46 distinct giver→rIXD1→rIXD2 lanes with ≥1 priced load):

| | Lanes | Loads | Units | Net $ |
|---|---|---|---|---|
| Net-POSITIVE lanes | 10 of 46 | 150 | 2,709,616 | **+$140,134** |
| Net-NEGATIVE lanes | 36 of 46 | 275 | 3,923,077 | **−$842,008** |

**Stated the way I'd defend it:** *"On the 425 loads I could fully price (63% of the 675-load
current-era executed base), the OB NTI Flip lever cost the network a net $701,874 MORE than the
planned linehaul it replaced would have — even after crediting every avoided downstream OTR
redirect I could find real market history for. A minority of the lever's lane mix (10 of 46 lanes,
35% of priced volume) IS genuinely net-positive (+$140,134) — see §3 for exactly which ones and
why."* This is the opposite of the lever's assumed economics; it is not a rounding error or a thin
comp artifact (see §7 for why the comps here are unusually well-measured for this kind of
analysis).

---

## 3) Mental-model validity — WHEN Will's formula is wrong (the central deliverable)

**The formula's algebra is fine. What breaks is the implicit geometric assumption baked into
"then pay a full OTR redirect rIXD1→rIXD2" — that rIXD2 is a comparably-distant regional
alternative to rIXD1.** It usually isn't, for this lever's dominant use case.

### 3a. The break-even geometry, quantified

Pulled `miles` for the executed New-leg VRID (Y) and the giver→rIXD1 corridor's own VLS median
miles (X) for every lane with both available (43 lanes). Sorted by `delta_mi = miles(Y) −
miles(X)` — how much FARTHER the new destination is than the original plan:

| Lane | delta_mi | net/load |
|---|---|---|
| HLI2→MDW2→BJC1 | **−926** (closer!) | **+$2,527** avg |
| XLA4→MDW2→IMO1 | −347 | net −$2,028 avg *(no OTR comp on this lane — see 3c)* |
| MEM1→MIA1→DAB2 | −253 | +$592 avg |
| LBE1→ORF2→AVP1/RMN3 | −155/−146 | +$1,679 / +$805 avg |
| MIT2/XLA4→PSP3→LAX9 | −53/−48 | +$521 / +$156 avg |
| PSC2→SCK4→MCC1 | −35 | −$198 avg *(near break-even, negative side)* |
| FWA4→CMH4→{CMH1,DTW1,DET6,GRR1} | +6 to +24 | +$279 (CMH1) to −$299 (GRR1) — **the literal
  break-even cluster** |
| ABQ2→SCK4→MCC1 | +47 | +$69 avg |
| TCY2→LAX9→GYR2 | +305 | +$373 avg |
| PSC2→LAS1→RFD2 | +947 | +$1,049 avg |
| **everything from GEU3→VGT2→RFD2 (+1,484mi) through POC2→LAS1→SWF2 (+2,571mi)** | **+1,484 to
  +2,571** | **−$884 to −$8,176 avg — every single one negative** |

**The pattern is essentially monotonic.** At the observed AZNG dedicated-linehaul rate
(~$2.5–3.5/mi on these lanes — see the X-comp table in §7), the break-even added distance is
roughly **~650 miles**, given the typical avoided-OTR credit runs $200–$3,800/load depending on the
rIXD1→rIXD2 pair. **Every lane in this dataset with delta_mi beyond ~650mi is net-negative; nearly
every lane at or below that threshold is net-positive or a small, defensible loss.**

### 3b. The decision rule (quotable, per-mile terms)

> **"The flip creates value only when rIXD2 is a genuine REGIONAL neighbor of rIXD1 — within
> roughly 650 miles of added distance from the giver. When rIXD2 is a cross-country alternative to
> a regionally-close rIXD1 (the observed failure case: Southwest nIXD origins whose planned
> destination was the nearby Vegas hub, LAS1/VGT2, 200–1,000mi away, get re-pointed to Midwest
> siblings 1,700–2,600mi FARTHER), the added linehaul cost ($4,000–$9,000/load) structurally
> exceeds any plausible avoided-OTR credit, and the flip is a net cost, not a savings."**

### 3c. When the true counterfactual isn't an OTR redirect at all

Pulled real VLS history on every observed rIXD1→rIXD2 pair, TRUCKLOAD mode, `ATS_BROKERAGE`/
`ATS_DEDICATED`, cost>0, not canceled, trailing 180d:

| rIXD1→rIXD2 | Real OTR comps (n) | Mode mix (all rows) |
|---|---|---|
| LAS1→RFD2 | **10** | 91 INTERMODAL / 10 TL |
| LAS1→FWA4 | **0** | 30 INTERMODAL / 1 TL |
| LAS1→MDW2 | **0** | 121 INTERMODAL / 0 TL |
| LAS1→SWF2 | **0** | 0 rows at all |
| VGT2→RFD2 | **0** | 30 INTERMODAL / 0 TL |
| VGT2→FWA4/MDW2/SWF2 | **0** | ≤3 rows each, no TL |
| MDW2→IMO1 | **0** | 1 row, not TL |

**7 of 8 LAS1/VGT2-hub rIXD1→rIXD2 pairs have ZERO real-world OTR truckload precedent.** The
lanes that DO move volume between LAS1/VGT2 and the Chicago-area sites move it **INTERMODAL**
(account `TransfersRedirects`, mode `INTERMODAL`) — i.e., this is the same corridor the parallel
`las1_tofc_q2` TOFC redirect program runs on. **The true historical counterfactual for a stressed
LAS1/VGT2 was very likely a TOFC/rail move, not a spot OTR truckload** — this analysis floor-states
that term at $0/EXCLUDED (never fabricated a number for it) rather than guess a rail-inclusive
figure; a full dray+rail+dray leg reconstruction on this specific corridor is the scope of the
parallel TOFC audit already running in this repo (`promo_doc/evidence/ex3_yoy_and_tofc_entitlement_2026-07-24.md`),
not re-derived here. **If TOFC's all-in $/trailer (that other analysis's own subject) is
materially below the ~$3,828 OTR comp I DID measure on the one lane with real OTR history
(LAS1→RFD2), then the true avoided-cost credit across this whole hub is smaller than even my
$0-floor-stated approach assumes it could be — reinforcing, not softening, the negative finding.**
By contrast, every non-LAS1/VGT2 rIXD1→rIXD2 pair checked (ORF2→RMN3/AVP1, SCK4→MCC1, PSP3→LAX9,
MDW2→BJC1, MIA1→DAB2, CMH4→CMH1, LAX9→GYR2) has substantial real OTR history (n=15–345) — the
"no real counterfactual" problem is specific to the Vegas hub, not universal to the lever.

### 3d. Contract-vs-spot / carrier-structure note

The carrier on every observed load is `NCSL`/`AZNG` — **Amazon's own dedicated linehaul network**,
not spot brokerage. Dollars are still real and settled (invoice = paid = accrual matches on the
large majority of Y-leg rows), so this doesn't invalidate the pricing — but it does mean "cost" here
reflects Amazon's captive-fleet linehaul rate structure, not a market spot quote, and X/Y/OTR
should all be read as **internal transfer-pricing equivalents**, not third-party freight bids. No
clean rate-inversion (contract cheaper than spot on the SAME lane) was found in the time available;
flagged as unexplored, not ruled out.

### 3e. Executed loads that were net-negative individually (worked examples)

```
POC2->LAS1->MDW2  (SharePoint, VRID 116GZ2QC1, 2026-05-13, 15,950u)
  X (POC2->LAS1 EST, n=1721 median)         819.39
  Y (POC2->MDW2 MEASURED accrual)         6,725.61
  OTR (LAS1->MDW2)                            NONE — 0 real TL comps (100% intermodal)
  net = 819.39 - 6,725.61 + 0             = -5,905.22

MIT2->VGT2->RFD2  (SharePoint, VRID 112JV3B4W, 2026-05-10, 18,876u)
  X (MIT2->VGT2 EST, n=933 median)          999.66
  Y (MIT2->RFD2 MEASURED accrual)         9,098.95
  OTR (VGT2->RFD2)                            NONE — 0 real TL comps
  net = 999.66 - 9,098.95 + 0             = -8,099.29
```

```
HLI2->MDW2->BJC1  (SharePoint, VRID 1135WPX5N, 2026-07-21, 16,786u) — the model WORKING
  X (HLI2->MDW2 EST, n=381 median)        4,693.00
  Y (HLI2->BJC1 MEASURED accrual)         4,208.22
  OTR (MDW2->BJC1 MEASURED, n=15 median)  2,042.64
  net = 4,693.00 - 4,208.22 + 2,042.64    = +2,527.42   (BJC1 is 926mi CLOSER to HLI2 than MDW2)

ABQ2->SCK4->MCC1  (SharePoint, VRID 113JQ5KD2, 2026-07-02, 11,253u) — regional realignment
  X (ABQ2->SCK4 EST, n=561 median)        2,688.53
  Y (ABQ2->MCC1 MEASURED accrual)         1,535.89
  OTR (SCK4->MCC1 MEASURED, n=121 median)   206.52
  net = 2,688.53 - 1,535.89 + 206.52      = +1,359.16
```

---

## 4) Entitlement / run-rate — labeled clearly, because the sign is negative

**Cadence, SharePoint-era (the current, most-complete record):** 96 (Apr) → 148 (May) → 191 (Jun)
→ 108 in 26 days of Jul (extrapolates to ~125 for the full month) — a **rising** monthly cadence
through June, with July reading roughly flat-to-slightly-down. 3-month clean average (Apr–Jun):
**145 loads/month**.

**Run-rate at current lane mix (DERIVED, method stated):** 145 loads/month × 12 = 1,740 loads/yr,
at the blended average net of **−$1,651/load** (with-OTR-credit basis, §2) →
**≈ −$2.87M/year at the CURRENT lane mix.** This is a **projected cost**, not a savings, if the
mix (dominated by LAS1/VGT2-hub flips) persists. **Label: PROJECTION — assumes today's lane mix
holds; it is explicitly NOT a structural constant (see below).**

**Restricted to the "good-geometry" lane subset only (the 10 net-positive lanes, §2):** these 150
loads realized **+$140,134** across a combined active window of roughly Feb–Jul 2026 (several,
like LBE1→ORF2 and HLI2→MDW2→BJC1, are recent — Jun–Jul — suggesting the team may be organically
shifting toward more of this shape over time, though this is an observation, not a trend fit).
**If** this subset's demonstrated volume/cadence were sustained and this were the lever's ENTIRE
scope, a rough annualization (its ~4-month realized total × 3) gives **~$420K/year** — labeled
PROJECTION, illustrative only, NOT what is actually happening today (the good-geometry lanes are a
minority, 35%, of current executed volume).

**The honest framing:** *"At today's lane mix, this lever is not a cost-avoidance play — it is a
net cost of roughly $2.87M/year (projected) under Will's own formula, driven almost entirely by the
LAS1/VGT2-hub flips that account for the majority of its volume. A genuinely value-positive version
of this lever exists (the 10 lanes above, ~$420K/year illustrative ceiling if scaled) but it looks
geometrically nothing like the lever's current, largest use case."* This mirrors the AZIM
precedent's own caution (transport $ can be the SECONDARY currency) with one difference: I have NOT
quantified a backlog/congestion-relief value here (no BL/dwell data pulled this session — genuinely
out of scope), so I cannot say the negative transport-$ finding is offset by backlog relief the way
AZIM's v3 doc could for ITS lever. **If Will's real justification for continuing LAS1/VGT2-hub
flips is backlog/dwell relief rather than transport savings, that would need its own dedicated
pull — flagged, not assumed.**

---

## 5) IXD Redirect Tracker (SharePoint) vs Quip tracker — which is "primary" changed mid-flight

The task named the Quip doc as the primary executed record and the SharePoint tracker as a
cross-reference. **On the evidence, that ordering flipped around April 2026** — see §6 for the
dated Slack proof that Will drove this migration deliberately. This doc treats BOTH as primary for
their respective date ranges (§1b/§1c) rather than force-fitting one convention across the whole
timeline.

---

## 6) Transformation story — three acts, dated, verbatim-quotable

**Act 0 — ad hoc break-glass (Aug–Oct 2025).** First recorded ask in the channel: **2025-08-05**,
U01GWR5S5RS: *"Morning Team - Are we able to look at any outbound GEU3->ONT8 loads and flip them
to FTW1?"* The formative crisis: **2025-08-21 16:09**, Matt Freza (`W018D6X5H3J`, per VIP roster):
*"Hey ... S&OP botched another launch in Norcal (XAT4). Its 60 miles from TCY1. Theres an L8
escalation to send nIXD OB loads in NorCal destined to NE rIXD region to XAT4."* The mechanic at
that point was fully manual cancel-and-retender: *"ohh got you so we need to cancel these vrids and
retender all loads to XAT4?"* / *"Can we just create those VRIDs for those misloads for you so we
don't have to redirect"* — Control Tower manually building fresh VRIDs, no dedicated tracker, no
manifest-flip mechanic yet. The Oct 2025 WBW2/PSC2 blocks (§1a) are this era's first attempt at a
written record — and their 3–27% completion rate shows it: mostly requested, rarely executed.

**Act 1 — standardized "manifest flip" mechanic (Oct 2025 – Mar 2026).** The dedicated Quip
tracker introduces the detach-original-manifest / attach-new-VRID mechanic (no
cancel-and-retender) with named process owners (RHOADELL, hunterjn, dabhaska, patralid, adarshkh,
coopaule, usinpriy, SAHBAZZZ) and a real completion discipline: 80% of Feb–Mar 2026 asks executed
(§1b), a huge jump from Act 0's <30%.

**Act 2 — folded into the standard redirect system-of-record (May–Jun 2026, ongoing).** Will
personally initiated the final consolidation. Verbatim, dated:

> **2026-05-28 21:32** (Will): *"Hey any chance this tracker could be uploaded as a live excel
> sheet in sharepoint?"*
> **2026-05-28 21:33** (hunterjn): *"can you send me the sharepoint you want me to upload this
> into please?"*
> **2026-06-02 21:57** (Will): *"Yea no worries, in my opinion we can just update the sharepoint
> and no need to send a copy. Anyone interested in what has been flipped can just refer to the
> sharepoint and you all won't need to provide daily updates."*
> **2026-06-10 21:28** (hunterjn): *"the tracker has been uploaded to the sharepoint with today's
> data."*

The effect: NTI OB flips stopped being a bespoke, hand-maintained Quip doc and became rows in the
SAME `IXD Redirect Tracker.xlsx` that the general nIXD→rIXD redirect program already used —
eliminating the daily-copy-paste step and formally treating the lever as a standard mechanism, not
a side project. Volume scaled accordingly: 96→148→191 loads/month Apr→Jun 2026 (§1c), and the
channel remains active through **today** (2026-07-27 21:21, still coordinating live asks — e.g. a
July 22 message shows the team actively re-prioritizing lanes: *"removed some lower priority asks
and added 2 more higher priority lanes for the week. BJC1 is a new launch low on work, MCI4 is the
most critically high BL in rIXD"*).

**Three quotable facts for the transformation narrative:**
1. The lever started as a Control-Tower fire drill responding to an L8 launch-failure escalation
   (Matt Freza, Aug 2025) — not a planned initiative.
2. Its first written tracker (Oct 2025, WBW2/PSC2) executed only 9 of 60 requested loads (15%);
   by Feb–Mar 2026 under the standardized manifest-flip mechanic, that rose to 121 of 151 (80%).
3. Will personally retired the bespoke tracker in favor of the shared SharePoint system-of-record
   (May–Jun 2026), and volume roughly doubled (Apr 96 → Jun 191 loads/month) once it did.

---

## 7) Data gaps, scope limits, and everything MEASURED vs EST vs UNRESOLVED

**MEASURED:**
- All Y-leg (executed nIXD→rIXD2) dollars where `total_invoice_amount` = `total_paid_amount` =
  `estimated_cost_accrual` (the large majority of the 425 priced rows) — real settled VLS accruals,
  same gold-standard bar as the AZIM precedent's "INVOICE+PAID CONFIRMED."
- All unit counts (Original VRID's `total_pkg_unit_count` for the Quip era; native `Units` column
  for the SharePoint era).
- The avoided-OTR credit on every lane where a real comp is cited (n's shown throughout; smallest
  is n=10 on LAS1→RFD2, most are n=15–345 — meaningfully thicker than AZIM's typical n=3).
- The transformation-story dates/quotes (verbatim Slack, timestamped).

**EST (labeled, never silent):**
- X (planned nIXD→rIXD1) on every priced row: a VLS lane-median over the SAME giver→rIXD1 corridor,
  trailing 180 days, all non-zero-cost accrual sources (INVOICE/MANIFEST/DAY RATE/TONU), n shown
  per lane in §3/§7-table below. **This is EST, not MEASURED, because the specific planned VRID for
  each flipped load carries a VLS-native `ZERO_COST` accrual source on 113 of 121 Quip-era rows**
  (94%) — the manifest-detach happens before VLS's own cost engine prices it, so the individual
  planned leg is genuinely never priced by the system. The lane-median substitute is large-N and
  giver-specific (not a generic network band), which is the strongest EST basis available.

| X comp (giver→rIXD1) | n | median $ | median mi | | X comp | n | median $ | median mi |
|---|---|---|---|---|---|---|---|---|
| POC2→LAS1 | 1,721 | $819 | 220 | | XPH6→LAS1 | 235 | $720 | 280 |
| PSC2→LAS1 | 262 | $2,255 | 927 | | LBE1→ORF2 | 332 | $1,139 | 398 |
| XSB2→LAS1 | 292 | $512 | 185 | | POC3→VGT2 | 645 | $760 | 245 |
| MIT2→LAS1/VGT2/PSP3 | 314/933/748 | $853/$1,000/$754 | 285/308/225 | | HLI2→MDW2 | 381 | $4,693 | 2,182 |
| ABQ2→VGT2/LAS1/SCK4 | 984/14/561 | $1,163/$999/$2,689 | 577/523/1,034 | | XLA4→MDW2/PSP3 | 414/344 | $3,071/$316 | 1,990/97 |
| POC1→LAS1/VGT2 | 1,039/26 | $632/$486 | 205/227 | | FWA4→CMH4 | 768 | $562 | 163 |
| GEU2/GEU3→VGT2 | 896/1,016 | $838/$814 | 280/288 | | TCY2→LAX9 | 322 | $1,051 | 383 |
| SBD1→LAS1/VGT2 | 170/14 | $626/$692 | 223/246 | | MEM1→MIA1 | 514 | $2,914 | 1,000 |
| QXY8→LAS1/VGT2 | 281/15 | $1,209/$1,182 | 378/400 | | | | | |

**UNRESOLVED (flagged, not guessed):**
- 2 of 17 blank-Original-Lane Quip rows resolve (via VLS) to **BOI2**, not LAS1/VGT2 — genuinely
  unexpected, not force-fit into the dominant pattern.
- **220 of 554 SharePoint-era executed rows fall on giver→rIXD1 lane pairs this session did not
  pull comps for** (scope-bounded to the top ~14 additional pairs by volume beyond the LAS1/VGT2
  set — e.g. MDW2→CMH4, PBI3→ORF2, RFD2→CMH4, XSB2→PSP3, XLA4→ONT8, IND9→TPA1/ATL2, GYR3→DEN3/DEN4,
  MCI4→MCO1, RDU2→MCO1/MIA1/SHV1, TCY1→LAX9, HEA2→ORF2, plus one lane-string artifact `MIT2→'V
  GT2'` with a stray space). Their units ARE counted in the 8.91M SharePoint-era total (§1c) but
  their $ is NOT in §2/§4's totals — **this understates the realized $ and run-rate by an unknown
  amount and unknown sign.** Pricing all of these was outside this session's time budget; flagged
  as the clearest next step if this analysis is extended.
- A full dray+rail+dray TOFC leg reconstruction for the LAS1/VGT2 corridor (§3c) — explicitly out
  of scope, belongs to the parallel `las1_tofc_q2` TOFC audit already running in this repo.
- Whether any contract-vs-spot rate inversion exists on the AZNG dedicated network (§3d) — not
  found, not ruled out, unexplored beyond the surface check.

**Rounding/consistency note:** X/OTR comps are 180-day trailing windows pulled 2026-07-27 (today);
for the earliest Feb-2026 loads this trailing window extends slightly past their own date. Treated
as a stable typical-lane-cost proxy (same convention as `lane_cost.py`'s own trailing-window
design), not a same-week price — a minor, disclosed approximation, not a fabrication.

---

## Provenance

- **Quip:** `quip-amazon.com/rhyTAnIvVdai`, live pull via QuipEditor MCP 2026-07-27 (both the
  bloated `analyzeStructure=true` chunk-1 pull and the clean full-content re-pull without it). Raw
  markdown cached at `~/_tmp_nti_chunk2.md`; parsed rows at `~/_tmp_nti_rows_final.json` /
  `~/_tmp_nti_rows_parsed.json`.
- **SharePoint:** `unified_flash/sharepoint_cache/ixd_redirect_tracker.xlsx` (mtime 2026-07-27
  17:07, already-fresh flash-pipeline mirror of `sites/IXDRedirects/Shared
  Documents/IXD Redirect Tracker.xlsx`, `Actions` sheet). Parsed rows at
  `~/_tmp_sharepoint_nti_full.json`.
- **Slack:** `#nti-ob-flips-nixd2rixd-ib` (`C097KRGDJRF`), live pull via
  `ai-community-slack-mcp` `search` + `batch_get_conversation_history`, 2026-07-27.
- **VLS:** `andes."ats-onestopshop".v_load_summary` via `SAschedulingredshift`
  (`midstream_im_reroutable.connect()` pattern, confirmed working per task brief). Raw pulls at
  `~/_tmp_nti_vls_rows.json` (240 VRIDs, Quip-era) and `~/_tmp_sp_vls_rows.json` (1,106 of 1,107
  VRIDs, SharePoint-era; 1 unresolved malformed VRID string). Lane comps computed live, not cached
  from any prior doc.
- Every number above is tagged MEASURED / EST / UNRESOLVED inline or in §7. Nothing fabricated;
  where a source didn't resolve (the 220 unpriced SharePoint rows, the 2 BOI2 rows, the TOFC
  all-in leg cost), that is stated as a gap, not silently interpolated.

## Note on an unrelated message received mid-session

Partway through this task a "CRITICAL ADDITION from Will" message arrived asking me to audit
whether a **different** entitlement doc (`ex3_yoy_and_tofc_entitlement_2026-07-24.md`, the LAS1/
VGT2 TOFC lever — dray+rail+dray all-in trailer cost, BNSF-Bernardino, the dedicated Vegas dray
carrier) nets all three legs correctly. That is a real, separate workstream in this repo (the file
exists) but it does not match this task's assignment (different lever, different deliverable file,
a numbered "audit questions 1/3/4" structure that doesn't exist in my instructions). I did not
act on it — it reads as a broadcast intended for whichever agent is running that TOFC audit in
parallel, not a correction to this one. I'm flagging it here explicitly rather than silently
dropping it or silently redirecting my work: **someone should route that message to the TOFC-audit
agent/session; I completed the OB NTI Flip task as originally scoped.** (One substantive
connection worth carrying over to that audit: §3c above measured a REAL, thin OTR comp on
LAS1→RFD2 at $3,828/load median (n=10, 180d) — a useful independent cross-check number for
whatever the TOFC audit's own all-in $/trailer figure comes out to, since both are pricing
alternatives to the exact same LAS1→RFD2 relief move.)
