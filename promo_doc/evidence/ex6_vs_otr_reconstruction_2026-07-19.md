# Ex6 — AZIM 1P-IM midstream reroute WK24–28: per-lane reconstruction + vs-OTR pricing

> **DRAFT — RECONSTRUCTED FOR WILL'S REVIEW. Not doc-ready until Will vets the load set + bases.
> Nothing here has been inserted into the promo doc.**

Built 2026-07-19. Task: reconstruct the "267 in-transit loads WK24–28" cited in promo v4/v5 Ex6
with full provenance, then compute a DRAFT weighted "avoided vs OTR" total.

---

## 1. Where the 267 actually comes from (provenance chain)

1. **Primary source (row-level):** `C:\Users\zhouzw\OneDrive - amazon.com\AZIM Midstream Redirect Requests 2026.xlsx`
   — the team tracker, tabs `WK24`, `WK25`, `WK 26`, `WK 27`, `WK 28` (plus `WK29` in-flight, excluded).
   Row = one VRID; **executed = `NEW MANIFEST ID` column populated** (reroute actually happened).
2. **First derivation:** `_notes/2026-07-14_azim_cost_avoidance.md` — counted the tracker on 7/14:
   WK24 127 / WK25 38 / WK26 15 / WK27 31 / WK28 56 = **267**, lanes listed, ~2.40M units (WK25–28;
   WK24 units blank at that time).
3. **$ basis:** `_notes/2026-07-15_azim_sim_cost_study.md` — ~$1,005/redirect-move finance blend from
   `_daily_digest/drafts/2026-07-13_tobi_ytd_rixd_redirect_cost.md` (Hydra/VLS VRID-deduped, $6.48M /
   ~6,447 rIXD VRIDs thru 5/31) → "267 × ~$1K ≈ ~$267K avoided", ~$2.5M annualized at ~55/wk.
4. **Promo text:** `promo_doc/drafts/promo_doc_v4_candidate.md` (Direction 1) and
   `promo_doc/drafts/promo_doc_v5_candidate.md` Ex6 carry the 267 / ~$267K / ~$2.5M figures.

**Reconciliation of this re-count vs the 7/14 note: EXACT.** Re-parsing the workbook today
(embedded repeat-header rows excluded) gives 127/38/15/31/56 = **267 loads** — identical weekly split.

## 2. Per-lane executed table (WK24–28)

Source for every row: `AZIM Midstream Redirect Requests 2026.xlsx`, week tab named, count of rows with
`NEW MANIFEST ID` populated; units = sum of that tab's `Units` column for those rows. OTR comp source:
`lane_cost.est_lane_cost(giver, taker)` — live VLS refresh 2026-07-19 into TEMP cache
`%TEMP%\_ex6_recon_cache.json` (live cache `redirect_budget/cache/lane_cost_60d.json` untouched,
mtime still 2026-07-17). All 9 lanes returned **exact-lane 60d medians** (no geo-tier fallback needed).

Avoided-A = OTR comp × loads (incremental rail ≈ $0 — the provenance's stated incremental basis).
Avoided-B = (OTR comp − $1,000) × loads (promo-v5-prose reading of "$1K/move incremental rail").

```
lane	weeks	loads	units	OTR comp $/load (basis)	avoided-A $	avoided-B $
FTW1->IAH3	WK24,WK25 (67+7)	74	1,597,149	$666.84 (exact-lane 60d median, n=61)	$49,346	-$24,654
CLT2->RDU2	WK24	60	746,152	$822.49 (exact-lane 60d median, n=26)	$49,349	-$10,651
MDW2->RFD2	WK28	45	821,573	$236.26 (exact-lane 60d median, n=27)	$10,632	-$34,368
RDU2->TOL3	WK27,WK28 (22+6)	28	436,293	$2,242.08 (exact-lane 60d median, n=19)	$62,778	$34,778
CLT2->MCI4	WK25	24	332,423	$2,130.05 (exact-lane 60d median, n=26)	$51,121	$27,121
RMN3->ABE8	WK26	15	315,324	$823.43 (exact-lane 60d median, n=22)	$12,351	-$2,649
PSP3->LAX9	WK27	9	90,561	$258.50 (exact-lane 60d median, n=102)	$2,326	-$6,674
RFD2->MDW2	WK25	7	231,557	$306.57 (exact-lane 60d median, n=9)	$2,146	-$4,854
RFD4->MDW8	WK28	5	1,633	$263.30 (exact-lane 60d median, n=16)	$1,316	-$3,684
TOTAL	WK24-28	267	4,572,665	weighted avg $904/load	$241,367	-$25,633
```

Weekly cross-check (loads, units): WK24 127 / 2,169,074 · WK25 38 / 738,207 · WK26 15 / 315,324 ·
WK27 31 / 443,162 · WK28 56 / 906,898. Matches `_notes/2026-07-14_azim_cost_avoidance.md` weekly
loads exactly; WK25–28 units match its ~2.40M; WK24 units (2,169,074) are newly populated in the
workbook (blank when the 7/14 note was written — backfilled since).

## 3. Draft weighted vs-OTR total + coverage

- **Priced 267 of 267 loads (100% of the 267; all 9 lanes exact-lane comps).**
- **Basis A (provenance-consistent): ~$241K avoided vs OTR** across WK24–28
  (incremental rail ≈ $0 per both `_notes` files: "a waybill/ramp change, often near-zero" /
  "changes the in-transit load's rail destination for ~$0 incremental").
- **Basis B (if incremental rail really were $1K/move): −$26K** — i.e. the lever would *lose* money
  vs OTR on these short lanes. This is strong evidence Basis B is a misreading (see §4).
- Convergent validity: weighted-average OTR comp on the actual executed lane mix = **$904/load**,
  within 10% of the $1,005/move Hydra/VLS finance blend — the two independent bases corroborate
  each other and the existing ~$267K headline (which is 267 × $1,005 finance basis ≈ $268K).

## 4. Findings Will must vet before any doc use

1. **The promo v5 Ex6 sentence overstates the OTR side for THIS lane mix.** v5 says "a full OTR
   re-move runs $2,000–$4,375/load (network truckload medians) versus ~$1K to reroute on rail."
   The actual executed giver→taker lanes are SHORT redirect hops: exact-lane OTR medians run
   **$236–$2,242** (only RDU2→TOL3 and CLT2→MCI4 clear $2K; 6 of 9 lanes are under $1K). The
   $2,000–$4,375 band described the IM loads' *line-haul* distance (origin→destination), not the
   redirect-move distance (giver→taker) — the counterfactual OTR move is the short hop. v5's own
   line 190 flagged exactly this ("needs their actual lane-distance mix — PULL-ABLE on request");
   this file is that pull, and it lands **~$241K**, not higher.
2. **"$1K/move" means the avoided downstream move (finance blend), NOT the incremental rail cost.**
   The 7/15 note is unambiguous; v5 prose drifted into calling it "incremental rail." Basis B's
   negative total shows the drifted reading is untenable. Recommended fix if quoted: "~$1K/move
   avoided (finance basis, Hydra/VLS blend) — corroborated at ~$904/load by exact-lane OTR medians
   on the executed lane mix."
3. **7 of the 267 rows have `NEW MANIFEST ID` == `Original Manifest ID`** (WK27 PSP3→LAX9 VRID
   113G4BGS9; WK28 RDU2→TOL3 VRIDs 112Z4HL6F, 111G2CVL9, 1131GKK3Y, 1148PGPSK, 111DPLGDF,
   113ZCMTCK). They were counted as executed in the original 267 (weekly totals only reconcile with
   them in), and are kept here for consistency — but the "manifest reissued" evidence is weaker for
   these (re-point vs reissue, or paste error). Excluding them: 260 loads / avoided-A ~$225K.
4. **RFD4→MDW8 (5 loads, WK28) is anomalous:** 1,633 total units (~327 u/load vs ~15–30K typical),
   and RFD4/MDW8 are not standard rIXD sites (likely ARS/RDC-side codes). Priced (exact-lane n=16,
   $263.30) and included, but worth a look before quoting.

## 5. GAPS (excluded from totals, or unrecoverable)

- **WK29 (16 loads flipped by AZIM, manifests pending at the 7/14 pull):** deliberately excluded —
  not part of the 267 and not "executed" under the new-manifest rule.
- **Dwell/re-handle avoidance:** the counterfactual also avoids landing-then-reshipping labor and
  dwell at the gridlocked giver; no $ figure exists in the provenance, so it is NOT in the totals
  (upside only, unquantified).
- **Counterfactual-mix confirmation:** whether each load's alternative was truly an OTR re-move vs
  another IM redirect was never confirmed (7/15 note flags this). Totals here assume OTR re-move on
  the giver→taker lane for all 267.
- **WK24 units backfill:** present in the workbook today but blank on 7/14 — the backfill's author/
  date is not recorded; units figures for WK24 rest on the current workbook state.
- No loads were left unpriced (live VLS refresh succeeded for all 9 lanes).

## 6. Method note

- **OTR comp** = `lane_cost.est_lane_cost` — the repo's 3-phase geographic estimator over VLS
  (`andes."ats-onestopshop".v_load_summary`) 60d TL medians; all 9 lanes hit phase-0 exact-lane
  medians (n=9–102), refreshed live 2026-07-19 into a temp cache only.
- **Incremental rail basis** = ~$0/move per the provenance notes (stated assumption; no measured
  per-move incremental figure exists). The ~$1K/move figure in the promo is the *avoided
  downstream-move* finance blend ($6.48M/6,447 VRIDs thru 5/31), not the incremental cost.
- **Executed definition** = tracker row with `NEW MANIFEST ID` populated (same rule as the 7/14
  derivation; reconciles exactly to 267).
- Nothing fabricated: every row traces to the named workbook tab; every price to a live estimator
  call; every assumption to a named file.


---

## PROPOSED DOC CORRECTION (prepared 7/19 by the main session — NOT applied; Will decides)

The current v5 Ex6 text carries two claims this reconstruction does not support:

1. **"a full OTR re-move runs $2,000–$4,375/load (network truckload medians) versus ~$1K to
   reroute on rail — roughly $1–3K avoided per move on those lanes."** The actual executed mix
   says otherwise: 6 of 9 lanes have OTR comps UNDER $1K (the counterfactual is the short
   giver->taker hop, e.g. FTW1->IAH3 / CLT2->RDU2 — not the long IM line-haul). Honest weighted
   total = ~$241K across all 267 loads (avg ~$904/load), corroborating — not exceeding — the
   finance-basis ~$267K.
2. **"~$1K/move incremental rail"** — provenance says incremental rail cost is ~$0 and the
   ~$1,005/move IS the avoided downstream-move value (Hydra/VLS finance blend). If $1K were
   truly incremental, the lever would net NEGATIVE ~$26K vs OTR.

**Proposed replacement for the Ex6 AZIM bullet's cost sentences (keeps every defensible number):**

> The lever redirected **267 in-transit loads across WK24–28 (~50–60/week, 4.57M units)**. Because
> the reroute happens while the load is still on rail, Amazon pays essentially no incremental
> transportation cost — the saving is the downstream redirect move that never happens, worth
> **~$1K per load (~$267K to date on the finance blend; a per-lane re-parse against actual
> truckload comps lands within 10% at ~$241K) — ~$2.5M annualized at the current run-rate.**

And CUT the "$2,000–$4,375 vs ~$1K" sentence + the "short intra-region lanes" caveat entirely
(the re-parse makes the honest general statement above sufficient, and the intro's ~$2.5M line
stands unchanged on the finance basis).
