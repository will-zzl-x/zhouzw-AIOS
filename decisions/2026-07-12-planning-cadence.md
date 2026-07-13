# Decision — Planning Cadence Stack (2026-07-12)

**Context:** During the Jul 12 weekly reflection, Will asked whether Todoist automatically re-prioritizes off weekly reflection updates (answer: by design yes, in practice no — see bug below), and whether the AIOS should run a multi-year / yearly / quarterly / monthly / weekly / daily planning system "or maybe less, whatever proven experts think works best."

## Decision 1 — The stack is Abdaal LifeOS, with one layer added and one explicitly rejected

Expert survey run 7/12 (sources below). All four converge on the same architecture; the stack ratified:

| Altitude | Ritual | Cadence | Owner |
|---|---|---|---|
| 3-year vision | 3-Year Sketch (re-run fresh) | Annually, inside annual review | `/annual-review` |
| **Yearly themes** | **Annual Review — NEW** | **2nd Sunday of December** (first: Dec 13, 2026) | `/annual-review` |
| Quarterly quests | RAP quarterly review | ~Feb / May / Aug / Nov | `/quarterly-review` |
| Weekly | Synthesis (Fri) + Reflection (Sun) | Weekly | `/weekly-synthesis`, `/weekly-reflection` |
| Daily | Morning brief → Todoist → evening archive | Daily 7am/9pm AZ | `cloud/morning-brief/` |

- **System chosen: Ali Abdaal LifeOS** (life compass → yearly themes → quarterly quests → weekly/daily) — the framework the quarterly review, quest vocabulary, and backlog quest-tags were already built on. The annual review is its previously-missing top layer. Anchor: standalone date (Will's pick), 2nd Sunday of December — clear of holidays, between the Nov and Feb quarterlies.
- **Monthly layer: REJECTED** for the general system. GTD makes weekly the only hard cadence below annual; Newport's multi-scale planning runs quarterly/weekly/daily with no monthly; this repo's own history shows even the weekly cadence slips under load (no reflection ran Jul 5). More layers fragment the same Sunday attention; they don't multiply it. Exception unchanged: `/relationship-os` keeps its domain-specific monthly check-in.
- **Hard rule inherited:** themes are annual and directional; quests are quarterly with win conditions; the annual never sets quests.

**Sources:** [Abdaal LifeOS](https://aliabdaal.com/lifeos) + [quarterly reflection ritual](https://aliabdaal.com/newsletter/its-time-for-your-quarterly-reflection/) · [GTD Horizons of Focus](https://gettingthingsdone.com/2011/01/the-6-horizons-of-focus/) (annual review at the 50k purpose/vision level) · [Newport multi-scale planning](https://www.asyncagile.org/blog/multi-scale-planning) (quarterly as top operational layer, the "less" option) · [Hyatt Full Focus](https://fullfocusplanner.com/system/) (annual→quarterly→weekly→daily cascade; considered, rejected for vocabulary overlap with existing quest machinery).

## Decision 2 — The reflection→Todoist pipe: root cause + fix

**Bug:** the morning brief Cloud Function reads `state.md`/`dashboard.md`/`backlog.md` from GitHub raw URLs on `AIOS_BRANCH` (default `master`, per `cloud/morning-brief/aios_reader.py`) — but Claude sessions push reflection updates to per-session `claude/*` branches. Result: weekly reflections were updating the files correctly and the daily brief never saw them. The README's env-var table also documented a wrong default branch (fixed 7/12).

**Fix + standing rule:** every reflection/synthesis session must land its changes on `master` (PR merge same-session, not just push the working branch). The 7/12 reflection is the first to follow it. If the deployed function's `AIOS_BRANCH` env var is set to something other than `master`, reset it to `master` at next deploy — `master` is where the evening archiver already commits, making it the only self-consistent choice.

## Registration caveat (action for Will)

`CLAUDE.md` is generated from `~/.agent-context/projects/aios.md` (personal laptop) — the `/annual-review` row and cadence line added to `CLAUDE.md` on 7/12 must be ported into that canonical source before the next `sync.py` run, or the registration gets clobbered.
