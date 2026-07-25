# Cycles index

**Layout rule:** the CURRENT cycle (yaml + its `-cook-plan.md`) lives at the top
level of `cycles/`; everything older lives in `cycles/archive/` (preserved, never
deleted). Scripts default to the newest TOP-LEVEL yaml (`lib/models.latest_cycle_path`
deliberately does not descend into `archive/`), so archiving can never change which
cycle `make week` runs. `make new-cycle` auto-archives the prior top-level cycle.

> When a new cycle starts: `make new-cycle` moves the old one to `archive/` —
> then update this index (new row on top, move the CURRENT marker).

## CURRENT CYCLE → [`2026-07-25.yaml`](2026-07-25.yaml) · [cook plan](2026-07-25-cook-plan.md)

## All cycles (newest first)

| Cycle | Files | One-liner |
|---|---|---|
| **2026-07-25** (CURRENT) | `2026-07-25.yaml`, `-cook-plan.md` | SHORT pre-NYC fridge-clear (Sat 7/25→Wed 7/29; fly Thu 7/30). Cook-almost-nothing-new, ~$0 grocery. Steak & salad, crispy chicken sandwich (#5), chicken parm, spaghetti-squash bolognese, egg bake + hot dog. Planned off a 7/24 photo audit; note-only cooks; deplete AFTER NYC. |
| 2026-07-18 | `archive/2026-07-18.yaml`, `-cook-plan.md` | First post-Banff full cycle. Egg-roll ramen (aging coleslaw, Sat cook #1), ginger-scallion chicken (fresh-pack swap), taco salad, fried rice (day-old rice), chipotle bowls, rotisserie. 4 cooks Sat / 3 preps Sun. |
| 2026-06-27 | `archive/2026-06-27.yaml` | Banff-split cycle. IP shredded chicken (urgent, pre-party), NY strip send-off, ginger-scallion chicken, crunchwraps, 2x spaghetti frozen for Elena's solo week. Depleted `--apply` 2026-07-17. |
| 2026-06-20 | `archive/2026-06-20.yaml` | Compressed SoCal-travel cycle — away Sat/Sun, Monday cook day, both slow cookers post-lift. |
| 2026-06-13 | `archive/2026-06-13.yaml`, `-cook-plan.md`, `-grocery.md`, `-socal-snacks.md` | Shortened by SoCal trip (home window Sat–Thu dinners + Fri M1). |
| 2026-06-07 | `archive/2026-06-07.yaml` | Hand-seeded SAMPLE cycle (demo target for the README quick start; never cooked). |
| 2026-06-06 | `archive/2026-06-06.yaml`, `-cook-plan.md`, `-grocery.md`, `-retro.md` | First real cycle. Retro produced the false-BUY findings that drove the fuzzy matcher. |
