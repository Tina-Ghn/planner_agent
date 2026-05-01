from models.schema import DayPlan


def validate_study_time(
    days: list[DayPlan],
    max_min_per_day: int,
    plan_num_days: int | None = None,
) -> dict:
    problems = []
    if plan_num_days is not None and len(days) != plan_num_days:
        problems.append(
            f"Plan must contain exactly {plan_num_days} days; got {len(days)}."
        )
    for day in days:
        if day.duration_minutes > max_min_per_day:
            problems.append(
                f"{day.day}: {day.duration_minutes} minutes exceeds limit of {max_min_per_day}"
            )
    return {"is_valid": len(problems) == 0, "problems": problems}
