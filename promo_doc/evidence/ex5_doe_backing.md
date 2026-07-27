# Example 5 backing — DOE Redirect Automation (stripped from v3 body)

## Undated/unverified dates (removed from body — ARC1 §3 #8)

- "joined the DOE program channel September 2025", "SIM-generation broke October 2025", "TX_GL → TX_MT region-mapping update late January 2026" — Slack-memory, no local artifact reproduces them. Body keeps the events, drops the dates.

## Script names + criteria formulas (banned in body)

- `sim_auditor.py` — SIM auditor; gate = Tagawa buffer x total-MDP x Gap-to-Goal (REVIEW 6/28 #8 corrected attribution).
- `validate_redirect.py` — CLI redirect validator; 5-criterion (3 giver-side + 2 taker-side A/B).
- v1 gate formula in body ("constraint-MDP gaps, WK+1 Gap-to-Goal, and giver BL vs regional-mean+sigma") — relocated here.

## Constraint-MDP correction (applied in body — ARC1 §5 B item 5)

Hans-approval reverse-engineering (`reconstruct_approval.py`; REVIEW 6/28 find #4): the assumed MDP-gap >=4d rule was NOT the gate — 10/11 approvals cleared below it; real drivers = giver buffer + WK+1 backlog persistence. Honesty limits: rejection class n=2; Hans never confirmed the reconstruction. Body states the finding as Will's analysis, claims no confirmation.

## Ownership evidence (GAP 3, `evidence/gaps_closed_2026-06-29.md`)

- Will authored + uploaded `ixd-redirect-feasibility.intake_v0.5.xlsx` to the program lead, 6/4 3:11pm AZ.
- 6/23 12:59pm AZ — Will orchestrating validation design: VSCOR inputs + **proposed** Hans/Naresh final signoff for rIXD/nIXD/USNS. Body states sign-off routing as PROPOSED, not accomplished (ARC1 §5 B item 5).
- v1's "named William as the IXD validation-intake owner" was WRONG (§3 #5): by-assignment + authored artifact, no explicit owner title. Body reads "assigned the IXD intake — and made it ownership by authorship."

## Name key (banned in body prose)

DOE/GL-redirects program lead = Federico Capello (`capelf@`) — "the program lead" in body. Channel `#doe-gl-redirects` (`C094P9KDWBB`).

## Consciously trimmed from v3 (ARC2 LOW-2b — restore if wanted)

v1 close: "That distinction positions William as the program-level translator between IPEX-ICT operational standards and the cross-org engineering team building Amazon's network-wide redirect automation." Dropped in the ≤250-word collapse; the authored-algorithm/program-owns-surface distinction survives in body.

## 11,700 hrs/yr (PENDING-WILL — DECISION 5b)

No OP-plan artifact carries it (repo grep + InternalSearch). Body attribution: "the program's stated goal." Cut if Will can't personally stand behind that.
