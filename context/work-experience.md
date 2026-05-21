# Work Experience & Skills — Zone of Genius

Last updated: May 20, 2026.

This file is the distilled inventory of Will's transferable capabilities, written for AIOS to use when evaluating business-acquisition fit (Codie Sanchez / Main Street Millionaire framework). Source material: Amazon Q2 2026 Talent Review + L4→L5 promo doc + project artifacts in `C:/Users/zhouzw/ict_automation/`. Internal Amazon names and exact unit/dollar metrics are abstracted where the specific value isn't load-bearing — all numbers below are accurate to within rounding.

## One-paragraph read

Will is an L4 supply-chain operator at Amazon who behaves like a one-person cross-functional program manager: he takes ambiguous, multi-team workstreams that nobody owns, designs the operational mechanism end-to-end (strategy → rules → SQL/data → execution), gets cross-org senior alignment same-day, and ships codified mechanisms rather than handed-off recommendations. He has personally led 3+ months of carrier-pricing renegotiation that returned ~$229K/yr in structural savings and ~47% per-move cost reduction; built a six-workflow GenAI automation suite that returns ~407 hr/yr individual capacity + ~224 hr/yr team-scaling capacity; and re-engaged a 4-month-stalled $22.5M opportunity to live execution within three weeks. His sharpest edge is **cloud-to-dirt** ownership — strategy, ops judgment, data layer, and execution all in one head, plus the financial framing to translate operational asks into structural-spend language senior leaders will move on.

## Transferable capabilities

### 1. Cross-functional negotiation with senior counterparties

- Led 3+ months of rate-methodology negotiation with a national carrier's pricing leadership (Sr Director level), restructuring the rate model so the buyer paid only incremental costs rather than full-lane rates. Outcome: ~$79K savings on ~359 redirects in test period, 47% average per-move cost reduction, ~$229K projected annual savings.
- Routinely secures same-business-day alignment from L7-Director-level senior cross-org partners on multi-team process designs.
- Drives 3+ levels above own pay grade in escalations when the data supports it.

**Acquisition relevance:** vendor pricing renegotiation post-close, supplier consolidation, contract renegotiation with the seller's existing accounts. The carrier-pricing arc maps directly onto post-close vendor terms in any service business with material COGS.

### 2. Building automation that codifies tribal knowledge

- Designed and shipped a six-workflow GenAI suite covering daily ops narrative, reactive-lane triangulation across three data sources, weekly business review, deterministic three-criterion redirect approvals, and a CLI request-validator. All Claude-Code-native, all production.
- Returns ~90 minutes/day on the daily narrative (~407 hr/yr individual, ~20% FTE), ~1 hr/week on approval audit with zero out-of-criteria approvals since launch, and ~224 hr/yr of team-scaling capacity if cloned to peers.
- Stress-tested in production: a teammate ran the full pipeline during Will's OOTO with a 3-word prompt — proves the suite is built to be cloned, not bespoke.
- Methodology: Context Document approach (taught to 11 stakeholders pre-Kiro) — encoding role constraints + decision frameworks so the same context doesn't have to be re-explained every task.

**Acquisition relevance:** post-close ops standardization. Most boring businesses have hours/week of human judgment locked inside the seller's head — Will can extract it into deterministic mechanisms within weeks of taking over. Especially relevant to recurring service businesses (cleaning, landscaping, pest, HVAC, fire-extinguisher inspection) where dispatching, route optimization, and quote-to-invoice are the bottlenecks.

### 3. Financial framing for operational decisions

- Built a 3-scenario unit-economics teardown showing $2.6K (intermodal-redirect) vs $4.3K (current routing) vs $6.6K (over-the-road) per trailer — pushed the structural-spend ask up two org levels rather than accepting the spot quote.
- Architected a 3-tier (DBR / WBR / QBR) business-review metrics framework — 49+ metric lines covering on-time-pickup/delivery, defect categorization, cost tracking — launched on a 6-week timeline, integrated into Analytics with automated daily refresh, served as P0 support for an L7-L8 quarterly business review.
- Routinely converts operational asks into $/year structural framing so senior decisions have a financial anchor.

**Acquisition relevance:** SDE-aware operating decisions, P&L modeling for post-close 90-day plans, build vs buy vs renegotiate trade-offs. The metrics framework muscle is the muscle for building a 13-week cash-flow + KPI dashboard for any acquired business.

### 4. Process design from genuine ambiguity

- Took primary on a 4-month-stalled $22.5M opportunity (originally unowned across SCAC provisioning, procurement alignment, site selection, and cancel-and-retender mechanics) and shipped first pilot load within 3 weeks of taking ownership. Designed the SCAC-split mechanism that protected the carrier's existing fulfillment KPIs while enabling the pilot.
- Authored the formal cross-team OB-NTI flip process Quip + dedicated Slack channel for what was previously verbal coordination. Operationalized so a partner team now executes ~7 redirects/day at given facilities with no further Will involvement.
- Designed a 4-party (procurement, sales, ops, carrier) flip-flop process for ~40 trailers with same-day senior alignment.

**Acquisition relevance:** the first 90 days post-close are pure ambiguity. Will has the muscle for "no one owns this and it's not going to fix itself — I'll write the SOP, name the channel, and run the cadence." This is exactly the muscle Sanchez calls "operator bench depth" but baked into one operator.

### 5. Direct customer/partner trust-building

- Multi-month carrier-pricing relationship with a national 3PL Sr Director — closed alignment in writing on adjusted rate methodology including a $150/move administrative fee + fuel surcharge structure.
- Sustained pilot relationships with a national carrier's GL Prepaid pilot owner + procurement leadership across a 6-week active pilot.
- 11-stakeholder training on the Context Document methodology — solo, no formal charter, on volunteer time. Translated to 2 ad-hoc demos when other internal teams reached out.

**Acquisition relevance:** the seller-handoff conversation, first-90-day customer retention calls, and supplier-trust rebuilding post-close. Will has done the equivalent of "carry an external Sr Director's relationship through a multi-month renegotiation" — that's the same shape as inheriting and renegotiating a seller's top 3 customer contracts.

## Domain knowledge surface area

Already deep:

- Supply chain & inbound logistics — cross-dock operations, redirect execution, network-health diagnostics, capacity matching, lead-time tradeoffs.
- Transportation rate structures — intermodal rail (rate-difference + admin-fee constructs, ramp-to-FC linehaul), TOFC vs OTR economics, fuel surcharge mechanics.
- Carrier procurement & 3PL contract dynamics — published rate review cadences, compensability arguments, EDI-level tendering mechanics.
- Operations data infrastructure — Redshift + DataGrip + Quicksight, root-causing per-row capacity bugs across 3+ source tables, restructuring SQL from correlated subqueries to proper joins.
- AI tooling for operations — Claude Code, Kiro, Context Document methodology, structured prompt caching, deterministic gating logic.
- Business review mechanism design — DBR/WBR/QBR cadence, metric-line ownership, automated refresh integration.

Adjacent / partial coverage:

- B2B service business mechanics (recurring revenue, dispatching, route optimization, quote-to-invoice) — known by analogy to cross-dock + carrier procurement, not yet by direct ownership.
- SBA 7(a) financing mechanics, deal sourcing, LOI / CIM diligence — being built by reading Sanchez + applying frameworks.

Cold zones:

- Direct-response marketing / lead-gen funnels.
- Pricing and offer construction for end customers (Hormozi territory — see `references/hormozi.md`).
- Owner-operator labor compliance (CDL, contractor licenses, payroll/HR mechanics) — explicit hard pass per `context/financial-state.md`.
- E-commerce / Amazon-third-party-seller mechanics (despite working at Amazon — different org, no exposure).

## Operating constraints (load-bearing for AIOS deal eval)

- **Time budget:** 10–15 hr/week combined with Elena, post-close. Semi-absentee model only.
- **Geography:** Phoenix-area until late 2027 (wedding-locked), then Dallas or Chicago. Acquisition must be remote-friendly OR have manager-in-place pre-move OR be sellable.
- **Capital:** $70K cash + SBA 7(a) preferred + open to seller financing. Target acquisition $200K–$500K, target SDE $80K–$200K/yr.
- **License auto-disqualifiers:** any business requiring Will personally to hold CDL, contractor's license, etc.
- **Customer concentration:** any business with >30% revenue from a single customer.
- **Capacity-of-attention boundary:** Q3–Q4 2026 = Amazon promo window. Acquisition activity through that window must not visibly compromise day-job behaviors that get him promoted. Post-promo (Q1 2027 onward) bandwidth opens significantly.

## Where Will is genuinely strong vs. needs to ramp

| Skill area | Self-rated | Acquisition relevance |
|---|---|---|
| Cross-functional negotiation w/ senior counterparties | 9/10 | high — vendor/customer renegotiation post-close |
| Building automation / SOP-ifying tribal knowledge | 9/10 | high — most boring businesses are 50%+ automation candidate |
| Financial framing of ops decisions | 8/10 | high — 13-week cash-flow muscle, structural-spend asks |
| Process design from ambiguity | 9/10 | high — first 90 days post-close |
| Operations data infrastructure (Redshift, Quicksight, dashboards) | 8/10 | medium — useful for any biz with QuickBooks/CRM data |
| Direct customer/partner trust-building | 8/10 | high — seller handoff, top-customer retention |
| Pricing & offer construction for end customers | 4/10 | medium — Hormozi-shaped gap; Sanchez framework partly compensates |
| SBA 7(a) deal sourcing / diligence / LOI | 3/10 | high — being built actively, primary current learning |
| Direct-response marketing / lead-gen | 2/10 | medium — not needed for most service businesses, critical for digital |
| Owner-operator labor compliance | 1/10 | low — auto-disqualified by criteria anyway |

## Backbone gap (carry from Q1 2026 review)

Documented growth area, relevant to acquisition: Will has the data and the conclusion but defaults to collaborate-then-follow-up rather than putting disagreement on the table at decision time. Concrete pattern: in an August 2025 admin-fee discussion, accepted a carrier's $150 additive within three days of proposal without escalating to manager — manager looped in via the carrier's CC four days post-acceptance, not through Will's own escalation. Subsequent renegotiation closed the methodology cleanly, but the moment-of-acceptance pattern is the gap.

**Acquisition relevance:** in deal negotiation and post-close vendor renegotiation, the moment-of-acceptance pattern translates directly. AIOS should flag this when Will is mid-LOI or mid-vendor-renegotiation and pattern-match the behavior. Active mitigation: name disagreement before the answer is fully baked, then commit to follow-up data — not the reverse.

## How AIOS should use this file

1. **Deal evaluation** — when Will brings a listing or a target for analysis, score it against the transferable-capabilities table and the operating constraints. Surface 1:1-transferable skills first, then ramp-required skills, then cold-zones-as-disqualifiers.
2. **Zone-of-genius checks** — when Will is about to spend time on a thing (especially during the Amazon promo window), check whether the activity uses the high-leverage skills (cross-functional negotiation, automation, financial framing) or the cold-zone ones. If cold-zone, flag.
3. **Council mode pairing** — when invoking `/council-mode` on an acquisition decision, pull `references/sanchez.md` (primary framework) + `references/hormozi.md` (offer/value lens) + this file (capability fit). Combined view should land before recommendation.
4. **Backbone-gap watch** — during any deal negotiation or vendor-renegotiation conversation, watch for the moment-of-acceptance pattern. Flag it in the moment, not after.

## Source material

For deeper detail (Amazon-internal, do not exfiltrate):

- `C:/Users/zhouzw/ict_automation/promo_doc/talent_review_q2_2026.md` — formal Q2 2026 self-assessment
- `C:/Users/zhouzw/ict_automation/promo_doc/promo_doc_v1.md` — long-form L4→L5 promotion case
- `C:/Users/zhouzw/ict_automation/CLAUDE.md` — project guide for the underlying work
