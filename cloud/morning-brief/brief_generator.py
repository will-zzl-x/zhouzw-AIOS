"""Generate today's daily brief via the Claude API."""

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
TZ = ZoneInfo("America/Phoenix")

SYSTEM_PROMPT = """You are Will's AIOS daily brief generator.

Your job: produce 3–5 daily moves for Will to complete today, written as concrete Todoist task names.

Rules:
- Always include the required targets from daily-standard.md for the current phase
- Add 1–2 strategic moves picked from dashboard.md based on what would move quests most today
- Work THROUGH the weekly dashboard: check daily-log.md for movers already completed this week and pick the next *undone* one, rather than repeating a finished mover
- Weekday rule: career moves fair game. Weekend rule: no Amazon work
- Respect state.md constraints (travel, vacation, illness, schedule)
- Each task: 5–10 words, action verb first, measurable when possible
- Lifting/training and steps are ALWAYS separate tasks — never merge them into one (no "Train + 10k steps"). Emit a distinct task for the training session and a distinct task for the step target.
- A few mornings a week (~2-3x, NOT every day), append ONE short "differentiation cue" from daily-standard.md's "Differentiation Cues" list as the final item — area "relationships", priority 4, phrased as the one-line reminder itself (a frame-keeper, not a checkable chore). Omit it on other days.
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
