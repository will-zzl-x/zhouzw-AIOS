William Zhou — L4 → L5 Promo Doc (Working Draft v1)

Drafted: 2026-05-19. Owner: William Zhou. Target: L5 SCMII within IPEX-ICT, Q3-Q4 2026.

Structure: Shelby/Niko hybrid — career-arc opener (Shelby pattern) + standalone Scope of Role (Niko pattern) + Promotion Assessment intro + 5 Examples + Readiness for L5 Scope closing.


---

William Zhou joined Amazon in October 2024 as a Supply Chain Manager I within Inbound Planning and Execution (IPEX). Within six months, William had architected ICT's DBR/WBR/QBR and owned redirects for two of five rIXD regions. When IPEX-NTI consolidated scope across multiple network types and prior owners in Q3–Q4 2025, William inherited rIXD NTI ownership and extended it to include nIXD — a combined network slice larger by units than its predecessor. Today, William owns rIXD + nIXD redirect execution for IPEX-ICT — 57 sites (34 rIXD + 23 nIXD) and ~302M units/week of inbound arrivals. He is also the IPEX-IXD business owner for the DOE (Decision Orchestration Engine) Redirect Automation program and the ICT point-of-contact for Smart Reroute integration into IPEX redirect planning.

The following examples demonstrate consistent L5 performance: handling ambiguous cross-functional problems with limited guidance, codifying judgment into reusable mechanisms rather than handing off recommendations, and reaching consensus with internal and external partner teams on new cross-org processes.


---


# Scope of Role

The Supply Chain Manager II (SCMII) Regional IXD (rIXD) + National IXD (nIXD) Redirect Execution role within IPEX-Inbound Control Tower (ICT) is an individual contributor scope where the rules and mechanics for daily reactive steering are not codified — they live as tribal knowledge across senior peers and require judgment to apply consistently. The role demands exceptional understanding of the IXD supply chain across constraint-level MDP, Tagawa buffer, Gap-to-Goal backlog, and yard utilization to guide tactical stakeholders (Site Operations, SCE, Smart Reroute, AGL, ATS, AFE, Carrier Procurement), lead cross-functional escalations up to three levels above their own, and push back with data on senior asks that risk shifting the problem rather than solving it. For example, when a multi-week redirect pattern emerges from upstream demand misplacement rather than a genuine capacity constraint, the SCMII flags the incongruency, pushes for proactive levers upstream, and declines the redirect — not just executing the ask but protecting the network from bullwhip. The SCMII owns rIXD + nIXD redirect execution across 57 sites (34 rIXD + 23 nIXD) and ~302M units/week of inbound arrivals, within a 2026 redirect budget of $36.3M ($20.4M NVF inbound + $15.9M NTI transfers). Given the breadth, the role codifies the rules governing reactive steering into tooling and standards — converting hours of morning human narrative into minutes of automated output, and tribal SIM-vetting judgment into deterministic criterion gates — and delegates tactical work to tooling and teammates. It holds internal and external partners (SCE, CM, J.B. Hunt, AZIM, AGL, ATS) to the same data bar before approving redirects or scope changes, and flags autonomously when a proposed plan appears risky. Finally, it requires high-Quality, high-Speed, high-Tact verbal and written communication — demonstrated daily in business reviews and director-level escalations.


---


# Promotion Assessment


## Introduction

William is the analytical and execution anchor of the IXD Redirect Execution workstream — a scope where reactive steering decisions historically required hours of cross-dashboard human judgment per day across multiple ICT leaders. His tenure has consolidated what was previously distributed across one L5 SCM and multiple ICT leaders' tribal knowledge into a singular L4-SCM-owned mechanism with codified rules, automated execution, and reusable scaffolding. Across H1 2026, he has re-engaged a 4-month-stalled $22.5M opportunity (HJBI Drop-to-Live Pilot) to live execution within three weeks of taking primary, automated the daily IPEX Ops Flash end-to-end — returning ~407 hours/year of individual capacity and ~224 hours/year of team-scaling capacity — and driven a YoY -$4M structural cost reduction in 3P intermodal redirect spend through rate methodology redesign. Not to be dismissed is William's ability to earn trust with the cross-org partners he engages (HJBI/J.B. Hunt, AZIM, AGL, AFE, SCE, Carrier Management) — establishing new processes and influencing upstream lever utilization is not possible without foundational relationships.

A WorkDocs link to artifacts referenced in the following examples is provided here: [TBD — Will to populate].


## Evidence


---

Example 1: 3P Intermodal Rate Restructure — Cross-Functional Cost Methodology with HJBI Pricing Leadership

In Q3 2025, third-party intermodal redirects ran on a spot-quote model that took 2-4 hours per request and exposed Amazon to ~$2M in historical overpayment — carriers receiving double payment for overlapping transportation segments. William led 3+ months of cross-functional negotiation with HJBI pricing leadership, Carrier Services, AP, and Controllership to restructure the rate methodology so Amazon paid only incremental costs rather than the full lane. The arc started 7/21/2025 with a foundational rate-publication agreement between William, HJBI's Intermodal Pricing Sr Director, and an Amazon SCM Intermodal Program Manager — quarterly rate reviews with published ramp-to-FC linehaul rates — and progressed through six weeks of methodology iteration to a rate-difference-plus-administrative-fee structure that reconciled HJBI's compensability concerns with Amazon's incremental-cost discipline. *William closed alignment with HJBI pricing leadership on 8/18/2025: "We are aligned @ $150 + fsc William! Thank you."* Manager- and finance-attested outcome in William's Q1 2026 Annual Review: $79K saved across 359 redirects, 47% average cost reduction per move, $229K projected annual savings, and 684 hours of spot-quote delays eliminated** ($23K annualized labor savings) via an automated rate-lookup tool enabling zero-wait pricing decisions.

This example also surfaces William's primary growth opportunity — a Have-Backbone gap named in his Q1 review and actively in remediation: in the August 2025 admin-fee discussion he accepted the $150 additive within three days rather than escalating at decision time. The fix is to use earned credibility to push back in the moment, especially with cross-org partners where his data position carries more weight than he has been using.

Leadership Principle(s) demonstrated: Frugality, Have Backbone (Disagree and Commit), Deliver Results, Earn Trust


---

Example 2: HJBI Drop-to-Live Pilot — Re-engaging a 4-Month-Stalled $22.5M Opportunity to Live Execution

In April 2026, the HJBI Drop-to-Live opportunity sized at $22.5M annualized (~3,168 convertible drop appointments YTD, 11.12% of HJBI volume, identified November 2025) had been sitting for four months. The original January 2026 launch had slipped, and the pilot needed a single owner across SCAC provisioning, HJBI procurement alignment, site selection logic, and cancel-and-retender mechanics — none of which sat cleanly under any one team. William took primary, replied to HJBI's pilot lead within 24 hours with substantive answers to all four of his concerns plus the pricing/EDI question, and pivoted the pilot mechanism off the original ISA-conversion approach when he identified that rescheduling existing ARRIVAL_SCHEDULED appointments would break HJBI's existing drop FPY — proposing instead the HJBL SCAC-split (a separate live-only carrier account) that protects FPY while enabling the pilot. He ran the walkthrough with HJBI and the Amazon GL Prepaid Trans pilot owner, drove SCAC creation to closure (HJBL provisioned 5/1/2026), reused AGL's existing "live-drop hybrid" pattern as the empty-swap solution rather than building one from scratch, and shipped `pilot_site_selection.py` — a Redshift-backed weekly site selector that matches per-shift live capacity against HJBI pushed loads on drop constraints — so the pilot's weekly site list is data-driven rather than judgment-by-feel. The formal pilot launched in WK20 and is executing live conversions against the four-KPI scorecard.

When his candidate-load selector disagreed with the operational SKED UI on slot availability, William refused the spot-fix and traced the discrepancy through three Redshift sources (`sked_constraints_daily`, `ipex.site_scheduled_capacity`, `ground_control_inbound_view_main_page_v2`), found a per-ISA capacity-counting bug, restructured the SQL from correlated subqueries into proper joins, and held the weekly candidate list until the source matched the UI ceiling — trading short-term velocity to keep HJBI's trust intact on the first weekly hand-off. At pilot conclusion, William is drafting a Lessons-Learned doc for scalability, sized to unlock up to $22.5M in annual cost/speed savings if the model holds (conservative 2026 target $2.25M / 2% of HJBI drop volume; KPIs: FPY, Driver Detention cost, NCNS rate, MDP benefit).

Leadership Principle(s) demonstrated: Ownership, Bias for Action, Earn Trust, Insist on the Highest Standards, Dive Deep


---

Example 3: IPEX Ops Flash Automation — Codifying Daily Network-Steering Judgment into a Reusable Mechanism

In H1 2025, the daily ICT flash consumed ~2 hours every morning across multiple ICT leaders, hand-built from 4+ Quicksight dashboards, two Excel exports, and a Quip Steering doc — a refined-over-years human narrative that nonetheless had to be rebuilt from scratch each day. William mapped the full judgment chain end-to-end — strategy → operational rules → SQL/data shape → execution — and rebuilt the flash as an automated, Claude Code-native pipeline. The IPEX Ops Flash (formerly ICT Flash) became fully automated in 2026, replacing 2+ hours of multi-leader morning work with a few minutes of generated output, and is now the team's daily flash of record. It returns ~407 hours/year of individual capacity (~90 minutes/day on the morning narrative, ~20% FTE) with ~224 hours/year of additional team-scaling capacity as other members adopt it. The deeper signal is cloud-to-dirt codification: because one person owned the strategy, the operational rules, the data layer, and the execution, the flash encodes judgment no siloed function could have — every recurring call the prior human narrative made by feel is now an explicit, repeatable rule. Building on the same foundation, William extended the pattern to adjacent reactive-steering work — an ESS Reactive Lanes triangulation (MDP + Tagawa buffer + Gap-to-Goal), a WBR narrative generator, and an in-progress SIM auditor that vets redirect approvals against a consistent gate where the team previously relied on verbally-agreed criteria. This isn't "I used AI" — it's that owning all four layers produced automation no tools-only or SME-only approach would have built.

The foundation is William's 2025 Context Document methodology — a structured way of teaching AI role constraints and decision frameworks so the same context isn't re-explained for every task. William trained 11 stakeholders across IPEX pre-Kiro (attested in his Q1 2026 Annual Review) — turning a personal capability into a transferable team practice.

Leadership Principle(s) demonstrated: Learn and Be Curious, Invent and Simplify, Deliver Results, Bias for Action


---

Example 4: OB NTI Flip Process — IPEX-Reactive Scheduling Manual Redirect at Source

Through Q1 2026, the rIXD network's standard redirect lever was reactive at destination: once an outbound trailer left the nIXD, the redirect happened by canceling and re-tendering once it arrived at the over-loaded rIXD. This created multi-day lead time, double dray cost, and constraint-pressure feedback to the nIXD yard. The opportunity was to flip outbound at the nIXD before the trailer departed — a manual cross-team process between IPEX, Reactive Scheduling (OB SKED), and ATS that didn't sit cleanly under any one team's SOP. William authored the formal process documentation Quip on 2/13/2026, created the dedicated `#nti-ob-flips-nixd2rixd-ib` Slack channel, and operationalized the manual process across IPEX + Reactive Scheduling — the OB SKED team has since run ~7 loads per day at nIXDs away from LAS1.

William owns the workstream cadence, starting and stopping giver sites against network-health data rather than running the lever indiscriminately. He also drives the process forward: proposing the TOFC variant (a $1.7K/trailer reduction vs current TOFC routing, $4K/trailer vs OTR — adopted into the Q2 LAS1 TOFC program) and the originate-at-source variant that eliminates the manual flip entirely by routing freight to the taker FC at manifest creation. The OB NTI flip is the platform on which William's LAS1 TOFC unit-economics work runs — the cross-functional muscle and operational mechanism that let him push AZIM-level structural redirect spend reduction. The ATS automation team is the upstream partner William is engaging to scale this beyond manual; the SIM auditor and CLI redirect validator are the codified-judgment inputs.

Leadership Principle(s) demonstrated: Invent and Simplify, Ownership, Earn Trust, Bias for Action


---

Example 5: DOE Redirect Automation — IPEX-IXD Business Owner for Network-Wide Redirect Validation Logic

Amazon's Decision Orchestration Engine (DOE) is targeting full network redirect automation as one of IPEX's 2026 OP plan technical investments, owned at program level by the DOE program lead. William joined the DOE program channel in September 2025 as the IPEX-IXD business owner — and drove program-level change requests on behalf of IPEX-IXD rather than staying at the validation-intake-fill-out level: surfacing the TX_GL → TX_MT region-mapping update (forced by Amazon's Two-Tier Regionalization) in late January 2026, pushing Insite change-request field-mapping clarifications, and providing the operational diagnosis when SIM-generation broke in October 2025. In May 2026, the DOE program lead formally distributed three intake templates — IXD, Sortable, Non-Sort — and named William as the IXD validation-intake owner, with the Sortable owner named separately. The IXD intake is the largest of the three by unit volume. This is ownership by authorship, not assignment: William generated and delivered the initial IXD redirect-feasibility intake artifact to the program lead, then drove the cross-functional validation design — soliciting VSCOR inputs on the criteria and routing rIXD/nIXD/USNS sign-off through the network decision owners.

The DOE program targets 11,700 hours/year in IPEX labor savings at full entitlement (the program's 2026 OP plan goal). William authored the IXD redirect-feasibility decision function that DOE encodes — the tiered eligibility logic (volume-type / SCAC / account / DROP-vs-LIVE / FC-type) plus the giver-criticality gates reverse-engineered from real approval behavior: constraint-MDP gaps, WK+1 Gap-to-Goal, and giver BL vs regional-mean+σ. This is logic no siloed function could have encoded, because it required owning the operational judgment and the data shape simultaneously. The codified judgment in his SIM auditor (`sim_auditor.py`) and CLI redirect validator (`validate_redirect.py`) is the working precursor to the DOE-validation logic he is upstreaming — he authored the algorithm; the DOE program owns the surface it runs in. That distinction positions William as the program-level translator between IPEX-ICT operational standards and the cross-org engineering team building Amazon's network-wide redirect automation.

Leadership Principle(s) demonstrated: Earn Trust, Bias for Action, Invent and Simplify, Customer Obsession


---


# Readiness for L5 Scope

William has demonstrated consistent L5 performance across the "Moving to L5" criteria in the Supply Chain Manager Role Guideline:

- Managing difficult problems and deciding when to handle or escalate — re-engaging the stalled HJBI Drop-to-Live pilot to live execution; and declining redirect requests that would shift the problem rather than solve it, pushing for proactive upstream levers instead to protect the network from bullwhip. William's manager backed this judgment on-record in a June 2026 cross-functional gridlock thread, framing William as "asking the right questions" when a site pushed for a redirect that the broader network cap and backlog did not warrant.
- Identifying priorities and knowing when situations require deep dives versus quick solutions — HJBI capacity-source debugging across three Redshift sources; LAS1 TOFC unit-economics teardown ($2.6K vs $4.3K vs $6.6K per trailer); the cloud-to-dirt mapping behind the flash automation.
- Working with partner teams to reach consensus on approaches that meet business goals — HJBL SCAC-split with HJBI + the GL Prepaid Trans pilot owner; OB NTI flip with Reactive Scheduling + ATS; DOE-IXD with the DOE program team; Smart Consolidation / PACE with C.H. Robinson + TCMT.
He has shipped >$22.7M in identified opportunity (HJBI $22.5M opportunity + 3PIM Rate Restructure $229K annualized savings), plus the unquantified Smart Consolidation/PACE entry into Amazon's 2027 public-launch product, and returned ~407 hr/year of individual capacity and ~224 hr/year of team-scaling capacity through the flash automation — all while sustaining daily reactive operations across rIXD/nIXD through the entire H1 2026 cycle.

These capabilities directly prepare William for the proposed L5 scope, which extends his current ownership in three forward directions:

1. Multi-network strategic levers. Cross-network coordination across SR, AGL, IM, and AZIM as one operating picture, with IPEX driving the network-health view rather than receiving it. The HJBI pilot, the OB NTI flip platform supporting LAS1 TOFC, and the Smart Reroute integration are all early shapes of this. When a Finance-set network trailer-cap directive landed in mid-2026 (a ~12% redirect-load reduction to free carrier capacity as liquidity tightened), William built the IPEX-side threshold and per-network elimination logic to hit that cap — deriving which redirects were non-critical and could be cut versus which had to hold on giver backlog persistence — rather than rationing indiscriminately or waiting to be told. 3P Rate Matrix Expansion to HUBG and PGLI (Q3 2026 goal, building directly on the 3PIM Rate Restructure Phase 1 win) is the next codification target — eliminating 95%+ of manual rate requests and reducing annual rate-request wait time from 200 hours to <50 hours.

2. Codified judgment as scalable team tooling — and the people-leadership scope behind it. The flash automation proves one person plus cloud-to-dirt ownership can convert hours of human judgment into reusable automation that the broader team adopts. The next horizon is to scale that pattern across the ICT control tower (and broader IPEX) so the team's bar rises with tooling, not headcount. DOE Redirect Automation (William as IPEX-IXD business owner) is the program-level upstreaming of this pattern — encoding rIXD + nIXD redirect-feasibility logic into Amazon's network-wide automation. Smart Reroute integration (William as the IPEX face to the FBA-CM / Smart Reroute / FBA CAMP partner teams) extends the same pattern across an FBA-CM cross-org boundary. Both are the natural launchpad for the people-leadership scope flagged for 2026 — partnering with AA managers and delegating tactical work so William can focus higher.

3. Program-level cross-org partnership. The patterns demonstrated in the examples above (HJBI drop-to-live cross-functional pilot, DOE-program IXD business ownership, OB NTI flip across IPEX + Reactive Scheduling + ATS) are the building blocks of program-level scope. At L5, William will continue serving as the IPEX-IXD analytical owner on emerging cross-org pilots — including Smart Consolidation / PACE (named ICT-Sort owner on Amazon's 2027 public-launch product with C.H. Robinson and TCMT) — while expanding the codification-and-tooling pattern that has defined his H1 2026 work.
