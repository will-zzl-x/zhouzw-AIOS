# ARC1 — Bar Audit Synthesis: promo_doc_v1.md vs the Shelby/Niko bar

**Date:** 2026-07-12 | **Inputs:** BAR AUDIT (section scoring vs TEMPLATE.md + git a4de771), CLAIMS (source-level verification: live Redshift, Quip, Outlook, Q1 2026 Annual Review PDF, repo grep), ORIGINALS (peer-doc recovery from Matt's 2026-05-15 Slack DM).
**Status:** internal working doc. v1 untouched; all rewrites target a v3 candidate. No external comms.

---

## 1. Executive verdict

**v1 is NOT at the Shelby/Niko bar.** 8 of 10 sections BELOW_BAR, 1 AT_BAR (Scope of Role, with caveats), plus a doc-wide mechanical failure (zero bold spans; one orphan `**` at L43). Claims: **19 VERIFIED / 6 WRONG / 7 UNVERIFIED.** The good news: the June review's honesty fixes held (all L6+ names scrubbed, $12.6M/32% gone, >$22.7M correctly recomputed, alignment-overclaims removed), the underlying content is strong, and the worst defects are concentrated — one contaminated number, one formatting strip, one repeated structural pattern across all five examples.

**The 3 changes that most move committee odds:**

1. **Kill the "-$4M YoY" Introduction claim (fabrication-class).** "-$4M" exists nowhere in the repo except Niko Tellez's own promo doc (his AR-S NTI org-goal line) and TEMPLATE.md quoting it — zero Will-derived source, and v1 self-falsifies it three paragraphs later with the attested $79K actual / $229K projected. A committee member holding Niko's doc sees the identical number. Same defect class as the $12.6M removed 6/28; this sibling was missed. Replace with the attested figures. ~10 minutes; highest single-claim risk in the doc.
2. **Restore the emphasis layer and rebuild all five examples to template DNA.** The doc-wide bold strip (likely a docx round-trip artifact from the 7/10 re-export) breaks DNA #1/#2/#4 in one shot — no bold headline numbers, no bold authorship/sizing/thesis sentences. Each example must become ONE ≤250-word paragraph: bold headline number in sentence 1–2, authorship-verb lead, partner teams named, 3–4 rebalanced LP tags, `*Role guideline:*` close. Episodes and methodology (day-dates, Redshift table names, script/channel names, inline quotes, attestation callouts) move to evidence-file backing. Commit a4de771 (6/22) shows exactly where every bold belonged.
3. **Fix the sizing spine with defensible numbers.** "~302M units/wk" is WRONG low — live WK28 actuals from the flash's own SANDOP query = **450.7M** (rIXD alone 358.7M exceeds the claim); "57 sites (34+23)" reproduces from no current source (canonical map today = 35 rIXD + 23 nIXD = 58). The true numbers make the scope claim STRONGER. Recreate the missing `_canonical_numbers.md` so every figure in the doc traces to a dated, tiered source — right now the numbers pipeline is unauditable by the template's own checklist.

**Bottom line:** one autonomous mechanical pass (accuracy kill-list + bold restore + example rebuild into a v3 candidate) plus one ~45-minute Will decision session (canonical numbers, Ex4 cut, Summary section, OOTO restore) gets this to at-bar. Nothing here requires new evidence generation — everything needed already exists in the repo, the Q1 PDF, or a4de771.

---

## 2. Gap matrix (section × verdict × fix)

| Section | Verdict | Highest-leverage fix |
|---|---|---|
| Career-arc opener (L10-12) | BELOW_BAR | Refresh sizing to canonical (see §3 #1/#4); re-bold present-tense ownership sentence; resolve REVIEW decision A (network-share denominator: re-add sourced, or formally drop) |
| Scope of Role (L20) | AT_BAR | Same sizing fix; re-bold Q/S/T + "The SCMII owns"; restore the dropped "optimizing for disciplined redirect execution within budget" org-goal clause (in a4de771); swap generic-hypothetical pushback vignette for the verified 6/26 gridlock episode's concrete-site shape (no quote); trim 290→~250 |
| Promotion Assessment — Intro (L31-33) | BELOW_BAR | Remove -$4M (Niko bleed — §3 #2); re-bold thesis + consolidation sentences; fill WorkDocs artifacts link (still `[TBD]`) |
| Example 1: 3P IM Rate Restructure (L41-47) | BELOW_BAR | Collapse to ONE paragraph; bold $79K/47%/$229K up front; delete inline JML praise quote + "Manager- and finance-attested" callout (§3 #3); "six weeks"→"four weeks" (§3 #6); drop 7/21 & 8/18 day-dates to evidence; move Have Backbone tag off (its own growth paragraph documents the failure); add Role-guideline line; fix orphan `**` L43; 281→≤250 |
| Example 2: HJBI Drop-to-Live (L52-58) | BELOW_BAR | Collapse to ONE paragraph; re-bold $22.5M; strip Redshift table names / SQL internals / pilot_site_selection.py to evidence backing; entire L56 debugging episode → evidence; LP tags 5→3-4; restore the own-OOTO "system ran without him" claim (review called it the stronger L5 signal — deleted instead); Role-guideline; 360→≤250 (worst offender) |
| Example 3: IPEX Flash Automation (L63-69) | BELOW_BAR | Collapse to ONE paragraph; bold headline hours (pending #7 sourcing decision); name partner teams (only example with none); cut tool inventory + "This isn't 'I used AI'" meta-narration; drop attestation-callout phrasing; anchor "flash of record" with the Flash_Workflow wiki + GitFarm package third-party proof (REVIEW find #5, never incorporated); Role-guideline; 336→≤250 |
| Example 4: OB NTI Flip (L74-80) | BELOW_BAR | DECISION (Will): cut it — peers ran 4 examples + summary, and this one has the weakest number (unaudited "~7 loads/day", no $ outcome) — or rebuild with dated "~7/day at Feb 2026 manual-pilot peak" (§3 #9) and fold TOFC unit-economics into Readiness |
| Example 5: DOE Redirect Automation (L85-91) | BELOW_BAR | Collapse to ONE paragraph; lead with authorship verb (currently "joined... as" / "named William as"); fix "named owner"→authored/owns-the-artifact (§3 #5); correct the constraint-MDP misstatement (Hans analysis found it was NOT the gate); state sign-off routing as PROPOSED, not accomplished; needs a personal headline number or honest framing that the 11,700 is the program goal; drop unsupported Customer Obsession tag; strip script names/criteria formulas; Role-guideline; 347→≤250 |
| Readiness for L5 Scope (L97-112) | BELOW_BAR | Move the inline Matt "asking the right questions" quote out of body (review-induced DNA #5 violation — paraphrase without quotation or move to a feedback section); bold criteria bullets; blank line before L104 (renders as list item); trim 654→~450; content itself is honest and strong — keep the recomputed >$22.7M, PACE-unquantified, trailer-cap honesty framing |
| Doc-wide / mechanical | BELOW_BAR | Restore full bold layer from a4de771; add `*Role guideline:*` close ×5; rebalance LP spread (Bias for Action on 4/5, Dive Deep once); strip header meta L3-5 before Matt sees it; recreate `_canonical_numbers.md` (checklist source file missing from repo entirely) |

---

## 3. Claims table — sorted by committee-credibility risk

### WRONG (6) — fix before anyone sees the doc

| # | Claim (location) | Risk | Source checked | Correction |
|---|---|---|---|---|
| 1 | "~302M units/week" (Opener + Scope, ×2) | HIGH | LIVE Redshift, SANDOP via unified_flash's own network_performance.sql, run 7/12: WK28 actual = rIXD 358.7M + nIXD 92.0M = **450.7M** (plan 449.0M). 302M traces only to doe_handoff_corrected.md (a comparison note, not a query); already flagged 6/29 | "~450M units/week of inbound arrivals (WK28 2026 actual)" — the true number is STRONGER; 302M is indefensible if audited (rIXD alone exceeds it) |
| 2 | "driven a YoY -$4M structural cost reduction in 3P intermodal redirect spend" (Introduction) | HIGH | Repo-wide grep: "-$4M / -95% YoY" appears ONLY in niko_tellez_..._ORIGINAL.md (his AR-S NTI org goal) + TEMPLATE.md quoting it. Zero Will-derived source. Own Q1 2026 Annual Review attests $79K actual / $229K projected | Remove; replace with attested "$229K projected annual, 47% avg cost reduction per move". Same template-bleed class as the removed $12.6M — present since 6/22, missed by the 6/28 review |
| 3 | "Manager- and finance-attested outcome..." (Ex1 attribution) | MED | Q1 2026 Annual Review PDF: figures sit in Will's SELF-REFLECTION section; manager summary endorses only generically; NO Finance attestation anywhere in the PDF | "attested in his Q1 2026 Annual Review" (manager-finalized); drop "finance-" unless a separate Finance artifact exists — and note the attestation-callout phrasing itself is banned in body (DNA #5), so in v3 this moves out of body prose regardless |
| 4 | "57 sites (34 rIXD + 23 nIXD)" (Opener + Scope, ×2) | MED | ict_regions.py canonical map = 35 rIXD (BJC1 launched 6/28); fc_region_full.csv = 35+23; live WK28 = 33 rIXD reporting; the 23 nIXD includes closed WBW2 (5/31) + PPO4 (Mar) + pre-launch GEU5. No current source reproduces 34 rIXD | "58 sites (35 rIXD + 23 nIXD)" with an as-of date, or a dated FOS node-list recount; pick ONE source and pin it in `_canonical_numbers.md` |
| 5 | "named William as the IXD validation-intake owner" (Ex5) | MED | gaps_closed_2026-06-29.md GAP 3 is explicit: "by-assignment + authored artifact, NO explicit 'owner' title"; artifact exists (ixd-redirect-feasibility.intake_v0.5.xlsx, authored 6/4) | Reword to ownership-by-authorship: "assigned the IXD intake and authored/owns the artifact" — which the same paragraph already argues |
| 6 | "six weeks of methodology iteration" (Ex1) | LOW | Outlook record: rate-publication agreement 7/21/2025 → "We are aligned @ $150 + fsc" 8/18/2025 = 4 weeks | "four weeks" — though the altitude pass moves these dates to evidence backing anyway |

### UNVERIFIED (7) — source or soften

| # | Claim (location) | Risk | Source checked | Disposition |
|---|---|---|---|---|
| 7 | "~407 hrs/yr individual + ~224 hrs/yr team-scaling" (Intro, Ex3, Readiness — ×3) | MED | 407 appears only as "Will's 407 hr/yr framing" in ai_training/redirect_exec_ai_training_scope.md; 224 has NO derivation anywhere. Arithmetic self-consistent (90 min/day ≈ 19.6% FTE) | Will decision: derive both into `_canonical_numbers.md`, or soften to "~20% of an FTE" experiential framing; 224 cannot survive as-is |
| 8 | "11,700 hrs/yr... program's 2026 OP plan goal" + Sept-2025/Oct-2025/late-Jan-2026 dates (Ex5) | MED | Repo grep + builder-mcp InternalSearch: no OP-plan artifact carries 11,700; the three dates are Slack-memory with no local artifact | Keep only with program-stated attribution Will can personally stand behind; the three day-dates die in the altitude pass regardless |
| 9 | "has since run ~7 loads per day" (Ex4) | MED | grill_agenda_2026-06-07.md: ~7/day is a FEBRUARY 2026 baseline; 3/4 stop-call; "no current KPI/volume/cost data"; tracker.md is a stub | If Ex4 survives the cut decision: "~7 loads/day at the Feb 2026 peak of the manual pilot" — present-perfect implies currency the data doesn't support ('verify counts before quoting') |
| 10 | "accepted the $150 additive within three days" (Ex1 growth area) | LOW | Outlook 8/18/2025: Will proposed 9:17am, confirmed 9:47am — same-day. Q1 PDF p4 confirms the growth area but gives no window | "same day" or drop the window; growth content relocates out of the example body anyway (DNA #1) |
| 11 | "sitting for four months" / "January 2026 launch had slipped" / "replied within 24 hours" (Ex2 color) | LOW | hjbi_pilot/CLAUDE.md log starts 4/20/2026; Calcote 4-concerns email 4/24 10:33 exists but Will's reply timestamp not retrievable; no artifact for the Jan target | Cut the color — the altitude/brevity pass wants these lines gone anyway |
| 12 | "flash consumed ~2 hours every morning... 4+ Quicksight dashboards, two Excel exports, a Quip Steering doc" (Ex3 baseline) | LOW | No repo artifact quantifies the pre-automation baseline | Keep as experiential testimony (defensible); don't present as audited fact; the tool inventory itself is an outcomes-over-tools cut |
| 13 | "joined Amazon in October 2024" (Opener) | LOW | No local artifact; Q1 PDF has no hire date; Phonetool search returned HTTP 400 | Will confirms in Phonetool/A-to-Z — 30 seconds, impossible from repo |

### VERIFIED anchors (19) — keep and bold

$36.3M budget ($20.4M NVF + $15.9M NTI — live Quip Goals doc); $79K/359 redirects/$229K/684 hrs/$23K (Q1 PDF p2/p4); 47% (p2 — **but p4 of the same signed PDF says 27%**: Will owes Matt a one-line reconciliation heads-up, still unlogged from the 6/28 review); ~$2M overpayment / 2-4 hr / 3+ months; 7/21 + 8/18 email record incl. verbatim $150 quote (verified — but the quote is banned in body); $22.5M / 3,168 / 11.12% / $2.25M / 2%; 3-weeks-to-live / HJBL 5/1 / WK20; the 3 Redshift source names (verified — but banned in body); four-KPI scorecard; 11 stakeholders trained; TOFC $1.7K/$4K/$2.6K/$4.3K/$6.6K; ~12% cap haircut (with correct Will-built-threshold framing); >$22.7M arithmetic; HUBG/PGLI 95%+/200→<50 hrs (correctly framed as goals); "IXD largest of three by unit volume" (live WK28); Matt 6/26 "asking the right questions" quote (verified verbatim — placement banned); GenAI 6-tool suite (all exist; 733 tests repo-wide); PACE ICT-Sort owner / 2027; DBR-WBR-QBR + 2-of-5 rIXD regions; May 2026 three-template distribution.

**Special flag:** "escalations up to three levels above their own" (Scope) is verbatim Niko-template language — a third template echo. Directionally supported by the escalation SOP, but reword to break the fingerprint.

---

## 4. What the recovered originals add

**FOUND — both peer docs, complete and verbatim.** They were never .docx files: Matt pasted the full texts as four Slack DM messages (2026-05-15, ~10:03–10:06 AM AZ, marked "confidential"). Recovered with provenance headers to:

- `C:/Users/zhouzw/ict_automation/promo_doc/reference/shelby_king_L4L5_promo_doc_ORIGINAL.md`
- `C:/Users/zhouzw/ict_automation/promo_doc/reference/niko_tellez_L4L5_promo_doc_ORIGINAL.md`

What this changes for the rewrite:

1. **TEMPLATE.md is now validated, not operative-by-default.** Recovered text matches TEMPLATE's quoted phrases verbatim ("Nik is the center of NTI Balancing/Steering", "26 buildings, 5.03% of network MDP") — the ~7/6 distillation was faithful. The v3 pass should still spot-check DNA rules (paragraph shape, LP-tag counts, Role-guideline mapping, Summary sections) against the originals directly rather than the distillation.
2. **The -$4M contamination is provable at source.** The figure is Niko's own AR-S NTI line in his own doc. Removal is non-negotiable, and v3 QA should grep the candidate against BOTH originals for any other number/phrase echo (the "three levels above" line is one already found).
3. **Peer structure is confirmable at source:** 4 examples each + a people-leadership summary — primary evidence for the Ex4-cut and add-a-Summary decisions.
4. **Caveat: Slack paste loses Word formatting.** The originals canNOT settle bold-layer questions — a4de771 + TEMPLATE's bold requirements remain the operative emphasis source. Pixel-faithful originals would require asking Matt; grading-wise the verbatim text is what matters.
5. **Confidentiality:** the paste was marked confidential. Reference files stay local to promo_doc/reference/, never quoted in v3 body, never redistributed.

---

## 5. NEXT-ARC plan — ordered rewrite passes

Target: `promo_doc/drafts/promo_doc_v3_candidate.md` built from v1 + a4de771. **promo_doc_v1.md is never edited.**

| Pass | What | Effort | Mode |
|---|---|---|---|
| A | **Canonical numbers file.** Recreate `promo_doc/_canonical_numbers.md`: every doc number → tier (live-query / signed-PDF / project-guide / testimony) + source + as-of date. Seed from §3 VERIFIED list + the live 450.7M/58-site pulls. Flag 407/224 and 11,700 as pending decisions | 30 min | Mechanical draft; Will signs the two contested numbers |
| B | **Accuracy kill-list.** Apply all 6 WRONG corrections; date/soften actionable UNVERIFIEDs (#8 dates out, #9 dated, #10 same-day, #11 cut); fix Ex5's two analysis misstatements (constraint-MDP was NOT the gate per the Hans analysis; sign-off routing = proposed, not accomplished) | 45 min | Mechanical |
| C | **Bold restore.** Diff v1 vs a4de771; reapply every bold span (headline numbers, thesis, ownership, sizing, Q/S/T, example titles, LP labels); fix orphan `**` L43; QA = zero-orphan `\*\*` grep + render check | 30 min | Mechanical |
| D | **Example rebuild.** Each example → ONE ≤250-word paragraph: bold number sentence 1–2, authorship-verb lead, partners named, 3–4 LP tags rebalanced (Have Backbone off Ex1, Customer Obsession off Ex5, Bias for Action ≤2), `*Role guideline:*` close. Episodes/methodology/quotes/attestation-callouts relocate to promo_doc/evidence/ backing files | 2–3 hrs | Mechanical draft; Will vets tone + LP mapping |
| E | **Opener / Scope / Intro / Readiness.** Sizing sentences from Pass A; restore org-goal clause; Readiness 654→~450 w/ quote moved out of body; bold criteria bullets; L104 blank line; strip header meta L3-5 | 1–1.5 hrs | Mechanical draft (vignette swap held for Will) |
| F | **Will decision session.** Queue below; fold outcomes into v3 | ~45 min | Judgment |
| G | **Final QA sweep.** Per-section word counts; zero L6+ names scan; Role-guideline ×N; LP-spread check; WorkDocs link present; grep v3 against both ORIGINALs for template echoes; markdown render check | 30 min | Mechanical |

### Mechanical — draftable autonomously into the v3 candidate (v1 untouched)

1. Remove -$4M; substitute attested $229K/47% (WRONG #2)
2. 302M → ~450M WK28-dated, both occurrences (WRONG #1); 57(34+23) → 58(35+23) as-of-dated (WRONG #4) — figures drafted from live pulls, Will ratifies in Pass F
3. "Manager- and finance-attested" → "attested in his Q1 2026 Annual Review", relocated out of body (WRONG #3)
4. Ex5 "named owner" → authored/owns-the-artifact wording (WRONG #5); "six weeks" → "four weeks" (WRONG #6)
5. Ex5 constraint-MDP gate misstatement corrected; sign-off routing stated as proposed
6. Bold-layer restore from a4de771 + orphan `**` fix
7. Five examples collapsed to one paragraph each, ≤250 words, number-first, authorship-verb lead, `*Role guideline:*` close ×5
8. Four banned inline quotes/attestations relocated (JML quote, two attestation callouts, Matt quote in Readiness → paraphrase or feedback section)
9. Methodology strip: Redshift table names, SQL internals, script names, Slack-channel names, criteria formulas → evidence files
10. Altitude strip: all day-dates/episode narration (Ex1 7/21+8/18, Ex2 L56 episode, Ex4 2/13 Quip + channel creation, Ex5 three dates) → evidence files
11. Restore "optimizing for disciplined redirect execution within budget" clause from a4de771
12. Ex3: anchor "team's flash of record" with Flash_Workflow wiki + GitFarm package (REVIEW find #5); name partner teams
13. Ex4 "~7/day" dated to Feb 2026 peak (in the keep-branch of the Pass F decision)
14. Readiness/format mechanics: bold criteria bullets, L104 blank line, header-meta strip, 654→~450 trim draft
15. `_canonical_numbers.md` recreated with tiered provenance
16. QA greps: orphan bold, L6+ names, template-echo scan vs both ORIGINALs

### Judgment calls — need Will

1. **Ratify canonical sizing:** adopt 450.7M (WK28 actual) + 58 sites (35+23, as-of 7/12), or pick a different dated source (FOS node recount); decide plan-vs-actual framing
2. **Cut Example 4?** Peers ran 4 examples + summary; Ex4 is numberless-weak at the 5-example ceiling. Cut and fold TOFC economics into Readiness, or rebuild dated
3. **Add the Summary (people-leadership) section** both peer docs carry — content candidates: 11-stakeholder training, enablement material currently buried in Readiness direction 2
4. **Restore the own-OOTO claim** ("the codified system ran without him") in Ex2/Ex3 — review called it the stronger L5 signal; Will confirms the dates/facts first
5. **407/224 hrs and 11,700 hrs:** derive, attribute-as-program-stated, or cut (224 has zero derivation)
6. **REVIEW decision A:** re-add a sourced network-share denominator or formally drop it
7. **Pushback vignette:** anchor on the 6/26 FTW2 gridlock episode (concrete-site shape, no quote) — Will's comfort call on using that thread
8. **47% vs 27% Q1-PDF self-contradiction:** one-line heads-up to Matt — Will sends personally (no agent comms)
9. **WorkDocs artifacts link** (L33 `[TBD]`) — Will populates
10. **Hire date Oct 2024** — Will confirms via Phonetool/A-to-Z
11. **Matt-quote destination:** paraphrase without quotation vs a separate feedback section

### Definition of done for the v3 candidate

Every number traces to `_canonical_numbers.md`; 0 WRONG claims; UNVERIFIED only where framed as testimony; DNA #1/#2/#4/#5 pass on every example; ≤4–5 examples, each 1 paragraph ≤250 words with Role-guideline close; Readiness ~450; whole doc ~2,300 words (from 2,957); zero L6+ names; zero template echoes vs the recovered originals.


