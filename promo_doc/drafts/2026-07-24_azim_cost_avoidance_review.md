<!-- DRAFT share-out for Parth Sheth (sheparth@) + AZIM team — cost-avoidance methodology
     review. LOCAL ONLY, no comms. Will reviews + sends. Purpose: put the midstream-reroute
     cost-avoidance number + method in front of AZIM for validation BEFORE it's quoted
     externally (promo doc, leadership). Source: _notes/azim_entitlement_ytd_deepdive_2026-07-21.md
     (the firmed rail-legs re-pull). Every number here traces to that deep-dive / the per-VRID TSV. -->

# AZIM Midstream Reroute — Cost-Avoidance Methodology, for AZIM Review

**From:** William Zhou (IPEX-ICT) · **To:** Parth Sheth + AZIM team · **Date:** 2026-07-24
**Ask:** sanity-check the methodology and the number below before I use it anywhere external. Where VLS/RRD can't price a leg, you're the authoritative source (AZIM billing / procurement IM lane rates) — flag anything that looks off.

---

## What this measures

The value of intercepting a 1P-IM load **while it's still on the rail leg** and diverting it to a taker that needs the work — versus letting it arrive and paying a full over-the-road (OTR) redirect afterward. We've been running this with you since WK24; this is the first full accounting of what it's saved.

## The method (one formula, per load)

```
savings/load = [OLD move: rail(origin→old dest ramp) + dray(old ramp→giver FC)]
             − [NEW move: rail(origin→new dest ramp) + dray(new ramp→taker FC)]
             + [avoided OTR (giver→taker) we'd have paid to move the freight anyway]
```

- **Same-ramp flips (8 of 9 lanes):** the rail legs are identical both ways, so they cancel — savings reduce to `avoided OTR − (new dray − old dray)`. Simple and fully measured from carrier settlement (VLS) accruals per VRID.
- **Ramp-change flips (1 lane, RDU2→TOL3, 28 loads):** the load was intercepted at the Chicago crosstown and never rode the Chicago→Charlotte rail leg — so that avoided rail leg is credited. **This is the piece I most want your eyes on** (see caveat below).

Everything is priced **load-by-load against actual VLS carrier-settlement accruals**, not modeled/corridor rates — 289 of 323 loads carry measured taker-leg costs; the RDU2→TOL3 rail credit is measured from the actual avoided-leg VRIDs ($996/load), not a corridor estimate.

## The number (WK24–WK30 YTD)

| | Loads | Units | Net transport avoidance |
|---|---|---|---|
| SIM-confirmed (WK24–29) | ~288 | ~4.78M | **~$122K** (rail credit measured) |
| WK30 FWA4→RFD2 (accrual lag) | 19 | 0.27M | $23K (estimated — VLS hasn't posted yet) |
| **YTD total** | **~307** | **~5.05M** | **~$145K** |

- **Only manifest-confirmed flips count.** A redirect counts as executed only when a **new manifest ID lands in the AZIM midstream SharePoint**. Requested-but-not-manifested asks are excluded — most recently the WK25 CLT2→MCI4 ask, which I requested off a bad redirectability read on my side and which was never manifested/executed; it's out of this number.
- **Best lane:** RDU2→TOL3 at ~$2,840/load (the crosstown-intercept case where the avoided rail leg is real).
- **Primary value is backlog relief, not transport $:** ~10M unit-days of backlog moved off constrained givers. The transport-$ number is the secondary currency — which is why I want the method validated.

## The one thing I'd like AZIM to confirm

**The counterfactual.** I price "avoided OTR" as the spot truckload we'd otherwise have paid to move the freight to the taker. If the real alternative on some loads was dwell (not an OTR move), the credit is mis-scoped on those. Does the OTR-counterfactual hold from your side?

*(The rail-credit billing mechanic on the RDU2→TOL3 crosstown flips — whether the waybill re-rates to the truncated route rather than billing the full through-route — is what makes that lane's ~$28K credit real. My understanding is the waybills DO get reworked on truncation; flag if that's ever not the case for a given move.)*

## What this is / isn't

- **~$145K realized to date**, ~90% measured load-by-load against VLS carrier-settlement accruals; the rest labeled EST (WK30 accrual lag). Pacing to **~$0.85M annualized** (volume-weighted to the seasonal redirect curve — not a flat 52-week extrapolation off a program that started WK24).
- Re-handle labor, dwell/gridlock relief, and detention are all **excluded** — they'd sit on top, not in this number.
- Every dollar is tagged MEASURED or EST in the per-load detail — happy to walk the full basis line-by-line.

**Bottom line for you:** ~$145K realized net transport avoidance since WK24, mostly measured, pacing to ~$0.85M annualized. Before I use the forward number anywhere, I want your read on the OTR counterfactual and a gut-check on the per-load method — I'd rather get it right with you than quote it and be wrong.

Let me know a good time to walk it — or just reply on the counterfactual question above.
