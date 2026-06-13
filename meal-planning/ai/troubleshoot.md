# AI Template — Ad-hoc Cook Rescue (TOKENS)

**When to run:** something is going wrong mid-cook and you need a fast fix —
sauce broke, protein overcooking, texture off, timing collision, substitution
needed. This is a real-time judgment call, the one fuzzy task scripts can't do.

**Output contract:** the single most likely fix first, then 1–2 alternates. Tight
and actionable — you're standing at the stove.

---

## Inputs (say what's happening)
- The recipe (id or name) + which step you're on.
- The symptom (broke / dry / bland / burning / undercooked / too thin/thick / timing).
- What equipment + ingredients you have right now.

## Context the rescue should respect
- **Equipment:** air fryer, rice cooker, 6qt enameled Dutch oven, wok, instant pot,
  slow cooker, Ninja Creami, cast iron. Electric stove, burner max 9.
- **Kitchen rules (from config):**
  - avocado oil high-heat; olive oil low-heat / air-fryer.
  - electric-stove Dutch oven: preheat 60–90s max, water-drop test (burn risk).
  - dissolve bouillon in warm water first.
  - day-old chilled rice for fried rice (fresh rice = mush).
  - salmon: never microwave; oven/air-fryer 325°F to reheat.
  - air-fried kale goes limp in storage.
- **Cut-aware:** prefer low-cal fixes (Greek yogurt to thicken/cool, low-cal sauces,
  acid + heat over butter/oil/sugar) when they'll work.

## Output format
```
Most likely fix: <one move, why it works>
If that doesn't take: <alternate 1>
Last resort / salvage: <alternate 2 — what to do so it's still edible/meal-preppable>
Prevent next time: <one line>
```
Keep it to what can be done in the next few minutes with what's on hand.
