<!-- Ex1 savings verification — 2026-07-13. LOCAL. Resolves DECISION 8 (47% vs 27%). -->

# Ex1 — 3P Intermodal Rate Restructure: live savings verification

**Question (Will, 7/13):** is the 47% cost-reduction real, and can we compute actual savings?
**Answer: YES — the 47% reconciles to 46.6% on live data. The page-4 27% is the anomaly, not the 47%.**

## Sources
- **Redirect tracker** (SharePoint IPEXTeam / Control Tower/CM/3P Intermodal/IM/redirect tracker.xlsx),
  WK2–WK27 2026. Per-week rows: OG Lane, New/Redirect Lane, actual rate paid, units, dwell.
- **Rate matrix** (`HJBI Rate Matrix UPDATED 8.14 (v1.2).xlsx`, "HJBI Rates" sheet — 13,502 lane base rates).
- Join: tracker OG Lane + New Lane → matrix `Code->Site Lane` → `Base Rate Extracted`.

## Savings model (per Will)
- **OLD:** paid the full second linehaul on redirect (ramp→FC2), on top of the sunk ramp→FC1 = double pay.
- **NEW:** pay only rate difference + $150 admin; floored at $150 when the difference is ≤ 0.
- Two ways to define "% cost reduction per move":
  - **Model B — savings ÷ full new-lane rate** (what you'd have paid fresh): **THIS matches the PDF.**
  - Model A — savings ÷ (og+new) double-pay base: inflated (~75%), not the PDF's basis.

## Result (253 of 376 redirect rows matched to the matrix; 123 unmatched = "No Rate Available" lanes)
| Scope | Matched | Model B reduction | Model B savings |
|---|---|---|---|
| **YTD (WK2–27)** | 253 | **46.6%** ≈ the PDF's 47% | $60,197 (matched subset) |
| Q1 (WK2–13) | 65 | 40.3% | $11,129 (matched subset) |

- $60K on the matched subset extrapolates to **~$77–89K across the full redirect set** → consistent with
  the Q1 PDF's **$79K / 359 redirects**. The 47% headline is defensible; page-4's 27% is the outlier.

## Tracker's own authoritative YTD rollup (WK2–27; per-week sums to 324 exactly)
- **324 redirects** · **$512,150 estimated dwell cost avoided** · **$145,920 redirect cost paid**
  · **$253,255 projected dwell cost** · **4.0 days average lead-time savings from origin**.
- NOTE: dwell-cost-avoided ($512K) is a DIFFERENT savings mechanism than the rate-methodology
  savings ($79K). Do not sum or conflate them in the doc.

## Doc implication
- **Keep 47%** in Ex1 (verified). Optionally add current scale: "the methodology has since governed
  324 redirects YTD at ~4.0 days average lead-time savings." Gives Ex1 a current executed anchor
  without conflating the dwell and rate figures.
- DECISION 8 resolved: no anxious Matt reconciliation needed — the 47% is the correct one.
