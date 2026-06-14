#!/usr/bin/env python3
"""equity_model.py — 3-person partnership equity calculator (Will / Elena / Dan).

Stdlib only. No AI, no tokens. A transparent, weighted-contribution model for the
Will + Elena + Dan bookkeeping/accounting acquisition partnership (Track 1).

WHAT THIS IS:
  A scaffold to *reason about* an equity split before the Frame B conversation.
  It is NOT a decision. It produces ILLUSTRATIVE numbers from ILLUSTRATIVE inputs.

WHAT THIS IS NOT:
  Real equity. Every cash figure, role weight, and strategic weight below is a
  clearly-marked EXAMPLE pending Will + Elena + Dan confirmation. The load-bearing
  unknowns (Elena's cash, the partners' hours, Dan's investor-capital terms,
  Dan's CPA-licensure status) are [NEEDS FILL] items only the partners can answer.

METHODOLOGY (three contribution dimensions):
  1. CAPITAL      — cash / equity injected at close (each partner's share of total
                    partner cash).
  2. ROLE/TIME    — ongoing operating role + hours committed (CEO / COO-CTO / CFO).
  3. STRATEGIC    — network, CPA-cover access, deal sourcing, investor relationships.

  Each partner gets a 0-1 score on each dimension. The three dimensions are weighted
  (DIM_WEIGHTS, must sum to 1.0). A partner's blended score is the weighted sum of
  their three dimension scores. Equity % = a partner's blended score / total blended
  score across all partners. So the split is always normalized to 100%.

  Capital scores are derived automatically from the cash inputs (each partner's cash
  / total partner cash). Role and strategic scores are entered directly as 0-1
  judgments per the dan-thesis.md role map.

Usage:
  python equity_model.py                 # prints example split + Elena-cash sensitivity
"""

# ----------------------------------------------------------------------------
# DIMENSION WEIGHTS — how much each contribution dimension drives equity.
# EXAMPLE values, pending Will + Elena + Dan confirmation. Must sum to 1.0.
# Rationale for the example: capital and ongoing operating role are co-primary
# (this is an owner-operated small business, not a passive holdco), strategic
# value is real but secondary. Will should tune these in the conversation.
# ----------------------------------------------------------------------------
DIM_WEIGHTS = {
    "capital":   0.40,   # EXAMPLE — pending confirmation
    "role":      0.40,   # EXAMPLE — pending confirmation
    "strategic": 0.20,   # EXAMPLE — pending confirmation
}

# ----------------------------------------------------------------------------
# CASH INJECTION (capital dimension) — LOCKED inputs (Will, 2026-06-14).
# NOTE: Dan puts in NO personal cash. His capital role is RAISING OUTSIDE INVESTOR
# capital — which is NOT his personal equity and does NOT count in this dimension
# (those investors take their own equity, separate from the 3-founder split / a
# cap-table topic for the call). Dan's value here is strategic (capital-raising +
# CPA cover + network), captured in STRATEGIC below — consider performance-linking
# his equity to capital actually raised rather than a flat grant.
# ----------------------------------------------------------------------------
WILL_CASH  = 50_000    # LOCKED: ~$50k from the $70k S&ME fund (keep ≥$20k reserve post-close).
ELENA_CASH = 50_000    # LOCKED: ~$50k to match Will, from Elena's $100k taxable (leaves ~$50k
                       # taxable + $44k earmarked as bridge/home runway — do NOT drain further).
DAN_CASH   = 0         # LOCKED: Dan brings $0 personal cash; he RAISES outside capital instead.

# ----------------------------------------------------------------------------
# ROLE / TIME scores (0-1) — ongoing operating role + hours committed.
# Updated to Will's 6/14 framing: "operator will be us to start." Will + Elena
# are BOTH heavy front-line operators early (Elena full-time-as-needed, tapering
# after ~Year 1 / once a manager is in). Dan is strategy/network, lighter day-to-day.
#   Will  = COO/CTO blend (AI/tech modernization + ops leadership + M&A sourcing).
#   Elena = CFO + co-operator, FULL-TIME EARLY (financial controls + process + QC + P&L).
#   Dan   = CEO-ish (strategy / direction / board-level), lighter day-to-day hours.
# Relative weights; they need not sum to 1 (the model normalizes). Tune on the call.
# ----------------------------------------------------------------------------
WILL_ROLE  = 0.80   # heavy operator (tech + ops + M&A)
ELENA_ROLE = 0.78   # heavy co-operator, full-time early (tapers after Yr1/manager hire)
DAN_ROLE   = 0.35   # strategy/direction, lighter day-to-day

# ----------------------------------------------------------------------------
# STRATEGIC scores (0-1) — network, CPA-cover access, deal sourcing, investor
# relationships. EXAMPLE judgments, pending confirmation.
#   Dan  = densest AZ professional-services network, CPA-cover access, investor
#          relationships (raises outside capital) — the strategic anchor.
#   Will = Frazier/Apify sourcing pipeline ownership + AI-modernization thesis.
#   Elena = process/QC rigor is operational, not strategic-network; scored low here.
# ----------------------------------------------------------------------------
WILL_STRAT  = 0.55   # EXAMPLE — sourcing pipeline + AI thesis
ELENA_STRAT = 0.20   # EXAMPLE — limited external network for THIS sector
DAN_STRAT   = 0.90   # EXAMPLE — CPA network + investor relationships + connector


def capital_scores(will_cash, elena_cash, dan_cash):
    """Each partner's capital dimension score = their cash / total partner cash."""
    total = will_cash + elena_cash + dan_cash
    if total <= 0:
        # Degenerate case (no partner cash) — split capital dimension evenly so
        # the model still runs; flag it loudly.
        return {"Will": 1 / 3, "Elena": 1 / 3, "Dan": 1 / 3}, total
    return {
        "Will":  will_cash / total,
        "Elena": elena_cash / total,
        "Dan":   dan_cash / total,
    }, total


def normalize(scores):
    """Normalize a dict of relative scores so they sum to 1.0."""
    total = sum(scores.values())
    if total <= 0:
        n = len(scores)
        return {k: 1 / n for k in scores}
    return {k: v / total for k, v in scores.items()}


def equity_split(will_cash, elena_cash, dan_cash, weights=DIM_WEIGHTS):
    """Return each partner's equity % from the three weighted dimensions."""
    cap, cap_total = capital_scores(will_cash, elena_cash, dan_cash)

    role = normalize({"Will": WILL_ROLE, "Elena": ELENA_ROLE, "Dan": DAN_ROLE})
    strat = normalize({"Will": WILL_STRAT, "Elena": ELENA_STRAT, "Dan": DAN_STRAT})

    blended = {}
    for p in ("Will", "Elena", "Dan"):
        blended[p] = (
            weights["capital"]   * cap[p]
            + weights["role"]    * role[p]
            + weights["strategic"] * strat[p]
        )
    # blended already sums to 1.0 (each dimension normalized, weights sum to 1),
    # but normalize again defensively against weight rounding.
    equity = normalize(blended)
    return equity, {"capital": cap, "role": role, "strategic": strat, "cap_total": cap_total}


def pct(x):
    return f"{x * 100:5.1f}%"


def print_split(label, will_cash, elena_cash, dan_cash):
    equity, detail = equity_split(will_cash, elena_cash, dan_cash)
    cap = detail["capital"]
    print(f"\n{label}")
    print(f"  cash inputs (EXAMPLE):  Will=${will_cash:,}  Elena=${elena_cash:,}  Dan=${dan_cash:,}"
          f"  (total partner cash ${detail['cap_total']:,})")
    print(f"  {'Partner':<7} {'capital%':>9} {'role%':>8} {'strat%':>8} {'-> equity':>11}")
    for p in ("Will", "Elena", "Dan"):
        print(f"  {p:<7} {pct(cap[p]):>9} {pct(detail['role'][p]):>8} "
              f"{pct(detail['strategic'][p]):>8} {pct(equity[p]):>11}")
    return equity


def main():
    print("=" * 72)
    print("3-PERSON PARTNERSHIP EQUITY MODEL — Will / Elena / Dan")
    print("ILLUSTRATIVE — pending Will + Elena + Dan confirmation. NOT real equity.")
    print("=" * 72)
    print(f"\nDimension weights (EXAMPLE): "
          f"capital={DIM_WEIGHTS['capital']:.0%}  "
          f"role={DIM_WEIGHTS['role']:.0%}  "
          f"strategic={DIM_WEIGHTS['strategic']:.0%}")
    print("Role scores (EXAMPLE 0-1):  "
          f"Will={WILL_ROLE} Elena={ELENA_ROLE} Dan={DAN_ROLE}")
    print("Strategic scores (EXAMPLE 0-1):  "
          f"Will={WILL_STRAT} Elena={ELENA_STRAT} Dan={DAN_STRAT}")

    # Base case — example cash inputs from the top of the file.
    base = print_split(
        "BASE CASE (example cash inputs)",
        WILL_CASH, ELENA_CASH, DAN_CASH,
    )

    # Sensitivity — what happens if Elena's cash DOUBLES (the Scenario B lever:
    # more Elena equity reduces required debt). Everything else held constant.
    sens = print_split(
        "SENSITIVITY — Elena's cash DOUBLES (Scenario B lever), all else held",
        WILL_CASH, ELENA_CASH * 2, DAN_CASH,
    )

    de = (sens["Elena"] - base["Elena"]) * 100
    print(f"\n  -> Doubling Elena's example cash moves her equity by "
          f"{de:+.1f} pts ({pct(base['Elena'])} -> {pct(sens['Elena'])}).")
    print("     (Magnitude depends entirely on the EXAMPLE weights/scores above —"
          " confirm with partners.)")
    print("\nReminder: replace every EXAMPLE input with a confirmed number before"
          " treating any % as real.")


if __name__ == "__main__":
    main()
