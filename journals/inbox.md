# Inbox — mid-week captures, cleared each Sunday reflection

<!-- Mid-week captures go here. Cleared each Sunday. -->

*Cleared June 7, 2026 reflection. Prior captures resolved: SoCal trip (Jun 19–21) fully booked + archived to backlog-done; pregnancy thread closed negative; meal-system script fixes (grocery.py, defrost.py) ranked into backlog. Carry-forward: build Apify scrape (work-quest unlock) + flip on Brave Shorts blocker (life-quest unlock).*

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
