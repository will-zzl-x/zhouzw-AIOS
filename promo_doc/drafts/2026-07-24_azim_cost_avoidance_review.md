<!-- DRAFT share-out for Parth Sheth (sheparth@) + AZIM team — cost-avoidance methodology
     review. LOCAL ONLY, no comms. Will reviews + sends. Purpose: put the midstream-reroute
     cost-avoidance number + method in front of AZIM for a light independent gut-check BEFORE
     it's quoted externally (promo doc, leadership) — Will has already resolved the two prior
     open questions (waybill re-rating; OTR counterfactual), so this is validation-for-record,
     not a blocker. Numbers refreshed 2026-07-27 to the final reclassified basis. Sources:
     _notes/azim_entitlement_ytd_deepdive_2026-07-21.md (+7/24 correction),
     promo_doc/evidence/azim_reclassified_crosstown_2026-07-24.md,
     promo_doc/evidence/azim_seasonal_annualization_2026-07-26.md. -->

# AZIM Midstream Reroute — Cost-Avoidance Methodology, for AZIM Review

**From:** William Zhou (IPEX-ICT) · **To:** Parth Sheth + AZIM team · **Date:** 2026-07-27
**Ask:** a quick gut-check on the method and the number below before I use it more widely. I've worked through the two things I was unsure about (below), so this is mostly for your independent read — flag anything that looks off, especially where you're the authoritative source on billing / IM lane rates.

---

## What this measures

The value of intercepting a 1P-IM load **while it's still on the rail leg** and diverting it to a taker that needs the work — versus letting it arrive and paying a full over-the-road (OTR) redirect afterward. We've been running this together since WK24; this is the first full accounting of what it's saved.

## The method (one formula, per load)

```
savings/load = [OLD move: rail(origin→old dest ramp) + dray(old ramp→giver FC)]
             − [NEW move: rail(origin→new dest ramp) + dray(new ramp→taker FC)]
             + [avoided OTR (giver→taker) we'd have paid to move the freight anyway]
```

- **Same-ramp flips (most loads):** the rail legs are identical both ways, so they cancel — savings reduce to `avoided OTR − (new dray − old dray)`, fully measured from carrier-settlement (VLS) accruals per VRID.
- **Crosstown interceptions (2 lanes so far — RDU2→TOL3 and WK30 MCI4→IND9):** the load was caught before its rail-carrier interchange and never rode the onward rail leg — so that avoided leg is credited (~$35K across the two lanes, measured from the separately-booked, canceled leg VRIDs at ~$0.76–1.0K/load, not a corridor estimate).

Everything is priced **load-by-load against actual VLS carrier-settlement accruals**, not modeled rates — ~90% measured, the remainder labeled EST (WK30 accrual lag). Full per-VRID basis available to walk line-by-line.

## The number (WK24–WK30 2026)

| | Loads | Units | Net transport avoidance |
|---|---|---|---|
| Confirmed (WK24–29) | ~288 | ~4.9M | ~$122K (measured) |
| WK30 (recent / accrual-lag) | ~28 | ~0.39M | ~$28K (partly EST) |
| **YTD total** | **~316** | **~5.29M** | **~$150K** |

- **Only manifest-confirmed flips count.** A redirect counts as executed only when a **new manifest ID lands in the AZIM midstream SharePoint**. Requested-but-not-manifested asks are excluded — e.g. the WK25 CLT2→MCI4 ask, which I requested off a bad redirectability read on my side and which was never manifested; it's out of this number.
- **Crosstown is the high-value profile** and it recurs — best lane RDU2→TOL3 at ~$2,840/load, and WK30's MCI4→IND9 was a second, structurally distinct crosstown (different hub + carrier pair), so this isn't a one-off.
- **Primary value is backlog relief, not transport $:** ~10M unit-days of backlog moved off constrained givers. The transport-$ number is the secondary currency — which is why I want the method sanity-checked.

## The forward number

**~$930K by year-end 2026, ~$1.3M full-year run-rate.** The lever launched WK24, so the EOY figure applies its demonstrated capture rate to the seasonally-expected redirect volume for the remaining weeks (our redirect demand curve runs ~2× heavier in Q4), and the full-year run-rate states the standing capability across a full seasonal cycle. Realized-to-date (~$150K) is the hard number; these are the forward projections built on it.

## The one thing I'd most like your read on

**The counterfactual.** I price "avoided OTR" as the spot truckload we'd otherwise have paid to move the freight to the taker. If the real alternative on some loads was dwell (not an OTR move), the credit is mis-scoped on those. Does the OTR-counterfactual hold from your side?

*(On the crosstown rail credit: my understanding is the waybill re-rates to the truncated route when we intercept before the interchange — the canceled legs show zeroed in settlement, consistent with that. Flag if there's ever a lane where it bills the full through-route instead.)*

## What this is / isn't

- **~$150K realized to date**, ~90% measured load-by-load against VLS settlement accruals; forward figures (~$930K EOY / ~$1.3M run-rate) are seasonal-curve projections off that base, clearly labeled as projections.
- Re-handle labor, dwell/gridlock relief, and detention are all **excluded** — they'd sit on top, not in this number.
- Every dollar is tagged MEASURED or EST in the per-load detail.

**Bottom line:** ~$150K realized net transport avoidance since WK24 (mostly measured), pacing to ~$930K by year-end. I've reconciled the pieces I was unsure about; before I lean on this more widely I'd value your gut-check on the OTR counterfactual and the per-load method. Happy to walk the full basis whenever works.
