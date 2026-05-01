from openai import OpenAI
from config import OPENAI_API_KEY
from config import MODEL_NAME
from models.schema import StudyPlan

client = OpenAI(api_key=OPENAI_API_KEY) 


def revise_study_plan(
    goal: str,
    old_plan: StudyPlan,
    problems: list[str],
    max_min_per_day: int,
    plan_num_days: int,
) -> StudyPlan:

    response = client.responses.parse(
        model=MODEL_NAME,
        input=[
            {
                "role": "system",
                "content": f"""
You revise study plans.

Fix all validation problems.
- The `days` array must contain exactly {plan_num_days} items, labeled "Day 1" … "Day {plan_num_days}" in order.
- No day may exceed {max_min_per_day} minutes.
Keep the plan realistic and practical.
Return structured data only.
"""
            },
            {
                "role": "user",
                "content": f"""
Goal:
{goal}

Old plan:
{old_plan.model_dump_json(indent=2)}

Validation problems:
{problems}
"""
            }
        ],
        text_format=StudyPlan
    )

    return response.output_parsed