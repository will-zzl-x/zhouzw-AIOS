---
name: deal-evaluator
description: Deal Evaluator — paste a business listing or provide a URL and get an instant go/no-go based on Will's hard filters and deal box. Triggered by "evaluate this deal", "run this through the filters", pasting a BizBuySell or Acquire.com listing or URL, or "/deal-eval [url]".
---

## Goal

Run a pasted business listing through Will's acquisition filters. Return: go/no-go + one paragraph reasoning. No fluff. No maybes without specifics.

## Reads

- `context/financial-state.md` — deal box, hard filters, return targets, operator model
- `references/hormozi.md` — offer/value lens (if available)
- `references/sanchez.md` — Codie Sanchez framework (if available)

## Deal Box (canonical: `context/acquisition.md`) — TWO-TIER as of 2026-07-12 annual review

**Deal #1 is the ACTIVE box.** The Scenario B box below it is now DEAL #2's box (2028+, on deal #1's track record). Evaluate current listings against DEAL #1 unless Will explicitly says "score this as a deal #2." Full principles: `context/acquisition.md` "Deal #1 Risk-Sizing Principles."

### DEAL #1 — Risk-Sized Box (ACTIVE — evaluate against this)

Deal #1's job: prove the muscle, cover its own debt, throw off real cash. NOT replace two salaries (that's gated on deal #2 / scale).

**Capital:** ONLY the S&ME fund is deal capital (house/retirement/emergency/wedding funds untouchable). **Max ~$50k cash in**, ≥$20k reserve stays in the fund.
**Price box:** **$150k–$300k.**
**SDE floor:** **≥$60k/yr** (NOT $286k — that's deal #2). At ≤3× that's $60–120k SDE across the price box.
**Revenue floor:** ≥$200k at 30%+ margin.
**Multiple:** ≤3× SDE.
**Debt:** seller note preferred (target ≥50% of price), SBA minimal or none. **DSCR ≥2.0×** — business SDE covers debt service twice over. (The $500k+ personal guarantee is what froze the 2025 search — respect it.)
**Freeze test (say it before any LOI):** "If this goes to zero we lose ≤$[cash-in]k of fund money, rebuilt in ~2 years of $2k/mo autos, touching nothing else." If that sentence doesn't freeze Will, the size is right.
**Operator model:** anywhere-operable (remote/digital or manager-run) by Dec 2027 — the late-2027 move breaks anything owner-present. Business affords a part-time manager (~$25–30k) by month 12.
**Recurring revenue:** ≥70%.
**Dan fit:** a $150–300k bookkeeping book of business fits this box AND the Dan thesis AND the anywhere-operable filter.

### DEAL #2 — Scenario B box (NOT active — for reference / explicit deal-#2 scoring only)

Price $500k–$700k clean / $1.0M hard ceiling; SDE floor $286k@$500k → $367k@$1M; revenue floor $953k+; pre-debt CF $213k; SBA 7(a) ~10.5%/10-yr. Full price-bound math in `context/acquisition.md`.

## Hard Filters (Auto-Disqualify) — DEAL #1 active thresholds

Any of these → immediate NO:
1. Requires Will or Elena to hold a license (CDL, contractor's, CPA)
2. Owner sole operator, no staff, full-time — and neither Will nor Elena can step into the work directly
3. Single client >25% revenue concentration
4. Declining revenue 2+ consecutive years without clear explanation
5. Acquisition price >3× SDE (deal #1 multiple ceiling)
6. Acquisition price >$300k (deal #1 box ceiling — a bigger deal is a deal-#2 conversation, not an auto-eval)
7. Net margin <30%
8. **SDE <$60k/yr** (deal #1 floor — NOT $286k; that floor is deal #2 only)
9. Requires cash-in >~$50k OR SBA debt with DSCR <2.0× (fails the risk-sizing principle)
10. Not anywhere-operable by Dec 2027 — requires physical presence from Will or Elena >1×/month
11. Owner unwilling to discuss any seller financing (deal #1 leans heavily on the seller note)

## Steps

1. Read `context/financial-state.md`.
2. **Determine input mode:**
   - **URL given:** Use Playwright MCP to fetch the listing page. Navigate to the URL, wait for page load, extract the visible listing text (business type, asking price, SDE/cash flow, revenue trend, location, owner involvement, reason for sale). If Playwright MCP is unavailable, ask Will to paste the listing text instead.
   - **Text pasted:** Parse directly.
3. Parse the listing: business type, asking price, SDE/cash flow, revenue trend, location, owner involvement, reason for sale, anything else stated.
4. **Hard filter check first.** If any hard filter is triggered, stop and output:
   ```
   NO — [which filter] 
   
   [One sentence on what specifically triggered it and why it's disqualifying.]
   ```
5. If no hard filters triggered, run the full evaluation:

   **Price / Return Check (deal #1):**
   - Does asking price fit $150k–$300k?
   - Implied multiple: [price ÷ SDE] — ≤3×?
   - Structure: seller note ≥50%? Cash-in ≤~$50k?
   - Estimated debt service on the note/loan + DSCR: [SDE ÷ annual debt service] — ≥2.0×?
   - Net cash flow after debt service: ~[amount/year]
   - Cash-on-cash return on cash-in: ~[%]
   - Run the freeze test explicitly: state the total-loss number.

   **Operator Model Check:**
   - Is semi-absentee realistic for this type of business?
   - Is there a manager in place or a clear hire path?
   - Does Will's 10–15 hr/week budget work?

   **Location / Transition Check:**
   - Relocatable before late 2027 move?
   - Phoenix-area: manageable if manager-dependent?

   **Qualitative Flags:**
   - Reason for sale: credible or suspicious?
   - Revenue trend: growing, flat, declining?
   - Customer concentration: diversified or concentrated?
   - Any stated risks or red flags in the listing?

6. Output:
   ```
   [GO / NO / CONDITIONAL GO]

   [One paragraph: what's compelling, what's the risk, what's the one thing to verify first if conditional. Specific numbers, not generalizations.]

   [If CONDITIONAL GO: "Ask seller: [the one question that would change the verdict]"]
   ```

## Rules

- Lead with the verdict. Don't bury it in caveats.
- Math must show your work — don't assert returns without the calculation.
- If the listing is missing key data (SDE, revenue trend), say what's missing and what the best-case / worst-case range implies.
- Don't evaluate based on what the business *could* be — evaluate what it *is* based on stated figures.
- One paragraph. Not a report.
