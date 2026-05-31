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

## Deal Box (canonical: `context/acquisition.md`)

**Active sequencing (May 31, 2026):** Scenario B Codie-honest — Elena scales W-2 to ~20 hr/week **at close**, Year 1 operator unpaid; 12-month manager-hire trigger ($55k market rate) moves business to truly-absentee Year 2. Underwriting bakes in operator salary so the manager hire is structurally affordable, not a future cash-flow shock.

**Capital:** $70k available; $50k effective down payment; ≥$20k reserve post-close. SBA 7(a) ~10.5% / 10-yr + seller financing preferred; standby seller note unlocks stretch range.
**Price range:** $500k–$700k clean / $700k–$1.0M stretch (with standby seller note) / **$1.0M hard ceiling**.
**Pre-debt CF floor:** $213k/yr ($101k Will + $57k Elena + $55k operator).
**SDE floor:** **$286k at $500k price → $367k at $1.0M** (price-scaled; pre-debt CF + debt service).
**Revenue floor:** $953k+ (at 30% margin).
**Margin floor:** 30%+ — pass below.
**Multiple:** ≤4× SDE hard ceiling; prefer 2–3×.
**Operator model:** Year 1 — Elena 20 hr/week, Will 5–10 hr/week, no outside manager. Year 2 — $55k manager hired at month 12 trigger after 90-day continuous-CF test; Elena steps out.
**Location:** Arizona preferred. Remote-manageable by late-2027 mandatory.
**Timeline:** Close in 2026 (search/LOI window ~Aug 2026). Stable + remote-manageable by late 2027.

**Price-bound math (SBA 7(a) @ 10.5% / 10-yr / $50k down):**

| Deal price | Loan | Debt service | Required SDE | Multiple |
|---|---|---|---|---|
| $500k | $450k | $73k | $286k | 1.75× |
| $600k | $550k | $89k | $302k | 1.99× |
| $700k | $650k | $105k | $318k | 2.20× |
| $800k | $750k | $122k | $335k | 2.39× |
| $1.0M | $950k | $154k | $367k | 2.72× |

## Hard Filters (Auto-Disqualify)

Any of these → immediate NO:
1. Requires Will or Elena to hold a license (CDL, contractor's, CPA)
2. Owner sole operator, no staff, full-time — and Elena can't step into the work directly
3. Single client >25% revenue concentration
4. Declining revenue 2+ consecutive years without clear explanation
5. Acquisition price >4× SDE (hard multiple ceiling)
6. Acquisition price >$1.0M (hard absolute ceiling regardless of multiple — cash position binds)
7. Net margin <30%
8. SDE below the price-bound floor (look up in price-bound math table; $286k at $500k → $367k at $1M)
9. Business can't afford a $55k operator by month 12 — fails "buying a job" test
10. Requires physical presence from Will or Elena >1×/month (post-2027 move killer)
11. Owner unwilling to discuss any seller financing

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

   **Price / Return Check:**
   - Does asking price fit $200k–$500k?
   - Implied multiple: [price ÷ SDE]
   - Estimated debt service (SBA 7(a), 10-yr, ~7%): ~[monthly payment]
   - Net cash flow after debt service: ~[amount/year]
   - Cash-on-cash return on $70k down: ~[%]

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
