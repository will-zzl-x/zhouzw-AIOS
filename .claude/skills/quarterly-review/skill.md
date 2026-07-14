---
name: quarterly-review
description: Quarterly Review — Reflect, Align, Plan. The 90-day reset that sets Will's main quests for work and life. Run once per quarter before the weekly reflection. Triggered by "quarterly review", "quarterly planning", "quarterly reset", or "/quarterly-review".
---

## Goal

Run the full Reflect → Align → Plan sequence. Takes 30–45 minutes. Output: a completed quarterly review file, updated quests in state.md, and a fresh dashboard.

Do not rush this. It's the most leveraged hour Will spends all quarter.

## Reads

- `state.md` — current life model
- `context/` — all context files
- `archives/` — last quarterly review + last weekly reflection
- `archives/YYYY-annual-review.md` (latest, if present) — **yearly themes steer this quarter's quest selection**; flag any proposed main quest that serves no theme
- `goals/` — active GPS docs
- `journals/inbox.md` — any pre-session captures
- `references/integrated-coach.md` — coaching lens

## Writes

- `archives/YYYY-QN-quarterly-review.md` — full quarterly review document
- `state.md` — updated with new quests
- `dashboard.md` — regenerated for the new quarter

---

## The RAP Framework

**Step 1 — Reflect:** Honest look at where you actually are.
**Step 2 — Align:** Clarify where you want to be heading (3-year direction).
**Step 3 — Plan:** Set the two main quests (work + life) for the next 90 days.

---

## Steps

### Phase 1 — Load Context (silent)
Read all files above. Note: what's changed since last quarter? What goals are active? Any notable drift between state.md and reality?

---

### Phase 2 — Reflect

**2A — Wheel of Life**

Present Will with 9 categories and ask him to rate each 0–10, plus a 10th for Joy — **rated against `references/wheel-of-life-rubric.md`** (find the band whose markers you meet; pick the number within the band by instinct):

```
Work area:
- Mission (does your work feel meaningful/purposeful?)
- Money (financial situation vs. where you want to be)
- Growth (are you developing, learning, advancing?)

Health area:
- Body (physical health, fitness, how you feel)
- Mind (mental clarity, stress, cognitive energy)
- Heart (emotional state, resilience, inner peace)

Relationships area:
- Romantic (connection with Elena)
- Family (mom, brother)
- Friends (quality and consistency of friendships)

+ Joy (are you actually enjoying your life right now?)
```

Format the ask as:
> "Rate each of these 0–10. Don't overthink it — first instinct. I'll calculate which areas have the most room. Mission, Money, Growth, Body, Mind, Heart, Romantic, Family, Friends, Joy."

After Will responds, show a simple summary:
```
Wheel of Life — [Date]

Work:     Mission [X] | Money [X] | Growth [X]
Health:   Body [X]    | Mind [X]  | Heart [X]
Relations: Romantic [X] | Family [X] | Friends [X]
Joy: [X]

Lowest scores: [list the 3 lowest]
Strongest scores: [list the 3 highest]
```

**2B — What's Working / What's Not**

Ask:
> "Two columns: Work and Life. Two rows: what's working and what's not. Give me bullet points. Rule: what's working must have at least twice as many items as what's not working."

After Will responds, reflect back a synthesis — what patterns do you see? Name the 1–2 things with the most leverage.

---

### Phase 3 — Align

**3A — 3-Year Sketch**

Ask:
> "It's [today's date + 3 years]. Things went well. What does your life look like? Where are you living, what are you working on, what does your relationship look like, what does your body feel like, what do your days feel like? Don't filter for realism — aim for what would actually feel great."

This should feel slightly aspirational and exciting. If the answer feels dull or obligatory, push back: "Is that actually what you want, or what you think you should want?"

After Will responds, synthesize the sketch into a short paragraph and 3–5 directional themes (e.g., "out of corporate, living in Dallas, business generating $X, strong body, more adventure with Elena").

---

### Phase 4 — Plan

**4A — Work Main Quest**

Ask:
> "One main quest for work this quarter. What is the single most important thing you could accomplish in the next 90 days that would move the needle most? Forget side projects — what's the one thing?"

Prompts if stuck:
- What would make you most proud 90 days from now?
- What one thing would make everything else easier?
- What have you been putting off that you know would be transformative?

Once Will names it, use this exact phrasing template to flesh it out (ask Will for each piece):

```
My work main quest is to: [specific outcome]

This is the single most important thing for me to accomplish this quarter because:
[Why it matters — intrinsic, not obligatory]

To complete the quest I commit that by [end date] I will have:
1. [objective, verifiable outcome A]
2. [objective, verifiable outcome B]
3. [objective, verifiable outcome C — optional]

This feels exciting and compelling because:
[The emotional pull — why this one, why now]

To make sure I complete the quest I am going to:
1. [concrete system or commitment]
2. [accountability mechanism]
3. [calendar or tracking action]
```

**Realism check:** before finalizing — does following this plan actually get Will there? What's the realistic chance he follows through? If either answer feels under 80%, the quest needs to be scoped or structured differently.

**4B — Life Main Quest**

Same process, different framing:

> "One main quest for life this quarter — not work. What one thing, if accomplished, would bring the most joy, peace, or fulfillment to your personal life?"

Prompts if stuck:
- What would positively impact every other area of your life?
- What have you been avoiding that would be transformative?
- If you dedicated 1 hour per day to X, what X would matter most?

Use the same template — fill in the life quest version.

**4C — Side Quests (optional)**

After main quests are locked:
> "Side quests: 2–3 things you want to make progress on but won't die if they slip. These are nice-to-have, not commitments. What are they?"

---

### Phase 5 — Write Outputs

**1. Write `archives/YYYY-QN-quarterly-review.md`:**

```
# Quarterly Review — [Q and Year]
Date: [date]
Next review: [date approximately 90 days out]

---

## Wheel of Life

| Category | Score |
|----------|-------|
| Mission | [X]/10 |
| Money | [X]/10 |
| Growth | [X]/10 |
| Body | [X]/10 |
| Mind | [X]/10 |
| Heart | [X]/10 |
| Romantic | [X]/10 |
| Family | [X]/10 |
| Friends | [X]/10 |
| **Joy** | [X]/10 |

Lowest: [X, X, X] | Strongest: [X, X, X]

---

## What's Working / What's Not

**Work — Working:** [bullets]
**Work — Not Working:** [bullets]
**Life — Working:** [bullets]
**Life — Not Working:** [bullets]

---

## 3-Year Sketch — [target date]

[Paragraph synthesizing Will's vision]

**Directional themes:** [3–5 themes]

---

## Main Quests — [Quarter]

### Work Main Quest
[Full quest using the template above]

### Life Main Quest
[Full quest using the template above]

### Side Quests
- [side quest 1]
- [side quest 2]
- [side quest 3 — optional]

---

## Carry-Forward
[1–2 sentences: what's the single most important thing to remember entering this quarter]
```

**2. Update `state.md`:** Add the new main quests to the Career and relevant sections. Mark old quests as complete or rolled over.

**3. Regenerate `dashboard.md`:** Movers for the first week of the new quarter, anchored to the main quests.

**4. Commit the repo:** `quarterly review [Q and Year]`

---

## Rules

- This is a 30–45 minute session. Don't rush Phase 2 — the reflection is what makes the plan real.
- Only one work main quest. Only one life main quest. Push back if Will tries to add a second.
- The quest template is not optional — the specific phrasing (especially the emotional why and the objective criteria) is what makes these stick.
- Objective, verifiable criteria means someone else could check whether Will did the thing. "Procrastinate less" fails. "Log 180 focused minutes/day 80% of workdays" passes.
- The 3-year sketch should feel exciting. If it feels like a to-do list, it's not a sketch — it's a plan. Push for the emotional picture.
- If Joy score is below 6, flag it before moving to planning. Don't paper over it with more goals.
- Side quests are optional. If Will has more than 3, cut them. The whole point is focus.
- Run this quarterly: February, May, August, November roughly. Flag if it's been >100 days since the last one.
