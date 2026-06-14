# Sector Evaluation Framework — Solo Track

Created 2026-06-08. Updated 2026-06-13 to match the post-6/10 12-sector candidate menu and the scrape-broad-narrow-after architecture.

For Will + Elena to use AFTER the Solo-track Apify scrape returns ranked outputs.

---

## Purpose

The Solo track of the dual-track acquisition strategy (`context/acquisition.md`) requires narrowing the 12-sector candidate menu down to top 2-3 sectors for Elena apprenticeship + Walking Billboard + 100/50/10/1 outreach focus.

**Architecture (locked 2026-06-10):** scrape broad first (all 12 sectors), narrow after seeing real per-sector yields + Elena's gut response to actual lead names. This doc is the **secondary narrowing tool** — applied AFTER the scrape, in concert with the ranked outputs.

**Use this when:**
- The Solo-track Apify scrape has finished and `leads-ranked-solo.csv` exists
- You and Elena sit down together for 30-45 min to lock the top 2-3 sectors

**Output:** top 2-3 sectors locked in `context/acquisition.md` Track 2 + Elena apprenticeship target list + main-street-accelerator priorities updated for chosen sector.

---

## The 12 candidate sectors (from `context/acquisition.md` 2026-06-10)

| # | Sector | Why on the list |
|---|---|---|
| 1 | HOA management services | Elena program management bullseye + 5,000+ Phoenix HOAs |
| 2 | Water treatment / softener service | Elena water credential; Phoenix hard-water market |
| 3 | MSP / IT managed services | Will tech/AI angle, monthly recurring king |
| 4 | Specialty distribution (B2B niche) | Will SCM home turf |
| 5 | Office plant care / interior landscaping | Underrated niche, high margins, quiet competition |
| 6 | Mat rental services | Boring = less competition, sub-$500k common |
| 7 | Document destruction / shredding routes | Simple ops, premium recurring, compliance-driven growth |
| 8 | Window cleaning commercial routes | Recurring B2B, sub-$500k common |
| 9 | Pool service routes | High sourcing volume, Elena water angle |
| 10 | Pest control routes | Highest recurring rev structure |
| 11 | Vending / micro-market routes | Semi-absentee bullseye |
| 12 | Coffee/water service routes | Boring B2B recurring |

All 12 already pass acquisition.md's hard filters (no licensure gap, absentee-capable, ≥30% margins achievable, no inherent customer concentration).

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
- Operator-identity gut check: could you say "I own X" at a dinner party without flinching?

Score 1: Sounds boring or distasteful
Score 5: Genuinely interested, would do for free briefly

### 3. Recurring revenue potential
- Is the customer relationship contractual / recurring?
- Or is it project-based / one-off?
- Codie's filter: ≥70% recurring revenue strongly preferred.

Score 1: Mostly project / one-off
Score 5: Pure subscription / contract / route-based recurring

### 4. Codie deal-box fit (Solo track $300-500k)
- Within $300-500k purchase price range?
- Likely SDE $253-286k achievable at that size?
- 30%+ margin typical for the sector?
- Owner-operated firms common (vs PE-backed roll-ups)?

Score 1: Sector dominated by PE, multiples too high, low margins
Score 5: Fragmented mom-and-pop market, easy to find sub-$500k deals

### 5. Sourcing reality (from scrape data + Elena access)
**This dimension changes after the scrape returns.** Pre-scrape: estimate. Post-scrape: replace your estimate with the actual yield band:

| Ranked-leads count | Score |
|---|---|
| 100+ viable leads | 5 |
| 60-99 viable leads | 4 |
| 30-59 viable leads | 3 |
| 15-29 viable leads | 2 |
| <15 viable leads | 1 (drop on sourcing reality) |

Plus a +1 bonus if Elena has a credible Walking Billboard angle into the sector (water credential for water treatment, engineering peers in property mgmt-adjacent, etc.).

---

## Scoring sheet template

Fill in separately, then compare:

| Sector | Skill fit | Interest fit | Recurring rev | Deal-box fit | Sourcing reality | Total | Notes |
|---|---|---|---|---|---|---|---|
| HOA management |  |  |  |  |  |  |  |
| Water treatment / softener |  |  |  |  |  |  |  |
| MSP / IT managed |  |  |  |  |  |  |  |
| Specialty distribution (B2B) |  |  |  |  |  |  |  |
| Office plant care |  |  |  |  |  |  |  |
| Mat rental |  |  |  |  |  |  |  |
| Document destruction |  |  |  |  |  |  |  |
| Window cleaning commercial |  |  |  |  |  |  |  |
| Pool service routes |  |  |  |  |  |  |  |
| Pest control routes |  |  |  |  |  |  |  |
| Vending / micro-market |  |  |  |  |  |  |  |
| Coffee / water service |  |  |  |  |  |  |  |

Total = sum (max 25 + sourcing bonus). Top 3 sectors with highest combined scores get carried forward.

---

## Hard filters (auto-disqualify, regardless of score)

A sector gets dropped if ANY of these are true:

1. **Licensure required for ownership** where neither of you holds it and licensing takes >12 months
2. **Physical presence required >1×/month** post-2027 move out of AZ (route businesses with no manager option fail this)
3. **Customer concentration risk inherent to the sector** (e.g., government contract specialists with single-agency exposure)
4. **Margin profile structurally below 30%**
5. **Neither of you can imagine introducing yourself as "I own X" at a dinner party** — operator-identity gut check, score honestly
6. **NEW (sourcing-reality filter):** <15 viable leads in the Apify ranked output after enrichment + filter. Sector fails the 100/50/10/1 sourcing math.

---

## Decision protocol

1. **Run the scrape first.** Solo template at `sourcing/apify-input-solo-template.json` → Apify → save to `sourcing/leads/solo-YYYY-MM-DD.json` → `python enrich.py leads/solo-YYYY-MM-DD.json --mode solo --out leads-ranked-solo`.
2. **Pull per-sector yield counts** from the ranked CSV (filter by `category` column).
3. **Each score separately** (you and Elena, 15 min each). Don't peek at the other's scores. Score dimensions 1-4 from gut + Zone of Genius; replace dimension 5 (sourcing reality) with the actual scrape yield band.
4. **Compare scores** (15 min). Look for:
   - Sectors where you both score 4+ on dimensions 1-2 (skill + interest) → strong candidates
   - Sectors where you score very differently → discuss what's behind the gap
   - Sectors that one would auto-disqualify but the other wouldn't → discuss
5. **Eyeball the actual lead names** in the top sectors' ranked output (top 30 per sector). Elena's gut response to real operators / niches IS load-bearing data — sourcing edge comes from her being IN the industry, so boredom kills that signal.
6. **Apply hard filters** to drop disqualified sectors
7. **Lock top 2-3 sectors** with rough rationale per sector
8. **Update files** per "Output once complete" below

---

## Tie-breaker / honest gut check

If two sectors score similarly, **default to the sector Elena finds more interesting**, since her apprenticeship-to-operator transition path makes her engagement load-bearing for the solo track. Sourcing edge comes from her being IN the industry — boredom kills that signal.

Will's role in the operator phase is more systems / strategy / AI — that travels across sectors more easily than Elena's daily operator engagement. So her interest weight wins ties.

---

## Output once complete

After this exercise, the following AIOS files update:

| File | Update |
|---|---|
| `context/acquisition.md` | Track 2 section: locked sectors with rationale, scrape yields cited |
| `journals/main-street-accelerator.md` | Note which modules to prioritize given chosen sectors |
| `backlog.md` | New row: "Elena apprenticeship/shadow exploration in [chosen sectors]" |
| `context/sector-evaluation-framework.md` (this doc) | Status update at top: "COMPLETED [date]: sectors picked = X, Y, Z" |
