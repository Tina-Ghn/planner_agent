from agent.validator import validate_study_time
from agent.reviser import revise_study_plan
from memory.store import load_memory
from agent.planner import (
    clamp_plan_num_days,
    create_study_plan_with_memory,
    suggest_plan_num_days,
)


class StudyPlannerAgent:
    def run(
        self,
        goal: str,
        max_min_per_day: int,
        plan_num_days: int | None = None,
        max_iterations: int = 3,
    ):
        memory = load_memory()

        length_meta = None
        if plan_num_days is None:
            est = suggest_plan_num_days(goal, max_min_per_day, memory)
            plan_num_days = clamp_plan_num_days(est.num_days)
            length_meta = {
                "model_suggested_days": est.num_days,
                "after_clamp": plan_num_days,
                "rationale": est.rationale,
            }
        else:
            plan_num_days = clamp_plan_num_days(plan_num_days)

        plan = create_study_plan_with_memory(
            goal=goal,
            max_min_per_day=max_min_per_day,
            memory=memory,
            plan_num_days=plan_num_days,
        )

        for i in range(max_iterations):
            validation = validate_study_time(
                plan.days,
                max_min_per_day,
                plan_num_days,
            )

            if validation["is_valid"]:
                out = {
                    "plan": plan,
                    "validation": validation,
                    "iterations": i + 1,
                    "plan_num_days": plan_num_days,
                }
                if length_meta is not None:
                    out["length_estimate"] = length_meta
                return out

            plan = revise_study_plan(
                goal=goal,
                old_plan=plan,
                problems=validation["problems"],
                max_min_per_day=max_min_per_day,
                plan_num_days=plan_num_days,
            )

        out = {
            "plan": plan,
            "validation": validate_study_time(
                plan.days,
                max_min_per_day,
                plan_num_days,
            ),
            "iterations": max_iterations,
            "plan_num_days": plan_num_days,
        }
        if length_meta is not None:
            out["length_estimate"] = length_meta
        return out




def study_planner_agent(
    goal: str,
    max_min_per_day: int,
    max_iterations: int = 3,
    plan_num_days: int | None = None,
):
    """If ``plan_num_days`` is None, the agent picks a length from the goal (see ``StudyPlannerAgent.run``)."""
    return StudyPlannerAgent().run(
        goal=goal,
        max_min_per_day=max_min_per_day,
        plan_num_days=plan_num_days,
        max_iterations=max_iterations,
    )