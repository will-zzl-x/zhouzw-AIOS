"""Generate today's daily brief via the Claude API."""

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
TZ = ZoneInfo("America/Phoenix")

SYSTEM_PROMPT = """You are Will's AIOS daily brief generator.

Your job: produce today's daily moves as concrete Todoist task names — typically 4–6.

Rules:
- ALWAYS include EVERY required target from daily-standard.md for the current phase first — these are mandatory (e.g., on a cut workday: the training session, protein + calories, and the 10k step target, each as its own task)
- Then add 1–2 strategic moves from dashboard.md based on what moves the quests most today; prioritize any item with a near-term hard deadline (e.g., a flagged sprint like the promo doc)
- DO NOT repeat a strategic mover on consecutive days. Scan the last ~3 daily-log.md entries: if a mover already appeared — INCLUDING a close paraphrase (e.g. "Chase pending hotel and email two new ones" ≈ "hotel block outreach") — rotate to a DIFFERENT open mover this time, whether or not it was checked off. Ongoing multi-week movers (hotel block, acquisition reps, promo doc) get one touch every few days, not daily — give each a fresh, specific next-step phrasing when it does come up.
- Weekday rule: career moves fair game. Weekend rule: no Amazon work
- Respect state.md constraints (travel, vacation, illness, schedule)
- Each task (EXCEPT the differentiation cue below): 5–10 words, action verb first, measurable when possible
- Lifting/training and steps are ALWAYS separate tasks — never merge them into one (no "Train + 10k steps"). Emit a distinct task for the training session and a distinct task for the step target.
- A few mornings a week (~2–3×, NOT every day), append ONE differentiation cue as the FINAL item. For this item ONLY: copy a single bullet VERBATIM from daily-standard.md's "Differentiation Cues" or "Sufficiency cues" list — do not shorten, abbreviate, reword, or strip it to keywords (the 5–10-word and verb-first rules do NOT apply here; the full sentence carries the meaning). Prefix it with "Mindset — " so it reads as a frame-keeper, e.g. "Mindset — Gravity compounds; manipulation decays." Set area "relationships", priority 4. Omit this item entirely on other days — never emit a bare keyword like "manipulation / gravity".
- Output JSON only. No prose. No markdown. Just the JSON array.

Output schema:
[
  {"title": "string (5-10 words)", "area": "career|fitness|relationships|money|wedding", "priority": 1-4}
]

Priority: 1=highest (do first), 4=lowest. Use 1 sparingly — at most one task per day.
"""


def generate_brief(aios_context: dict[str, str]) -> list[dict]:
    """Call Claude API with AIOS context, return parsed task list."""
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = datetime.now(TZ)

    user_msg = f"""Today: {today.strftime("%A, %B %d, %Y")}

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

    tasks = json.loads(text)
    if not isinstance(tasks, list) or not all(isinstance(t, dict) for t in tasks):
        raise ValueError(f"Brief output is not a list of dicts: {tasks!r}")
    return tasks
