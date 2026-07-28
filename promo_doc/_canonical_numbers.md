# Canonical Numbers — v3 Candidate Provenance Ledger

**Owner:** William Zhou | **Regenerated:** 2026-07-12 (Pass A of ARC1 rewrite) | **Replaces:** the a4de771 (2026-05-19) ledger, which predates the June corrections.
**Rule:** every number in `drafts/promo_doc_v3_candidate.md` must appear here with a tier, source, and as-of date before the doc ships.

**Tiers:** `LIVE` = live-query verified | `PDF` = signed Q1 2026 Annual Review PDF | `GUIDE` = committed project guide/tracker | `TESTIMONY` = experiential claim, framed as such in body | `PENDING-WILL` = do not ship until Will ratifies.

---

## Sizing spine (Opener + Scope)

| Number | Tier | Source | As-of | Notes |
|---|---|---|---|---|
| **~450M units/wk rIXD+nIXD inbound arrivals** (450.7M actual) | LIVE | SANDOP via unified_flash `network_performance.sql`, run 2026-07-12: rIXD 358.7M + nIXD 92.0M; plan 449.0M | WK28 2026 | Replaces WRONG "~302M" (ARC1 §3 #1). Ratify in Pass F (DECISION 1) |
| **55 sites = 35 rIXD + 20 nIXD** (doc uses 55) | LIVE | `ict_regions.py` map (35 rIXD, incl. BJC1 launched 6/28) + `fc_region_full.csv` fc_type='IXD - National' (23) minus closed WBW2/PPO4 + pre-launch GEU5 = 20 nIXD. Verified 2026-07-13 | 2026-07-13 | v4 body uses 55 (35+20); the raw 58/23 is the pre-exclusion count. DECISION 1 RESOLVED — clean count in body, no exclusion parenthetical per Will 7/13 |
| **1DC network slice (on-paper scope)** | GUIDE | Ownership stated as 1DC + rIXD + nIXD redirect execution; **not volume-sized — Will's call 7/12, no pull needed** | 2026-07-12 | Body names 1DC as owned ("...plus the 1DC network") with the volume sentence explicitly labeled rIXD+nIXD. Settled — no DECISION marker |
| **RDC launch-volume forward scope (IMO1/XLA4)** | GUIDE | rDC-launch DW feed; per Will 2026-07-12 live correction | 2026-07-12 | One verified-framed clause in Scope of Role only; no volume claimed |
| **$36.3M 2026 redirect budget ($20.4M NVF + $15.9M NTI)** | LIVE | ICT Goals Quip (ygt1AHeub90J), Finance WK6 | 2026-07 | Verified anchor (ARC1 §3) |
| Career arc: 2 of 5 rIXD regions (first 6 mo) → **all 5 rIXD in Q3 2025** → **+nIXD in Q1 2026** | GUIDE | Will's live correction 2026-07-13 (supersedes the "IPEX-NTI consolidation Q3–Q4 2025" framing, which was WRONG). SOP-POC "attested by" clause DROPPED from body per Will 7/13 | 2025–2026 | Opener rewritten 7/13 |
| ~~DOE program business owner~~ — Will is **no longer the DOE business owner** (Will 7/13) | — | Removed from opener + Readiness; DOE now framed as intake AUTHORSHIP only (see Ex5 row) | 2026-07 | Smart Reroute also removed from exec summary (Will: low-impact vs HJBI) |
| Joined Amazon **October 21, 2024** | LIVE | Phonetool (`phonetool.amazon.com/users/zhouzw?job-history=true`), verified 2026-07-13: hire_date 21-OCT-24, job_level 4, mgr mffreza | 2024-10-21 | DECISION 10 RESOLVED — "October 2024" confirmed |

## Example 1 — 3P IM Rate Restructure

| Number | Tier | Source | As-of | Notes |
|---|---|---|---|---|
| **$79K saved / 359 redirects** | PDF | Q1 2026 Annual Review p2 | Q1 2026 | |
| **47% avg cost reduction per move** | PDF+LIVE | Q1 PDF p2 — **VERIFIED 2026-07-13** against live redirect tracker + rate matrix at **46.6%** (Model B = savings ÷ full new-lane rate; `evidence/ex1_savings_verification_2026-07-13.md`). p4's 27% is the outlier, not the 47%. DECISION 8 RESOLVED — keep 47%, no Matt reconciliation needed | Q1 2026 + WK2–27 | |
| **~$85K rate savings YTD / 324 redirects / ~4.0d avg LTS** | LIVE | Redirect tracker (SharePoint IPEXTeam) WK2–27 + HJBI rate matrix; $60K on 253 matched lanes → ~$85K extrapolated to all 324; tracker YTD rollup = 324 redirects, 4.0d avg LTS | WK2–27 2026 | Dwell-cost-avoided ($512K) intentionally EXCLUDED from doc per Will 7/13 — different mechanism, do not conflate |
| **$229K projected annual savings** | PDF | Q1 PDF p2 | Q1 2026 | Also replaces the killed "-$4M YoY" Intro claim (ARC1 §3 #2 — Niko-doc bleed, removed) |
| **684 hrs spot-quote delays eliminated / $23K labor** | PDF | Q1 PDF p2 | Q1 2026 | |
| ~$2M historical overpayment | PDF | Q1 PDF p2 | 2025 | |
| 2–4 hrs per spot-quote request | PDF | Q1 PDF p2 | 2025 | |
| 3+ months cross-functional negotiation | PDF | Q1 PDF; Outlook record 7/21–10/2025 | 2025 | |
| Four weeks methodology iteration | LIVE | Outlook: rate-publication agreement 7/21/2025 → alignment 8/18/2025 | 2025 | Replaces WRONG "six weeks" (ARC1 §3 #6). Dates live in `evidence/ex1_3pim_rate_backing.md`, not body |

## Example 2 — HJBI Drop-to-Live

| Number | Tier | Source | As-of | Notes |
|---|---|---|---|---|
| **$22.5M annualized opportunity** | GUIDE | `hjbi_pilot/CLAUDE.md` (sizing analysis, Nov 2025) | 2025-11 | KNOWN peer-doc overlap: $22.5M / 3,168 / $2.25M also appear in a peer's identification analysis — same real opportunity, handed off (peer endorsement 4/22 — verbatim in `evidence/targeted_thread_pulls.md`, restored from a4de771 on 7/12). Will's doc claims re-engagement/execution, never identification; Readiness total now states the peer-identified/Will-executed split in-sentence (ARC2 HIGH-2). Committee-safe as long as those lines hold |
| ~3,168 convertible drop appointments YTD / 11.12% of HJBI volume | GUIDE | `hjbi_pilot/CLAUDE.md` L31 | 2025-11 | |
| Stalled since November 2025 identification; live within three weeks of taking primary (April 2026) | GUIDE | `hjbi_pilot/CLAUDE.md` log; WK20 launch | 2026-05 | "Four months sitting / Jan slip / 24-hr reply" color CUT (ARC1 §3 #11) |
| HJBL SCAC provisioned May 2026 | GUIDE | `hjbi_pilot/CLAUDE.md` (5/1/2026 — day-date to evidence) | 2026-05 | |
| Pilot launched WK20; four-KPI scorecard (FPY, Driver Detention cost, NCNS rate, MDP benefit) | GUIDE | `hjbi_pilot/CLAUDE.md` | 2026-05 | |
| Conservative 2026 target $2.25M / 2% of HJBI drop volume | GUIDE | `hjbi_pilot/CLAUDE.md` | 2026 | |

## Example 3 — IPEX Ops Flash Automation

| Number | Tier | Source | As-of | Notes |
|---|---|---|---|---|
| 2+ hours multi-leader morning work → minutes | TESTIMONY | Pre-automation baseline has no repo artifact (ARC1 §3 #12) — framed experientially in body | H1 2025 | |
| **~20% of an FTE returned** (~90 min/day) | TESTIMONY (softened) | Safe-default framing of the ~407 hr/yr figure (ARC1 §3 #7) | H1 2026 | **PENDING-WILL**: derive 407 + 224 into this ledger, or keep softened framing, or cut (DECISION 5). 224 hr/yr has NO derivation anywhere — cannot ship as a number |
| Flash of record: authored internal wiki + GitFarm package | LIVE | REVIEW 6/28 find #5 — `Flash_Workflow` wiki (authored/owned) + GitFarm package w/ onboarding | 2026-06 | Third-party-visible anchor |
| GenAI suite inventory (six components: morning + afternoon flash, ess_lanes, wbr, sim_auditor, validator) | GUIDE | Repo; 733 tests repo-wide | 2026-07 | Body no longer states a count ("an interlocking suite of workflows") — the Ex3 sentence enumerates only four, so "six" was not reader-reproducible (ARC2 MED-3) |
| 11 stakeholders trained (Context Document methodology, pre-Kiro) | PDF | Q1 PDF p2 | 2025 | Used in PROPOSED Summary. Q1 PDF says he **"Learned about"** the methodology — body verb must be adopted/operationalized, never "developed" (ARC2 HIGH-1) |

## Example 4 — OB NTI Flip (KEEP branch; cut decision = DECISION 2)

| Number | Tier | Source | As-of | Notes |
|---|---|---|---|---|
| **~7 loads/day at the February 2026 peak of the manual pilot** | GUIDE | `grill_agenda_2026-06-07.md` — Feb 2026 baseline; 3/4 stop-call; no current KPI/volume data | 2026-02 | Dated per ARC1 §3 #9 — present-perfect "has since run" removed |
| TOFC variant: $1.7K/trailer vs current TOFC routing; $4K/trailer vs OTR | GUIDE | `las1_tofc_q2/CLAUDE.md` unit-economics teardown (verified verbatim 5/19) | 2026-05 | Adopted into Q2 LAS1 TOFC program |
| Multi-day lead time / double dray (destination-side baseline) | GUIDE | `ob_nti_flip/CLAUDE.md` | 2026-Q1 | Qualitative mechanism, no unit claim |

## Example 5 — DOE Redirect Automation

| Number | Tier | Source | As-of | Notes |
|---|---|---|---|---|
| **Authored** the IXD redirect-feasibility intake artifact (NOT program business owner — Will 7/13) | LIVE | `evidence/gaps_closed_2026-06-29.md` GAP 3 — Will uploaded `ixd-redirect-feasibility.intake_v0.5.xlsx` 6/4; drove validation design 6/23 | 2026-06 | "owns" softened to "authored" in body 7/13; Ex4 rests on authorship + the constraint-MDP disproof (both historical), not current ownership — FLAGGED for Will: still a keeper as example #4? |
| Three intake templates (IXD / Sortable / Non-Sort), May 2026 distribution; IXD largest by unit volume | LIVE | Program-lead template distribution (Slack, May 2026); "largest by unit volume" cross-checked vs live WK28 network series | 2026-05 | |
| **11,700 hrs/yr IPEX labor savings at full entitlement** | PENDING-WILL | No OP-plan artifact carries it (repo grep + InternalSearch, ARC1 §3 #8); attributed in body as the program's stated goal, not Will's commit | — | DECISION 5: keep with program-stated attribution, or cut |
| Approval-gate drivers = giver buffer + WK+1 backlog persistence (constraint-MDP was NOT the gate) | GUIDE | Hans-approval reverse-engineering (`reconstruct_approval.py` analysis; REVIEW 6/28 find #4) | 2026-06 | Corrects v1's constraint-MDP misstatement; sign-off routing stated as PROPOSED |

## Readiness / forward scope

| Number | Tier | Source | As-of | Notes |
|---|---|---|---|---|
| **>$22.7M identified opportunity taken into execution** ($22.5M HJBI + $229K 3PIM annualized) | GUIDE+PDF | Arithmetic recomputed in REVIEW 6/28 #9 | 2026-06 | Verb = "taken into execution", NOT "shipped" — realized-on-record is $79K + a $2.25M pilot target (ARC2 HIGH-2); peer-identified attribution stated in-sentence; PACE stays unquantified (still covered in Readiness bullet 3 + direction 3) |
| LAS1 TOFC teardown: $2.6K (TOFC nIXD) vs $4.3K (current LAS1) vs $6.6K (OTR) per trailer | GUIDE | `las1_tofc_q2/CLAUDE.md`, verified verbatim 5/19 | 2026-05 | |
| **AZIM 1P-IM midstream: ~316 executed loads / ~5.29M units WK24–30; net transport avoidance ~$150K realized; ~$930K EOY-2026 pace / ~$1.3M full-year run-rate** | MEASURED+EST | `_notes/azim_entitlement_ytd_deepdive_2026-07-21.md` (+7/24 correction) + `_loads.tsv` (per-VRID VLS actuals; model = avoided_OTR − (Y_full − X_full) + crosstown avoided-rail) + `promo_doc/evidence/clt2_mci4_verification_2026-07-24.md` + `azim_reclassified_crosstown_2026-07-24.md` + `azim_seasonal_annualization_2026-07-26.md` | 2026-07-26 | **CURRENT (supersedes the ~$145K/$0.85M row).** Realized **$148,841–$151,565** ("~$150K"), 316 loads / 5,291,537 units, priced load-by-load vs VLS carrier-settlement actuals (~90% measured). **EOY-2026 ~$930K / full-year ~$1.3M** via the SEASONAL method (Will's spec 7/26, supersedes the retired ÷16.7% and the flat ×52): capture rate (aggregate 7-week, $0.00365/redirect-unit ≈ 12.9% of total redirect units — NO week exclusions per Will) × seasonally-expected redirect volume from trailing-18-mo steering trackers (2025 44-wk curve shows WK40–52 ~2.0× mid-year; ×0.9146 YoY scale). Corrections folded: CLT2→MCI4 lane REMOVED (no manifest ID, never executed — Will's call, was −$7,394 so removal raised the base); WK30 MCI4→IND9 +9 loads ADDED (timing gap, confirmed CROSSTOWN via run-structure join — a 2nd distinct hub/carrier crosstown pair, so crosstown is recurring not one-off); tracker column-drift audited (manifest-ID col moves 8→14 within a tab — 0 miscounts). RDU2→TOL3 crosstown avoided-rail MEASURED ~$996/load (waybill re-rates — Will confirmed 7/24). OTR counterfactual confirmed by Will. Cost SOURCE = VLS `ats-onestopshop.v_load_summary`; fallback = AZIM billing / procurement IM lane rates. |
| ~12% network trailer-cap haircut (Finance/ATS-set); Will built the IPEX-side threshold + per-network elimination logic | LIVE | `evidence/gaps_closed_2026-06-29.md` GAP 2 (6/8 + 6/10 verbatim) | 2026-06 | **Back in READINESS dir-1** (was briefly Ex4 on 7/13, then Will chose DBR/WBR/QBR for Ex4; trailer-cap detail preserved in Readiness dir-1). Framing: he built the threshold, did NOT set the cap. 520-cap / >3.0d giver-W+1-BL gate / ~560→under-520 all from Will's own 6/8+6/10 posts. Derived figures (~301 weekly redirect loads, ~36 cut ≈12%, 1,000→750mi gate) trace to `reference_redirect_reduction_baseline` — CONFIRM current. AZNG account figures = Hartland/Udit directive context, NOT Will's |
| HUBG/PGLI expansion: eliminate 95%+ manual rate requests; 200 hrs → <50 hrs annual wait | GUIDE | `3p_rate_matrices/CLAUDE.md` — correctly framed as Q3 2026 goals | 2026-07 | |
| Smart Consolidation / PACE: named ICT-Sort owner, 2027 public launch | GUIDE | `smart_consolidation/CLAUDE.md` + agent-context (verified 5/19) | 2026 | Unquantified $ |
| Manager's June 2026 on-record backing (gridlock thread) | LIVE | `evidence/gaps_closed_2026-06-29.md` GAP 1 — verbatim 6/26 quote | 2026-06 | Quote itself BANNED in body (DNA #5) — paraphrased; destination = DECISION 11 |
| Architected DBR/WBR/MBR/QBR (49+ metric lines, DBR v1 launched 3/28/2025, first six months) | PDF+EMAIL | Q1 PDF p2 + DBR Metric Review thread Mar 25–May 31 2025 (`evidence/ex4_dbr_wbr_backing.md`) | 2025 | **EXAMPLE 4** (Will's 7/13 call). Now fully backed — taxonomy (execution/OTP-OTD/defect-controllability × network × mode + WBR LTS components), the created_by D-1 data-dependency escalation + fix, IPEX Analytics/IBWR coordination, published metric of record. Version churn + meeting dates + individual names held to backing per altitude/name rules |

| **TOFC Q2 2026: 189 trailers executed; ~$685K estimated cost avoidance ($684,330)** | MEASURED+EST | `promo_doc/evidence/tofc_methodology_audit_2026-07-27.md` §5 waterfall | 2026-07-28 | **SUPERSEDES the $336K / 146-trailer figure** (steering-tracker undercount; desk-EST both sides). Ground truth = SharePoint VRID tracker (190 rows − 1 fake-executed `112BFXS56`, VLS+Slack corroborated). TOFC cost MEASURED all-in 3 legs (Vegas dray + rail + dest dray), mean $3,946/trailer, 183/189 rail legs invoice-settled; rate-parity win: rail leg $3,597→$2,313 flat (−36%, $1.18/mi) WK18+. Credit = live OTR market comps per lane ($6.5K–$8.3K, lane_cost geo-relaxed; validated by NV/SW→MW mileage-band n=6,500+ median ~$5.9K and by real early-2026 executed OTR redirects — SIM CM 77384, VRID `114B8B7F4` $5,073 exact cross-check). Will's ruling 7/28: OTR is the counterfactual; use OTR comps. Label = "estimated" (credit side EST). |
| **OB NTI Flip: 675 loads / 10.46M units executed Feb–Jul 2026; ~$570K estimated net cost avoidance ($572,468 on the 425 fully-priced loads, basis C)** | MEASURED+EST | `promo_doc/evidence/ob_nti_entitlement_2026-07-27.md` + `ob_nti_counterfactual_sensitivity_2026-07-27.md` (basis C) | 2026-07-28 | First $ claim for this lever. Formula: (planned nIXD→rIXD1 EST n≥235 + avoided downstream OTR at live market comps) − executed nIXD→rIXD2 MEASURED settlement. Basis C = Will's ruling 7/28 ("OTR was the alternative"): Vegas-hub lanes credited at lane-specific live ESTs $6.3–9.1K (validated by mileage-band + real Feb SIM record). Fully-priced = 425/675 (63%); remainder accrual-lag/unresolved-origin, NOT extrapolated. Floor basis B (credits $0 where no real comp) = −$702K — the spread is the counterfactual, disclosed in evidence. Verify pass CONFIRMED aggregates to the dollar; per-lane table in sensitivity doc has known row-level errors (credit omitted on 4 Quip-era rows; do NOT quote lane rows until patched). Do NOT quote a forward run-rate for this lever (lane-mix dependent). |

## PENDING-WILL register (do not ship without ratification)

1. **450.7M WK28 + 58 sites (35+23) as-of 7/12** — figures are live-verified; Will ratifies the as-of framing + plan-vs-actual choice (DECISION 1).
2. **~407 hr/yr individual + ~224 hr/yr team-scaling** — 407 = self-framing in `ai_training/redirect_exec_ai_training_scope.md`; **224 has zero derivation**. Body ships the softened "~20% of an FTE" testimony framing; restore numbers only if derived here first (DECISION 5).
3. **11,700 hrs/yr DOE entitlement** — program-stated attribution only (DECISION 5).
4. **Hire date October 2024** — Phonetool/A-to-Z confirm (DECISION 10).
5. **47% vs 27% Q1-PDF self-contradiction** — doc uses p2's 47%; Will sends Matt the one-line heads-up personally (DECISION 8).
