---
name: acquisition
description: Acquisition Project — 5-mode skill covering deal capture, deal logging, inbox scanning, outreach drafting, and weekly deal review. Triggered by "capture acquisition notes", "log this deal", "scan deals", "draft outreach", "acquisition review", or "/acquisition [mode]".
---

## Goal

Make Will's acquisition search systematic. Capture learning from books/podcasts. Log deals seen with verdicts. Scan Gmail for deal alert emails. Draft broker outreach. Review what's in the pipeline.

## Reads

- `context/acquisition.md` — playbook, deal box, hard filters, business type ranking, outreach scripts, lessons learned
- `context/financial-state.md` — deal box and hard filters (source of truth)
- `references/sanchez.md` — Codie Sanchez framework
- `journals/acquisition-log.md` — running deal flow log

## Writes

- `context/acquisition.md` — when capturing new notes or lessons
- `journals/acquisition-log.md` — when logging a deal

---

## Mode: `capture`

**Triggers:** "capture acquisition notes", "from Codie", "I read something about", pasting book passages, pasting podcast notes

**Action:**

1. Parse what Will shared — is it framework notes, a specific concept, outreach script material, or a lesson learned?
2. Identify which section of `context/acquisition.md` it belongs in:
   - Framework/concepts → Codie Sanchez Framework section
   - Business type notes → Business Types section
   - Outreach → Outreach Scripts section
   - Post-deal lesson → Lessons Learned section
3. Append to the right section. Don't rewrite — append.
4. Confirm: "Added to [section] in context/acquisition.md."

**Rules:**
- Never overwrite existing content — append only.
- If it's unclear which section, ask one clarifying question before writing.
- If it's a direct Codie quote, note the source.

---

## Mode: `log-deal`

**Triggers:** "log this deal", "log a deal", "saw a listing", pasting a BizBuySell or Acquire.com listing URL or text

**Action:**

1. If a URL is given and Playwright MCP is available: fetch the listing page and extract: business type, asking price, SDE/cash flow, revenue trend, location, owner involvement.
2. If pasted text: parse the same fields.
3. Run hard filters from `context/financial-state.md`. If triggered → verdict is NO.
4. If no hard filters triggered → run quick eval (price range, SDE multiple, operator model fit).
5. Append to `journals/acquisition-log.md`:

```
**[Date]** | [Source] | [Business type] | [Asking price]
URL: [link or "pasted listing"]
SDE: $[X]/yr | Multiple: [X]x | Revenue trend: [growing/flat/declining]
Verdict: GO / NO / CONDITIONAL — [one-sentence reason]
Action taken: evaluated only
```

6. Confirm the log entry. If it's a CONDITIONAL or GO, ask: "Do you want to draft broker outreach for this one?"

**Rules:**
- Don't ask for information that's missing — state what's missing and give a verdict based on available data.
- Hard filter hits get an immediate NO with the specific filter named.
- Verdict must match the math — don't call it GO if the numbers don't support it.

---

## Mode: `scan-inbox`

**Triggers:** "scan deals", "what's new in the inbox", "weekly deal scan", "scan for deals"

**Action:**

1. Use Gmail MCP to search inbox for deal alert emails. Search terms:
   - From: bizbuysel.com, acquire.com, quietlight.com, empireflippers.com
   - Subject contains: "new listing", "deal alert", "business for sale", "matches your criteria"
   - Label: "Acquisitions" (if Will has set this up)
2. For each email found: extract business type, asking price, and any SDE/revenue data from the subject/preview.
3. Run hard filters against each. Filter out anything that clearly fails.
4. Report only the ones that pass hard filters:

```
**[Business type]** — $[asking price] | [Source]
[One sentence: what stands out, what to verify]
→ [Link or email subject for reference]
```

5. If nothing passes: "No deals this week that cleared the hard filters."
6. If there are passing deals: "X deal(s) passed filters. Run `/acquisition log-deal [URL]` to evaluate and log."

**Rules:**
- Don't report deals that fail hard filters — just surface the count ("3 emails scanned, 1 passed").
- If Gmail MCP isn't connected: say so clearly and tell Will what to set up.
- Don't evaluate in depth here — that's `/deal-eval` or `log-deal`. Just triage.

---

## Mode: `outreach`

**Triggers:** "draft outreach", "draft a broker email", "write to the seller", "draft a cold email"

**Action:**

1. Read `context/acquisition.md` — outreach scripts section and deal box.
2. Ask Will: which deal or business type is this for? (Or pull from context if he just logged a deal.)
3. Draft an outreach message. Tone: direct, credible, prepared. Not eager. Not a template.

**Structure for broker outreach:**
- Who Will is (brief — supply chain background, capital ready, proven buyer criteria)
- Why this listing (specific — reference the business, not generic interest)
- What Will needs (IM, financials, owner call) — specific ask
- Credibility signals (proof of funds available, SBA pre-approval status if applicable)

**Structure for cold owner outreach:**
- Open with something specific to their business (shows research)
- Why Will is a serious buyer (capital, operator model, timeline)
- Ask for a simple response: "Would you be open to a 15-minute call?"
- No pressure, no lowball anchoring in first contact

4. Output the draft. Will sends — AIOS does not send.
5. Save to `context/acquisition.md` Outreach Scripts section if Will says it's worth keeping as a template.

**Rules:**
- AIOS drafts. Will sends. Never trigger any send action.
- No generic templates — every outreach references something specific.
- Keep it short: 5 sentences max for cold outreach, 8 max for broker email.

---

## Mode: `weekly-review`

**Triggers:** "acquisition review", "/acquisition review", called from `/weekly-reflection`

**Action:**

1. Read `journals/acquisition-log.md` — this week's entries.
2. Read `context/acquisition.md` — where Will is in the 3/9/12 timeline.
3. Surface:
   - How many deals logged this week?
   - Any CONDITIONALs or GOs that need follow-up action?
   - Any broker relationships initiated?
   - Are there deals that were logged without action taken?

4. Output:

```
**Acquisition Week Review — [Date]**

Deals logged: [X]
  GO: [X] | CONDITIONAL: [X] | NO: [X]

[If CONDITIONALs or GOs with no follow-up:]
Follow-up needed:
→ [Business type + one action]

[Phase status: Learn / Find+Close / Stabilize]
[Days until search window: X]

[If no deals logged:]
Deal flow drought — nothing logged this week. Source check: when did you last check BizBuySell / Acquire.com?
```

5. If Will is still in the Learn phase and hasn't been logging anything: note that mock deal evals via `/deal-eval` count as learning even if no real deal is pending.

**Rules:**
- No fluff. Numbers first.
- If nothing's in the log: say so directly and ask what happened.
- Don't summarize what Will already knows — surface what needs action.
