"""Generate today's daily brief via the Claude API."""

import json
import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

from anthropic import Anthropic

from backlog import filter_eligible, parse_backlog

MODEL = "claude-sonnet-4-6"
TZ = ZoneInfo("America/Phoenix")

SYSTEM_PROMPT = """You are Will's AIOS daily brief generator.

Your job: produce today's daily moves as concrete Todoist task names — typically 5–8.

The output is a layered stack: (A) required-target gates from daily-standard.md, (B) Daily Consistents from dashboard.md, then (C) 1–2 Major Moves from the strategic_moves list. Layers A and B are mandatory and never rotate. Only layer C is subject to anti-repeat.

Rules:

1. DAILY-STANDARD GATES (mandatory, always emit, never rotate, sm_id: null) —
   ALWAYS emit EVERY required target from daily-standard.md's current-phase "Done when" gates as its own task. On a cut workday this is the training session, protein target, calorie target, and the 10k step target — each as a distinct task. Lifting/training and steps are ALWAYS separate tasks; never merge them (no "Train + 10k steps").

2. DAILY CONSISTENTS (mandatory if still open, always emit, never rotate, sm_id: null) —
   ALWAYS emit EVERY item from dashboard.md's "## Daily Consistents (every day, do not rotate)" section that is still open. These are cross-area daily gates: BJJ booking until done, Sunday paste habit on Sundays only, Elena presence beats, friend cadence when due, Zone 2 cardio, etc. Apply day-of-week constraints when the consistent specifies one (e.g. a "Sunday paste" item only fires on Sundays). If the consistent is already marked complete in dashboard.md or shows up as done in today's daily-log.md, omit it.

3. MAJOR MOVES (1–2 items, sm_id REQUIRED, anti-repeat applies) —
   THEN add 1–2 Major Moves drawn ONLY from the strategic_moves list provided in the user message. That list is already pre-filtered for eligibility (status open/in-progress, gate satisfied, all blockers done) — do not invent moves and do not pull from elsewhere. Pick by, in order:
     a. **Hard deadline within 7 days wins regardless of quest tag** — any move with gate "deadline:YYYY-MM-DD" within 7 days of today goes first. Deadlines override the quest filter.
     b. **Prefer Main Quest items over Side Quest items** at every remaining tier. Each strategic_moves entry has a `quest` field with values: "work-main" / "life-main" / "side" / "not-quest". When picking 2 Major Moves, aim for one work-main AND one life-main if both are available. If only one Main Quest tier has eligible items, fill with the highest-priority side or not-quest item.
     c. Within each quest tier (e.g. all work-main items), apply secondary priority:
        - Hard deadline within 14 days first
        - Then window-locked items (gate "window:MM-DD..MM-DD" where today is in window)
        - Then drift items (no recent touch in journals/daily-log.md)
        - Then rank order (lower # = higher priority)
   Each Major Move task MUST include the sm_id field, copied VERBATIM from the strategic_moves entry's id.

4. ANTI-REPEAT (Major Moves ONLY) —
   Do NOT surface a Major Move that already appeared in journals/daily-log.md in the last 2 days, INCLUDING close paraphrases (e.g. "Chase pending hotel and email two new ones" ≈ "hotel block outreach"). Rotate to a different eligible move. EXCEPTION: a hard deadline within 7 days overrides anti-repeat — surface it anyway. Daily Consistents and required-target gates are NEVER subject to anti-repeat.

5. WEEKDAY/WEEKEND ROUTING — Weekday: career Major Moves fair game. Weekend: no Amazon work; pick non-career Major Moves only.

6. STATE CONSTRAINTS — Respect state.md (travel, vacation, illness, schedule).

7. TASK SHAPE — Each task EXCEPT the differentiation cue below: 5–10 words, action verb first, measurable when possible. Give recurring movers a fresh, specific next-step phrasing each time.

8. DIFFERENTIATION CUE (~2–3× per week, NOT every day) — On those mornings, append ONE cue as the FINAL item. For this item ONLY: copy a single bullet VERBATIM from daily-standard.md's "Differentiation Cues" or "Sufficiency cues" list — do not shorten, abbreviate, reword, or strip it to keywords (the 5–10-word and verb-first rules do NOT apply here; the full sentence carries the meaning). Prefix it with "Mindset — ". Set area "relationships", priority 4, sm_id null. Omit entirely on other days — never emit a bare keyword.

9. OUTPUT — JSON array only. No prose. No markdown fences. 5–8 tasks total.

Output schema:
[
  {"title": "string (5-10 words)", "area": "career|fitness|relationships|money|wedding", "priority": 1-4, "sm_id": "string | null"}
]

Example (illustrative — your actual output reflects today's context):
[
  {"title": "Train Session 4: squat + press triples", "area": "fitness", "priority": 2, "sm_id": null},
  {"title": "Hit 180g protein, 2200 kcal", "area": "fitness", "priority": 2, "sm_id": null},
  {"title": "Walk 10,000 steps", "area": "fitness", "priority": 3, "sm_id": null},
  {"title": "Book BJJ trial class this week", "area": "fitness", "priority": 3, "sm_id": null},
  {"title": "Send promo doc draft to Matt for review", "area": "career", "priority": 1, "sm_id": "promo-doc-final"}
]

Priority: 1=highest (do first), 4=lowest. Use 1 sparingly — at most one task per day.
sm_id: required field. String for Major Moves (copy verbatim from strategic_moves). null for daily-standard gates, Daily Consistents, and the differentiation cue.
"""


def build_strategic_moves_section(backlog_text: str, today: date) -> str:
    """Format the eligible strategic moves as a JSON section for the user message.

    Parses backlog.md, applies the eligibility filter (status open/in-progress,
    gate satisfied for `today`, all depends-on resolved to done), and returns
    a labeled section the LLM can read directly. Each entry exposes the fields
    the prompt actually needs: id, title, area, gate, notes.
    """
    moves = parse_backlog(backlog_text)
    eligible = filter_eligible(moves, today)
    payload = [
        {
            "id": m["id"],
            "title": m["title"],
            "area": m["area"],
            "quest": m["quest"],
            "gate": m["gate"],
            "notes": m["notes"],
        }
        for m in eligible
    ]
    body = json.dumps(payload, indent=2, ensure_ascii=False)
    return (
        "# strategic_moves (eligible from backlog.md, status:open or "
        "in-progress, gating-clear, depends-on satisfied)\n\n"
        "# quest values: work-main / life-main / side / not-quest — "
        "Main Quest items (work-main, life-main) get priority when picking "
        "Major Moves per Rule 3.\n\n"
        f"{body}"
    )


def generate_brief(aios_context: dict[str, str]) -> list[dict]:
    """Call Claude API with AIOS context, return parsed task list."""
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = datetime.now(TZ)

    strategic_moves_section = build_strategic_moves_section(
        aios_context.get("backlog", ""), today.date()
    )

    user_msg = f"""Today: {today.strftime("%A, %B %d, %Y")}

{strategic_moves_section}

# priorities.md
{aios_context["priorities"]}

# state.md
{aios_context["state"]}

# daily-standard.md
{aios_context["daily_standard"]}

# dashboard.md
{aios_context["dashboard"]}

# daily-log.md (recent completions — use to avoid re-surfacing finished weekly movers)
{aios_context["daily_log"]}

Generate today's brief as JSON."""

    resp = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    text = resp.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    # Defensive extraction: model sometimes adds a prose preamble or unknown
    # fence variant. Find the JSON array bounds and parse just that slice.
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"No JSON array found in brief output. Raw text: {text!r}")
    text = text[start : end + 1]

    try:
        tasks = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Brief output is not valid JSON ({e}). Raw text: {text!r}") from e
    if not isinstance(tasks, list) or not all(isinstance(t, dict) for t in tasks):
        raise ValueError(f"Brief output is not a list of dicts: {tasks!r}")
    return tasks
