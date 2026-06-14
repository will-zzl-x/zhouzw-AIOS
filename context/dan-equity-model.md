# 3-Person Partnership Equity Model — Will / Elena / Dan

Re-models the original 4/22/2025 partnership-percentages spreadsheet (which assumed a
2-person Will+Dan structure) into the 3-person **Will + Elena + Dan** structure that
Scenario B requires. Flagged as a gap in `context/dan-thesis.md` ("needs re-modeling to
a 3-person Will+Elena+Dan structure before the Frame B message goes").

**This is a DRAFT framework, not a decision.** Every hard number below is either a
clearly-marked EXAMPLE or a `[NEEDS FILL]` / `[Will fills: ...]` placeholder. The
load-bearing inputs (Elena's cash, each partner's hours, Dan's investor-capital terms,
Dan's CPA-licensure status, and the agreed dimension weights) can only come from
Will + Elena + Dan. Do not present any percentage here as a settled split.

Calculator: `sourcing/equity_model.py` (stdlib, runs in seconds, all inputs at the top).

---

## 1. The three contribution dimensions

Equity in an owner-operated small-business acquisition should track what each partner
actually puts in — not a handshake guess. Three dimensions capture it:

| Dimension | What it measures | How it's scored |
|---|---|---|
| **(a) Capital / cash injection** | Equity cash each partner contributes at close. Reduces the SBA debt required — the core Scenario B lever. | Each partner's cash ÷ total partner cash (auto-derived in the model). |
| **(b) Role / ongoing operating time** | Day-to-day operating load: function ownership + hours/week, weighted across the Year-1 ramp and Year-2 steady state. | Direct 0-1 judgment per partner, from the dan-thesis.md role map. |
| **(c) Strategic value** | Network access, CPA-cover for the AZ 51% rule, deal sourcing, investor relationships that raise outside capital. | Direct 0-1 judgment per partner. |

These are deliberately separate. A partner can be light on cash but heavy on role
(Will), or light on day-to-day hours but the strategic anchor (Dan). Collapsing them
into "who wrote the biggest check" is exactly the mistake the 2-person 4/22/2025 model
risked — and it under-weights Elena, whose contribution is cash **and** operating role.

---

## 2. Partner role map (from `context/dan-thesis.md`)

| Partner | Title | Capital | Role / time | Strategic |
|---|---|---|---|---|
| **Dan** | CEO-ish | Brings own + raises outside capital via investor network (terms TBD — equity vs. debt) | Strategy / direction / board-level; lighter day-to-day | **Strategic anchor**: AZ CPA network, CPA-cover access, investor relationships, connector |
| **Will** | COO/CTO blend | S&ME-fund equity portion (TBD) | **Heaviest Year-1 operator**: AI/tech modernization (the thesis bet) + ops leadership + M&A sourcing | Frazier/Apify sourcing pipeline + AI-modernization thesis |
| **Elena** | CFO | `[NEEDS FILL]` cash — the Scenario B debt-reduction lever | Heavy operator: financial controls, process/SOP buildout, QC, firm P&L; ~20 hr/wk Year 1 | Process/QC rigor (operational, not external-network) |

**Small-partnership constraint (operating principle):** no fourth founder. Sector
expertise, CPA licensure, and bookkeeping production come in via hired/retained/
referenced relationships — NOT equity at the founders' table. A retained CPA (AZ 51%
path #2) and the Year-2 GM are **not** founders; see §5.

---

## 3. Methodology

1. Assign each dimension a **weight** (`DIM_WEIGHTS`), summing to 1.0. The example
   below treats capital and role as co-primary and strategic as secondary, because
   this is an owner-operated business (operating role matters as much as the check)
   rather than a passive holding company.
2. Score each partner **0-1 on each dimension**. Capital scores are auto-derived from
   the cash inputs (a partner's cash ÷ total partner cash). Role and strategic scores
   are entered directly from the §2 role map.
3. Each dimension's scores are **normalized** to sum to 1.0 across partners (so the
   dimension answers "of this contribution type, what share is each partner's?").
4. A partner's **blended score** = weighted sum of their three normalized dimension
   scores: `equity_i = Σ_d (weight_d × score_{i,d})`.
5. Blended scores already sum to ~1.0; normalize once more defensively → **equity %**.

The formula in one line:

```
equity_i = w_capital · (cash_i / Σcash)
         + w_role    · (role_i / Σrole)
         + w_strat   · (strat_i / Σstrat)
```

All three `w` are tunable in the conversation. The point of the model is to make the
trade-offs **visible and adjustable**, not to assert a single answer.

---

## 4. Scenarios — LOCKED inputs (Will, 2026-06-14) + sensitivity

> **Inputs now LOCKED to Will's 6/14 decision** (Will $50k · Elena $50k · Dan **$0** personal
> cash). The split below is the model's output on those inputs. It is still a STARTING POINT
> for the call, not a settled grant — the role/strategic scores and dimension weights remain
> tunable, and Dan's % in particular is a negotiation (see note). Do not treat as final equity.

**Dimension weights:** capital 40% · role 40% · strategic 20%.
**Role scores (0-1):** Will 0.80 · Elena 0.78 (full-time co-operator early, tapers after Yr1/manager) · Dan 0.20 (advisory only).
**Strategic scores (0-1):** Will 0.60 · Elena 0.20 · Dan 0.50 (network + guidance; NOT CPA cover, NOT primary capital-raiser).

> **Dan reframed to ADVISORY 2026-06-14.** Dan is not becoming a CPA and is not the primary capital-raiser — his contribution is advice / guidance / network. So his role score dropped 0.35→0.20 and strategic 0.90→0.50 (CPA-cover and linchpin-capital premiums removed). This is the honest economic anchor for the negotiation in `context/dan-equity-negotiation.md`.

### LOCKED base case — Will $50k · Elena $50k · Dan $0 (advisory)

Cash inputs: Will $50k · Elena $50k · Dan **$0** (total partner equity $100k → ~$500k SBA loan on a $600k deal).

| Partner | capital% | role% | strat% | → equity |
|---|---|---|---|---|
| **Will** | 50.0% | 44.9% | 46.2% | **~47.2%** |
| **Elena** | 50.0% | 43.8% | 15.4% | **~40.6%** |
| **Dan** | 0.0% | 11.2% | 38.5% | **~12.2%** |

### Sensitivity — if Elena goes to $100k (drains her taxable; NOT recommended)

Cash inputs: Will $50k · Elena $100k · Dan $0. All else held.

| Partner | capital% | role% | strat% | → equity |
|---|---|---|---|---|
| Will | 33.3% | 44.9% | 46.2% | **~40.5%** |
| Elena | 66.7% | 43.8% | 15.4% | **~47.3%** |
| Dan | 0.0% | 11.2% | 38.5% | **~12.2%** |

### What this shows + the 50/50 question

- **The honest contribution split is ~Will 47 / Elena 41 / Dan 12.** Will + Elena hold ~88% combined — they bring **100% of the cash, all the operating work, and the entire pipeline.** Dan's ~12% is advisory value: guidance + network, no cash, no day-to-day, no CPA cover.
- **Dan asked for 50/50. On contribution, that's ~4× his ~12%** — and a flat "Dan 50 / Will 50" also erases Elena. **Do NOT default-accept it.** The play is to give Dan a "50/50" he can point to on a layer where it's fair: 50/50 on the **residual upside** (after Will+Elena's capital is returned-with-preferred and operators are paid market salaries), an **earn-up ladder** to 50% tied to capital raised, and/or 50/50 on the **next deal / platform** he helps capitalize. Full playbook + scripts: **`context/dan-equity-negotiation.md`**.
- **Why NOT push Elena to $100k:** the sensitivity makes her the majority owner (~47%) but drains her $100k taxable that's also the bridge fund + home down payment. Hold $50k/$50k; fill gaps with Dan's raise + a seller standby note (`context/dan-elena-decision-brief.md`).
- **Elena is a NAMED co-founder** — not folded into Will's half — in every structure. **Outside investors take their own equity**, separate from the founder split.

### Exact calculator output (for reproducibility)

```
========================================================================
3-PERSON PARTNERSHIP EQUITY MODEL — Will / Elena / Dan
ILLUSTRATIVE — pending Will + Elena + Dan confirmation. NOT real equity.
========================================================================

Dimension weights (EXAMPLE): capital=40%  role=40%  strategic=20%
Role scores (EXAMPLE 0-1):  Will=0.8 Elena=0.78 Dan=0.2
Strategic scores (EXAMPLE 0-1):  Will=0.6 Elena=0.2 Dan=0.5

BASE CASE (example cash inputs)
  cash inputs (EXAMPLE):  Will=$50,000  Elena=$50,000  Dan=$0  (total partner cash $100,000)
  Partner  capital%    role%   strat%   -> equity
  Will        50.0%    44.9%    46.2%       47.2%
  Elena       50.0%    43.8%    15.4%       40.6%
  Dan          0.0%    11.2%    38.5%       12.2%

SENSITIVITY — Elena's cash DOUBLES (Scenario B lever), all else held
  cash inputs (EXAMPLE):  Will=$50,000  Elena=$100,000  Dan=$0  (total partner cash $150,000)
  Partner  capital%    role%   strat%   -> equity
  Will        33.3%    44.9%    46.2%       40.5%
  Elena       66.7%    43.8%    15.4%       47.3%
  Dan          0.0%    11.2%    38.5%       12.2%

  -> Doubling Elena's example cash moves her equity by +6.7 pts ( 40.6% ->  47.3%).
     (Magnitude depends entirely on the EXAMPLE weights/scores above — confirm with partners.)

Reminder: replace every EXAMPLE input with a confirmed number before treating any % as real.
```

---

## 5. Open questions to resolve with the partners

Must be answered before any percentage here is treated as real:

1. **`[NEEDS FILL]` Elena's cash injection** — concrete $ amount, source, and whether
   it's a one-time injection at close or sustained. Drives the capital dimension and is
   the load-bearing number Dan will ask about. (`[Will fills: $E_cash equity at close]`.)
2. **`[NEEDS FILL]` Each partner's hours/week** — Year-1 ramp, Year-1 steady-state,
   Year-2 absentee phase. Governs the role/time scores (currently EXAMPLE judgments).
3. **`[NEEDS FILL]` Dan's investor capital — equity or debt?** If it's outside
   *investor* equity, those investors may need their own cap-table line and Dan's
   personal capital score is separate. If it's *debt* (a note), it should NOT count in
   the capital dimension at all — it's leverage, not partner equity. This materially
   changes Dan's %.
4. **`[NEEDS FILL]` Dan's CPA-licensure status as of 2026** — if Dan licenses (AZ path
   #1), the CPA-cover constraint resolves through a founder and his strategic score
   rises. If the deal uses a **retained CPA** (path #2), that CPA holds ≥51% of the
   *firm's* regulated entity but is **not a founder** on the partnership cap table —
   keep that line distinct from the three-way founder split.
5. **Founder vs. retained-CPA vs. staff cap-table lines** — three distinct buckets:
   (a) the three founders (this model), (b) any retained CPA needed for AZ 51%
   compliance, (c) the **Year-2 GM hired with an equity vest** ($55k operator-salary
   line in the Codie-honest box) — staff equity on a **vesting schedule**, carved from
   an option pool, NOT a founder grant. Decide whether the founder %s are pre- or
   post-pool dilution.
6. **Dimension weights** — the example 40/40/20 is a starting point, not agreed. If the
   partners decide capital should dominate (debt-reduction is the whole Scenario B
   thesis), raise the capital weight and Elena's/Dan's cash matters more.
7. **Vesting / cliff for the founders themselves** — given Will ramps out of Amazon on
   the late-2027 timeline, decide whether founder equity vests over the transition or
   is granted at close.

---

## Cross-references

- `context/dan-thesis.md` — strategic case, role split, the `[NEEDS FILL]` gaps this model closes
- `context/acquisition.md` — deal box, AZ CPA 51% law, Codie-honest math, operator model
- `sourcing/equity_model.py` — the calculator that produced §4
- Original 4/22/2025 2-person spreadsheet (Will+Dan) — superseded by this 3-person model
