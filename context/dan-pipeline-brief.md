# Dan Pipeline Brief — Modernized Sourcing Output

**For the 30-min Dan reactivation call. One-pager.**
Track 1 (Dan-partnered): acquire an established, AI-enabled-able **accounting / bookkeeping / tax-strategy firm with a fractional-CFO / advisory upgrade path** in Phoenix metro ($500k–$1M revenue), modernize the recurring back-office + advisory work with AI. (This is Dan's named target per `context/dan-thesis.md`: *"accounting / tax strategy firms with an upgrade path to fractional CFO / consulting."*)

Source files: `sourcing/leads-ranked-dan.csv` (Maps-only score) → `sourcing/leads-dan-reranked.csv` (Dan-thesis re-rank) → `sourcing/leads-dan-shortlist.md` (top 25). Scoring logic in `sourcing/enrich.py` + `sourcing/rank_dan.py`.

---

## Headline

The modernized sourcing pipeline produced **505 candidate firms** — bookkeeping / accounting / payroll / tax / CPA / financial-services shops in the **Phoenix metro**, after de-duping a Google Maps scrape and dropping national chains (H&R Block, Jackson Hewitt, Liberty Tax, ADP, Paychex, Intuit) and out-of-state results.

- **Geo:** Phoenix metro, 20mi (sector LOCKED to accounting/bookkeeping per the one-sector-one-city rule).
- **Contactability:** **505 of 505 have a website**; **496 have a phone**. (No emails in the Maps export — those come from per-firm research before each outreach.)
- **How scored:** a **Maps-only acquisition-fit heuristic (0–100)** — review-count sweet spot tuned to the Dan deal size (30–150 reviews = "established but not too big for the $1M cap"), rating health, website + phone presence, and a revenue-type signal from the firm's name/category.

**What the score knows vs. what it does NOT know — say this out loud to Dan.** The score is a *sourcing heuristic, not a qualification.* It ranks which firms look most like an established, owner-operated shop with recurring/advisory revenue worth a phone call. It knows nothing about the financials, the owner's age or sell-motivation, staff count/tenure, client concentration, or net margin. **All of that comes only after contact** — captured via the Frazier walls-down first conversation, then run through `/deal-eval` against the deal box. The pipeline produces the *call list*, not the *buy list*.

---

## The Dan-thesis re-rank — the actual insight

The first pass (Maps-only score) treated every accounting and tax shop roughly the same. The re-rank (`rank_dan.py`, `dan_fit_score`) up-weights the revenue models Dan's thesis actually wants and down-weights the one it doesn't:

- **UP — recurring back-office + advisory:** bookkeeping, payroll, ongoing/monthly accounting, controller/CFO, **and tax-strategy / tax-advisory / fractional-CFO** (Dan's explicitly named high-conviction target — ongoing advisory work, *not* a filing-season spike).
- **DOWN — seasonal tax-PREP:** pure Jan–Apr filing-season commodity work (income-tax prep, "tax service" storefronts) with no ongoing book.

> **Important distinction (this is the nuance):** the re-rank does **not** down-weight "tax" wholesale. *Tax strategy / advisory* is recurring and is a core part of Dan's thesis — it scores at the top tier alongside bookkeeping. Only *seasonal tax-prep* (one-time filing-season work) is demoted. Example: "K&R Strategic Partners, CPAs & Tax Advisors" ranks **#8** (tax-advisory, recurring); a pure "Income Tax Service" storefront lands near the bottom.

**The composition shift in the top 25:**

| Top 25 | Recurring-leaning (incl. tax-strategy/advisory) | Seasonal tax-prep |
|---|---|---|
| Before re-rank (Maps-only) | 22 | 3 |
| After re-rank (Dan-fit) | **25** | **0** |

The **top 10 is now 100% recurring/advisory** firms; the entire top 25 is recurring-leaning. (Full-list revenue-class mix: **204 recurring · 93 mixed · 132 unknown · 76 seasonal-tax**, out of 505.)

**Why this matters for the thesis.** The whole bet is *AI modernization of a recurring back-office + a higher-margin advisory layer*. A seasonal tax-prep shop spikes in Jan–Apr and goes quiet — no steady book of monthly work to modernize, revenue one-time/relationship-dependent rather than contractual. A bookkeeping/payroll/ongoing-accounting firm **or a tax-strategy/advisory practice** carries a recurring client relationship (the deal box wants ≥70% recurring revenue) — exactly where AI automation of the production grind compounds month over month, and exactly the profile that survives the "is the revenue still there in 12 months without the owner present?" test. The re-rank moves those firms to the front of the call list.

---

## Top tier to work first

Point Dan at `sourcing/leads-dan-shortlist.md` (top 25). The **top 10 to call first** — all recurring/advisory, all with website + phone:

1. Elite Bookkeeping Solutions — 34 reviews, 5.0
2. Bookkeeping Done Right, LLC. — 99 reviews, 5.0
3. Numbers Matter Accounting & Bookkeeping LLC — 49 reviews, 5.0
4. Old Glory Bookkeeping — 31 reviews, 4.9
5. dA Bookkeeping LLC — 55 reviews, 5.0
6. Better Ways Accounting & Tax — 104 reviews, 4.9
7. Arrington Accounting Services — 31 reviews, 4.6
8. K&R Strategic Partners, CPAs & Tax Advisors — 78 reviews, 5.0 *(tax-strategy/advisory — Dan's named target; CPA-branded, see deal-structure flag)*
9. Sapphire Bookkeeping & Accounting — 30 reviews, 4.3
10. FreedomFromAccounting — 46 reviews, 5.0

Beyond the top 10, the shortlist runs through #25 (Get Smart Accounting, SJS Accounting, Mesa Heights Accounting, Journey Payroll & HR, etc.). **19 firms score dan_fit ≥90; 46 score ≥80; 109 score ≥70** — plenty of depth below the top 10 once outreach starts attriting.

> **Two top-25 firms to eyeball before dialing:** the heuristic reads from names, so verify revenue model on the website first. (1) Any firm whose name leans "tax" but classed recurring — confirm it's advisory/ongoing, not seasonal prep. (2) CPA-branded firms (4 in the top 25) carry the AZ-51% flag below.

---

## The funnel — this is the "100"

Codie's **100 / 50 / 10 / 1**:

- **100 — contact.** The 505-firm ranked list is the top of the funnel; we work the ~top tier first. (505 is well past Codie's 100; the score tells us *what order* to dial.)
- **50 — qualify.** Firms that take the Frazier walls-down call and clear the three pre-financial questions (what does the owner do daily / who'd still be there if they left / is the revenue there in 12 months without them).
- **10 — diligence.** Firms that pass `/deal-eval` against the deal box — 30%+ margin, SDE floor $286k→$367k price-scaled, ≤4× multiple, recurring ≥70%, seller open to financing.
- **1 — LOI.** The one we structure and close.

The pipeline only manufactures the **100**. Qualification, diligence, and the LOI all happen *after* contact — they are not in this list.

---

## AZ 51%-CPA-ownership flag (deal-structure)

AZ law: non-CPAs can't exceed 49% ownership IF the firm does audits/reviews OR has "CPA" in the name. The pipeline tags CPA-branded firms because they carry that constraint.

- **CPA-branded across the full list:** **176 of 505 (~35%).** Roughly two-thirds of the pipeline is non-CPA-branded (bookkeeping/payroll/accounting), which **sidesteps the constraint entirely** under the "avoid CPA-only services / no CPA in name" path.
- **In the top 10:** only **1** is CPA-branded (K&R, #8). **In the top 25:** **4.** The recurring-revenue re-rank naturally skews toward non-CPA bookkeeping shops — the cleaner ownership path.

**Read:** the constraint is real but **not the gating factor** for most of the call list. Where a CPA-branded firm is otherwise a strong fit, that's where Dan's CPA-cover/licensure path (below) does its work; where it's a non-CPA bookkeeping firm, the constraint doesn't bind. Note the tension: Dan's highest-conviction *tax-strategy/advisory* targets are more likely to be CPA-branded — so the advisory-tier firms are exactly where Dan's CPA path matters most.

---

## What we need from Dan

Tied to the partnership split in `context/dan-thesis.md` (Dan = CEO / strategy + capital + external network). Keeping this factual — Dan's actual commitments are his to make on the call:

- **CPA cover / licensure path.** Which of the three AZ-51% paths are we defaulting to — Dan pursues licensure, retain CPAs as equity partners, or avoid CPA-only services and bias the call list toward the ~65% non-CPA-branded firms? Dan's current licensure status is an open item to confirm. *[Will fills: Dan's 2026 CPA-licensure status — started / decided against / conditional on the partnership]*
- **Sector emphasis — confirm with Dan.** Does Dan still see the target as *accounting/tax-strategy with a fractional-CFO/consulting upgrade* (his 2025 framing), or has his thinking shifted? The re-rank assumes the 2025 framing. *[Will confirms on the call — this brief should not assume Dan's current view is unchanged.]*
- **Network intros.** Dan as connector into the AZ CPA / financial-services operator world — both for off-market seller leads (the 4A/accountant-referral channel) and for the retained-CPA relationships if we go that path.
- **Capital.** Dan's investor-network role to raise outside capital alongside Elena's equity contribution — together reducing the SBA debt required and de-risking the Amazon-exit timing (the precise fix to the 2025 stall). *[Will fills: Elena's equity contribution $ and time/week; updated 3-person partnership-percentage model — both load-bearing and currently UNKNOWN]*

---

### Key stats used (all from the pipeline files; nothing invented)

- 505 ranked candidate firms (`leads-ranked-dan.csv` / `leads-dan-reranked.csv`, 505 data rows each).
- Contactability: 505/505 website, 496/505 phone, 0 emails in export.
- Revenue-class mix: 204 recurring · 93 mixed · 132 unknown · 76 seasonal-tax.
- Top-25 shift: 22→25 recurring-leaning; 3→0 seasonal-tax. Top 10 = 100% recurring/advisory.
- Dan-fit score bands: 19 firms ≥90 · 46 ≥80 · 109 ≥70.
- CPA-branded: 176/505 full (~35%); 1/10 top-10; 4/25 top-25.
- Scoring: Maps-only heuristic (`enrich.py`, Dan mode) → recurring+advisory-weighted re-rank (`rank_dan.py`). Sourcing heuristic, NOT qualification.

> **Re-rank correction note (2026-06-14):** the first cut of `rank_dan.py` lumped all "tax" as seasonal and promoted a wealth-management/AUM firm (JBrooks) on a stray "advisor" token. Fixed: tax-*strategy*/advisory now scores recurring (Dan's named target); pure tax-*prep* is demoted; wealth-management/AUM is carved out of the "advisor" recurring signal (JBrooks moved #7 → #117). Pending Will's confirmation that the accounting/tax-strategy framing still matches Dan's current thinking.
