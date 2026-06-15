# Weekly Reflection — June 14, 2026

Covers **June 8–14 (W24)**. Run Sunday 6/14 19:10 AZ. **Synthesized autonomously from captured data, not a live interview** — sources: `archives/synthesis/2026-W24.md`, `journals/inbox.md` (Banff + Sedona + ZoG captures), `daily-log.md` (6/8–6/14, all □), backlog status deltas, `state.md` (frozen 6/8). Reads on top of the W24 synthesis (which has Decisions / Patterns / Cross-Domain Bridges). Where Will's direct read would sharpen a section, it's flagged in *(italics)*.

---

## Career

W24 was the hardest execution week of the cut so far and the one with the least margin: Will absorbed **Colton's USNS scope while Colton was out sick** on top of his own rIXD/nIXD, published the daily IPEX Ops Flash Mon–Thu, and drove the redirect board to outcome — **WBW2 closure essentially complete** (WBW2→HIA1 SIM ~100%, MDP drained -2.29d). The standout L5-grade move wasn't throughput, it was the third consecutive week of **challenging the measurement, not the operation**: the **AZNG trailer-reduction metric pushback** (6/12, to Cam Nelson / Rajesh / Matt / Naresh / Laura / Shelby) disputing the T4WK-vs-T8WK baseline and demanding a 1P-vs-3P SCAC split before scoring against goal. W23 was IFSA_CHILD unit-inflation + GL_MW; W24 adds AZNG. That's a clean, repeatable "diagnose the metric up the chain" pattern — textbook cross-functional influence and strategic framing.

The structural risk is the same one the synthesis named: **the AZNG pushback is promo evidence going un-ported.** It lives in an Outlook thread, not the promo doc (Jun 30 hard cutoff). And this happened at the worst possible time to lose the witness — the **manager-gap window opened 6/13** (Matt paternity OOTO 6/15–20, Hans 6/13–28, Colton sick, Chris Wong out 6/12–15). Will is running largely independent through peak ramp with approvals routed to Dwight/Laura/Shelby. The 6/12 2pm Matt 1:1 was the last touchpoint before that gap, and **whether it landed DOE + promo Section 1 is unconfirmed** in any captured source. *(Will: did the 6/12 Matt 1:1 close out DOE + promo Section 1, and did you make the eligibility-vs-4-gate call?)* The AFMM upstream bottleneck (PSP3→LAX9 stuck at 9%) is now a 3-week structural constraint, not Will's lever.

---

## Fitness

The data story is the same as the last two weeks, now worse: **a two-week logging blackout.** Every entry in `daily-log.md` for 6/8–6/14 is □ — no weight re-log, no session count, no step confirmation, no Z2 confirmation. Taken literally that's a total miss across every gate; in reality it's the known-broken evening-archive pipeline writing *planned* tasks without capturing *completion*. But the distinction matters less each week it persists: the cut is now **flying blind in Wk 3→4 at the caloric floor**, and the Larsen Press 3-lift canary (the abort signal, sitting at 1 green / 1 yellow / 1 red as of 6/7) **cannot be read without session logs.** The 6/8 carry-forward was explicit — *land `fitness_logger.DRAFT.py` and confirm the Sunday keystone fires through it.* There's no captured evidence either happened. *(Will: what's the 7-day rolling weight avg right now, did the Larsen back-offs recover off 6,4,4, and did the logger land?)*

The cut was already behind pace (~0.73 lb/wk vs. plan) because the two non-food levers — steps (9,165 avg vs. 12,500 target) and Z2 (14 min vs. 60+) — weren't firing. A blind week stacked on an under-fired week is exactly the failure mode the re-baseline to ~174–175 by Jul 11 was supposed to absorb, but only "if inputs actually fire." With no data, we can't tell if they did. The pipeline (#74) is no longer a nice-to-have; it's the single thing standing between the cut and a third blind week.

---

## Relationships

Two real closes and one large open. **The pregnancy thread officially closed negative 6/14** — the multi-week "11 days late" question from 5/28 is resolved, no longer an open planning sensitivity. Clean. The **Banff/Canmore friend trip (Jul 2–12)** is the week's center of gravity on the relationship/friendship axis: a ~10-person trip, Will confirmed P1 (7/2–7/7), with a fully-built planning state — locked transport (2 rental SUVs), two live Airbnb candidates (Option A Banff in-park $14,050/10nt sleeps-10, Option B Canmore sleeps-8 cheaper), flattened budget table, and a **7:30pm PST call tonight (6/14) to lock headcount and phases.** This is the first concrete test of the long-flagged friendship gap (`context/relationships.md` L74–80) — a real roster, real logistics, Will doing the organizing work.

The differentiation-relevant thread inside Banff: **Elena bailed at the $3,510 baseline (6/12), then reopened** when the cook+cut path dropped the combined cost to $2,670–2,910. Her attendance is pending her review of the full breakdown. And separately, Will planned **Elena's birthday weekend in Sedona (Sep 11–14)** — a goal-anchored trip (`goals/desire-polarity.md`: novelty + private hot-tub cabin + Saturday birthday peak + Sunday stargazing), ~$1,280 all-in, reservations to lock by 2026-07-20. That's a structured, own-gravity investment in the same register as the SoCal trip — not a logistics date night. The daily presence gates (full presence / no intimacy talk, unannounced solo block, desire-polarity rep) were prescribed daily but, as with everything else, unverifiable in the blackout.

---

## Money / Acquisition

**The Work Main Quest carry-forward executed.** The 6/8 reflection's #1 acquisition move — *run the Apify scrape* — is **DONE (6/14):** scrape + enrich complete, **505 ranked firms** saved and committed (`sourcing/leads-ranked-dan.csv`), plus a Dan-thesis re-rank (recurring + tax-advisory up-weighted, seasonal tax-prep + wealth-mgmt demoted → `leads-dan-reranked.csv` + `leads-dan-shortlist.md`). This is the at-risk-quest recovery move from last week, fired. The sector is **LOCKED: bookkeeping/accounting** (Dan track), resolving Codie's "one sector, one city" rule. The Main Street Accelerator continued with Elena co-working.

The pipeline now has two near-term gates, both narrow: **dan-reachout is fully unblocked** (all three readiness gates closed) — the only thing left is **Will filling three load-bearing numbers** (Elena's cash $ + source + timing, Elena's hours/week per phase, Dan's 2026 CPA-licensure status), then strip the `[Will fills]` brackets and send. And the **Solo-track ZoG sector pick** is still open — widened from 4 to a 10–12 candidate menu after Will pushed to stay broader; it gates the solo scrape and Elena's apprenticeship targeting. Volume is now built; the gating count is still *logged reps through `/deal-eval`* and *real broker/seller conversations*, neither of which the scrape itself produces. *(Will: did you lock the final solo sector list, and are you sending Dan this week or holding for the three numbers?)*

---

## Wedding

**Movement, after three reflections of zero.** The hotel block advanced — sign Element (9 rooms) bringing secured to ~19, with the premium-block chase live (The Remi / Hotel Valley Ho both ghosted Engine → re-RFP + direct group-sales calls, no backup tier). And two weekend-itinerary decisions locked: **Brat Haüs Old Town reserved** for the Sat 10/23/27 no-host post-wedding dinner (~20 ppl), and the Sat-morning brunch narrowed to three candidates (Mission / Henry / Hearth '61) for a Spring-2027 reservation. The drift-decay flag from 6/8 is cleared for now — but the ~14–17 room gap on the block and the un-set Uber/Lyft guest-credit budget (~2–3× understated at $1k) both still carry.

---

## Weekly Quest Check — June 14, 2026

**Work Main: Deal-Ready by Aug 31** (acquisition Learn phase)
- **On track: recovering — was at-risk 6/7, the recovery move fired.** The Apify scrape is done (505 ranked firms), sector locked, Dan packet send-ready. The infrastructure and sourcing volume are now built. But the *gating count* — 12+ listings through `/deal-eval`, 2+ broker/seller conversations — has not started converting yet. Volume ≠ reps.
- **This week's #1:** **Send Dan (Frame B).** It's the highest-leverage unblocked move — fill the three numbers, strip the brackets, send. It converts 505 leads + a built thesis into the first real broker/known-buyer conversation, which is a literal win-condition count.
- **Removing:** The only blocker is Will-side, not the leads — the three load-bearing numbers (Elena's cash/hours, Dan's CPA status). Decide them with Elena this week (the Banff/Accelerator co-work sessions are the natural slot) or send with Dan's CPA status as an explicit open call question rather than waiting.

**Life Main: Become My Own Point of Origin** (keystone: Sunday Zone 2 incline treadmill, cut phase)
- **On track: at risk — third week running with no confirmed keystone rep.** Same exact pattern the 6/8 and 5/31 reflections flagged. Career and Money both advanced structurally this week; the Life keystone is still a value statement without a single logged fire. The blackout makes it unobservable — and per the integrated-coach read, an unlogged keystone reads identically to a skipped one for a quest that measures *inputs*.
- **This week's #1:** **Run today's Sunday 6/14 Zone 2 (60–90 min) and log it by hand** — don't wait on the pipeline. One confirmed rep, manually pasted, breaks a three-week pattern.
- **Removing:** The blocker is the broken logging pipeline (#74). The keystone may be firing and going unrecorded — but three weeks of "maybe firing" is itself the signal. Land `fitness_logger.DRAFT.py` this week (a weekend block, per the standing guardrail — not promo-doc time) so the keystone becomes observable for the first time.

**Both Main Quests carry a recovery move into next week.** Work-main: send Dan. Life-main: log one keystone rep + land the logger. The Life-main recovery is the load-bearing one — see carry-forward.

---

## Carry-Forward — single most important thing

**Make the Life Main Quest observable: run today's Zone 2 keystone, hand-log it, and finish `fitness_logger.DRAFT.py` this week.** This is the same carry-forward as 6/8, now non-negotiable because it has rolled unaddressed for three weeks while every achievement axis advanced. It sits at the intersection of two threads going blind simultaneously — the cut (no weight/session data through Wk 3→4 at the floor, canary unreadable) and the Life keystone (zero confirmed reps, the quest the whole quarter was built to protect). Everything else this week was net-positive and largely self-sustaining: the Apify scrape closed the work-quest's at-risk flag, the pregnancy thread is shut, Banff/Sedona are moving, wedding unstuck. The one item that, left undone, guarantees next week's reflection is blind in exactly the way the last two were — is the fitness/keystone logging. The pattern is no longer a data-pipeline curiosity; it's the precise dynamic the Life quest was created to interrupt (Joy 4, Heart 5 — winning on paper, not feeling it). More acquisition progress will not touch it.

Second, smaller: **send Dan** — the unblocked tip of the Work Main Quest, and the move that converts built infrastructure into a win-condition count.

---

## Coach Observation (integrated read)

**Schofield active fifth consecutive week** on the career axis — and the take sharpens, doesn't repeat. The AZNG metric pushback is the third straight week of measurement-level influence aimed up the chain (IFSA_CHILD → GL_MW → AZNG), which is genuinely L5-shaped work. But it landed at the start of the manager-gap window, with the last manager touchpoint already behind it. Schofield's read: **witness-less L5 work that never gets ported into the promo doc is a scoreboard win that never converts to the title.** The capture→evidence step — lifting the AZNG dispute and the mechanism diagnoses out of email threads and into the Jun 30 doc — is the one move Will keeps leaving on the table, three weeks running. With the witness absent through 6/20, the `_notes/` write-up *is* the only artifact that survives. Log it in real time or it didn't happen, institutionally.

**The Life Main Quest is the quietest signal worth hearing — for the third week running, and that's the headline.** Last week's coach note called this "a two-week pattern, not a one-off"; it's now three. The structure is consistent: when the achievement axes are this loud (a closed work-quest unlock, a 10-person trip organized, a birthday weekend designed, a wedding unstuck), the point-of-origin work is the first thing to silently slip — which is *exactly* the dynamic the quest names. The integrated read isn't "try harder on the keystone." It's that the keystone keeps losing to legible, externally-witnessed wins, and the entire premise of "become my own point of origin" is learning to value the un-witnessed input. One hand-logged Zone 2 rep this Sunday is worth more to that axis than all 505 ranked firms.

**Perel/Schnarch — clean, with one thing to watch.** The pregnancy close was handled with presence; the Sedona trip is differentiation-friendly (own gravity, novelty, a real birthday peak). The watch item is subtler: Will did an enormous amount of *organizing labor* this week (Banff logistics, budget tables, Elena's cost breakdown, the Sedona itinerary). That's generous and capable — Principle 1 territory — but the relationship lever in `relationships.md` is explicitly *not logistical effort*; it's presence and not-over-pursuing. The trips are good. Just notice if the planning energy is standing in for the presence work, the way achievement can stand in for the keystone. No flag yet — noting the adjacency.
