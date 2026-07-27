# AZIM 1P-IM midstream reroute — seasonally-adjusted EOY-2026 and full-year annualization

**Built:** 2026-07-26 · **Owner:** William Zhou · **Status:** READ-ONLY. This is the ONLY file
written this session. No SIM/tracker writeback, no posting, no other file edits.

**Replaces (as the primary forward figure):**
- The retired **÷16.7%** method (~$0.85–0.87M) — already retired in
  `azim_annualization_2026-07-24.md` §0; assumed a false full-year-flat seasonality share.
- The **flat ×52 run-rate** (~$1.11M) and its companion **flat EOY** (~$620K) — both assume AZIM's
  weekly $ rate is constant all year. This doc replaces that assumption with an actual measured
  seasonal shape from the steering trackers themselves.

**Quip access:** CONFIRMED LIVE this session (`users/current` probe → HTTP 200, `William Zhou`,
2026-07-26). All Quip pulls below are fresh, not reused from the 2026-07-24 evidence docs, except
where explicitly marked "given, not recomputed" (the $148,841–$151,565 AZIM realized figure and its
per-lane/per-week composition, per task instruction).

---

## 0) TL;DR

| Question | Answer |
|---|---|
| **EOY-2026 estimate (base case)** | **~$778K** (durable-cadence capture rate × seasonally-projected WK31–52 volume + $150,203 realized WK24–30) |
| **EOY-2026 sensitivity band** | **$778K (durable-cadence) → $972K (clean-4-week)**, cross-checks: $877K (median-week), $932K (aggregate 7-week) |
| **Full-year run-rate (hypothetical, all 52 weeks at 2026 volume/seasonality)** | **~$1.06M** (durable-cadence) → **$1.38M** (clean-4-week), band spans **$1.06M–$1.38M** |
| **Capture rate used (primary)** | **$0.00293 per total-redirect-unit** (durable-cadence: WK25,26,28,29,30 — excludes WK24 launch-burst and WK27's one-time crosstown windfall, same exclusion Will's team already established for the $-only run-rate) |
| **Capture rate range (all variants)** | $0.00293/unit (durable-cadence) to $0.00383/unit (4-clean-week) to $0.00365/unit (aggregate 7-wk); AZIM-units-as-%-of-total ranges 10.1%–12.9% across the same cuts |
| **How seasonality moved the EOY number vs flat** | **+25% to +56% HIGHER** than flat EOY (~$622K) across every capture-rate variant — because the trailing-12-18-month steering-tracker shape shows a real Q4 peak (WK40–52 ran **~2.0×** the WK11–30 mid-year weekly baseline in 2025), and the flat method assumes WK31–52 keeps running at the WK24–30 average instead. |
| **How seasonality moved the full-year run-rate vs flat ×52** | **Mixed sign** — ranges from **–5.4%** (durable-cadence, $1.056M vs flat $1.116M) to **+23.8%** (clean-4-week, $1.382M vs $1.116M). The Q4 seasonal boost is real, but whether it nets positive vs the flat figure depends on which capture rate is paired with it — the flat ×52 figure already bakes in the WK27 crosstown windfall's $/week average uniformly across 52 weeks, which happens to roughly offset the seasonal boost under the conservative (durable-cadence) capture rate. |
| **Biggest data problems hit** | (1) 2025 tracker folder is missing WK1–3, WK5–9 (8 of 52 weeks, no tabs — NOT interpolated, flagged everywhere it affects a total). (2) The steering-tracker docs are LIVE and being edited — my 2026-07-26 pull of WK25/26/28/30 totals differs from the 2026-07-24 pull already published in `azim_annualization_2026-07-24.md` §5 (WK25: 8.40M→6.26M; WK26: 6.38M→5.22M; WK28: 6.51M→6.16M; WK30: 4.84M→4.81M — WK24, WK27, WK29 matched exactly). This is expected staleness, not an error; flagged explicitly wherever it changes a downstream number. (3) Both years show a handful of individual weeks that diverge sharply in shape from each other (see §3) — likely one-time events in each year, not a stable structural difference; not fully diagnosable within this task's scope. |

---

## 1) Method, in order (per Will's 2026-07-26 spec)

1. Pull weekly TOTAL steering-tracker redirect volume (all networks: rIXD/nIXD/NS/ARS/AMXL_CA),
   2025 full year + 2026 YTD, using `all_team_slides/build_ytd_from_steering.py`'s own
   `enumerate_trackers` / `fetch_records` / `_is_executed` functions, executed-status rows only.
   Deduped across weekly trackers on the SAME key that function's own `build()` uses
   (`date, giver, taker, sim, network`), keeping the most-complete (latest-week / highest
   trailers-then-units) snapshot per lane — but bucketed by the **tracker's own WK label** (not a
   recomputed calendar-ISO week), so every number here lines up natively with the WK24–30 labels
   already used throughout every AZIM evidence doc. Hydra was NOT used anywhere in this pull
   (per Will's explicit instruction — AZIM midstream flips don't book to
   `TRANSFERSINTERMODALREDIRECTS`).
2. Compute each week's share/index of the measured annual total → the seasonal curve. Show 2025
   (full-shape) vs 2026 (front-half validation), flag material disagreement.
3. Take the AZIM realized $148,841–$151,565 / 316 loads / 5,291,537 units (WK24–30 2026) as GIVEN
   from `azim_reclassified_crosstown_2026-07-24.md` — NOT recomputed. Divide by the SAME weeks'
   fresh-pulled total steering volume → capture rate, two ways ($/unit and units-%).
4. Project WK31–52 AZIM $ = capture rate × (2025's week-N shape × a 2026 YoY scale factor).
   Sum → EOY-2026 estimate. Apply the same capture rate to the full 52-week curve (all
   counterfactually scaled to 2026 level) → full-year run-rate.
5. Compare to the flat ×52 and flat-EOY reference figures.

---

## 2) Weekly TOTAL steering-tracker redirect volume — the demand curve

**Source:** Quip folders `UCF9OAFdxvE` (2025) and `dKL9OAnfDIa` (2026), live pull 2026-07-26,
via `enumerate_trackers`/`fetch_records`/`_is_executed` + the same cross-week dedup key as
`build_ytd_from_steering.build()`. All networks combined (rIXD+nIXD+NS+ARS+AMXL_CA). MEASURED.

### 2025 (full year, 44 of 52 weekly tabs found)

**KNOWN GAP, per Will's brief, confirmed empirically:** the 2025 Quip folder has **no tab for
WK1–3 or WK5–9** (8 weeks). This is not an artifact of my query — `enumerate_trackers` returns
zero matches for those WK numbers; the folder jumps straight from WK4 to WK10. **Not
interpolated.** Every total/index below that spans those weeks is explicitly built from the
**44 weeks that exist**, and is flagged as such everywhere it matters (§4, §7).

| WK | Units (dedup) | Trailers (dedup) | Lanes | WK | Units (dedup) | Trailers (dedup) | Lanes |
|---|---|---|---|---|---|---|---|
| 1–3 | **NO TAB** | — | — | 27 | 4,559,468 | 436 | 45 |
| 4 | 13,343,559 | 751 | 59 | 28 | 9,131,266 | 586 | 77 |
| 5–9 | **NO TAB** | — | — | 29 | 4,609,484 | 279 | 38 |
| 10 | 10,658,779 | 693 | 49 | 30 | 5,684,475 | 392 | 28 |
| 11 | 6,023,964 | 515 | 36 | 31 | 4,594,911 | 366 | 27 |
| 12 | 22,236,217 | 1,224 | 74 | 32 | 2,965,288 | 248 | 29 |
| 13 | 10,259,798 | 707 | 47 | 33 | 1,463,672 | 198 | 28 |
| 14 | 4,135,646 | 410 | 37 | 34 | 4,954,603 | 459 | 45 |
| 15 | 5,668,746 | 399 | 49 | 35 | 5,672,983 | 360 | 34 |
| 16 | 4,532,579 | 427 | 39 | 36 | 6,103,042 | 479 | 41 |
| 17 | 4,835,829 | 370 | 33 | 37 | 11,663,383 | 805 | 63 |
| 18 | 6,758,884 | 472 | 24 | 38 | 10,500,730 | 880 | 61 |
| 19 | 7,328,742 | 541 | 29 | 39 | 10,902,282 | 1,004 | 84 |
| 20 | 6,555,015 | 531 | 37 | 40 | 13,880,323 | 1,108 | 75 |
| 21 | 3,395,736 | 340 | 27 | 41 | 16,003,601 | 1,247 | 99 |
| 22 | 4,259,981 | 393 | 29 | 42 | 12,682,060 | 1,026 | 88 |
| 23 | 3,990,220 | 315 | 29 | 43 | 9,556,350 | 763 | 63 |
| 24 | 7,185,444 | 536 | 45 | 44 | 14,072,334 | 1,138 | 92 |
| 25 | 7,834,852 | 746 | 61 | 45 | 16,671,672 | 1,278 | 110 |
| 26 | 6,628,475 | 684 | 64 | 46 | 20,058,079 | 1,520 | 125 |
| | | | | 47 | 18,522,108 | 1,445 | 114 |
| | | | | 48 | 11,816,161 | 934 | 94 |
| | | | | 49 | 14,315,224 | 972 | 96 |
| | | | | 50 | 13,613,544 | 1,201 | 100 |
| | | | | 51 | 7,418,848 | 781 | 68 |
| | | | | 52 | 6,958,833 | 462 | 44 |

**Measured 2025 annual total (44 weeks with data): 394,007,190 units / 30,421 trailers / 2,536
deduped lanes.** MEASURED. (Raw, undeduped sum was 394,309,184 units — the ~302K/0.08% gap is
cross-week double-counting of lanes that stayed open across tracker weeks; negligible at the
annual level, confirming the dedup step matters more for individual-week accuracy than for the
annual total.)

### 2026 YTD (WK1–30 populated; WK31 tab exists but has zero rows as of 2026-07-26 — too new)

| WK | Units (dedup) | WK | Units (dedup) | WK | Units (dedup) |
|---|---|---|---|---|---|
| 1 | 2,260,701 | 11 | 10,552,516 | 21 | 8,757,604 |
| 2 | 5,357,856 | 12 | 8,923,256 | 22 | 10,412,129 |
| 3 | 5,496,735 | 13 | 5,138,500 | 23 | 12,776,997 |
| 4 | 1,772,047 | 14 | 7,081,740 | 24 | 7,086,152 |
| 5 | 4,419,725 | 15 | 3,421,179 | 25 | 6,262,707 |
| 6 | 3,598,321 | 16 | 7,513,359 | 26 | 5,222,231 |
| 7 | 4,081,214 | 17 | 4,587,861 | 27 | 7,456,624 |
| 8 | 6,149,480 | 18 | 6,528,903 | 28 | 6,159,039 |
| 9 | 6,508,982 | 19 | 7,992,918 | 29 | 4,173,526 |
| 10 | 1,502,633 | 20 | 7,851,932 | 30 | 4,807,259 |
| | | | | 31 | 0 (empty tab) |

**Measured 2026 YTD total (WK1–30): 183,854,126 units.** MEASURED, 2026-07-26 pull.

**Freshness flag:** comparing WK24–30 against the same weeks as pulled 2026-07-24 in
`azim_annualization_2026-07-24.md` §5 — WK24 (7,086,152), WK27 (7,456,624), and WK29 (4,173,526)
matched **exactly**. WK25 (8,401,677→6,262,707), WK26 (6,375,570→5,222,231), WK28
(6,510,308→6,159,039), and WK30 (4,843,433→4,807,259) **changed** — the steering trackers are live
documents under active edit; recent weeks move as rows get updated/closed. This pull (2026-07-26)
is used as the current MEASURED basis throughout; it is not a contradiction of the prior doc, just
two days more current.

---

## 3) Seasonal shape

### 3a. 2025 seasonal index (share of the 44-week measured annual total)

Full table in Appendix A. Headline read: **weeks WK40–52 (13 weeks, the Amazon fiscal Q4/peak
window) account for 44.6% of the full measured 2025 annual total**, at an average of **13.5M
units/week** — **~2.0× the WK11–30 mid-year baseline average of 6.78M units/week.** DERIVED from
the MEASURED 2025 weekly series above. This is the Q4 peak the seasonal method is designed to
capture and the flat method assumes away.

### 3b. 2025 vs 2026 shape — where they agree and where they disagree materially

Both years' weekly shares are normalized against the SAME comparison basis for a fair read: each
week's units ÷ the sum of the 22 weeks present in **both** years (WK4, WK10–30). DERIVED.

| WK | 2025 share of overlap | 2026 share of overlap | pp diff | Note |
|---|---|---|---|---|
| 4 | 8.36% | 1.21% | −7.15pp | diverges — 2025 WK4 had an unusually large single week not repeated in 2026 |
| 10 | 6.68% | 1.03% | −5.65pp | diverges |
| 11 | 3.77% | 7.23% | +3.45pp | diverges |
| 12 | 13.93% | 6.11% | −7.82pp | diverges — 2025's single biggest week of the whole overlap window |
| 13 | 6.43% | 3.52% | −2.91pp | diverges |
| 14 | 2.59% | 4.85% | +2.26pp | diverges |
| 15–20 | 1.7%–4.6% | 2.3%–5.5% | ≤+1.3pp | broadly consistent |
| 21 | 2.13% | 6.00% | +3.87pp | diverges |
| 22 | 2.67% | 7.13% | +4.46pp | diverges |
| 23 | 2.50% | 8.75% | +6.25pp | diverges — 2026's biggest single-week spike in the window |
| **24** | **4.50%** | **4.85%** | **+0.35pp** | **AZIM-active window starts — well matched** |
| **25** | **4.91%** | **4.29%** | **−0.62pp** | well matched |
| **26** | **4.15%** | **3.58%** | **−0.58pp** | well matched |
| **27** | **2.86%** | **5.11%** | **+2.25pp** | diverges — largest gap inside the AZIM window |
| **28** | **5.72%** | **4.22%** | **−1.50pp** | borderline |
| **29** | **2.89%** | **2.86%** | **−0.03pp** | best-matched week in the whole table |
| **30** | **3.56%** | **3.29%** | **−0.27pp** | well matched |

**Read:** the mid-year weeks (WK10–23) show real, sometimes large, shape disagreement between the
two years — most look like one-off events in one year or the other (e.g., 2025's WK12 spike,
2026's WK21–23 run-up) rather than a stable structural shift; this task did not have scope to
diagnose the specific cause of each. **The AZIM-active window itself (WK24–30) — the one that
matters most for near-term projection — is comparatively well matched between years** (mostly
under ±1.5pp, one outlier at WK27's +2.25pp), which is reassuring for using 2025's WK31–52 shape,
scaled, as the near-term projection basis in §5. The mid-year instability is a genuine caveat on
using 2025's shape for anything before WK31 — not used for anything here, since WK1–30 2026 is
already MEASURED and doesn't need projecting.

---

## 4) YoY scale factor

Computed over the 22 weeks present in **both** years (WK4, WK10–30) — the widest common,
apples-to-apples window available, to avoid over-fitting to just the 7 AZIM-active weeks.

```
2025 sum, overlap weeks:  159,617,159 units   MEASURED
2026 sum, overlap weeks:  145,981,112 units   MEASURED
scale_factor = 2026/2025 = 0.9146  (91.5%)     DERIVED
```

**2026's total steering-tracker redirect volume is running ~8.5% BELOW 2025's, on a like-for-like
weekly basis.** This is the network-wide "denominator" trend and should not be confused with
AZIM's own activity, which didn't exist in 2025 at all.

**Sensitivity check**, using only the 7 AZIM-active weeks (WK24–30) instead of the full 22-week
overlap: scale_factor = 0.9021 (90.2%) — close to the 22-week figure (within 1.3pp), so the choice
of window doesn't materially change the projection. The 22-week version is used as primary
(n=22 vs n=7 — more stable).

---

## 5) Demonstrated capture — capture rate vs TOTAL steering-tracker volume

**AZIM realized $ / units / loads, WK24–30 2026 — GIVEN, not recomputed**
(`azim_reclassified_crosstown_2026-07-24.md` §3, §5):

| WK | Loads | Units | Net $ | Note |
|---|---|---|---|---|
| 24 | 126 | 2,154,884 | $6,337.00 | launch-burst week |
| 25 | 5 | 132,106 | −$83.00 | data-quality low (2 largest asks failed verification, not a demand low) |
| 26 | 15 | 315,324 | $7,382.00 | |
| 27 | 31 | 443,162 | $65,875.00 | RDU2→TOL3 one-time crosstown windfall ($61,536 of it) |
| 28 | 56 | 906,898 | $27,754.00 | |
| 29 | 55 | 953,644 | $14,142.00 | median week by $ |
| 30 | 28 | 385,519 | $27,434.06–$30,158.00 | corrected: 19 orig (EST) + 9 new MCI4→IND9 (§4 of the crosstown doc) |
| **TOTAL** | **316** | **5,291,537** | **$148,841.09–$151,565.03** (mid **$150,203**) | |

**Total steering-tracker volume, SAME weeks, fresh 2026-07-26 pull (MEASURED, §2 above):**
41,167,538 units (WK24–30 sum).

**Capture rate, week by week:**

| WK | AZIM $ | AZIM units | Total steering units | $ per total-redirect-unit | AZIM units as % of total |
|---|---|---|---|---|---|
| 24 | $6,337.00 | 2,154,884 | 7,086,152 | $0.000894 | **30.41%** |
| 25 | −$83.00 | 132,106 | 6,262,707 | −$0.000013 | 2.11% |
| 26 | $7,382.00 | 315,324 | 5,222,231 | $0.001414 | 6.04% |
| 27 | $65,875.00 | 443,162 | 7,456,624 | **$0.008834** | 5.94% |
| 28 | $27,754.00 | 906,898 | 6,159,039 | $0.004506 | 14.72% |
| 29 | $14,142.00 | 953,644 | 4,173,526 | $0.003389 | 22.85% |
| 30 | $28,796.03 (mid) | 385,519 | 4,807,259 | $0.005990 | 8.02% |

DERIVED from the two MEASURED tables above.

**Which metric is stabler week to week?** Coefficient of variation (stdev/|mean|) across all 7
weeks: **$/unit = 81.3%**, **units-% = 74.6%**. Restricted to the durable-cadence 5 weeks (excl.
WK24, WK27): **$/unit = 70.1%**, **units-% = 67.9%**. **AZIM-units-as-%-of-total is modestly
stabler than $/total-redirect-unit in both views — but neither is actually stable**; both carry
very high week-to-week variance, because AZIM's $ realization concentrates heavily in specific
lanes (RDU2→TOL3's WK27 windfall alone drives the $/unit metric's outlier), while unit volume
spreads a bit more evenly across the ask. DERIVED.

### Which weeks define the "representative" capture rate — decision + justification

Per Will's own already-established $-run-rate methodology (`azim_annualization_2026-07-24.md`
§3–4), **WK24 is a launch-burst (the tracker's first week, plausibly a backlog dump) and WK27 is
dominated by a one-time rail-crosstown windfall (RDU2→TOL3, $61,536 of $65,875)** — neither is
argued to be a repeatable weekly pattern. **This doc extends the exact same exclusion logic to the
capture rate**, since the capture rate's numerator is the same lumpy $ series:

| Cut | Weeks used | AZIM $ | Steering units | $/unit | Units % | Status |
|---|---|---|---|---|---|---|
| **Durable-cadence (PRIMARY)** | 25,26,28,29,30 | $77,991.03 | 26,624,762 | **$0.002929** | **10.12%** | recommended — mirrors the established $-run-rate exclusion |
| Median week (WK29, cross-check) | 29 only | $14,142.00 | 4,173,526 | $0.003389 | 22.85% | outlier-robust single-week check; lands inside the band |
| Aggregate, all 7 weeks | 24–30 | $150,203.03 | 41,167,538 | $0.003649 | 12.85% | "use the aggregate rate" alternative the task explicitly allows |
| 4-clean-week (excl. WK24/25/27) | 26,28,29,30 | $78,074.03 | 20,362,055 | $0.003834 | 12.58% | upper case if WK25's data-quality-low is ALSO treated as noise, not real demand |
| Min single week | WK25 | −$83.00 | 6,262,707 | −$0.000013 | 2.11% | illustrative only — not usable directly |
| Max single week | WK27 | $65,875.00 | 7,456,624 | $0.008834 | 5.94% | illustrative only — not usable directly |

**Decision: durable-cadence is the primary capture rate**, for the same reason Will's team already
adopted it for the $-only run-rate — it's the cleanest read of "what this lever does in a typical
week" once the launch artifact and the one-time crosstown windfall are set aside. The other three
multi-week cuts (median, aggregate, 4-clean-week) are shown as the sensitivity band, all used
below in the projection so the spread is visible, not hidden behind one number.

---

## 6) Projecting WK31–52 2026

**Projected total steering-tracker volume, week N = 2025's actual week-N units × 0.9146 (§4).**
DERIVED. Full table:

| WK | 2025 actual | Projected 2026 (×0.9146) | WK | 2025 actual | Projected 2026 (×0.9146) |
|---|---|---|---|---|---|
| 31 | 4,594,911 | 4,202,369 | 42 | 12,682,060 | 11,598,635 |
| 32 | 2,965,288 | 2,711,964 | 43 | 9,556,350 | 8,739,954 |
| 33 | 1,463,672 | 1,338,631 | 44 | 14,072,334 | 12,870,139 |
| 34 | 4,954,603 | 4,531,333 | 45 | 16,671,672 | 15,247,416 |
| 35 | 5,672,983 | 5,188,342 | 46 | 20,058,079 | 18,344,523 |
| 36 | 6,103,042 | 5,581,661 | 47 | 18,522,108 | 16,939,770 |
| 37 | 11,663,383 | 10,666,984 | 48 | 11,816,161 | 10,806,710 |
| 38 | 10,500,730 | 9,603,656 | 49 | 14,315,224 | 13,092,279 |
| 39 | 10,902,282 | 9,970,903 | 50 | 13,613,544 | 12,450,543 |
| 40 | 13,880,323 | 12,694,531 | 51 | 7,418,848 | 6,785,058 |
| 41 | 16,003,601 | 14,636,418 | 52 | 6,958,833 | 6,364,342 |

**Sum, projected total steering volume WK31–52: 214,366,160 units.** DERIVED.

**Projected AZIM $, by capture-rate variant** (weekly detail; $ = projected total units × rate):

| WK | Proj. total units | Durable-cadence (primary) | Median-wk29 | Aggregate 7-wk | Clean-4-wk |
|---|---|---|---|---|---|
| 31 | 4,202,369 | $12,310 | $14,240 | $15,333 | $16,113 |
| 32 | 2,711,964 | $7,944 | $9,189 | $9,895 | $10,398 |
| 33 | 1,338,631 | $3,921 | $4,536 | $4,884 | $5,133 |
| 34 | 4,531,333 | $13,273 | $15,354 | $16,533 | $17,374 |
| 35 | 5,188,342 | $15,198 | $17,581 | $18,930 | $19,894 |
| 36 | 5,581,661 | $16,350 | $18,913 | $20,365 | $21,402 |
| 37 | 10,666,984 | $31,246 | $36,145 | $38,919 | $40,900 |
| 38 | 9,603,656 | $28,132 | $32,542 | $35,040 | $36,823 |
| 39 | 9,970,903 | $29,207 | $33,786 | $36,380 | $38,231 |
| 40 | 12,694,531 | $37,186 | $43,015 | $46,317 | $48,675 |
| 41 | 14,636,418 | $42,874 | $49,596 | $53,402 | $56,120 |
| 42 | 11,598,635 | $33,975 | $39,302 | $42,319 | $44,473 |
| 43 | 8,739,954 | $25,602 | $29,615 | $31,888 | $33,512 |
| 44 | 12,870,139 | $37,700 | $43,610 | $46,958 | $49,348 |
| 45 | 15,247,416 | $44,664 | $51,666 | $55,631 | $58,463 |
| 46 | 18,344,523 | $53,736 | $62,160 | $66,931 | $70,338 |
| 47 | 16,939,770 | $49,621 | $57,400 | $61,806 | $64,952 |
| 48 | 10,806,710 | $31,656 | $36,619 | $39,429 | $41,436 |
| 49 | 13,092,279 | $38,351 | $44,363 | $47,768 | $50,200 |
| 50 | 12,450,543 | $36,471 | $42,189 | $45,427 | $47,739 |
| 51 | 6,785,058 | $19,875 | $22,991 | $24,756 | $26,016 |
| 52 | 6,364,342 | $18,643 | $21,566 | $23,221 | $24,403 |
| **SUM WK31–52** | **214,366,160** | **$627,936** | **$726,380** | **$782,132** | **$821,942** |

DERIVED throughout this section.

---

## 7) EOY-2026 estimate and full-year run-rate

### EOY-2026 estimate = $150,203 realized (WK24–30 mid) + Σ(WK31–52 projected)

| Capture-rate variant | Realized WK24–30 | + Projected WK31–52 | = EOY-2026 estimate |
|---|---|---|---|
| **Durable-cadence (base case)** | $150,203 | $627,936 | **$778,139** |
| Median-wk29 (cross-check) | $150,203 | $726,380 | $876,583 |
| Aggregate 7-wk | $150,203 | $782,132 | $932,335 |
| Clean-4-wk (upper) | $150,203 | $821,942 | $972,145 |

**Base case + sensitivity band: EOY-2026 ≈ $778K, range $778K–$972K.** DERIVED.

### Full-year run-rate (hypothetical: capture rate × the full 52-week seasonal curve, all scaled
to 2026 level — NOT a mix of actual+projected; this mirrors exactly what the flat ×52 method
already does, just with a seasonal shape instead of a flat one)

Covers only the **44 of 52 weeks** where 2025 has a tab (WK1–3, 5–9 excluded — **not
interpolated**, so this figure structurally undercounts a true 52-week total to whatever extent
those 8 missing weeks carried real volume; no attempt made to estimate that gap).

Sum, projected 2026-scaled units across those 44 weeks: **360,347,272 units.**

| Capture-rate variant | Full-year run-rate (44/52-week basis) |
|---|---|
| **Durable-cadence (base case)** | **$1,055,553** |
| Median-wk29 | $1,221,037 |
| Aggregate 7-wk | $1,314,756 |
| Clean-4-wk (upper) | $1,381,676 |

**Base case + sensitivity band: full-year run-rate ≈ $1.06M, range $1.06M–$1.38M** (44/52-week
basis; true 52-week figure is ≥ this). DERIVED.

---

## 8) Comparison to the flat methods

| Metric | Flat method (no seasonality) | Seasonal method (this doc), base case | Seasonal method, full band |
|---|---|---|---|
| **EOY-2026** | **~$622K** (realized $150,203 + flat WK24–30 avg $21,458/wk × 22 remaining weeks) | **$778,139** (+$155,869 / **+25.0%**) | $778K–$972K (+25% to +56%) |
| **Full-year run-rate** | **~$1.116M** (realized-avg $21,458/wk × 52) | **$1,055,553** (**−5.4%**) | $1.06M–$1.38M (−5.4% to +23.8%) |

DERIVED (flat-method figures recomputed here from the same $150,203-midpoint base the crosstown
doc uses, for an apples-to-apples comparison; they land within $5K of the task brief's own quoted
~$1.11M / ~$620K reference figures, confirming this reproduces the intended baseline).

**What the seasonality adjustment changes, and why:**

- **EOY-2026 is unambiguously HIGHER under every capture-rate variant** (+25% to +56% vs flat
  EOY). The flat method assumes AZIM keeps earning at its WK24–30 average rate straight through
  WK31–52. The measured 2025 shape shows the network's total redirect volume in WK40–52 running
  **~2.0× the WK11–30 baseline** (§3a) — a real Q4 peak. Even holding AZIM's capture rate flat at
  its conservative (durable-cadence) level, that much more total redirect volume flowing through
  the network in Q4 means more of it is available for AZIM's mechanism to intercept, which raises
  the projected back-half $ regardless of which capture-rate cut is used. **This is the headline
  finding: the flat EOY figure is very likely an UNDERSTATEMENT, not a reasonable point estimate,
  because it ignores a demonstrated, measured Q4 volume surge.**
- **The full-year run-rate comparison is genuinely mixed-sign, and that nuance should not be
  smoothed over.** The flat ×52 figure is built from a $/week average that includes WK27's
  one-time crosstown windfall spread flat across all 52 hypothetical weeks. The durable-cadence
  capture rate deliberately excludes that windfall — so even though the seasonal curve correctly
  adds a Q4 volume boost, the LOWER, cleaner capture rate it's paired with is enough to bring the
  base-case full-year figure slightly BELOW the flat ×52 number (−5.4%). Only the sensitivity
  variants that keep some or all of WK27's windfall in the capture rate (median/aggregate/clean-4)
  land above flat ×52. **Bottom line: seasonality raises the volume side of the equation in every
  case; whether the final $ figure ends up above or below the flat number depends on whether the
  capture rate itself still carries the WK27 windfall.**

---

## 9) Caveats — read before citing any number above

1. **n=7 capture-rate sample, and it's highly volatile.** Every capture-rate variant is built from
   just 7 weeks of AZIM history (WK24–30 2026 — the lever's entire tracked existence). Both
   capture-rate metrics carry ~70–81% coefficient of variation across that sample (§5). This is a
   genuinely thin, noisy base for a 22-week-forward projection, not a mature run-rate. Treat the
   sensitivity band as a real statement of uncertainty, not a formality.
2. **2025's shape has an 8-week hole (WK1–3, WK5–9) that was NOT interpolated.** This has zero
   effect on the EOY-2026 estimate (which only needs 2025's fully-present WK31–52), but it means
   the "full-year run-rate" figure (§7) is built on 44 of 52 weeks and structurally understates a
   true 52-week total by whatever those 8 missing weeks actually carried — unknown, not zero.
3. **The steering trackers are live documents, not frozen snapshots.** This pull is dated
   2026-07-26; re-running it even a few days later will likely move the most recent weeks' totals
   (WK25/26/28/30 already moved between the 2026-07-24 and 2026-07-26 pulls — §2). Anything
   downstream of "today's total steering volume" inherits this.
4. **2025-vs-2026 shape disagreement in the mid-year weeks (WK10–23) is real and unexplained.**
   Several weeks diverge by 3–8 percentage points of the overlap-window share (§3b) — plausibly
   one-time events in one year or the other, not diagnosed further here. The AZIM-active window
   (WK24–30) itself is comparatively well matched, which is the relevant reassurance for the
   near-term (WK31–52) projection specifically, but this doesn't validate using 2025's shape for
   anything before WK31 blindly.
5. **WK30's capture-rate jump (5.5%→8.0% units-share) is partly a real correction, partly a
   pull-freshness artifact.** The AZIM-units numerator grew from 267,957 to 385,519 units because
   of the confirmed MCI4→IND9 crosstown addition (a real finding, per the crosstown doc); the
   total-steering denominator also shrank slightly between the 2026-07-24 and 2026-07-26 pulls
   (4.84M→4.81M, a live-document artifact). Both effects point the same direction (higher AZIM
   share), so this isn't a contradiction, but the exact magnitude split between "real new
   crosstown volume" and "stale-vs-fresh total" wasn't separately isolated.
6. **WK25 is a demonstrated data-quality low, not necessarily a demand low** (per the
   annualization doc: its two largest asks failed verification). It's kept IN the primary
   (durable-cadence) capture-rate cut for consistency with Will's already-established $-run-rate
   convention, but the "clean-4-week" variant (which also excludes it) is shown precisely because
   reasonable people could argue either way — it's flagged, not silently resolved.
7. **AZIM's own capture rate has no history before WK24 2026** — there is no way to test whether
   AZIM's real-world capture rate actually rises in Q4 the way this projection assumes (it simply
   assumes the measured capture rate holds constant while volume seasonally rises). IM capacity,
   crew availability, and carrier interchange patterns could all behave differently in Q4 peak
   than they did in the mid-summer weeks this capture rate was measured against — genuinely
   unknown, not modeled.
8. **The $148,841–$151,565 AZIM realized figure and its per-week/per-lane composition were taken
   as given, per task instruction, and NOT recomputed or re-verified in this session** — see
   `azim_reclassified_crosstown_2026-07-24.md` for that figure's own derivation and caveats.

---

## Appendix A — full 2025 seasonal index (share of the 44-week measured annual total, 394,007,190
units)

| WK | Units | Index | WK | Units | Index | WK | Units | Index |
|---|---|---|---|---|---|---|---|---|
| 4 | 13,343,559 | 3.39% | 21 | 3,395,736 | 0.86% | 38 | 10,500,730 | 2.67% |
| 10 | 10,658,779 | 2.71% | 22 | 4,259,981 | 1.08% | 39 | 10,902,282 | 2.77% |
| 11 | 6,023,964 | 1.53% | 23 | 3,990,220 | 1.01% | 40 | 13,880,323 | 3.52% |
| 12 | 22,236,217 | 5.64% | 24 | 7,185,444 | 1.82% | 41 | 16,003,601 | 4.06% |
| 13 | 10,259,798 | 2.60% | 25 | 7,834,852 | 1.99% | 42 | 12,682,060 | 3.22% |
| 14 | 4,135,646 | 1.05% | 26 | 6,628,475 | 1.68% | 43 | 9,556,350 | 2.43% |
| 15 | 5,668,746 | 1.44% | 27 | 4,559,468 | 1.16% | 44 | 14,072,334 | 3.57% |
| 16 | 4,532,579 | 1.15% | 28 | 9,131,266 | 2.32% | 45 | 16,671,672 | 4.23% |
| 17 | 4,835,829 | 1.23% | 29 | 4,609,484 | 1.17% | 46 | 20,058,079 | 5.09% |
| 18 | 6,758,884 | 1.72% | 30 | 5,684,475 | 1.44% | 47 | 18,522,108 | 4.70% |
| 19 | 7,328,742 | 1.86% | 31 | 4,594,911 | 1.17% | 48 | 11,816,161 | 3.00% |
| 20 | 6,555,015 | 1.66% | 32 | 2,965,288 | 0.75% | 49 | 14,315,224 | 3.63% |
| | | | 33 | 1,463,672 | 0.37% | 50 | 13,613,544 | 3.46% |
| | | | 34 | 4,954,603 | 1.26% | 51 | 7,418,848 | 1.88% |
| | | | 35 | 5,672,983 | 1.44% | 52 | 6,958,833 | 1.77% |
| | | | 36 | 6,103,042 | 1.55% | | | |
| | | | 37 | 11,663,383 | 2.96% | | | |

(WK1–3, 5–9: NO TAB — excluded, not interpolated.)

---

## Sources / provenance

- **Quip, live 2026-07-26:** `all_team_slides/build_ytd_from_steering.py`'s
  `enumerate_trackers`/`fetch_records`/`_is_executed` functions, folders `UCF9OAFdxvE` (2025, 44
  trackers WK4–WK52) and `dKL9OAnfDIa` (2026, 31 trackers WK1–WK31, WK31 empty). Auth probe
  (`/1/users/current`) returned HTTP 200 for William Zhou before the pull. Executed-status rows
  only, deduped across weekly trackers on `(date, giver, taker, sim, network)` per
  `build_ytd_from_steering.build()`'s own convention, bucketed by the tracker's own WK label. Raw
  per-week (undeduped) totals also captured for cross-check (§2 freshness note). Nothing exported
  to disk beyond this file and a local temp cache used mid-session
  (`~/_tmp_azim_seasonal_cache.json`, not part of the repo, deleted after use).
- `promo_doc/evidence/azim_reclassified_crosstown_2026-07-24.md` — AZIM realized $148,841–
  $151,565 / 316 loads / 5,291,537 units and its WK24–30 per-week composition. Taken as given,
  per task instruction; not recomputed here.
- `promo_doc/evidence/azim_annualization_2026-07-24.md` — retired-method context (÷16.7%), the
  flat-run-rate methods this doc replaces as the primary forward figure, and the durable-cadence
  exclusion rationale (WK24 launch-burst, WK27 one-time crosstown windfall) extended here to the
  capture rate.
- `all_team_slides/ytd_rollup.json` / `ytd_rollup_2025.json` — read only to confirm network
  category conventions (rIXD/nIXD/NS/ARS/AMXL_CA); not used as a data source for any number above
  (both are monthly-bucketed, stale as of their own generation date, and superseded here by a
  fresh weekly pull).
- Every number above is tagged MEASURED, DERIVED, or EST inline. Nothing was fabricated or
  interpolated across the 2025 gap weeks.
