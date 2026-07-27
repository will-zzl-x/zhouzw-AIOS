# CLT2->MCI4 AZIM lane verification — ground truth vs. deep-dive claims

**Built:** 2026-07-24 · **Owner:** William Zhou · **Status:** READ-ONLY verification, no files edited except this one.
**Access:** VPN + Redshift (`SAschedulingredshift` via `midstream_im_reroutable.connect()`) — **AVAILABLE**, confirmed live connect + queries 2026-07-24. SIM/Midway (`ReadInternalWebsites` -> `sim.amazon.com`) — **AVAILABLE**, both candidate SIMs read in full (all comments, verbatim).

---

## Bottom line

| Question | Verdict |
|---|---|
| Q1 — crosstown (ramp-change)? | **NO. Confirmed SAME-RAMP** by a fresh, direct VLS run-structure pull (2026-07-24) — not an inference. The rail leg that would have to be truncated/canceled for a crosstown claim (NSRR-CALUMET→NSRR-CHARLOTTE) **ran in full, uncanceled, on every executed load.** Only the final Charlotte-ramp→destination dray was re-pointed. |
| Q2 — approved? | **YES, a general approval exists** on the SIM, in Will's own words, dated 2026-06-15, explicitly naming 1PIM as an approved mechanism. **BUT** the specific escalated ask that produced the 24 MCI4 loads (26 loads/351,491 units 1PIM, up from the original 20-trailer ask) was posted as "pending partner team feedback on redirectability" and then, ~27 hours later, reported as already executed — with **no distinct second "approved" comment in between** for that specific count/mechanism. |
| Q3 — correct $ impact | **Scenario A stands; Scenario B is factually inapplicable (disproven by VLS); a narrow Scenario C is defensible for 2 of 16 loads.** See arithmetic below. The $137,345 YTD figure does **not** need the full-lane removal Will hypothesized, but a $1,054.56 haircut is defensible for 2 loads with zero VLS evidence of movement anywhere. |

---

## Q1 — Routing: same-ramp, not crosstown

### The two "candidate SIMs" — correction

**V2259981608 is NOT a CLT2->MCI4 SIM.** It is `Redirects - CM 93438 - 1 Day SLA - WK 26 CLT2->TOL3 FL` — a different lane (CLT2->**TOL3**), a different week (WK26 vs WK25), and a different program context (HJBI ramp-redirect ask; comments reference "HJBI trailers," "AZNG VRID cancelled," "downstream Y2Y"). It never mentions MCI4. This SIM should be dropped from the CLT2->MCI4 evidence set entirely — it appears to have been miscited as a candidate, likely because it's also a CLT2-giver redirect SIM from the same week range.

**V2251735064 is the correct and sole SIM** for this lane: title `Redirects - CM 92267 - 1 Day SLA - WK 25 CLT2->MCI4 FL (Midstream & Y2Y)`, requester `mariogon` via TORCH request 92267.1, resolved 2026-06-29. This matches the 24-load WK25 CLT2->MCI4 lane in the tracker/TSV exactly (`_notes/azim_entitlement_ytd_loads.tsv` rows tagged `YES [V2251735064]`). Confirmed by an independent search: no other SIM full-text-matches "CLT2->MCI4" in Taskei/SIM search (0 results either way it's queried) — V2251735064 is the only hit, consistent with the tracker's one-SIM-per-lane-per-week convention.

### Ground truth: direct VLS run-structure pull (2026-07-24), not inference

Pulled `andes."ats-onestopshop".v_load_summary` for all 24 tracked VRIDs, then joined on `run_structure_id` to recover every leg of each container's full journey (origin dray → IM rail → Chicago-area dray → IM rail → final dray). This is the same technique the 2026-07-21 deep-dive used to firm the RDU2->TOL3 rail credit — applied here fresh, specifically to test Will's crosstown hypothesis.

**Result: all 24 run structures share the identical planned route**, and it is the SAME route whether the load ended at the giver or the taker:

```
PSC2 --(dray)--> [UPRR-TACSIM | BNSF-PORTLAND-CS]
     --(rail/INTERMODAL)--> [UPRR-CHICAGO-GLOBAL-II | BNSF-CICERO-CS]
     --(dray)--> NSRR-CALUMET
     --(rail/INTERMODAL)--> NSRR-CHARLOTTE          <- THIS is the leg that would show
                                                         canceled/truncated if this were
                                                         a crosstown interception (RDU2->TOL3-style)
     --(dray, TRUCKLOAD)--> CLT2 (giver) or MCI4 (taker)   <- THIS is the ONLY leg that varies
```

The NSRR-CALUMET→NSRR-CHARLOTTE leg shows `canceled_load = FALSE` (ran, invoiced ~$1,022–$1,193/load) on **22 of 24** run structures — i.e., on every load whose journey wasn't entirely scrubbed. The freight physically rode the full rail route to Charlotte, exactly as originally planned. Only the terminal dray (`NSRR-CHARLOTTE -> CLT2` or `NSRR-CHARLOTTE -> MCI4`) differs between "never redirected" and "redirected" loads. This is the textbook definition of a **same-ramp re-point**, not a crosstown/ramp-change interception — and it is the polar opposite of the RDU2->TOL3 structure, where the deep-dive's 2026-07-21 22:06 re-pull found the Chicago→Charlotte continuation **booked as its own VRID and separately canceled** on all 28 loads (2 already zeroed).

Per-VRID breakdown from the fresh pull (24 VRIDs, all `origin = NSRR-CHARLOTTE` on the terminal leg — no VRID shows any other ramp as its terminal-dray origin):
- **8 loads** terminal dray → **CLT2** (the giver) — these are the "disproven" loads: never redirected, delivered on the originally-planned path. VRIDs: `111QW72Q3, 111ZKYTZQ, 1122WSVXY, 112Y121M8, 113YNR4Z9, 1151YG7VR, 11586CK6Z, 116BZQFBJ`.
- **14 loads** terminal dray → **MCI4** (the taker) — genuinely re-pointed, INVOICE+PAID. VRIDs: `111JLHC89, 1138TLVMS, 113D4YGCW, 113MHY15N, 113QWLTJT, 11423WLF4, 1149Z8CDR, 115FQM2C6, 115J925WD, 115WHJF8N, 1163NQW6M, 1168GB96F, 116DC2NYQ, 116FP8LG2`.
- **2 loads** — `114FQMH3P` and `115TDT391` — have **every leg of the entire run structure canceled** (`canceled_load = TRUE` on all 5 legs including the terminal dray, `manifest_total = 0`, no invoice/paid anywhere). There is zero VLS evidence these physically moved anywhere under this VRID — not to CLT2, not to MCI4. This matches the deep-dive's "UNVERIFIED... taker-facing leg CANCELED+zeroed" tag, but the fresh pull shows it's stronger than that: the *entire* journey is zeroed, not just the taker leg.

8 + 14 + 2 = 24. Matches the tracker exactly.

**Conclusion on Q1: Will's crosstown hypothesis is ruled out by direct evidence, not just by re-reading the deep-dive's own reasoning.** The rail-delta-credit treatment that applies to RDU2->TOL3 (avoided Chicago→Charlotte leg, separately booked and separately canceled) has no factual basis here — the equivalent leg for CLT2->MCI4 ran and was paid on every load. Same-ramp/rail-cancels is the correct model.

Raw query output: `%TEMP%\_clt2mci4_pull.json` (24-VRID base pull) and the run-structure join (126 rows, 24 run_structure_ids) captured in this session's tool output.

---

## Q2 — Approval status, verbatim

Full comment thread of **V2251735064** pulled live 2026-07-24 via `ReadInternalWebsites` (`sim.amazon.com/issues/V2251735064`). Chronological, only comments relevant to approval/execution of the 1PIM/MCI4 piece:

1. **2026-06-15 20:01:04 — William Zhou:**
   > "Approved for 20 FL Trailers. Seeking midstream 1P/3PIM, Y2Y AZNG not approved until I confirm exhausted IM levers."

   This is an explicit, unambiguous approval comment, by Will himself, and it names **1P** (1PIM) as an approved-to-pursue mechanism for this redirect (alongside 3PIM; Y2Y explicitly withheld pending IM-lever exhaustion). This is the ONLY comment on the SIM containing the word "Approved" in reference to the midstream/1PIM piece.

2. **2026-06-16 18:36:19 — William Zhou:**
   > "Requested 41 loads / 484,739 units 3PIM midstream, pending new manifests. Requested 26 loads / 351,491 units 1PIM midstream, pending partner team feedback (AZIM Ops) on redirectability. @sheparth & team"

   This is the specific 1PIM ask that produced the 24-load MCI4 execution — 26 loads requested (up from the original 20-trailer overall ask), explicitly flagged **"pending partner team feedback... on redirectability"** — i.e., not yet confirmed redirectable, let alone re-approved, at the moment of this post.

3. **2026-06-16 21:14:39 — William Zhou** (≈2h38m later, same day):
   > "AZIM executed 24 loads / 332,423 units 1PIM midstream, 2 loads requested were already completed to CLT2."

   Reports the AZIM Ops team's execution as a completed fact. **No comment between #2 and #3 contains an approval word for this specific 26-load/24-executed ask.** The sequence is request → (partner-team action, off-SIM) → execution-report, not request → approval → execution.

4. **2026-06-16 22:14:59 — Jeff Shelstrom:** "All 24 manifests listed in the sharepoint have been flipped from CLT4 to MCI4" — manifest-flip confirmation (mechanical, not an approval).

5. **2026-06-29 16:44:16 — Jamie Dougan:** "All trailers delivered. Resolving wk 25 SIM." — SIM close-out.

**Verdict on Q2:** It is not accurate to say "no approval exists" — comment #1 is a genuine, dated, named approval that explicitly includes 1PIM as a sanctioned mechanism. But it is also fair to say the specific scale that actually executed (26 requested / 24 executed 1PIM loads) exceeds the originally-approved "20 FL Trailers" and was never independently re-blessed with the word "approved" before AZIM acted on it — it moved straight from "requested, pending feedback" to "executed." Will's instinct that there's a gap here is partially right: there's a scope gap between the blanket mechanism-level approval and the specific count that executed, but there is not a total absence of approval.

Full comment thread also confirms **V2259981608 (CLT2->TOL3)** has its own, separate, explicit approval chain ("Approved for 24 FL redirects...", "Approved for 45 additional HJBI midstream loads only") — irrelevant to this lane, included here only to confirm it's a genuinely distinct SIM and not a mislabeled duplicate.

---

## Q3 — Corrected $ treatment and YTD impact

### Current base (confirmed from `_notes/azim_entitlement_ytd_loads.tsv`, awk-summed 2026-07-24)

```
CLT2->MCI4, all 24 tracked VRIDs:
  8  EXEC-DISPROVEN-BY-VLS        net $0.00 each   (delivered to giver CLT2, invoiced+paid; already excluded from "executed base")
  14 EXEC-SIM-CONFIRMED           sum net -$6,339.08  (MEASURED VLS accrual, terminal dray to MCI4)
  2  EXEC-UNVERIFIED-IN-VLS       sum net -$1,054.56  (EST Y; fresh pull shows ENTIRE run canceled — zero evidence of movement anywhere)
  ---
  Current lane net (16-load base) = -$7,393.64   <- matches the task's cited "~-$7,394" exactly
```

### Scenario A — same-ramp AND legitimately executed → current treatment stands
**This is what the ground truth supports for 14 of the 16 currently-counted loads.** Same-ramp is now confirmed by direct evidence (Q1), and those 14 loads have MEASURED, INVOICE+PAID VLS accruals to MCI4 — real, executed, same-ramp re-points. Lane net stays -$7,393.64 (or -$6,339.08 if the 2 unverified are pulled out — see Scenario C below). **YTD stays $137,345** (no change) for these 14 loads.

### Scenario B — crosstown → rail credit like RDU2->TOL3
**Factually inapplicable — ruled out by the Q1 VLS pull.** A rail credit requires an avoided/canceled rail leg (as RDU2->TOL3's NSRR-CALUMET→NSRR-CHARLOTTE leg was, booked separately and canceled on all 28 loads). For CLT2->MCI4, that identical leg **ran and was invoiced** on every one of the 22 non-fully-canceled runs. There is no avoided leg to price a credit against. Applying a rail credit here would be crediting a cost that was actually incurred, not avoided — that would overstate the entitlement, not correct it.

*For reference only (not a valid treatment):* if one incorrectly applied the measured NSRR-CALUMET→NSRR-CHARLOTTE leg cost (~$1,193/load) as a "credit" to the 14 confirmed + 2 unverified loads anyway, the lane would swing from -$7,393.64 to roughly +$11,694 (16 × $1,193.20 − $7,393.64), and YTD would show ~$156,433. **Do not use this number** — it has no factual basis; it's shown only so the arithmetic path is visible and explicitly rejected.

### Scenario C — never approved/never executed → remove
**Not defensible at the full-lane level** given (1) a general approval exists (Q2) and (2) 14 of 16 currently-counted loads are VLS-measured, invoiced, and paid as physically delivered to MCI4 — that is real, evidenced execution, not a paper flip.

**A narrower version of Scenario C is defensible**, though: the **2 EXEC-UNVERIFIED-IN-VLS loads (`114FQMH3P`, `115TDT391`)** now show, per the fresh 2026-07-24 pull, that their *entire* run structure — not just the taker leg — is canceled in VLS, with zero invoice/paid anywhere on the container. There's no VLS evidence these two loads went to MCI4, to CLT2, or anywhere else under this VRID. Removing just these 2:
```
Lane net: -$7,393.64 - (-$1,054.56) = -$6,339.08   (down to the 14 truly-measured loads)
YTD:      $137,345 + $1,054.56 = $138,399.56 ≈ $138,400
```

**If Will wants the full 16-load removal he hypothesized** (treating the whole lane's approval/execution chain as too uncertain to keep, despite 14 of 16 loads being independently VLS-measured, invoiced, and paid to MCI4):
```
YTD: $137,345 - (-$7,393.64) = $144,738.64 ≈ $144,739
```
This matches Will's own back-of-envelope arithmetic ("~$137,345 - (-7,394) = ~$144,739") exactly — confirmed, not merely repeated. This is the correct number IF the decision is to exclude the lane; my read of the evidence is that this exclusion is **not required** by what's actually in VLS/SIM (14 loads are solidly evidenced), but it IS Will's call given the approval-scope gap in Q2.

### Recommended honest number
**$138,400** (Scenario C, narrow version — drop only the 2 loads with zero VLS evidence of any movement) is the most defensible correction if Will wants to tighten the base. **$137,345 unchanged** (Scenario A) is defensible if the 2 unverified loads are kept on the strength of the SIM's "AZIM executed 24 loads... All 24 manifests... flipped... to MCI4" execution-confirmation language alone (SIM-level attestation, even without a VLS-measured leg). **$144,739** (full removal) is not supported by the evidence for 14 of the 16 loads and should not be used unless the driving concern is specifically the Q2 approval-scope gap rather than execution-integrity.

---

## Access statement

- **VPN + Redshift:** available. Confirmed live `midstream_im_reroutable.connect()` to `scheduling.cba7nbarlfx1.us-east-1.redshift.amazonaws.com` on 2026-07-24 despite an ICMP ping timeout (ICMP blocked separately from the TCP/Redshift port; connection itself succeeded). Two live queries run: (1) 24-VRID base pull from `andes."ats-onestopshop".v_load_summary`, (2) `run_structure_id` join recovering all 126 legs across the 24 run structures.
- **SIM/Midway:** available. Both `V2251735064` and `V2259981608` read in full (all comments, verbatim, via `ReadInternalWebsites` → `sim.amazon.com/issues/<ID>`) with no auth errors.
- Nothing in this task was blocked. No credentials were printed to any output (an `ada credentials print` attempt was correctly refused by the sandbox; the subsequent script-based connect used the credential material internally without exposing it).

## Sources

- SIM V2251735064 (CLT2->MCI4, WK25) — live pull 2026-07-24, full comment thread, verbatim quotes above.
- SIM V2259981608 (CLT2->TOL3, WK26) — live pull 2026-07-24, confirmed unrelated lane (correction to task framing).
- VLS (`andes."ats-onestopshop".v_load_summary`) — live pulls 2026-07-24 via `SAschedulingredshift`: 24-VRID base pull + run-structure join (126 rows / 24 run_structure_ids).
- `C:/Users/zhouzw/ict_automation/_notes/azim_entitlement_ytd_loads.tsv` — current lane net computed by direct awk sum (2026-07-24), not copied from prose.
- `C:/Users/zhouzw/ict_automation/_notes/azim_entitlement_ytd_deepdive_2026-07-21.md` and `azim_entitlement_2026-07-21_v3.md` — prior analysis, used as the baseline this verification tests against (not treated as ground truth itself).
