# Ex6 cost-avoidance — how to put a defensible $ on the low-cost levers (DRAFT, 2026-07-18)

Will asked (7/18): *"can we use the query I used for the budget dashboard to help with cost for promo?"*
Answer: **yes** — the budget-dashboard source (VLS = `andes."ats-onestopshop".v_load_summary`,
per-VRID actual cost, self-serve, no Finance export) can turn Ex6's *estimated* avoidance bands
into *actual executed-load dollars*. But it must be done **per executed VRID**, not by lane median.

## Why not lane medians (verified 7/18, don't retry this way)

I pulled VLS 60d IM-vs-TL medians for the TOFC/midstream anchor lanes and got **0 rows**:

```
LAS1->RFD2  IM n=0  TL n=0        (all sparse in 60d — same reason the region tier exists)
LAS1->MDW2  IM n=0  TL n=0
LAS1->SWF2  IM n=0  TL n=0   (only 4 INTERMODAL loads in 365d, 0 in 60d)
VGT2->MDW2  IM n=0  TL n=0
VGT2->RFD2  IM n=0  TL n=0
```

These FC→FC lanes carry almost no *direct* VLS history, so a lane-level "actual IM vs OTR TL" delta
can't be computed for them. The number has to come from the **actual executed loads by VRID**.

## The method that works (per-VRID)

For each executed lever set (the ~267 AZIM-midstream WK24-28 loads; the TOFC moves; the OB-NTI flips):

1. **Actual cost** — look up each executed load's real cost in VLS by VRID:
   ```sql
   SELECT vr_id, origin, final_destination, shipment_mode,
          estimated_cost_accrual AS actual_cost, miles
   FROM "andes"."ats-onestopshop".v_load_summary
   WHERE vr_id IN (<executed VRIDs>)
     AND estimated_cost_accrual > 0
     AND (canceled_load IS NULL OR canceled_load::varchar NOT IN ('true','t','TRUE','T'));
   ```
   (3PIM loads without a stamped VRID → join on ISA id instead; `manifest_id`/`isa` are on the row.)

2. **OTR counterfactual** — the TL cost that lane WOULD have cost over-the-road, from the estimator
   that already exists: `lane_cost.est_lane_cost(giver, taker)` (cache-first; the new **region tier +
   TL/road mileage anchor** now returns a comp even for sparse transcon lanes like LAS1→SWF2 = ~$9.15k
   — this is exactly what unlocks the OTR side for these lanes). Falls back to the OTR band
   ($2,001 for 500-1000mi, $4,375 for 1000mi+) only when the estimator no-comps.

3. **Avoided per load** = `OTR_comp − actual_cost`; **total avoided** = Σ over the executed set.
   Report with provenance: `VLS 60d actuals, N loads, OTR comp basis <estimator basis>, self-serve`.

## The one input needed from Will

The **executed-load VRID/ISA list per lever**. It is NOT in a clean file today — it's spread across
the SIM comments (`unified_flash/_sim_*_comments.json`) + the steering tracker, and `audit_results.json`
holds only the current 15 records without VRID/cost. Options:
- Will pastes/points to the executed VRID list (fastest, cleanest), or
- we define an "executed" source (FMC execution feed filtered to the lever + WK24-28) and I reconstruct
  it — bigger job, and I will NOT fabricate a list for a promo figure.

Once the list exists, this is a ~1-hour run producing a defensible total-$ avoided for Ex6, replacing
the current banded estimate ("~$1-3K/move"). **Say go + hand over the list.**

## Reuse, don't refork
- OTR comp: `lane_cost.est_lane_cost` / the geo estimator (region tier live as of 7/18).
- Cost tiering / OTR classification: `redirect_economics.py` (`cost_tier`, `economic_verdict`) already
  consumes `est_lane_cost` — the avoidance calc should sit next to it, not duplicate it.
- Source: VLS `v_load_summary` (same as budget dashboard / lane_cost). No Finance export.
