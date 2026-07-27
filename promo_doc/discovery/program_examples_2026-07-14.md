# Program-Level Cross-Org Partnership Candidates — Discovery 2026-07-14

**Task C** — replacements for DOE intake + Smart Consolidation/PACE in the promo doc.
Excluded per brief: DOE intake, PACE/Smart Consolidation. Already covered elsewhere: HJBI Drop-to-Live, 3P IM rate restructure (Ex1), OB NTI, AZIM midstream.
Sources mined: Slack (ai-community-slack-mcp), Outlook (email_search), InternalSearch, local project guides. All snippets verbatim.
**Verification pass 2026-07-14 (second run):** spine citations for #1 (C0AHBSNN0TY ts 1779126337.189119), #2 (D0A6VJQM1PA ts 1784062890.798779), #3 (C0B9RU52RGU ts 1781110319.839059 / 1781482742.532609; C0B9P3L7Y66 ts 1781119711.612179; D07T7MM7Z3K ts 1781027806.481359), #4 (C0AVAR06T4H ts 1778598356.292739) re-pulled live from Slack — verbatim confirmed.

---

## RANKED CANDIDATES

### #1 — AFE Flip-Flop program (in-flight PO/ISA flips of AFE customer freight)

**One-line:** Will authored, from scratch, the 3-party IPEX × AFE Sales × AFE Ops process (later + AF Finance for cost allocation) to flip ARRIVAL_SCHEDULED AFE customer loads to closer/healthier takers pre-arrival, then built the closest-feasible matcher automation behind it.

**Why strong:** Clearest authorship of any candidate — Will literally wrote the process draft and secured the cross-org alignment himself; customer-facing freight (AFE Sales relationships) makes it genuinely cross-organizational, not just cross-team; quantified lead-time outcome per batch; a Finance workstream (cost allocation) spun out of it with L-level Finance/Ops stakeholders.

**Citations:**
- Slack #project-flip-flop-2-26-26 (C0AHBSNN0TY), ts 1778882480.154219, 2026-05-15: "Problem: LAX9 Yard utilization is at 94% after the site lost their offsites, and floor MDP is sitting at 8.29d… Ask: Flip ~40 arrival_scheduled live floor AFE loads from LAX9 → GYR3 (same SouthWest AFE seller region)."
- Slack same channel, ts 1779126001.831559, 2026-05-18: "I see that we have AFE Sales alignment & partial AFE ops alignment to commit bandwidth to support, so wanted to spin up a tracking sheet… Average lead time savings we would see on these if flipped is 18 days faster receive."
- Slack same channel, ts 1779126337.189119, 2026-05-18 — **the process authorship artifact**: "Process draft (open to feedback): 1. AFE Sales (Gerline team): confirm flip eligibility and update tracking sheet 2. IPEX (shelstro on my team)— secure new ISAs at GYR3, update PO/ISA info… 3. AFE Ops (Abel+Jake team)— make the SMC update so new VRIDs push through FMC."
- Slack mpdm-zhouzw--vairavac--shelbtk (C0B46BHP5LP), ts 1779145830.527179, 2026-05-18: "So far I have AFE Sales and AFE Ops aligned to support, we will be working on flipping loads this week."
- Slack C0AHBSNN0TY, ts 1779310546.090629, 2026-05-20: "next batch of LAX9 → GYR2 flip candidates ready… new SAT being on average 10d faster than the current SAT. Constraint mix: Drop_FL: 18 loads / 219K units - Live_FL: 6 loads / 165K units…"
- Email: "Need to ID AF Finance POC to Work with IPEX on Flip-Flop Cost Allocation" — Gaurav Walawalkar, 2026-05-27 ("these are AFE loads so we cannot use IB account as we still need to pick a portion of cost and revenue"); Bill Nesbit, 2026-06-04 ("Cost of redirect (Total cost to execute) – Average cost of planned move (linehaul + fuel) = incremental charges to be re-allocated").
- Local: `initiatives.md` (AFE Flip-Flop entry): "recent passes LAX9 618K / POC1+POC3 ~165K units flipped pre-arrival to GYR2/3, QXY8… Matt's GL cost-absorption sign-off secured (6/7)." **VERIFY 618K/165K against live tracker before doc use** (feedback_verify_counts_before_quoting).
- Local: `afe_flip_flop/CLAUDE.md` — matcher automation (decision rules, 37-col tracker emitter, tests anchored POC1 5/21).

---

### #2 — RDC Domestic PO Re-route launch (IMO1/XLA4 — first RDC network launch)

**One-line:** Will is the IPEX/ICT-side owner standing up redirect + PO-flip support for the launch of an entirely new network type (RDC), defining the redirect posture in the launch playbook, wiring the approval chain, and executing the first-ever RDC redirect on 7/14.

**Why strong:** Widest breadth — RDC launch team, S&OP (Hans approval), ESS/FBA seller teams, procurement-portal L8 approval chain, AFMM, external carriers (Estes/EXLA, UPS rates); it is net-new network-level scope (the "emerging RDC launch volume" in Will's on-paper scope); concrete dated outcome (first executed load) plus doc-level influence on the launch playbook. Caveat: freshest of all candidates — execution record is 1 test load as of 7/14; RDC team (biystuti) owns the upstream PO-flip plan, Will owns the redirect-execution side.

**Citations:**
- Slack DM (D0A6VJQM1PA), ts 1784062890.798779, 2026-07-14: "First load for first RDC launch (IMO1). Site shares MW_GL IBMR with the giver rIXD. RDC team requesting IPEX redirect intervention for this site while they work on more upstream PO flip solutions. Hans has approved the redirects…" + approval.amazon.com/approval/49120616.
- Email: "Approval fully approved - PO Edit Approval (49120616)" — AmazonApprovals, 2026-07-14: "This approval request is from William Zhou."
- Email: "[V2287440709] WK29 NVF RDC - Testing MDW2->IMO1" — William Ellis (patricwi Taskei comment), 2026-07-14: "Executed 1 EXLA redirect Units: 9,524 Cost: $2,350.88."
- Email: "MDW2->IMO1 Redirect Request" — Paul Kaye, 2026-07-14: "We have a one off shipment we're hoping to test and redirect to a new rDC site, IMO1."
- Email: "Meeting summary: RDC IMO1 Domestic PO Re-route [Daily]" — 2026-07-10: "Team discussed XLA4 rail flips starting today and analyzed PO redirectability for IMO1 launch volume."
- Slack mpdm-kaluvai--kylneuma--zhouzw--mffreza (C0BAST0RE65), ts 1781642740.407409, 2026-06-16 — playbook review: "short answer is: almost no redirect options in steady-state, and only PO-flips within the IBMR for unplanned disruptions >24hr… In break-glass… we can explore PO flips to RDC or out of network to rIXD in the same IBMR in conjunction with FBA seller comms."
- Slack mpdm-kaurishn--biystuti--amzparsh (C0BCAFRGUKG), ts 1782161975.322249, 2026-06-22: "we can try the PO flip process where the RDC team proactively selects POs they would like for RDC, and then IPEX would need to vet the POs for ability to flip unilaterally without approval."
- Slack #rdc-domestic-po-redirect-imo1 (C0BFN7G5ESU), ts 1784058485.228469, 2026-07-14: "5 redirects have been added to the tracker. I reached out to AFMM on 4… We got a rate back from Estes on 'RE: [EXTERNAL] MDW2->IMO1 Redirect Request'."
- Slack mpdm-dbmark--kaluvai--dieconno--biystuti (C0BB82ZQ71C), ts 1781729509.175919, 2026-06-17 — procurement-portal/L8 approval-chain dimension: "Every PO flip/trailer redirect we do cross-network gets blocked by procurement portal and needs to goes to our L8 for approval."

---

### #3 — Network trailer-cap governance mechanism (520/wk redirect-reduction commitment)

**One-line:** Off an L8 linehaul cost directive (Hartland/Udit AZNG/RLB reduction), Will built the IPEX-side control mechanism — warrant gate (giver W+1 BL >3.0d), per-network sub-caps, and daily glidepath tracking — and ran the cross-network coordination that landed ICT under the 520-trailer weekly cap.

**Why strong:** L7/L8-visible network-$ commitment; Will converted a top-down cap into an operating mechanism spanning Linehaul/ATS, NAST, USNS/NS team, S&OP, and IXD; concrete outcome (WK24 landed ~500 vs 520 with cap allocator live). Note: currently in v3 Readiness dir-1 — this is a PROMOTE-to-full-example candidate, evidence base already partially in `evidence/gaps_closed_2026-06-29.md` GAP 2.

**Citations:**
- Email: "Linehaul Load Reduction- Transfer Redirect/Missort" — Matthew Freza, 2026-06-05: "FYI on ask to reduce AZNG/RLB redirects through Prime… can we identify non-critical IXD/USNS redirects to hit these caps? Will need to leverage 3P, upstream PO flips, upstream origin NTI flips, and labor solves." (6/12 continuation includes Ricky Gannon/ATS, Siddharth Krishnan/NAST.)
- Slack DM to Matt Freza (D07T7MM7Z3K), ts 1781027806.481359, 2026-06-09: "Just a heads up how we're tracking the redirect reduction ask: ICT IXD+USNS redirected trailers: 147 WTD vs. 520 (Udit-committed cap) executed… Will flag risk to IXD/USNS stakeholders if we are trending to miss goal of <520 trailers executed per week."
- Slack mpdm USNS group (C0B9RU52RGU), ts 1781110319.839059, 2026-06-10 — the cross-network negotiation: "We're at 272 trailers executed WTD vs. our 520 weekly cap and projected to ~560 by Saturday without adjustment. On the IXD side we're rejecting all downstream moves unless gridlocked / site closure and only approving additional redirects if giver W+1 BL stays elevated >3.0d… USNS needs to stay under ~369 to land under cap."
- Slack #ixd-sop-ipex-lts-team (C09HVUEJYFP), ts 1781112182.827379, 2026-06-10: "current week across all networks we're at 47% to our trailer cap at 246 trailers redirected, based on current open SIMs on track to breach 520 total (committed cap) by EOW."
- Slack C0B9RU52RGU, ts 1781482742.532609, 2026-06-15 — mechanism productized: ":white_check_mark: Trailer Cap — WK24 EOD status… WTD executed: 0/520 TL (0%) · headroom 520… (Will covering Colton on AZNG cap)."
- Slack C0B9RU52RGU, ts 1781365349.088809, 2026-06-13 — automated alerting live (found in 7/14 verify pass): ":no_entry: Trailer Cap Risk — WK24 (auto-alert, Sat 8:41AM AZ) WTD executed: 422/520 TL (81%) · headroom 98… Projection caps each lane by what's both redirectable on-floor at the giver (CARP/NVF vs TRANSSHIP/NTI) AND executable in the days remaining — not raw asks." (companion test post ts 1781293713.998559, 6/12: "The cc line, hourly breach-alert, and 4:47pm EOD post are now live for WK24.")
- Slack mpdm-aricordo--darelb--mightd--mariogon--jesasaki--malaura (C0B9P3L7Y66), ts 1781119711.612179, 2026-06-10 — Will correcting the org-wide framing: "IPEX redirect capacity is currently capped at 520 trailers per week across all IXD & USNS. We have ARS unconstrained due to need for downstream customer facing solves."
- Local: `initiatives.md` Redirect Reduction entry — "WK24 verified: NS 278/rIXD 86/AMXL 17/nIXD 6, ARS 113 unconstrained → 500≤520"; `sim_auditor/cap_allocator.py`.

---

### #4 — Vegas TOFC intermodal redirect program (LAS1/VGT2 → BNSF rail, Q2 2026)

**One-line:** Will stood up and ran the Q2 trailer-on-flat-car redirect program as IPEX point — defining the 3-step IPEX/AZIM/site execution process, coordinating AZIM + ATS + BNSF + Procurement + site ops, and proposing the cheaper nIXD-direct-to-ramp variant ($2.6K vs $4.3K vs $6.6K OTR per trailer).

**Why strong:** Includes an external railroad (BNSF) and Amazon Procurement alongside AZIM/ATS/site ops; Will owned the process definition, tracker of record, and the cost-innovation proposal (nIXD-direct), with an escalation path he managed through Matt. Outcome: Feb run ~71 trailers across 4 days (GUIDE tier); Q2 run executing (e.g., 6/1 approvals of LAS1→MDW2 floors via TOFC). Overlap caution: the per-trailer cost teardown already appears in v3 Readiness (LAS1 TOFC) and Ex4/OB-NTI branch — use as a program example only if OB NTI stays cut.

**Citations:**
- Slack #vegas-tofc-redirects-q2-2026 (C0AVAR06T4H), ts 1778598356.292739, 2026-05-12 — process authorship: "this is the new channel where we are coordinating the TOFC moves. The current process is: 1. We provide redirectable VRIDs, trailers, and new destination on the pinned sharepoint tracker 2. AZIM helps us create the redirect run structures and new VRIDs for each of the transportation legs 3. we attach the trailer to the first leg VRID and flip the manifest to the new destination on the last leg VRID." (full verbatim, re-pulled 7/14)
- Slack same channel, ts 1778865260.675919, 2026-05-15 — cross-org push: "Could I get an answer this morning on AZIMs ability to support a process change for this TOFC lever… We're looking to move away from entirely TOFC moves from LAS1/VGT2 and instead sending the freight from the nIXDs before it lands in vegas."
- Slack #nti-ob-flips-nixd2rixd-ib (C097KRGDJRF), ts 1778772452.785799, 2026-05-14 — the variant proposal: "Wondering if we could try a new process using TOFC (aka trailer rail ramp redirects) to save some money on the LAS1/VGT2 flips."
- Slack DM to Matt Freza (D07T7MM7Z3K), ts 1778865327.936429, 2026-05-15: "I followed up with a quantified ask to the AZIM team and will escalate if no answer in a couple hrs here (re: nIXD OB Flips -> TOFC proposal)."
- Slack mpdm-zhouzw--sravangt--mariogon (C0ANZDWGPL4), ts 1780331254.374749, 2026-06-01: "I'm approving LAS1->MDW2 floors this week through TOFC."
- Slack DM (D0A4Y0NUH6F), ts 1777051790.073009, 2026-04-24 — program start WK17: "help me vet redirectable 1P TL TI FL trailers at LAS1 and provide them in this excel sheet: LAS1 TOFC Redirects WK17. Need 15 total today."
- Local: `las1_tofc_q2/CLAUDE.md` — working group (William Zhou IPEX point; Lex Swaim AZIM; Brian McMillan BNSF; Procurement Varun/Aditya/Protsahan), Feb 2026 first run "~71 trailers across 4 days", cost table $4.3K/$2.6K/$6.6K.

---

### #5 (weak / forward-only) — HUBG/PGLI rate-matrix expansion

**Status: NOT FOUND for program execution.** `3p_rate_matrices/CLAUDE.md` (last review 2026-04-22): "Not started — awaiting kickoff. Tracker is a stub." Goals only (eliminate 95%+ manual rate requests; 200→<50 hrs/yr, due Q3 2026). Only email artifact is "HUBG Ramp Redirect Rates" — Paul Kaye, 2025-04-23 ("We're exploring redirect options with HUBG out of SCK8… This rate for SJC7 is pretty egregious"), which Will did not author. Keep in Readiness as forward scope; do NOT present as a delivered program.

## Honorable mentions (not program-level or not Will's authorship)
- **3P IM operational redirect execution** (#3p-intermodal-redirects-, C0BBDTAGZBN — e.g., ts 1781809249.682709, 2026-06-18: "PSP3->LAX9… 8 IM Drop_PL loads pre-PSP3 receipt at the LA ramps (BNSF San Bernardino / UP LATC) — HJBI 5 + PGLI 3, ~34K") — strong ops evidence but reads as an extension of covered Ex1/AZIM material.
- **UPS small-parcel terminal divert** — Will codifying the lever for SCE partners (mpdm C0BH11M6PGA, ts 1784052740.626749, 2026-07-14: "Existing lever we do is to divert at the UPS terminal before delivery — not yard-to-yard"), anchored on SOP policy.a2z.com/docs/622587 — knowledge codification, not a Will-authored program.
- **BJC1 rIXD launch redirect unblocking** (#bjc1-freight-planning C0AUCTJCC66, ts 1780961773.496719, 2026-06-08) — launch support incident, subsumed by the RDC example.

## Caveats for doc use
1. AFE 618K/165K unit totals are GUIDE-tier (initiatives.md) — verify against live IXD Redirect Tracker before shipping numbers.
2. RDC execution record = 1 test load (9,524 units) as of 7/14 — frame as "stood up the mechanism for the first RDC launch," not as scaled volume.
3. Trailer-cap example must keep the "Will built the threshold, did NOT set the cap" framing (canonical ledger, Readiness dir-1 row); AZNG account figures are Hartland/Udit directive context, not Will's.
4. Peer-bleed check: Gerline (AFE Sales), Stuti Biy. (RDC), Lex Swaim (AZIM) are partner-org names — external-partner naming OK per rules, but scrub L6+ Amazon names from promo prose.
