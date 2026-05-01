from openai import OpenAI
from models.schema import PlanLengthEstimate, StudyPlan
import json
from config import OPENAI_API_KEY
from config import MODEL_NAME
from config import MAX_PLAN_DAYS
from config import MIN_PLAN_DAYS
from memory.schema import StudyMemory

client = OpenAI(api_key=OPENAI_API_KEY)


def suggest_plan_num_days(
    goal: str,
    max_min_per_day: int,
    memory: StudyMemory,
) -> PlanLengthEstimate:
    response = client.responses.parse(
        model=MODEL_NAME,
        input=[
            {
                "role": "system",
                "content": f"""
You estimate how many consecutive study days are needed to make solid progress on the learner's goal.

Rules:
- Use only the goal text, the stated minutes per day ({max_min_per_day}), and memory (completed topics) — do not invent external exam dates unless the goal states them.
- If the goal gives a horizon (e.g. "two months", "8 weeks"), translate that into a reasonable number of study days (e.g. weekdays only or full weeks — state your assumption briefly in rationale).
- Output a single integer `num_days` between {MIN_PLAN_DAYS} and {MAX_PLAN_DAYS} inclusive.
- Prefer realistic pacing over cramming; more daily minutes can support a shorter calendar span only if justified.
""",
            },
            {
                "role": "user",
                "content": f"""
Goal:
{goal}

Minutes available per study day: {max_min_per_day}

Learner memory:
{json.dumps(memory.model_dump(mode="json"), indent=2)}
""",
            },
        ],
        text_format=PlanLengthEstimate,
    )
    return response.output_parsed


def clamp_plan_num_days(raw: int) -> int:
    return max(MIN_PLAN_DAYS, min(MAX_PLAN_DAYS, raw))


def create_study_plan_with_memory(
    goal: str,
    max_min_per_day: int,
    memory: StudyMemory,
    plan_num_days: int,
) -> StudyPlan:
    response = client.responses.parse(
        model=MODEL_NAME,
        input=[
            {
                "role": "system",
                "content": f"""
You are a study planning agent.

Create a study plan based on the goal and the learner's memory.

Hard requirements:
- The `days` array must contain exactly {plan_num_days} items — one study day each, labeled "Day 1" through "Day {plan_num_days}" in order.
- Each day's `duration_minutes` must be at most {max_min_per_day} (use the full allowance when appropriate).
- Spread topics across all days to match the learner's horizon and goal; do not collapse multiple weeks into fewer days.

Use the learner's memory to avoid repeating completed topics.
"""
            },
            {
                "role": "user",
                "content": f"""
Goal:
{goal}

Plan shape: exactly {plan_num_days} consecutive study days (Day 1 … Day {plan_num_days}), up to {max_min_per_day} minutes each day.

Learner memory:
{json.dumps(memory.model_dump(mode="json"), indent=2)}
"""
            }
        ],
        text_format=StudyPlan
    )

    return response.output_parsed