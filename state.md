# State — Last updated May 25, 2026

## Daily Loop
- **Todoist daily brief live.** GitHub Actions runs the morning brief at 7am AZ (14:00 UTC) → 3–5 tasks to Todoist "AIOS Daily"; evening archive at 9pm AZ (04:00 UTC) writes completions to `journals/daily-log.md`. Workflows: `.github/workflows/morning-brief.yml` + `evening-archive.yml`. Secrets in GitHub repo settings (ANTHROPIC_API_KEY, TODOIST_API_KEY). Migrated off GCP Cloud Functions/Scheduler — old `cloud/morning-brief/` retained as source but no longer the trigger. Source of truth for "what should I do today" is Todoist.
- **Security note:** Anthropic + Todoist keys rotated; two exposed GitHub PATs revoked. Resolved May 25.

## Career
- Amazon SCM I (L4). Promotion window Q3–Q4 2026.
- **Promo doc drafted.** Open: final review pass → manager alignment (target June 30).
- Escalation scraper: threshold logic developing on work laptop, not finished. Next: build out logic around the escalation identifier.
- SCM II behaviors: deliberately deprioritized for the promo-doc sprint. Two-plus weeks at zero — resume logging once promo doc ships (no captures = no L5 narrative).

## Fitness
- **NYC Cut Week 1 done (May 17–23).** 7-day avg 182.6 lb, −3.0 WoW off 185.6 — water/glycogen, expected. Not real fat loss yet.
- BF: ~20–21% estimated. Lean mass: ~147 lb.
- Cut target: execute clean through Jul 11. 168 lb is wedding suit target (Oct 2027), not Q2 deadline.
- Actuals wk1: protein 169g/day, steps 10.7k/day, cals 1,914 (deficit confirmed — don't chase 1,820; let scale steer, add steps before cutting cals).
- Refeed trigger: 7-day rolling avg ≤176 lb (not a spot weigh-in).
- Abort signal: Larsen Press drops >10% → come up to ~2,000 cal. **Held 155 lb W4→W5 — canary green.**
- Hard floor: 168 lb — do not cut below.
- Reverse diet: Jul 12–29. NYC maintenance: Jul 30–Aug 5.
- Program: GVS Ravage Week 5. Neutral Pull-Up trending up (2/2/1 → 3/3/2) but still flagged weak vs. BW+45×5 standard.
- **Gap:** no sleep data flowing — next week's capture. Sun May 24 Legs B logged (manual paste — Liftosaur token expired); no May 25 session recorded yet.

## Relationships
- Elena: improving. **Desire gap closed this week** — architecture date happened, intimate once (better than last). Differentiation approach working — keep building the separate self, don't reverse-engineer it into a tactic.
- Solo pursuit: MMA or bachata 1–2x/week — **night still not locked (slipped 2 weeks).** Lock it or pick something else. Ravage counts as solo separateness.
- Zero night talks about intimacy — hard rule.
- Friendships: roster seeded (8 people). **Sahil touchpoint still not done (slipped 2 weeks).**

## Wedding
- **Contract signed.** Clayton House Elite, Oct 22, 2027, Scottsdale.
- **St. Andrew Oct 22, 2027 LOCKED.** Pre-Cana process to schedule.
- **Virehouse: BOOKED. Deposit paid May 18.**
- **Hotel block:** 10 rooms secured vs. ~35-room OOT target. 2 hotels declined, 1 pending. **25-room gap** — chase the pending hotel + open new ones.
- LED candles needed. Late-night bite: Chick-fil-A chicken minis ~$300 (outside vendor approved by Bailee May 10).

## Travel
- NYC trip: Jul 30 – Aug 5. Will + Elena. Paramount Hotel (4 nights) + friend's place Hell's Kitchen. ESM NYC dance festival at Marriott Marquis. Confirmation G7LGXE. Book Broadway show + ESM passes before trip.

## Money / Acquisition
- $70k earmarked for income-growth investments. Not deployed.
- $2k/mo recurring allocations.
- **Acquisition restart:** End of Week 1, Learn phase. Zero listings reviewed. Saturday review cadence active (started May 23).
- **Goal: truly absentee** (quarterly check-in), not just semi-absentee. Primary = Path A (service business, 2–3 staff, Elena operates yr 1 → manager hire yr 2). Path B (digital) is a parallel second track.
- Zone of Genius, Ideal Owner Experience, and Deal Box **complete** — now live in `context/acquisition.md`. Phase 1 target: $252k–$504k price, $126k CF floor; Phase 2 (Elena scales back) grows into $198k CF.
- Framework reference: `references/sanchez.md` (Codie Level 1 — pure framework; Will's filled-in answers moved to `acquisition.md`).
- Dan Nguyen accounting firm thesis: intact, not active. Secondary option if a licensed CPA resolves AZ ownership law.
- Search window opens ~August 2026 (end of 3-month learn phase).
