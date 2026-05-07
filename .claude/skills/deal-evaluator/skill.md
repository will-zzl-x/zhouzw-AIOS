---
name: deal-evaluator
description: Deal Evaluator — paste a business listing and get an instant go/no-go based on Will's hard filters and deal box. Triggered by "evaluate this deal", "run this through the filters", pasting a BizBuySell or Acquire.com listing, or "/deal-eval".
---

## Goal

Run a pasted business listing through Will's acquisition filters. Return: go/no-go + one paragraph reasoning. No fluff. No maybes without specifics.

## Reads

- `context/financial-state.md` — deal box, hard filters, return targets, operator model
- `references/hormozi.md` — offer/value lens (if available)
- `references/sanchez.md` — Codie Sanchez framework (if available)

## Deal Box (from financial-state.md)

**Capital:** $70k available. SBA 7(a) + seller financing acceptable.
**Price range:** $200k–$500k acquisition price.
**SDE target:** $80k–$200k/year.
**Multiple:** 2–3× SDE.
**Minimum cash-on-cash return:** 20%+ after debt service.
**Operator model:** Semi-absentee. Manager runs day-to-day. Will's time: 10–15 hr/week.
**Location:** Remote preferred. Phoenix-area physical acceptable if manageable. Relocatable preferred.
**Timeline:** Close in 2026. Must be stable/sellable/remotely manageable by late 2027 move.

## Hard Filters (Auto-Disqualify)

Any of these → immediate NO:
1. Requires owner to hold a license (CDL, contractor, etc.)
2. Owner-operator only — no clear path to semi-absentee
3. Single customer >30% revenue concentration
4. Declining revenue 2+ consecutive years without clear explanation
5. Acquisition price >$500k without exceptional seller financing

## Steps

1. Read `context/financial-state.md`.
2. Parse the listing Will pasted: business type, asking price, SDE/cash flow, revenue trend, location, owner involvement, reason for sale, anything else stated.
3. **Hard filter check first.** If any hard filter is triggered, stop and output:
   ```
   NO — [which filter] 
   
   [One sentence on what specifically triggered it and why it's disqualifying.]
   ```
4. If no hard filters triggered, run the full evaluation:

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

5. Output:
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
