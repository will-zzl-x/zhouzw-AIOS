# State — Last updated June 7, 2026

## Quests (Q2 — set in the May 25 quarterly review; full doc `archives/2026-Q2-quarterly-review.md`)
- **Work main:** Exit Codie's 3-mo acquisition Learn phase deal-ready by Aug 31 (12+ framework reps, 2+ broker contacts, LOI template). `goals/acquisition.md`.
- **Life main:** Become my own point of origin — self-validation, worth from inside not the scoreboard. Keystone: **Sunday morning Zone 2 indoor incline treadmill (60–90 min)** (cut phase — cut-additive cardio doubling as solo-pursuit; BJJ + Thursday Muay Thai resume post-cut Jul 12+ as the embodied/skill axis). Measure inputs, never score outputs. `goals/desire-polarity.md`.
- **Side:** ship promo doc (~Jun 30) · execute the cut through Jul 11 · friend touchpoint every 2 wks.
- **Wheel low axis (the focus):** Joy 4, Heart 5 — winning on paper, not feeling it. The Life quest targets the root.

Phase: **NYC Cut Wk 2 ending** — May 17 – Jul 11 (daily gates by weekday/weekend in `daily-standard.md`)

## Daily Loop
- **Todoist daily brief live.** GitHub Actions runs the morning brief at 7am AZ (14:00 UTC) → 3–5 tasks to Todoist "AIOS Daily"; evening archive at 9pm AZ (04:00 UTC) writes completions to `journals/daily-log.md`. Workflows: `.github/workflows/morning-brief.yml` + `evening-archive.yml`. Secrets in GitHub repo settings (ANTHROPIC_API_KEY, TODOIST_API_KEY). Source of truth for "what should I do today" is Todoist.
- **Security note:** Anthropic + Todoist keys rotated; two exposed GitHub PATs revoked. Resolved May 25.
- **Daily-Sync cadence partial 2 weeks running** (W21 0/5, W22 3/5). `_notes/` is the healthier write surface than personal journals — Sunday `/weekly-reflection` reads from `_notes/` mtime ≥ Monday alongside journals.
- **Fitness logging pipeline broken.** Liftosaur CSV + weight spreadsheet + step source don't auto-flow to AIOS — synthesis false-flagged "fitness signal: zero" 5/29 while Wk2 actually had a Larsen Press top-set rep PR. Manual Sunday paste habit until pipeline build (task #74).

## Career
- Amazon SCM I (L4). **Talent Review .docx submitted 5/19** — Q3–Q4 promo window now needs L5-grade evidence. RAPID rebalance + mechanism notes (SKED Flex 5/27, WEPAY_IMPORTS 5/29) are the W22 deposits. Acquisition is the work/income main quest; leaving Amazon late 2027.
- **RAPID seat (W22 lock):** Agree (giver-side feasibility) + Perform. Brian Chaput 5/29 reorg moved WK0 Decide/Recommend to Rajesh's team (Hans/Dwight/Naresh). Matt 1:1 same morning explicit rebalance feedback. Will accepted day 1 — executed Mario's 4 LTS asks in the new lane same afternoon.
- **Promo doc drafted.** Open: final review pass → manager alignment (target Jun 30, hard sprint).
- **Active workstreams (W22):** SKED Flex Mechanism proposal authored 5/27 (`_notes/sked_flex_mechanism_proposal.md`), WEPAY_IMPORTS finance lever scoped 5/29 (`_notes/wepay_imports_finance_lever.md`). Both Recommend-lane cross-functional bridge work.
- **Jeff rIXD-secondary-owner ramp:** plan accepted with Colton (3-wk shadow→solo handoff, kicks off ~Jun 1). **Prioritized higher next week** to free Will's bandwidth for DOE push.
- Escalation scraper: threshold logic developing on work laptop, not finished. Lower priority than promo doc + Jeff ramp.
- **SCM II behavior-logging retired** — measure promotion by deliverables, not behavior counts. `goals/scm-ii-promotion.md` parked.

## Fitness
- **NYC Cut Wk 2 ending (May 17–31).** Wk1 avg 182.6 → Wk2 avg 182.2 (essentially flat) → 5/31 single read 179.8.
- BF: ~20–21% estimated. Lean mass: ~147 lb.
- **Cut target HOLDS: 172 by Jul 4.** Caloric floor is at BMR on non-eat-out days (no further cut available). Closing the math via steps + cardio.
- **Step target +25%: 12,500/day** (was 10,265 W22 avg). Add **2–3× Zone 2 cardio/wk** (20-min, post-lift fasted or AM).
- Wk2 sessions: 11 in 15 days (above 6×/wk target). Steps held at 10,265/day (71.85k/wk total).
- **Larsen Press canary green getting greener:** 155 × 6,4,5 @9–9.5 pre-cut → 155 × 6,6,6 @9 on 5/30. Top-set rep PR on the cut.
- **Neutral pull-up:** 4/2/2 on 5/30 (top-set rep PR for that load). Still flagged weak vs. BW+45×5 standard but moving the right direction.
- **Abort signal:** Larsen 155×5/5/5 @9 → re-baseline target to 176 by Jul 11 / full target by NYC Jul 30.
- Refeed trigger: 7-day rolling avg ≤176 lb (currently ~181.7).
- Hard floor: 168 lb — do not cut below.
- Reverse diet: Jul 12–29. NYC maintenance: Jul 30–Aug 5.
- Program: GVS Ravage Week 6. Macros tracked in **Cronometer**.
- **Meal-planning system live (6/6):** token-efficient weekly cook-cycle in `meal-planning/` (built in a separate Claude Code session, merged 6/6). 20 vetted recipes, deterministic Python loop for serving math / coverage / grocery / defrost / cook-order / depletion (zero tokens), 4 AI templates for fuzzy tasks. Wired to `/health-os` → "plan a meal cycle". Cut constraints baked in (M1/M2 starch-free, ~150g protein/day, ~45g/feeding, dining-out = carb-forward refeed). Source of truth: `data/recipes.json`. Separate from the deprecated Streamlit meal-planner app (`github.com/will-zzl-x/meal-planner`).
- **Combat keystone reset (6/1) → boxing pivot considered (6/2 AM) → Zone 2 sub locked (6/2 PM):** BJJ deferred to post-cut (Jul 12+). Boxing technique class at Boxout AZ (Sun 9:30 AM) considered as substitute but dropped — Ravage runs 2 upper days/wk, forcing a Mon-upper-after-Sunday-boxing adjacency that compromised the Larsen canary on a 1,820 cal deficit. Cut-phase keystone is now **1× Sunday morning Zone 2 indoor incline treadmill, 60–90 min** — same recurring solo-pursuit slot, cut-additive (Schofield prefers low-intensity steady-state — walking/incline/bike — over high-impact cardio on a cut, `references/schofield.md` L130), zero Ravage interference. Single 60–90 min bout meets the weekly Z2 *minutes* target but not frequency — spread sessions adapt better; single-bout chosen for cut-phase sustainability/keystone-identity, revisit post-cut (Jul 12+) when BJJ/Muay Thai return and Sunday becomes the dedicated LISS slot. Skill/embodied combat axis returns post-Jul 11 when BJJ + Thursday Muay Thai ramp on original cadence. Style/grooming overhaul still sprinting in parallel.

## Relationships
- **Elena (W22 read):** stressed about work, anxious, nausea earlier in the week (now improving), one ~few-hour evening 5/27 of smell sensitivity, no fatigue, no breast tenderness, appetite recovering. Pregnancy possibility from 5/28 capture still on the table — 11 days late on the pill is the part that doesn't go away as a question. Test-plan close-the-loop deferred to Will + Elena's call. Posture under stress-load: presence, not caretaking; don't reverse-engineer differentiation into a tactic.
- **Friend cadence anchored W22.** Sahil ✓ (~5/26 from W21), Spencer ✓ this week, group hang 5/30 (Annie, Jeff, Charlie, James, Spencer, Miguel). Cleared the 2-wk rhythm twice over.
- **Solo-pursuit keystone (cut phase, final 6/2): 1× Sunday morning Zone 2 indoor incline treadmill, 60–90 min**, same recurring slot. Replaces BJJ for cut sustainability — same Life quest role, zero Ravage interference, cut-additive. BJJ + Thursday Muay Thai both ramp post-Jul 11 as the embodied/skill axis returns.
- Zero night talks about intimacy — hard rule.

## Wedding
- **Contract signed.** Clayton House Elite, Oct 22, 2027, Scottsdale.
- **St. Andrew Oct 22, 2027 LOCKED.** Pre-Cana process to schedule.
- **Virehouse: BOOKED. Deposit paid May 18.**
- **Hotel block (rebaselined 6/7 from guest sheet):** Booking via Engine, courtesy blocks only (0% attrition, Sep 20 2027 rooming cutoff). **Target ~33–36 rooms** — derived: ~108 OOT invited × 75% = ~81 attending, −10 alt-accommodation (Elena's parents + others), ÷~2/room ≈ 30–36 (swing = 9 kid-families self-booking AirBnBs). **Secured: Courtyard Marriott 10 ✅ + Element SkySong 9 (signing 6/7) = 19.** Active chase: premium block 12–15 rooms (The Remi OR Hotel Valley Ho — both ghosted Engine this week → re-RFP + direct group-sales calls; no backup tier so push hard). **Declined:** Senna House Curio (lukewarm, $417 all-in), Courtyard Salt River (singles-only + redundant), Papago Reside (overkill). Transport = Uber/Lyft guest credits ($1k budget line ~2–3× low). Full detail: `context/wedding.md`.
- Late-night bite: Chick-fil-A chicken minis ~$300 (outside vendor approved by Bailee May 10).

## Travel
- No active travel. NYC Jul 30 – Aug 5 next anchor (Will + Elena, Paramount Hotel 4 nights + friend's place Hell's Kitchen, ESM NYC dance festival at Marriott Marquis, confirmation G7LGXE). Book Broadway show + ESM passes before trip.

## Money / Acquisition
- $70k earmarked for income-growth investments. Not deployed.
- $2k/mo recurring allocations.
- **Acquisition: not silent.** End-of-W22, today's session was one of the most active acquisition days in the file. First listing reviewed end-to-end (Chandler cleaning co $645k → NO on margin floor 26.9% + SDE $183k below floor). Saturday rep ✓ done.
- **Sector LOCKED:** bookkeeping/accounting (with Dan re-engagement). Resolves Codie's "one sector, one city" rule. Other sectors are inbound-only secondary.
- **Goal: truly absentee** (quarterly check-in) by Year 2. Primary = Path A (service/professional services with 2–3 staff; Elena scales W-2 to ~20 hr/week at close, Year-1 operator unpaid; 12-month manager-hire trigger moves to absentee Year 2). Path B (digital) parallel second track.
- Zone of Genius, Ideal Owner Experience, and Deal Box **complete** in `context/acquisition.md`. **Scenario B Codie-honest (5/31):** $500k–$700k clean / $700k–$1.0M stretch / $1.0M hard ceiling. $286k SDE floor at $500k → $367k at $1M (price-scaled). $953k+ revenue, 30%+ margin. Bakes in $55k operator salary so Year-2 manager hire is structurally affordable.
- Codie-vetting (5/31) surfaced gaps: 4A Club + Walking Billboard sourcing missing entirely (vs. Codie emphatic), learn-phase volume light vs. 100/50/10/1 ratio.
- Framework reference: `references/sanchez.md`. Mike Warren `references/warren.md` + Roland Frazier `references/frazier.md` (workflow-generated, quality unverified per task #73).
- **Dan Nguyen partnership thesis:** Scenario B = **Elena steps in** (cash + time) resolves the original $500k–$1M debt-load objection that put it dormant May 2025 — the stall wasn't deal-box math, it was debt-load incompatibility with Will's Amazon W-2. Elena's cash reduces the debt required; her CFO/COO bandwidth splits post-acquisition operational load → no forced early Amazon exit. **Reactivation = next-week move.** Reach-out frame B (direct ask). AZ CPA 51% paths kept open (retain CPAs as equity ≥51% OR dodge CPA-only services — decided when concrete deal forces it). Roland Frazier value/opportunity outreach script v2 + Apify Google Maps scrape + Claude Code lead-enrichment owed before message goes. Prep work Mon–Thu, message readiness-gated. **Thesis files reconstructed 2026-06-03**: `journals/dan-thesis-history.md` (chronological) + `context/dan-thesis.md` (strategic). Remaining gaps: Elena's specific cash + time commitment (to make the resolution concrete vs. directional), Dan's current sentiment / CPA status.
- Search window opens ~August 2026 (end of 3-month learn phase).
