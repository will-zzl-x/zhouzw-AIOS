# Sector Evaluation Framework — Solo Track

Created 2026-06-08. For Will + Elena to use during the Zone of Genius re-read exercise.

---

## Purpose

The Solo track of the dual-track acquisition strategy (`context/acquisition.md`) requires picking a sector. This doc gives a structured way to evaluate candidate sectors against (a) your combined Zone of Genius, (b) deal box constraints, (c) sourcing reality.

**Use this when:** you sit down together for 30-45 min to narrow from the long candidate list to top 2-3 sectors.

**Output:** top 2-3 sectors locked in `context/acquisition.md` Track 2 section + Apify scrape configuration in `sourcing/apify-input-solo-template.json` ready to run.

---

## The pre-work (do separately, then compare)

Each of you, separately, score each candidate sector across 5 dimensions on 1-5 scale. Then compare notes.

**Candidate sectors** (from `context/acquisition.md` Track 2 list):
- Light commercial services (cleaning, janitorial)
- HVAC services
- Plumbing services
- Electrical services
- Pool service routes
- Landscape / lawn care routes
- Pest control routes
- Specialty distribution (B2B niche)
- Compliance / regulatory services
- Property management

---

## The 5 evaluation dimensions

For each sector, score 1-5 on:

### 1. Skill fit (your combined Zone of Genius)
- Does Will's SCM / ops / AI / process background apply?
- Does Elena's CFO/COO / modeling / engineering / process background apply?
- Would you be the kind of operators sellers want to sell to?

Score 1: Total mismatch, you'd be learning from zero
Score 5: Direct skill application, you have operator-relevant experience

### 2. Interest fit (could you do this for 5-10 years?)
- Would you read industry publications voluntarily?
- Could you talk to operators / customers without it feeling like a chore?
- Is the daily work itself bearable-to-enjoyable?

Score 1: Sounds boring or distasteful
Score 5: Genuinely interested, would do for free briefly

### 3. Recurring revenue potential
- Is the customer relationship contractual / recurring?
- Or is it project-based / one-off?
- Codie's filter: ≥70% recurring revenue strongly preferred.

Score 1: Mostly project / one-off
Score 5: Pure subscription / contract / route-based recurring

### 4. Codie deal-box fit
- Within $300-500k purchase price range?
- Likely SDE $253-286k achievable at that size?
- 30%+ margin typical for the sector?
- Owner-operated firms common (vs PE-backed roll-ups)?

Score 1: Sector dominated by PE, multiples too high, low margins
Score 5: Fragmented mom-and-pop market, easy to find sub-$500k deals

### 5. Sourcing reality (can you actually find deals?)
- Apify scrape would surface real candidates?
- Walking Billboard (Elena's apprenticeship) translates to sourcing?
- Off-market signals (retirements, burnouts) detectable?
- Brokers covering this space, or off-market only?

Score 1: Hard to source, dominated by exclusive networks
Score 5: Plenty of fragmented operators, easy to start conversations

---

## Scoring sheet template

Fill in separately, then compare:

| Sector | Skill fit | Interest fit | Recurring revenue | Deal-box fit | Sourcing reality | Total | Notes |
|---|---|---|---|---|---|---|---|
| Light commercial services |  |  |  |  |  |  |  |
| HVAC services |  |  |  |  |  |  |  |
| Plumbing services |  |  |  |  |  |  |  |
| Electrical services |  |  |  |  |  |  |  |
| Pool service routes |  |  |  |  |  |  |  |
| Landscape routes |  |  |  |  |  |  |  |
| Pest control routes |  |  |  |  |  |  |  |
| Specialty distribution |  |  |  |  |  |  |  |
| Compliance / regulatory |  |  |  |  |  |  |  |
| Property management |  |  |  |  |  |  |  |

Total = sum (max 25). Top 2-3 sectors with highest combined scores get carried forward.

---

## Hard filters (auto-disqualify, regardless of score)

A sector gets dropped if ANY of these are true:

1. **Licensure required for ownership** (CDL, plumbing contractor license, electrical license, etc.) where neither of you holds it and licensing takes >12 months
2. **Physical presence required >1×/month** post-2027 move out of AZ (route businesses with no manager option fail this)
3. **Customer concentration risk inherent to the sector** (e.g., government contract specialists with single-agency exposure)
4. **Margin profile structurally below 30%** (retail, restaurants — already excluded)
5. **Neither of you can imagine introducing yourself as "I own X" at a dinner party** — this is the operator-identity gut check, score it honestly

---

## Decision protocol

1. **Each score separately** (you and Elena, 15 min each). Don't peek at the other's scores.
2. **Compare scores** (15 min). Look for:
   - Sectors where you both score 4+ → strong candidates
   - Sectors where you score very differently → discuss what's behind the gap
   - Sectors that one of you would auto-disqualify but the other wouldn't → discuss
3. **Apply hard filters** to drop disqualified sectors
4. **Lock top 2-3 sectors** with rough rationale per sector
5. **Update `context/acquisition.md`** Track 2 section with the picks
6. **Update `sourcing/apify-input-solo-template.json`** with search terms for picked sectors (3-5 terms per sector × 8 cities = 24-40 total search strings)
7. **Run the Apify scrape** with the new config → enrich with `--mode solo`

---

## Tie-breaker / honest gut check

If two sectors score similarly, **default to the sector Elena finds more interesting**, since her apprenticeship-to-operator transition path makes her engagement load-bearing for the solo track. Sourcing edge comes from her being IN the industry — boredom kills that signal.

Will's role in the operator phase is more systems / strategy / AI — that travels across sectors more easily than Elena's daily operator engagement. So her interest weight wins ties.

---

## Output once complete

After this exercise, the following AIOS files update:

| File | Update |
|---|---|
| `context/acquisition.md` | Track 2 section: locked sectors with rationale |
| `sourcing/apify-input-solo-template.json` | searchStringsArray populated with sector-specific terms |
| `journals/main-street-accelerator.md` | Note which modules to prioritize given chosen sector |
| `backlog.md` | New row: "Elena apprenticeship/shadow exploration in [chosen sectors]" |

Then this doc gets a status update at top: "COMPLETED [date]: sectors picked = X, Y. Apify Solo-track config updated."
