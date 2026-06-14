# Inbox — mid-week captures, cleared each Sunday reflection

<!-- Mid-week captures go here. Cleared each Sunday. -->

*Cleared June 7, 2026 reflection. Prior captures resolved: SoCal trip (Jun 19–21) fully booked + archived to backlog-done; pregnancy thread closed negative; meal-system script fixes (grocery.py, defrost.py) ranked into backlog. Carry-forward: build Apify scrape (work-quest unlock) + flip on Brave Shorts blocker (life-quest unlock).*

---

## 2026-06-14 — Acquisition sourcing pipeline: Dan + Solo scrapes COMPLETE, sector-narrowing teed up

**Major milestone** — both work-main-quest scrapes from backlog (#3 apify-scrape-dan + #5 apify-scrape-solo) shipped today via a free path. Sourcing infra is now operational and producing real funnels.

**Path pivot:** Apify free tier wouldn't cover the full 180-string Solo scrape (~$15-25 paid). Instead built `sourcing/places_scrape.py` — Google Places API (New) drop-in replacement, runs under GCP's $200/month free credit (used ~$2-5). Same JSON config shape as Apify, same output shape `enrich.py` reads. Sets up free monthly re-scrapes going forward.

**Pipeline files (all committed, branch `claude/weekly-reflection-lifting-data-Gsh0P`):**
- `sourcing/places_scrape.py` — free Apify replacement (Google Places API)
- `sourcing/enrich.py` — upgraded to sector-aware solo mode + AZ geo filter + per-sector yield reporting + sector_tag classification
- `sourcing/apify-input-dan-bookkeeping.RUN.json` + `sourcing/apify-input-solo.RUN.json` — comment-stripped paste-ready configs
- `sourcing/leads-ranked-dan.md/.csv` — 505 viable bookkeeping/accounting firms (Dan track)
- `sourcing/leads-ranked-solo.md/.csv` — 620 viable leads across 8 sourceable sectors (Solo track)
- `context/sector-evaluation-framework.md` — rewritten 6/13 to match the post-6/10 12-sector menu; repositioned as POST-scrape narrowing tool
- `sourcing/.env` — GCP API key (LOCAL ONLY, gitignored — must be re-grabbed from GCP console on the other machine, OR rotate per security flag)

**Dan track results — 505 ranked viable bookkeeping/accounting firms** (827 raw → 7 out-of-state → 63 chain drops → 252 off-category → 505 kept). Top 10 are all 4.3-5.0★ with phones + websites; clean for AZ 51% law (non-CPA firms scored higher). Names ready to cite in the Frame B message to Dan.

**Solo track results — per-sector sourcing-reality (dimension-5 score band):**

| Sector | Viable leads | Band |
|---|---|---|
| specialty-distribution | 170 | **5** Strong |
| pest-control | 117 | **5** Strong |
| hoa-management | 114 | **5** Strong |
| window-cleaning | 58 | **3** Workable |
| pool-service | 57 | **3** Workable |
| vending-micromarket | 34 | **3** Workable |
| water-treatment | 28 | **2** Thin |
| msp-it | 23 | **2** Thin |
| document-destruction | 13 | **1** DROP (hard filter) |
| coffee-water-service | 5 | **1** DROP |
| mat-rental | 1 | **1** DROP |
| office-plant-care | 0 in AZ | **1** DROP |

**12 candidate sectors → 8 that survive sourcing-reality.** Sunday Elena session is now: score the surviving 8 on dimensions 1-4 (skill/interest/recurring-rev/deal-box) using framework doc, compare, lock top 2-3, update `context/acquisition.md` Track 2 + add Elena apprenticeship backlog row.

**Backlog flips this commit:**
- `apify-scrape-dan` (#3) → DONE
- `apify-scrape-solo` (#5) → DONE (scrape-broad architecture meant we ran it before sector-pick, not after — gate obsolete)
- `dan-reachout` (#10) → UNBLOCKED (both readiness gates closed: Frazier script v2 at `context/frazier-outreach-script.md` + Apify scrape done)
- `zog-sector-pick` (#4) → still open, now backed by yield data — Sunday session w/ Elena (timing TBD; Banff call 7:30pm PST is already on tonight)

**Pick-up state for other machine:**
1. `git pull origin claude/weekly-reflection-lifting-data-Gsh0P`
2. Open `sourcing/leads-ranked-solo.md` + `sourcing/leads-ranked-dan.md` — they're the working deliverables
3. If wanting to re-run scrape on other machine: re-grab/rotate GCP API key, drop into `sourcing/.env` (gitignored, not in repo)
4. Sunday session: walk through `context/sector-evaluation-framework.md` with Elena, use the dimension-5 yield table from `leads-ranked-solo.md` as the sourcing-reality score
5. Post-session: update `context/acquisition.md` Track 2 with locked top 2-3 sectors + add `elena-apprenticeship-[sector]` backlog row

---

## 2026-06-10 — Elena birthday trip Sedona Sep 11-14 (locked plan, needs booking)

**Trip**: Elena's birthday weekend Sep 11-14, 2026. Sedona, 3 nights, drive up Fri after work, return Mon afternoon. **0.5 PTO total** (Mon PM). Goal-anchored to `goals/desire-polarity.md` — novelty + stressor removal + private hot tub/fireplace cabin + Saturday birthday peak + Sunday stargazing peak.

**Schedule**:
- Fri 9/11 — full workday PHX, leave 5:30pm, arrive Sedona ~8pm, in-cabin dinner + hot tub
- Sat 9/12 (birthday) — Doe Mountain hike 8am, packed-lunch from cabin, afternoon cabin/Tlaquepaque, **Cucina Rustica (Village of Oak Creek) 7:30pm**
- Sun 9/13 — slow morning, **Red Rock Loop Rd + Crescent Moon Picnic Site scenic drive ~10am-1pm**, cabin lunch + rest, light cabin dinner, **Sedona Stargazing tour 7-9pm**, hot tub under stars
- Mon 9/14 — remote work 7-noon on cabin patio (she lounges/sleeps in), **Black Cow brunch on way out**, drive 1pm, arrive PHX 3pm

**Cabin spec** (Vrbo/Airbnb): West Sedona / Page Springs / Cornville, private outdoor hot tub (non-negotiable), patio with southern sky view, strong WiFi (work Mon AM), no shared walls. Target $150-180/night. OK to skip fireplace + accept smaller/older property if reviews 4.7+.

**Reservations to make**:
1. Vrbo/Airbnb cabin — **shortlist now (free), BOOK early July** for cashflow timing
2. Cucina Rustica (Village of Oak Creek) 7:30pm Sat 9/12 — mid-July via OpenTable, mention birthday
3. Sedona Stargazing tour 7pm Sun 9/13 — mid-July
4. Dog sitter Fri 9/11 eve → Mon 9/14 PM (3 nights @ $30) — late July

**Restaurants intentionally limited to 2 total**: Cucina Rustica (Sat birthday — Lisa Dahl's best Italian, swapped from Cress after Will flagged Cress reviews as overpriced/mixed) + Black Cow (Mon brunch on way out). All other meals from grocery stop en route to cabin (Whole Foods West Sedona). Pink Jeep tour cut as the lowest-impact-on-desire-goal item; Sunday afternoon = free scenic drive instead.

**Budget**: ~$1,280 all in (down from $1,835 after Pink Jeep cut + food tightening + Cress→Cucina Rustica swap + cabin tier reduction $225→$165/night). Cabin paid in July for cashflow.

**Add to backlog at next Sunday reflection** (life-main, Relationships, deadline 2026-07-20 for all reservations locked).

---

**2026-06-13 — Banff trip Jul 2–12: full planning state (Sunday 6/14 7:30pm PST call pending)**
Large friend-group trip (originally Summer2026Trip group chat, ~14 people). Council decided on Banff/Canmore over cruise. Will + Elena attending Phase 1 only.

**Locked decisions:**
- Destination: Banff/Canmore, Alberta. Trip shape: Banff icons (Moraine Lake, Lake Louise, Banff Gondola, Lake Agnes, Johnston Canyon).
- Dates: July 2–12, 2026. Transition day: July 7 (Phase 1 group departs morning, Phase 2 group's stay continues/overlaps)
- **Lodging structure: single Airbnb for all 10 nights is the working assumption** (was originally 2-house sequential — pivoted as single-Airbnb candidates emerged). Fallback to 2 sequential only if P1/P2 headcounts split very hard. Hotels considered and ruled out (kills cook+cut path, higher per-person, loses group hangout space).
- **Transport LOCKED: 2 rental vehicles (SUVs/minivans, 7-seat) from YYC.** Cost basis ~$120/day per vehicle all-in (rental + insurance + gas). Capacity comfortable for 8, tight for 10.
- Bed requirements: private queens only for couples actually present in each phase. Solo guys all bunk/share.
- Base ruled out: Invermere (~2h each way to Banff = 4h/day driving), Golden/Kicking Horse (~2h to Banff townsite, ~1h to Lake Louise — workable for Lake Louise-heavy days but penalizes Banff townsite days).

**Roster / phase assignments:**

*Confirmed:*
| Person | Phase | Origin | Notes |
|---|---|---|---|
| Will | P1 only (7/2–7/7) | PHX | locked |
| Elena | TBD — reconsidering after cook+cut math | PHX | bailed 6/12 at $3,510 baseline; cook+cut path is $2,670-2,910 combined w/ Will, may bring her back. If she joins, needs 1 private queen room |
| Daniel Zheng | P1 only | SF | his stated preference |
| Dhanush Bathala | 7/4 AM–7/12 (partial P1 + full P2) | DTW | PTO locked |
| Daniel Kong + Annie Chen | P2 only | Chicago area | sharing a bed |
| Spencer Liu | OUT | | |
| Helena Li | OUT | | |

*TBD (Sunday 6/14 call must lock):*
| Person | Status | Origin |
|---|---|---|
| Miguel Magno + Saya Takai | phase unconfirmed | DTW |
| Jeffrey Lin | leaning full trip, not committed | Chicago |
| Charlie Peng | leaning full trip (through 7/11 or 7/12) | unsure |
| Justin Peng | leaning full, unconfirmed | Seattle |
| James Li | coming, phase unconfirmed | Orlando |
| Sahil Dogra | leaning full, unconfirmed | NYC |

**Headcount ranges (pre-Sunday call):**
- P1: 2 confirmed (Will, Daniel Z) + 0–7 TBDers + Dhanush nights 3-5 = 3–10, realistic 6–10
- P2: 3 confirmed (DK+Annie, Dhanush) + 0–7 TBDers = 3–10, realistic 6–9
- Plus Dhanush joining P1 night 3

**Budget table — FLATTENED (current group-message version, includes rental car share):**
All-in per person = flights + lodging + food + activities + rental car share

| Phase | Cook + cut | Baseline | Splurge |
|---|---|---|---|
| Half trip — 5 nights (P1 or P2) | ~$1,500 | ~$1,850 | ~$2,200 |
| Full trip — 10 nights | ~$2,850 | ~$3,150 | ~$3,400 |

Add ~$150–300/person if Option A (Banff in-park) vs Option B (Canmore).

**Will / Will+Elena specifically (cook+cut path, PHX origin, P1 only):**
| Scenario | Total |
|---|---|
| Will solo, Option B (Canmore) | ~$1,500 |
| Will solo, Option A (Banff in-park) | ~$1,620 |
| Will + Elena combined, Option B | ~$3,000 |
| Will + Elena combined, Option A | ~$3,240 |

(Earlier $1,335 / $2,670 figures were pre-rental-car; bumped ~$165/person for half trip.)

**Per-origin flight estimates (peak holiday week — Canada Day + July 4):**

Seattle ~$400 | SF ~$425 | Chicago ~$475 | DTW ~$475 | NYC ~$500 | PHX ~$550 (confirmed live $500–600 this week) | Orlando ~$600 (likely a connection). Unknown-origin default $550.

**Rental car math (LOCKED at 2 vehicles):**
- 2 SUVs/minivans × ~$120/day all-in (rental + insurance + gas)
- 5-day total: ~$1,600–1,700 → ~$170–215/person at 8–10 occupants
- 10-day total: ~$3,200–3,400 → ~$320–425/person at 8–10 occupants

**Activities — paid vs. free (sourced 2026 prices):**
- Worth paying: Banff Gondola ($55–96 CAD dynamic, ~$55–70 USD); Banff Upper Hot Springs ($19.75 CAD ~$14.50 USD); Moraine Lake/Lake Louise Parks Canada shuttle reservation ($3.50 CAD — **already open since April 15, 2026, book ASAP**); Parks Canada park entry (~$11 CAD/person/day, or $151.25 CAD/adult Discovery Pass if 6+ park days)
- Optional splurges: Lake Minnewanka cruise (~$50–55 USD; free shuttle runs June 13–Sept 7, 2026); Lake Louise canoe rental (~$110–130 USD/hr/boat); Sunshine Meadows gondola (~$50–60)
- Free: Lake Louise lakeshore, Moraine Rockpile Trail, Johnston Canyon + Ink Pots, Lake Agnes Tea House hike, Tunnel Mountain, Vermilion Lakes, Bow Falls/Surprise Corner, Two Jack Lake, Bow Valley Parkway, Banff Ave townsite

**Critical path:**
- Sunday 6/14, 7:30pm PST — group call to finalize headcount/phases. Headcount-or-floor threat is live (lodging booking depends on it).
- Shared Airbnb planning doc (currently empty): https://docs.google.com/document/d/1PXv4PO0L7kaDOXgqO1MXQAk_S2nR2Fo-CboBFmXmfVQ/edit
- Still need explicit phase commits from: Justin, James, Sahil+1

**Lead Airbnb candidate (under review):**
"EPIC Hot Pools w/MTN Views-Perfect for Families" — entire townhouse in Banff, 5 min drive to downtown Banff (in-park location, ~25 min from Canmore)
- Sleeps 8 recommended / up to 10 with pull-out couch (hard cap 10)
- 3 BR / 5 beds / 2 baths: Room 1 Queen, Room 2 Queen (both ground floor private), Loft 2 Queens (shared room), Common-space Queen pull-out couch
- 4.7 stars, 105 reviews, Superhost (Chris, 4 years)
- **$14,050 base for 10 nights Jul 2-12** + $25/person/night for each adult over 4 (paid at front desk if group >8)
- Full kitchen + parking + laundry + BBQ + hot tub + heated pool + sauna + Roam bus passes
- Listing URL: airbnb.com/rooms/660655534983361756

**Cost math at realistic scenarios:**
| Scenario | Total | Per person | Per person/night |
|---|---|---|---|
| Full trip, ~10 nights peak 10 / avg ~8.5 | ~$15,500 | varies | ~$164 |
| P1 only, 5 nights, 10 people | ~$7,775 | ~$778 | ~$155 |
| P2 only, 5 nights, 9 people | ~$7,650 | ~$850 | ~$170 |

**Cap-bust check (post Sahil-solo correction):** P1 max = 2 confirmed + 7 TBD + Dhanush nights 3-5 = **10 at cap, not over**. Listing is viable for single-Airbnb full-trip plan.

**Budget tier shift if this listing wins** (vs Canmore baseline of $125-145/person/night):
- P1 only baseline: $1,750-1,900 (vs $1,600 doc baseline)
- P2 only baseline: $1,900-2,050 (vs $1,750)
- Full trip baseline: $3,100-3,300 (vs $2,800)

**Canmore value alternative (Option B):**
"2BR MTN Chalet w/ POOL & Hot Tub: Prime Loc-BBQ-AC" — entire townhouse in Canmore, 5-min walk downtown, 20 min to Banff townsite, 1-min walk to Roam bus stop
- Sleeps 8 hard cap | 2 BR / 5 beds / 2 baths
- Master King (private, ensuite) + 2nd BR with 2 Doubles (shared, 4 people) + Sofa bed in living room
- 4.92 stars, 130 reviews, Guest Favorite, Superhost (Franco, 6 yrs)
- $709/night base flagged "lower than usual" — realistic peak July ~$900-1,000/night → ~$131/person/night at sleeps-8 max
- Includes Banff Pass + pool + hot tub + parking + full kitchen + A/C
- **Cheapest sleeps-8 Will found.** Works ONLY if 2+ TBDers skip P1 (sleeps-8 cap).

**Decision rule between A vs B at Sunday call:**
- If P1 lands 9-10 → must pick Option A (Banff in-park, sleeps-10)
- If P1 lands ≤8 → either works; B saves ~$200-300/person vs A; A wins on icon proximity

**Deliverables READY to send:**
1. Group chat kickoff message — drafted, ready to paste into Messenger. Drives Saturday-night phase commits from Miguel+Saya, Jeffrey, Charlie, Justin, James, Sahil. Includes flattened budget ranges (half/full trip) + GDoc link placeholder.
2. Doc artifact — full restructured trip doc drafted (overview, headcount, budget w/ rental cars, how-numbers-built, both Airbnb options, transportation, Sunday call agenda, open logistics). Ready to paste into empty GDoc.
3. Text to Elena — cost breakdown drafted (Option B $3,000 combined, Option A $3,240 combined including rental car share).

**Open action items:**
1. Send kickoff message + drop GDoc link
2. Talk to Elena tonight (have the cost breakdown text ready)
3. Book PHX→YYC flight this weekend — target ~$450 with fare alerts
4. URGENT: book Moraine Lake shuttle reservation now (window already open since 4/15/26)
5. Track phase commits Saturday → Sunday 7:30pm PST call locks
6. Post-call: book Airbnb (Option A or B based on headcount), assign booking lead + payment method, lock rental car reservations
7. Group passport check (valid through 7/13/26)
8. Group dinner reservations
9. Day-by-day itinerary skeleton (drafted, ready as Sunday-call strawman)

**Status of Elena's attendance:** TBD as of 6/12 → reconsidering 6/12 PM. Bailed at $3,510 baseline (Will+Elena). Cook+cut path lands at $2,670 combined (Option B Canmore) or $2,910 (Option A in-park) — $600-900 cheaper than what made her bail. Decision pending Elena's review of full breakdown. If she joins, needs 1 private queen room (impacts Option B sleeping config — only 1 private King master available).

**Trip-shape decision LOCKED (6/12):** Banff icons trip (Moraine Lake, Lake Louise, Banff Gondola, Lake Agnes, Johnston Canyon). Base in Banff/Canmore corridor — Invermere ruled out (~2h each way to Banff = 4h/day driving overhead, kills daily icon access).

---

## 2026-06-10 — Modular meal-prep pattern (the working design)

**The pattern**: cook once, fork at the plate. Three layers — protein, bulk veg, carb — bulk-cooked, then each person assembles their bowl with different ratios + different add-ons:

| Layer | Will (cut) | Elena (palatable) |
|---|---|---|
| Protein | Same portion (~5 oz lean) | Same portion (~5 oz) |
| Bulk veg | 2x volume (fills the plate) | 1x normal |
| Carb | 1/3 portion or skip | Full portion |
| Fat adds | Skip — low-cal sauces only | Cheese / avocado / oil / sour cream / butter |
| Flavor lift | Acid + heat + herbs (salsa, hot sauce, lime, cilantro, vinegar) | Fat + richness (parmesan, feta, olive oil, butter, tahini) |

**Encoded in recipes.json today** (no schema change — dual assembly captured in `notes` + `recipe_steps`):
- **#28 Modular Bittman Chinese Steamed Chicken Bowl** — converted from 3-srv Elena-only to 10-srv `for: both`. Will gets bok choy/spinach stir-fry bulk + 0.3 cup rice + light scallion-sauce drizzle; Elena gets 0.75 cup rice + full scallion-sauce pour. Cucumber salad SHARED. KBBQ #19 stays as Will-only gochujang option.
- **#31 Modular Slow-Cooker Chicken + Sheet-Pan Veg + Rice (NEW)** — 10 srv, `for: both`. Will gets 2 cups veg + 0.3 cup rice + sriracha/hot sauce; Elena gets 1 cup veg + 0.75 cup rice + avocado/Greek yogurt/cheese. **Salsa SHARED** (Elena wants it too — not a low-cal Will sub).
- **#32 Modular Mediterranean Lemon Chicken + Roasted Veg + Tzatziki Fork (NEW)** — 10 srv, `for: both`. Merged the Mediterranean (Set 4) + Greek lemon chicken (Set 6) ideas per Will's brief — uses lean chicken instead of salmon for the Mediterranean profile. Will gets 2 cups veg + tzatziki only; Elena gets 1 cup veg + farro + pita + feta + olives + olive oil drizzle. Tzatziki SHARED (nonfat Greek yogurt — creaminess without fat).

**Rejected from the brainstorm**: ground turkey tacos (not interesting), lean beef chili (no).

**Salmon Mediterranean**: NOT done as a modular — Will wanted leaner protein for that profile, so #32 is chicken-based. Salmon stays as #26 canned salmon/hummus toast (M3 quick lunch).

**Open**: 6 more modular sets could be added later (sheet-pan salmon w/ low-cal dressing fork, stuffed peppers, etc.). Hold for now — let these 3 prove out over 2-3 cycles before expanding.

**System work still pending (deferred)**: cycle YAML schema upgrade for forked-slot expression; `coverage.py` per-eater serving counts. Modular recipes currently report 10 servings total — Will and Elena each take 5. Coverage today treats it as "10 srv pool" which is correct enough.

---

## 2026-06-10 — Dual-track meal planning (Will cut + Elena palatability)

**Architecture decision**: Will's cut-optimized recipes stay intact; Elena's palatability-driven preferences get parallel/forked recipes, not in-place modifications to Will's.

**Mechanism**: Recipes get a `for` field — values: `"will"`, `"elena"`, `"both"` (default if unset = both).
- `"both"` — single shared prep, both eat the same
- `"will"` — Will-preferred when forked (Elena uses her variant in this slot)
- `"elena"` — Elena-preferred when forked (Will uses his own variant)

**Today's deltas to `meal-planning/data/recipes.json`**:
- `#18 Alfredo` — creaminess upgrades (4% cottage cheese flex, 1/3 reduced-fat cream cheese, milk 10→6 oz, blend 90 sec full smooth, more pasta water buffer). Stays `"both"` — Will's macros barely affected (~+15-20 cal/srv).
- `#25 Chipotle` — fresh toppings flagged SERVE-TIME ONLY in instructions (avocado/Greek yogurt/salsa/cilantro/lime stay separate from Tupperware). Stays `"both"`.
- `#19 KBBQ` — tagged `"for": "will"` because Elena flagged the gochujang chicken marinade as too heavy.
- **NEW #28 Bittman Chinese Steamed Chicken + Cucumber Salad** — `"for": "elena"`, Will-compatible (leaner than KBBQ). Elena's replacement protein for #19 slot.
- **NEW #29 Goat Cheese + Crackers Snack Plate** — `"for": "elena"`, M3 light option Elena requested. Not cut-optimized; Will alternative for same slot = #26 salmon hummus toast.
- **NEW #30 Strawberry Protein Shake** — `"for": "both"`, M1 or M3. Cut-friendly base (skim + whey + frozen strawberries) + optional Elena richer variant notes (whole milk + banana + Greek yogurt) inline.

**Still TODO (cycle-level changes)**:
- `cycles/*.yaml` schema needs a per-slot fork structure when Will and Elena eat different recipes — e.g., slot M4 Tue = `{will: 19, elena: 28}` instead of single recipe ID. Defer to next system-fix sprint.
- `coverage.py` needs to track per-eater servings when slots are forked. Defer.
- `grocery.py` aggregation already handles arbitrary recipe list (no change needed).

**For now**: Will picks recipes per cycle the old way (single recipe per slot) but can intentionally pick Elena-preferred recipes for slots where she cares. The forked-slot YAML upgrade unlocks "Will eats #19, Elena eats #28 on the same Tue night" — needs work.

---

## 2026-06-10 — Zone of Genius sector pick IN PROGRESS (Solo Track)

**Decision (in flight)**: Initial 4-sector pick (pool, pest, janitorial, irrigation) widened to ~10-12 candidate sectors after Will pushed back ("not sure those are the best fit, stay even more open to start"). Scrape-broad / outreach-focus architecture remains: scrape all candidates (marginal cost negligible), focus Elena apprenticeship + Walking Billboard + 100/50/10/1 outreach on TOP 2-3 based on (a) scrape yields per sector, (b) Elena's gut response to actual lead lists.

**Current ranked candidate menu** (final pick pending Will's add/drop):
1. HOA management — Elena program mgmt bullseye, 5,000+ Phoenix HOAs
2. Water treatment / softener service — Elena water differentiator
3. MSP / IT managed services — Will tech + AI angle
4. Specialty distribution (B2B niche) — Will SCM home turf
5. Office plant care / interior landscaping — Underrated niche
6. Mat rental services — Boring B2B recurring
7. Document destruction routes — Premium recurring, compliance growth
8. Window cleaning commercial routes — B2B recurring
9. Pool service routes — High sourcing volume
10. Pest control routes — Recurring rev king (despite saturation)
11. Vending / micro-market routes — Semi-absentee bullseye
12. Coffee/water service routes — Boring B2B recurring

**Geographic scope**: Phoenix metro core 5 cities (Phoenix, Mesa, Scottsdale, Chandler, Tempe). Radii capture Gilbert/Glendale/Peoria/Surprise via overlap.

**Licensure stance**: OK if seller or hired employee holds operator license. Doesn't gate ownership.

**Dropped (post-broader review)**: HVAC, plumbing, electrical (deal size + contractor licenses); property management residential (capital + AZ real estate license); compliance/regulatory consulting (hard to source); landscape/lawn care (commodity pricing).

**Files updated (initial checkpoint)**:
- `context/acquisition.md` Track 2 section — IN PROGRESS, candidate menu published
- `sourcing/apify-input-solo-template.json` — populated with initial 4 sectors (60 strings); will widen to final list once Will picks
- Inbox capture (this entry)

**Unblocks backlog**:
- #5 apify-scrape-solo — partially unblocked; awaiting final sector list before scrape
- #7 elena-apprenticeship — still pending top-2-3 narrowing post-scrape

**Next move**: Will picks final ~8-12 sector list from the candidate menu → I update Apify config → Will runs scrape → enrich.py --mode solo → per-sector yield review + Elena gut response → narrow to top 2-3 for apprenticeship/outreach focus.
