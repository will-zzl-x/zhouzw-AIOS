# Elena Conversation Brief — the 3 numbers that unblock the Dan reach-out

**Purpose:** A focused aid for Will + Elena to make the decisions that are the *only* thing
standing between the drafted Frame B message and sending it to Dan. Everything else in the
Dan packet is built and verified (`context/dan-frame-b-message.md`, `dan-pipeline-brief.md`,
`dan-equity-model.md`). These three answers fill the `[Will fills]` placeholders.

**Why this matters:** the entire credibility of the Dan reactivation rests on Elena's
contribution — it's the literal fix to the 2025 stall ("couldn't service $500k–$1M of debt
while W-2 at Amazon"). The message can't go until the contribution is *concrete*, not directional.

Created 2026-06-14. Frameworks to hold: `references/perkins.md` (Die With Zero — you're already
past coast FIRE), `references/schnarch.md` / `references/perel.md` (this is a shared-risk decision,
hold it as two differentiated adults choosing together, not one selling the other).

---

## Decision 1 — Elena's role in the Dan-acquired firm

**Will's current answer (2026-06-14):** *Full-time at first as needed, then tapering to whatever
level and hours she wants over time.*

This is cleaner than either older doc and it **resolves a contradiction** the planning docs carried:
- `acquisition.md` (May 31) said "Elena = Year-1 operator, ~20 hr/wk, unpaid."
- `goals/elena-scale-back.md` (LOCKED June 8) said "Elena exits engineering mid-2027, **fully out —
  not a 20hr scale-back**."

The reconciliation: Elena exits **engineering** fully (per the locked plan), goes **full-time into the
acquired firm early** while it needs the most hands (CFO + ops as required), and **tapers** as the
12-month manager hire + AI-systems buildout reduce the load — toward the truly-absentee Year-2 end state.
That's consistent with *both* docs and is a stronger story for Dan: not "my fiancée will grind 20 unpaid
hours," but "Elena is leaving her career to go all-in on this, with full availability up front."

**What to confirm together:**
- Is "full-time at first" right, or does Elena want a ceiling from day one (e.g. never more than ~30 hr/wk)?
- Roughly when does the taper start — tied to the manager hire (month 12), or a fixed date she wants?
- Does the underwriting still bake in the $55k operator salary regardless? **Yes — keep it.** It's what
  makes the taper real instead of "buying a job." Elena full-time early just means that salary line is
  covered by her unpaid labor in Year 1, then funds the manager when she steps back.

> **Upstream sensitivity — CLOSED 2026-06-14.** The late-May pregnancy-possibility question is
> resolved (officially negative). It no longer gates Elena's role or the timeline. The full-time-early
> → taper plan and the late-2027/early-2028 close can be locked without it hanging over them.

---

## Decision 2 — Elena's equity-cash contribution at close

**Status: deliberately NOT modeled yet** (per Will, 2026-06-14). Left as `[Will + Elena decide]` in the
message + equity model. Here's the trade-off space so you can set it together.

**Sources available** (from `context/financial-state.md`):
- Elena's taxable: **$100k** (the natural acquisition-equity source; `acquisition.md` already notes it
  "may bridge if larger")
- Elena's earmarked fund: **$44k** (wedding/car/misc — mostly spoken for; wedding is ~$40k total, partly
  Elena-funded)
- Will's S&ME fund: **$70k** → ~$50k effective down + $20k reserve (already the baseline)

**The two things Elena's cash drives — debt reduction and her equity share** (Will $50k, Dan $50k
illustrative personal equity, 40/40/20 weighting; $600k example deal):

| Elena cash | Total equity injection | SBA loan (~$600k deal) | Illustrative equity split (W / E / D) |
|---|---|---|---|
| **~$25k** (conservative) | $125k | ~$475k | 40% / 26% / 34% |
| **~$50k** (matches Will) | $150k | ~$450k | 37% / 31% / 32% — near-balanced |
| **~$80k** (aggressive) | $180k | ~$420k | 35% / 35% / 30% |

*(Numbers are ILLUSTRATIVE — Dan's personal equity is a placeholder and may be debt not equity; weights
are unconfirmed. Run `python sourcing/equity_model.py` with real inputs once you decide.)*

**The tension to talk through:**
- **More Elena cash → less debt → smaller monthly note → less pressure on the Amazon-exit timing.** This
  is the direct mechanism that fixes the 2025 stall. Every $1 of equity is ~$1 less SBA principal at
  ~10.5%/10yr.
- **But** her $100k taxable is also the **bridge fund** for the mid-2027 (Elena exits) → late-2027/2028
  (acquisition close) income gap — the locked plan budgets a worst-case $12–24k draw from it.
- **And** it's partly the home-down-payment source for the post-2027 Dallas/Chicago move.
- **Safety check (`elena-scale-back.md`):** you're already **~$650k over** the Die-With-Zero need at a
  $100k lifestyle. The contribution decision is a liquidity/sequencing question, **not** a "can we
  afford to retire" question. That should lower the stakes on going somewhat aggressive.

**Recommended framing (not a decision):** ~$50k "matches Will" is the clean default — it makes the
partnership feel equal three ways, leaves Elena ~$50k taxable + the $44k earmarked for bridge/home, and
still cuts the loan meaningfully. Go to ~$80k only if you both want maximum debt reduction and are
comfortable with tighter bridge liquidity.

**LOCKED 2026-06-14: Will $50k / Elena $50k / Dan $0 personal cash.** Will asked whether to put in more.
**Recommendation: hold at $50k/$50k — do not add more now.** Reasons: (1) $100k combined is already
*above* the SBA 10% equity floor across the clean $500–700k range (only the $1M stretch binds at exactly
10%); (2) the constraint is liquidity sequencing, not safety — you're ~$650k over your Die-With-Zero need,
but Elena's $100k taxable is also the mid-2027→close bridge fund + post-2027 home down payment, so $50k
keeps the right reserve; (3) **Dan raising outside capital is the *designed* lever for anything above the
clean range** — self-funding a bigger injection undercuts the whole reason Dan's a partner. Make "Dan
raises $X" + a **seller standby note** the gap-fillers, not more of your own cash. Revisit only in the
narrow case of a $1M stretch deal where Dan can't raise AND the seller won't carry. Equity on these
inputs: **~Will 43 / Elena 39 / Dan 18** (`context/dan-equity-model.md`).

---

## Decision 3 — AZ 51% CPA cover (RESOLVED 2026-06-14: Dan not licensing)

**Dan is not becoming a CPA** (confirmed 6/14 — he runs multiple businesses with operators reporting to
him; licensure isn't on the table). So path 1 is dead. AZ law: non-CPAs can't exceed 49% ownership if the
firm does audits/reviews OR has "CPA" in the name. **Two live paths:**

1. ~~Dan pursues CPA licensure~~ — **ruled out.**
2. **Retain a CPA** as a minority equity holder of the regulated entity (Dan's network *supplies* one;
   that CPA is NOT a founder). Use this if you target a CPA-branded / attest firm.
3. **Buy a non-CPA bookkeeping/accounting firm** — sidesteps the rule entirely. **~65% of the 505 leads
   qualify**; 9 of the top-10 re-ranked are non-CPA-branded. **Likely the default.**

**What to confirm with Dan:** not *his* status (settled), but which path fits the kind of firm you go
after — and whether his network can supply a retained CPA if you want the CPA-branded/advisory tier. The
Frame B bullet (d) is already reframed to this question.

> **Note from the re-rank:** Dan's highest-conviction target (tax-strategy/advisory with a fractional-CFO
> upgrade) skews more CPA-branded. Since Dan isn't licensing, that tier needs path 2 (retained CPA via his
> network); the plain-bookkeeping tier needs no cover at all. The path interacts with which leads you work first.

---

## After the conversation — what to do (or hand back to AIOS)

1. Fill the 3 placeholders in `context/dan-frame-b-message.md` (Elena cash+source+timing, Elena
   role/hours framing, Dan CPA status).
2. Run `python sourcing/equity_model.py` with the real cash inputs → paste the split into
   `dan-equity-model.md` for the call.
3. Strip **all** `[Will fills...]` brackets from the message before sending.
4. Send via the channel in the message's Delivery notes. **AIOS never sends — Will sends.**

The leads, the brief, the equity scaffold, and the re-rank are all done and pushed. These three answers
are the whole remaining critical path.
