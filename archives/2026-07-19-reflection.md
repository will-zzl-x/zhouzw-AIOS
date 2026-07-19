# Weekly Reflection — July 19, 2026 (W29)

Covers **July 13–19** — first full week of the reverse diet, first live week of the solo-space rotation, the week the instruments broke (and got fixed), Elena's 35-commit wedding planning session, and the fourth promo-doc slip.

---

## The week the instruments failed

Three AIOS failures ran concurrently this week, all silent:

1. **Todoist completion sync returned 0 every day** — `get_completed_today` bug, so `journals/daily-log.md` recorded a week of empty boxes regardless of what Will actually did. Diagnosed + fixed 7/19, read-only backfill report tool added for the lost 7/12–7/18 window.
2. **The 7/17 morning brief crashed** (`NameError: import re` in brief_generator) — fixed same day.
3. **Weekly synthesis hasn't produced a file since W24** (~5 weeks) — the Friday auto-fire on the work laptop isn't landing in `archives/synthesis/`. Flagged, not yet diagnosed.

**Consequence: per-area completion rates from daily-log are NOT computable this week** — the data is lost, not absent. Primary sources substitute where they exist: training 6/6 via Liftosaur CSV, weigh-ins 5/7 via the weight sheet, deal evals 0 via acquisition-log, Z2 0 via Will's report. The notable human fact: with every external trigger broken around him, Will still trained 6 of 7 days. The habits are becoming self-sustaining; the instruments still need to work.

---

## Fitness — Banff verdict: water. Canary: recovered. Z2: broke.

**The Friday Jul 17 verdict came in clean.** Week of 7/12 averaged **179.8** (down from 180.5), Friday reading **178.4** — ~1 lb above the cut's 177.4 low, *while calories were increasing*. Weight falling during a reverse diet means the Banff bounce was glycogen/water, as hypothesized. The cut's −7.7 lb is banked. Sunday 7/19 reading: 179.8.

**Reverse diet is ahead of the paper schedule and that's fine.** Plan said ~1,970→2,150 over two weeks; Will ran >2,000 average last week and stepped to **2,150–2,200 as of Friday**, by feel, untracked (deliberate, standing). **Steering rule updated at Will's request: the weight target is now DYNAMIC** — trend-based per the evidence-based reverse-diet playbook (Helms/McDonald school): flat-to-+0.5 lb/wk on the 7-day avg is acceptable; pause the calorie add only if trend exceeds that two weeks running. The fixed ≤180–181 ceiling is retired as the primary instrument (kept as a soft two-week check). Weigh-in adherence 5/7 (missed Wed, Sat) — good, not the non-negotiable 7.

**Training was the week's standout: 6 sessions in 7 days, zero misses**, including a same-day double (Legs B early AM + Torso B late night, 7/14). And the **Jul 19 canary confirmed the recovery Schofield's framework predicted 8 days earlier**: Larsen 145×8,7,6 @9–9.5 vs. 7/11's 145×6,4,4 — reps nearly doubled on back-offs at identical load after 8 days of added calories. Narrow Pulldown 112.5×15 @9. The post-cut/post-Banff dip was fatigue, not lost capacity. **Next Torso A: test 155 and re-anchor the canary threshold.**

**Z2 keystone broke at streak = 1.** Zero reps this week (today's Sunday rep pending at reflection time). Cause per Will: time. Same cause as the dance shortfall — see Life Main.

**Sleep scores: killed deliberately.** The 1–5 morning score never fired and Will deprioritized it explicitly ("my sleep is fine"). The gummy stack runs without an outcome measure by choice. Off the consistents list.

**Meal cycle shipped 7/18** — first cycle at reverse-diet calories (recipes #40 egg-roll ramen + #41 fried rice vetted in, weekend cooks rebalanced 4 Sat / 3 Sun). The "new cycle needed this week" carry-forward from 7/12: done.

---

## Career — the fourth slip

The promo doc did not ship by Friday Jul 17. Fourth deadline missed (Jun 26, Jul 1, Jul 17, and the informal 7/13 restart). Will's own call this morning: **it is today's top priority, before anything else** — including this reflection's other moves. Nothing else career-wise this week by his explicit instruction. The pattern note for the record: the doc has now outlived every external deadline attached to it; the only deadline that can work is the one where it ships before other work is permitted to start. That is the design this week.

---

## Relationships

**The desk resolved itself in the healthiest possible way:** Elena deprioritized it on her own — "just an idea for a future home." The 7/12 repair (reverse decisively, she picks, no commentary) stands as the point; the purchase was never it. Row parked by Will 7/17.

**Solo-space rotation — first live week: decent.** Reps fired, including a dance-private-homework overlay (body-rolls + transitions) logged 7/16. But **dance is under-repped by Will's own read** — "not dancing enough privately/solo/with her practice" — and it carries into next week with more weight. Blocker named: **time**. The fix is anchor design, not willpower (theme 1): micro-rep attaches to an existing anchor (post-lift, music already on; or while dinner cooks), 1–2 songs, binary check.

**Flowers stay retimed to ~week of Jul 28** (Will's timing call from 7/12) — ordering this week for delivery next week. Ordinary-day, no occasion, no commentary.

**Friend cadence:** touchpoint due ~Jul 26; the NYC trip (Jul 30, with Michael in the city) covers it structurally the following week.

---

## Money / Acquisition — deep prep, zero reps

Two truths about the same week. The Dan packet got its best work yet (7/16 session): size question adjudicated **structure-first, size-second**; Dan confirmed not lendable, so cash-in resolves by arithmetic ($75k fund splits ~$50k seller cash + ~$25k working capital); the 50/50 ask priced with structures that honor contribution without gifting risk; CPA line contingent, profits-interest 50/50 the likely landing zone; deal-#1 finance sectors expanded with the AI-positioning rule, P&C books the lead; Dan track constrained to the established thesis with a sub-segment filter.

And: **zero deal evals ran.** The Saturday keystone (2 listings) didn't fire; the work-main win condition still reads 0 of 12+ with ~6 weeks to Aug 31. Dan sit-down not yet locked — plan is **text Wednesday 7/22, meet Friday 7/24 early evening**. Will's stated priority order: promo doc, then deal evals as #2.

---

## Wedding — Elena's big week

Elena ran a full planning session 7/18 (~35 commits, merged to master with this reflection). Headlines:

- **Pre-Cana session date LOCKED** — the 4-reflection carry-forward resolves. Full St. Andrew requirement map now in `context/wedding.md`: Marriage Prep Inventory (Deacon Ramsey, by Aug 2026) → Class #1 Life Skills (**starts Sep 11, 2026**, 4 Thursdays + 1 Saturday, $140) → Class #2 God's Plan → Class #3 NFP → affidavits, baptismal cert (Feb 2027), and the day-of chain through confession.
- **⚠️ Conflict flag (new, this week):** Class #1 starts **Sep 11 — the same day Sedona starts (Sep 11–14)**. Confirm actual session dates against the trip *before* registering.
- **Premium hotel chase DROPPED** — Villa Solara covers the overflow. Row retired.
- **Virehouse corrected: it's the photographer, not a rehearsal venue.** Rehearsal dinner venue is a new open item (Elena's parents paying, decide Spring 2027). Brat Haüs back to "deciding," not booked.
- **Will's near-term lane:** ask **Michael for the Affidavit of Free Status in person during NYC** (trip lands exactly on the first-week-of-August target). Pre-trip: get the form requirements from St. Andrew so the ask is executable, send Michael a heads-up text. On the NYC packing list (`context/nyc-2026-trip.md`, new).

Website pushed to Oct 2026, registry Oct 2026, save-the-dates early Nov 2026 (Elena's call — 13 months out felt too far). ~48 wedding rows now in the backlog with date gates — theme 1 applied to the whole wedding timeline.

---

## Life Main Quest — point of origin

**Status: genuinely mixed, trending real.** The rotation went live and fired. The differentiation self-check is on pace (~8 of 10 reflections). Elena's desk data point resolved without Will needing to do anything — which is itself the lesson landing. And the most important sentence of the interview was Will's, unprompted: **"I feel I've been doing better with letting wins land and enjoying things being better."** That's theme 3 progress claimed on the merits, not on the scoreboard.

On that basis Will **deprioritized the therapist intake with intention** — not drift; a decision, made eyes-open, with the Jul 31 deadline released and an explicit revisit at the Aug 24 quarterly. The coach position stays on the record: "don't feel like I need it" during an up-swing is the exact pattern the annual review flagged, and the quarterly revisit is where it gets tested against a full quarter of evidence.

The losses: Z2 broke at 1, dance under-repped. Both trace to time, both get anchor redesigns this week rather than bigger willpower asks.

---

## Weekly Quest Check — July 19

**Work Main: deal-ready by Aug 31** (12+ evals, 2+ broker convos, LOI template)
- **On track: AT RISK** — 0 of 12+ evals logged, 0 broker conversations, ~6 weeks left. Dan verbal is warm but unconverted to a calendar block.
- **This week's #1:** 3–4 logged evals before Friday + Dan text Wednesday → sit-down Friday 7/24 early evening.
- **Removing:** the promo doc — ships today (Sunday), before anything else opens. Fourth slip ends the deadline-scheduling approach; the doc now gates the week's other work instead of the reverse.
- **Constraint check (Hormozi):** binding constraint is **reps on paper**. This week's effort went to packet refinement — real but automatable-comfortable work. Next week's effort points at the constraint: evals logged, meeting held. Nothing on this quest's plate needs killing; it needs the counter to move.

**Life Main: become my own point of origin** (solo-space ≥5 days/wk + Sunday Z2; self-check ≥10 reflections)
- **On track: MIXED** — rotation live and firing ✓, self-check on pace ✓, Z2 0/1 weeks since restart ✗, dance under-repped ✗.
- **This week's #1:** the daily dance micro-rep, actually daily, via anchor (post-lift or dinner-cook; 1–2 songs; binary check). Doubles as solo-space rep and feeds ESM/NYC.
- **Removing:** time scarcity via design — Z2 gets fixed slots (Sunday post-reflection + Tue/Thu 20-min on off-leg days); dance rides an existing anchor instead of needing a found window.
- **Constraint check (Hormozi):** the constraint is **structural time placement, not motivation** — the week proved motivation exists (6/6 training with broken instruments). Killed with intention this week: therapist intake (→ Aug 24 quarterly), sleep scores, Aer/aviators/tailor buys, Elena's desk (her call). The plate is lighter and more honest than it was last Sunday.

---

## Coach Observations

**Schofield:** Textbook week. The scale answered the Banff question exactly as predicted (water), the canary answered the strength question exactly as predicted (fatigue, not tissue), and both answered *because* the reverse diet did its job. Test 155 on the next Torso A and re-anchor the canary to the new block. The Z2 miss is the only blemish, and it's a scheduling problem, not a physiology one.

**Sanchez/Hormozi:** The constraint on the acquisition quest is not knowledge, not the packet, not Dan — it's logged reps, and the count is zero. Everything this week optimized the meeting; nothing optimized the number the win condition actually counts. The redirect is mechanical: evals are the Saturday keystone plus one weekday slot, and the packet is now good enough to stop touching. On the promo doc: four slips means deadlines have stopped carrying information. "Ships before other work opens" is the correct final design — it makes the doc the gate instead of the casualty.

**Perel/Schnarch:** The desk ending is worth savoring: Will reversed on the merits, dropped the commentary, and Elena — given full ownership of her want — decided she didn't need it yet. That's two differentiated people, not a negotiation. And "wins are landing better" alongside "the strongest desire signal to date" is the mechanism working end-to-end: center held, gravity built, nothing watched for. The therapist deferral is acceptable *because* it was decided rather than avoided — and the quarterly is where it gets re-examined honestly.

**Abdaal (system lens):** This was the week the externalized triggers all failed at once — brief crash, completion-sync bug, synthesis gap — and the underlying behaviors mostly survived on their own. That's the good news. The bad news is the system lied by omission for six days before anyone noticed. Instrument health needs its own trigger: the carried-task flag shipped this week; a "zero completions two days running = alarm, not data" check belongs next to it.

---

## Carry-Forward

**The one thing: reps over prep.** The week produced beautiful artifacts — the packet, the meal cycle, the wedding map — while both quest counters (evals logged: 0; promo doc shipped: no) stayed at zero. Next week is measured in counted things: doc shipped, 3–4 evals logged, Dan meeting held, dance reps daily.

Supporting moves:
1. **Promo doc ships today.** It gates everything else this week.
2. **Deal evals: 3–4 logged before the Friday Dan sit-down** (text Wednesday to lock it).
3. **NYC pre-trip lane by Jul 29:** St. Andrew affidavit requirements → Michael heads-up text → festival wardrobe call (ESM is during the trip) → packing list (`context/nyc-2026-trip.md`).
4. **Sedona × Pre-Cana Class #1 conflict check** with Elena before registering.
5. **Flowers ordered for week of Jul 28 delivery.**
6. **Z2 + dance run on anchors, not found time** — Sunday + Tue/Thu slots; post-lift/dinner-cook micro-rep.
7. **Screen-time pipeline:** locate where the phone actually writes, land it in this repo on master, then it becomes a weekly review input.
