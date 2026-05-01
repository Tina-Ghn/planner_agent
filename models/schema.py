from pydantic import BaseModel, Field


class PlanLengthEstimate(BaseModel):
    """Structured output for how many study days the learner likely needs."""

    num_days: int = Field(description="Number of consecutive study days to plan")
    rationale: str = Field(
        default="",
        description="One or two sentences: why this length fits the goal and daily minutes",
    )


class DayPlan (BaseModel):
    day: str = Field(description="Example: Day 1")
    topic: str
    duration_minutes: int
    task: str

class StudyPlan(BaseModel):
    goal: str
    days: list[DayPlan] = Field(
        description="One entry per study day; length must match the requested number of days."
    )