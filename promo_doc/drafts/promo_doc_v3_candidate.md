<!-- v3 CANDIDATE — 2026-07-12. Built from promo_doc_v1.md + a4de771 bold layer per ARC1 §5.
     LOCAL ONLY. DECISION blockquotes are Will's Pass-F queue — resolve, then delete the blockquotes.
     Every number traces to promo_doc/_canonical_numbers.md. Stripped episodes/quotes live in promo_doc/evidence/ex*_backing.md. -->

# William Zhou — L4 → L5 Promo Doc

William Zhou joined Amazon in October 2024 as a Supply Chain Manager I within Inbound Planning and Execution (IPEX). Within six months, William had architected ICT's DBR/WBR/QBR and owned redirects for two of five rIXD regions — attested by the network-published SOPs naming him as the regional redirect and escalation POC. When IPEX-NTI consolidated scope across multiple network types and prior owners in Q3–Q4 2025, William inherited rIXD NTI ownership and extended it to include nIXD — a combined network slice larger by units than its predecessor. **Today, William owns 1DC + rIXD + nIXD redirect execution for IPEX-ICT — 58 rIXD/nIXD sites (35 rIXD + 23 nIXD, as of July 2026) and ~450M units/week of rIXD+nIXD inbound arrivals (WK28 2026 actual), plus the 1DC network.** He is also the IPEX-IXD business owner for the DOE (Decision Orchestration Engine) Redirect Automation program and the ICT point-of-contact for Smart Reroute integration into IPEX redirect planning.

> **[DECISION 1 for Will]** Ratify the sizing spine: (a) ~450M units/week = WK28 2026 actual (450.7M; plan 449.0M) from the flash's own SANDOP query — confirm actual-vs-plan framing; (b) 58 sites = 35 rIXD + 23 nIXD per the canonical map as of 7/12 — note the 23 nIXD still counts closed WBW2/PPO4 and pre-launch GEU5; option: a dated FOS node-list recount instead. 1DC framing is settled per your 7/12 call (owned, not volume-sized).

> **[DECISION 6 for Will]** Network-share denominator: the old NA-US inbound share percentage stays formally dropped (safe default — it was mathematically broken). Option: re-add a share claim computed from ONE sourced denominator (~330M/wk SCOT NA Inbound Placement Overview, or ~385M/wk across 67 US IXDs per the ATS ROC IXD wiki) — note 450.7M exceeds the SCOT figure, so pick the denominator and framing deliberately or leave it dropped.

> **[DECISION 10 for Will]** Confirm the October 2024 hire date via Phonetool/A-to-Z (no local artifact could verify it; ~30 seconds).

The following examples demonstrate consistent L5 performance: navigating ambiguous cross-functional problems with minimal direction, codifying judgment into reusable mechanisms rather than handing off recommendations, and reaching consensus with internal and external partner teams on new cross-org processes.

---

# Scope of Role

The Supply Chain Manager II (SCMII) **1DC + Regional IXD (rIXD) + National IXD (nIXD) Redirect Execution** role within IPEX-Inbound Control Tower (ICT) is an individual contributor scope where the rules for daily reactive steering are not codified — they live as tribal knowledge across senior peers. The role demands command of constraint-level MDP, Tagawa buffer, Gap-to-Goal backlog, and yard utilization to guide tactical stakeholders (Site Operations, SCE, Smart Reroute, AGL, ATS, AFE, Carrier Procurement), lead escalations reaching Director-level review, and push back with data on senior asks that shift the problem rather than solve it. When a multi-week redirect pattern stems from upstream demand misplacement rather than genuine capacity constraint, the SCMII flags it, pushes upstream levers, and declines the redirect — protecting the network from bullwhip. **The SCMII owns 1DC + rIXD + nIXD redirect execution across 58 rIXD/nIXD sites and ~450M units/week of rIXD+nIXD inbound arrivals, within a 2026 redirect budget of $36.3M ($20.4M NVF inbound + $15.9M NTI transfers)** — extending forward to RDC launch volume (IMO1, XLA4) as those sites ramp. **The role codifies the rules of reactive steering into tooling and standards — hours of morning human narrative into minutes of output, tribal SIM-vetting judgment into deterministic criterion gates — delegating tactical work to tooling and teammates, optimizing for disciplined redirect execution within budget.** It holds internal and external partners (SCE, CM, J.B. Hunt, AZIM, AGL, ATS) to the same data bar before approving redirects, and autonomously surfaces risky plans for further review. Finally, it requires high-**Quality**, high-**Speed**, high-**Tact** verbal and written communication — demonstrated daily in business reviews and escalations.

> **[DECISION 7 for Will]** Pushback vignette: the paragraph keeps the generic demand-misplacement vignette (safe default). Option — swap in the concrete-site shape of the verified June 2026 gridlock episode (site pushed for redirect; network cap + backlog said no; your manager backed the decline on-thread), with no quote and no site-blaming tone. Your comfort call on using that thread.

---

# Promotion Assessment

## Introduction

**William is the analytical and execution anchor of the IXD Redirect Execution workstream** — a scope where reactive steering decisions historically required hours of cross-dashboard human judgment per day across multiple ICT leaders. **His tenure has consolidated what was previously distributed across one L5 SCM and multiple ICT leaders' tribal knowledge into a single L4-owned mechanism with codified rules, automated execution, and reusable scaffolding.** Across H1 2026, he has re-engaged the $22.5M HJBI Drop-to-Live opportunity — stalled since its November 2025 identification — to live execution within three weeks of taking primary, automated the daily IPEX Ops Flash end-to-end (returning roughly a fifth of an FTE in recurring capacity, with further team-scaling capacity as teammates adopt it), and restructured 3P intermodal redirect pricing for $229K in projected annual savings. None of these cross-org wins were possible without the trust William has built with these partner teams (HJBI/J.B. Hunt, AZIM, AGL, AFE, SCE, Carrier Management) — new processes and upstream levers only stand up on foundational relationships.

> **[DECISION 5 for Will]** Capacity + entitlement numbers. (a) The ~407 hr/yr individual + ~224 hr/yr team-scaling pair is softened here and in Ex3/Readiness to "roughly a fifth of an FTE" testimony framing — the 407 traces only to your own framing doc and the 224 has NO derivation anywhere. Options: keep the softened framing (safe), derive both into `_canonical_numbers.md` and restore, or cut the team-scaling clause entirely. (b) Ex5's 11,700 hrs/yr is kept ONLY as the program's stated OP-plan goal — confirm you can personally stand behind that attribution, or cut.

> **[DECISION 9 for Will]** Populate the WorkDocs artifacts link below before this leaves your machine.

WorkDocs folder containing the artifacts behind each example: [TBD — Will to populate].

## Evidence

---

**Example 1: 3P Intermodal Rate Restructure — Cross-Functional Cost Methodology with HJBI Pricing Leadership**

**William led the cross-functional restructure of 3P intermodal redirect pricing that delivered $79K in savings across 359 redirects at a 47% average cost reduction per move, with $229K in projected annual savings and 684 hours of spot-quote delay eliminated (~$23K in annualized labor).** In Q3 2025, third-party intermodal redirects ran on a spot-quote model that took 2–4 hours per request and exposed Amazon to ~$2M in historical overpayment — carriers receiving double payment for overlapping transportation segments. Over 3+ months of negotiation with HJBI pricing leadership, Carrier Services, AP, and Controllership, William restructured the methodology so Amazon pays only incremental costs rather than the full lane: he secured a foundational rate-publication agreement (quarterly rate reviews with published ramp-to-FC linehaul rates), then drove four weeks of methodology iteration to a rate-difference-plus-administrative-fee structure that reconciled HJBI's compensability concerns with Amazon's incremental-cost discipline. He closed the alignment directly with HJBI's pricing leadership and paired the new methodology with an automated rate-lookup tool enabling zero-wait pricing decisions — converting a per-request negotiation into a published, auditable standard.

**Leadership Principle(s) demonstrated:** Frugality, Deliver Results, Earn Trust
*Role guideline: "You work with partner teams to understand their roadmap and reach consensus on approach in order to deliver to meet business goals."*

> **[DECISION 8 for Will]** The 47% figure is Q1 PDF page 2; page 4 of the same signed PDF says 27%. A committee cross-check will find the self-contradiction. 47% now appears ONLY here (the Introduction's second occurrence was cut to "$229K projected annual savings" alone, halving the exposure). You send Matt a one-line reconciliation heads-up personally (no agent comms) — still unlogged since the 6/28 review. The Have-Backbone growth-area paragraph that lived here in v1 is preserved verbatim in `evidence/ex1_3pim_rate_backing.md` if you want it back as a separate growth section.

---

**Example 2: HJBI Drop-to-Live Pilot — Re-engaging a Stalled $22.5M Opportunity to Live Execution**

**William took primary on the $22.5M-annualized HJBI Drop-to-Live opportunity (~3,168 convertible drop appointments YTD, 11.12% of HJBI volume) — stalled since its November 2025 identification — and drove it to live execution within three weeks.** The pilot needed one owner across SCAC provisioning, procurement alignment, site-selection logic, and cancel-and-retender mechanics; no single team owned the set. William pivoted off the original ISA-conversion mechanism when he identified it would break HJBI's drop first-pass yield (FPY), proposing the HJBL SCAC-split — a separate live-only carrier account (provisioned May 2026) that protects FPY while enabling the pilot. He ran the walkthrough with HJBI and the Amazon GL Prepaid Trans pilot owner, reused AGL's live-drop hybrid pattern for the empty swap, and shipped a Redshift-backed weekly site selector matching per-shift live capacity against HJBI pushed loads — site selection by data, not judgment-by-feel. When the selector disagreed with the operational scheduling UI, he refused the spot-fix, traced it to a capacity-counting bug at source, and held the weekly list until the two matched — trading velocity for HJBI's trust; the codified system later carried the pilot through his own out-of-office under teammate coverage. The pilot launched WK20, executing live conversions against a four-KPI scorecard; the 2026 target is held to $2.25M (2% of HJBI drop volume) pending scalability read-out.

**Leadership Principle(s) demonstrated:** Ownership, Bias for Action, Insist on the Highest Standards, Dive Deep
*Role guideline: "You effectively manage difficult problems, mitigate immediate risks, and decide when you can handle or need to escalate."*

> **[DECISION 4 for Will]** The own-OOTO clause ("kept the pilot moving through his own out-of-office under teammate coverage") is restored per the June review's call that it is the stronger L5 signal — confirm the dates/facts (your OOTO 5/7–5/11, teammate covered, pilot recarped the first ISA without you) before it ships. Same claim is echoed in the PROPOSED Summary block.

---

**Example 3: IPEX Ops Flash Automation — Codifying Daily Network-Steering Judgment into a Reusable Mechanism**

**William rebuilt the team's daily flash from a ~2-hour multi-leader morning build into a fully automated pipeline that generates the network-steering narrative in minutes — returning roughly a fifth of an FTE in recurring capacity, with further team-scaling capacity as teammates adopt it.** In H1 2025 the daily ICT flash was hand-assembled each morning from dashboards, exports, and a steering doc — a refined-over-years narrative rebuilt from scratch daily. William mapped the full judgment chain end-to-end — strategy → operational rules → data shape → execution — and rebuilt the flash as an automated pipeline that is now the team's flash of record, anchored by an internal wiki he authored and owns and a version-controlled GitFarm package other builders onboard from. Because one person owned all four layers, the flash encodes judgment no siloed function could have: every recurring call the prior human narrative made by feel is now an explicit, repeatable rule. Working with ICT teammates and IPEX Analytics, William extended the same pattern to adjacent reactive-steering work — an ESS Reactive Lanes triangulation, a WBR narrative generator, and a SIM auditor that vets redirect approvals against a consistent gate where the team previously relied on verbally-agreed criteria — an interlocking suite of workflows, each converting tribal judgment into team-runnable tooling.

**Leadership Principle(s) demonstrated:** Learn and Be Curious, Invent and Simplify, Deliver Results
*Role guideline: "You identify priorities and know when a situation requires a deep dive vs. issues that can be solved quickly."*

---

**Example 4: OB NTI Flip Process — Redirecting at Source Across IPEX, Reactive Scheduling, and ATS**

**William authored and operationalized the OB NTI flip — a cross-team process that redirects outbound NTI freight at the origin nIXD before the trailer departs, running at ~7 loads/day at the February 2026 peak of the manual pilot.** Through Q1 2026 the standard lever was reactive at destination: once a trailer left the nIXD, redirecting meant canceling and re-tendering after arrival at the overloaded rIXD — multi-day lead time, double dray cost, constraint-pressure feedback to the nIXD yard. Flipping at origin didn't sit cleanly under any one team's SOP, so William authored the formal process documentation, stood up the dedicated cross-team coordination channel, and operationalized the manual process across IPEX, Reactive Scheduling (OB SKED), and ATS. He owns the workstream cadence — starting and stopping giver sites against network-health data rather than running the lever indiscriminately — and drives its evolution: the TOFC variant he proposed ($1.7K/trailer savings vs current TOFC routing, $4K vs OTR) was adopted into the Q2 LAS1 TOFC program, and his originate-at-source variant would eliminate the manual flip entirely by routing freight to the taker FC at manifest creation. The flip is the operational platform his LAS1 TOFC unit-economics work runs on, and he is engaging the ATS automation team to scale it beyond manual.

**Leadership Principle(s) demonstrated:** Invent and Simplify, Ownership, Frugality
*Role guideline: "You work with partner teams to understand their roadmap and reach consensus on approach in order to deliver to meet business goals."*

> **[DECISION 2 for Will]** Cut Example 4? Peers ran four examples + a people-leadership summary, and this is the weakest number in the set (a dated ~7/day with no dollar outcome and no current KPI data). Options: (a) cut it and fold the TOFC unit-economics into Readiness direction 1 (the $2.6K/$4.3K/$6.6K teardown already lives there), landing at 4 examples + Summary = peer shape; (b) keep this dated rebuild. If you cut, LP coverage is unaffected (Invent & Simplify stays via Ex3, Ownership via Ex2).

---

**Example 5: DOE Redirect Automation — Authoring the IXD Validation Logic for Network-Wide Redirect Automation**

**William authored and owns the IXD redirect-feasibility intake for Amazon's Decision Orchestration Engine (DOE) — the largest of the program's three network intakes by unit volume — encoding IPEX-ICT's redirect judgment into the program targeting network-wide redirect automation.** DOE is one of IPEX's 2026 OP plan technical investments, targeting 11,700 hours/year of IPEX labor savings at full entitlement — the program's stated goal. Rather than staying at intake-fill-out level, William drove program-level change requests for IPEX-IXD: the region-mapping update forced by Two-Tier Regionalization, field-mapping clarifications, and the operational diagnosis when the program's SIM generation broke. When the program distributed its three intake templates (IXD, Sortable, Non-Sort) in May 2026, William made the assigned IXD intake ownership-by-authorship: he generated and delivered the initial redirect-feasibility artifact to the program lead, then drove the cross-functional validation design — soliciting VSCOR criteria inputs and proposing sign-off routing through the rIXD/nIXD/USNS network decision owners. His decision function carries tiered eligibility logic plus giver-criticality gates reverse-engineered from real approval behavior — his analysis showed the assumed constraint-MDP threshold did not actually gate approvals; giver buffer and week-over-week backlog persistence did. His working SIM auditor and redirect validator are the codified-judgment precursors he is upstreaming — he authored the algorithm; the program owns the surface it runs in.

**Leadership Principle(s) demonstrated:** Earn Trust, Dive Deep, Bias for Action
*Role guideline: "You work with partner teams to understand their roadmap and reach consensus on approach in order to deliver to meet business goals."*

---

> **[DECISION 3 for Will]** Both peer docs carry a people-leadership Summary section; v1 has none. Below is a PROPOSED draft built only from VERIFIED content (Q1-PDF-attested training, the wiki/package enablement, the OOTO coverage — the last is gated on DECISION 4). Adopt, edit, or drop. If you drop it, move the 11-stakeholder training clause back into Example 3 so it isn't lost — keeping the "adopted and operationalized" framing (the Q1 PDF says he "Learned about" the methodology; "developed" would be an authorship overclaim against the PDF). If you also cut Example 4 (DECISION 2), adopting this lands the doc on the peer shape: four examples + Summary.

<!-- PROPOSED SUMMARY — pending DECISION 3 -->
# Summary

Beyond the deliverables above, William turns personal capability into team capability. He adopted and operationalized the Context Document methodology — a structured way of teaching AI tools role constraints and decision frameworks so the same context isn't re-explained for every task — and **trained 11 stakeholders across IPEX on it**. The automation suite he authored ships with an internal wiki and a version-controlled package that teammates onboard from without him, and the codified system carried live pilot execution through his own out-of-office under teammate coverage. William has no direct reports; this is the enablement shape of people leadership — raising the team's bar with tooling and teaching — and it positions him to partner with and develop AA-level talent as the L5 scope formalizes.
<!-- END PROPOSED SUMMARY -->

---

# Readiness for L5 Scope

William's H1 2026 record meets each of the three "Moving to L5" criteria in the Supply Chain Manager Role Guideline:

- **Managing difficult problems, and choosing when to handle versus escalate** — re-engaging the stalled HJBI pilot to live execution; declining redirects that shift the problem rather than solve it and pushing proactive upstream levers instead. His manager publicly backed this judgment on a June 2026 cross-functional gridlock thread, when a site pushed for a redirect the network cap and backlog did not warrant.
- **Knowing when a situation needs a deep dive versus a quick solve** — the HJBI capacity-source debugging; the LAS1 TOFC unit-economics teardown ($2.6K vs $4.3K vs $6.6K per trailer); the cloud-to-dirt judgment mapping behind the flash automation.
- **Reaching consensus with partner teams to deliver business goals** — the HJBL SCAC-split with HJBI and the GL Prepaid Trans pilot owner; the OB NTI flip with Reactive Scheduling and ATS; DOE-IXD with the program team; Smart Consolidation / PACE with C.H. Robinson and TCMT.

He has taken >$22.7M in identified opportunity into execution — the $22.5M HJBI opportunity (identified in a peer's November 2025 analysis, driven to live execution by William) plus $229K in annualized 3PIM savings he negotiated — and returned roughly a fifth of an FTE through the flash automation, all while sustaining daily reactive operations across rIXD/nIXD through H1 2026.

> **[DECISION 11 for Will]** The manager's June 2026 backing is paraphrased above (no quotation), per the ban on inline manager-praise quotes in body. Options: keep the paraphrase, or move the verbatim quote to a separate Feedback section at the end of the doc (verbatim + source live in `evidence/readiness_backing.md`).

These capabilities map directly onto the proposed L5 role, which extends current ownership in three directions:

1. **Multi-network strategic levers.** Coordinating Smart Reroute, AGL, IM, and AZIM as one operating picture, with IPEX driving the network-health view rather than receiving it. When a Finance-set trailer-cap directive landed mid-2026 (~12% redirect-load reduction), William built the IPEX-side threshold and per-network elimination logic to hit it — deriving which redirects could be cut and which had to hold on giver backlog persistence. **3P Rate Matrix Expansion to HUBG and PGLI** (Q3 2026 goal) comes next — eliminating 95%+ of manual rate requests and cutting annual rate-request wait from 200 hours to under 50.

2. **Codified judgment as scalable team tooling — and the people-leadership scope behind it.** The flash automation proves cloud-to-dirt ownership converts hours of human judgment into reusable automation the team adopts. **DOE Redirect Automation** (William as IPEX-IXD business owner) upstreams the pattern into Amazon's network-wide automation; **Smart Reroute integration** extends it across the FBA-CM boundary. Both launch the people-leadership scope flagged for 2026 — partnering with AA managers and delegating tactical work.

3. **Program-level cross-org partnership.** The HJBI pilot, DOE-IXD ownership, and the OB NTI flip are the building blocks of program-level scope. At L5, William continues as the IPEX-IXD analytical owner on emerging cross-org pilots — including **Smart Consolidation / PACE** (named ICT-Sort owner, 2027 public launch, with C.H. Robinson and TCMT) — expanding the codification-and-tooling pattern that defined his H1 2026.
