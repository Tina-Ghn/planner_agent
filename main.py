from agent.agent import StudyPlannerAgent
from config import DEFAULT_PLAN_DAYS, MAX_MIN_PER_DAY, MAX_ITERATIONS
from memory.store import mark_day_completed


def _prompt_int(message: str, default: int) -> int:
    raw = input(message).strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"Invalid number; using default {default}.")
        return default


def _prompt_plan_days(message: str) -> int | None:
    """Return None to let the agent infer length from the goal; otherwise a positive int."""
    raw = input(message).strip().lower()
    if not raw or raw in ("auto", "agent", "a"):
        return None
    try:
        n = int(raw)
        return n if n >= 1 else None
    except ValueError:
        print("Invalid number; agent will choose plan length.")
        return None


def main():
    agent = StudyPlannerAgent()

    print("Study Planner Agent")
    print("-------------------")
    print("1. Create study plan")
    print("2. Mark day as completed")

    choice = input("Choose an option: ")

    if choice == "1":
        goal = input("Enter your study goal: ")
        minutes = _prompt_int(
            f"Minutes you can study per day (default {MAX_MIN_PER_DAY}): ",
            MAX_MIN_PER_DAY,
        )
        plan_days = _prompt_plan_days(
            "Number of days this plan should cover "
            f"(or blank / 'auto' for the agent to decide from your goal; typical fixed default is {DEFAULT_PLAN_DAYS}): "
        )

        result = agent.run(
            goal=goal,
            max_min_per_day=minutes,
            plan_num_days=plan_days,
            max_iterations=MAX_ITERATIONS,
        )

        if result.get("length_estimate"):
            le = result["length_estimate"]
            print("\n=== Agent-chosen plan length ===")
            print(f"Days: {result['plan_num_days']} (model suggested {le.get('model_suggested_days')})")
            if le.get("rationale"):
                print(f"Why: {le['rationale']}")

        print("\n=== Final Study Plan ===")
        print(result["plan"].model_dump_json(indent=2))
        print("\n=== Validation ===")
        print(result["validation"])

        print("\nIterations:", result["iterations"])

    elif choice == "2":
        day = input("Which day did you complete? Example: Day 1 ")
        note = input("Any note? ")

        memory = mark_day_completed(day=day, note=note)

        print("\nMemory updated:")
        print(memory.model_dump_json(indent=2))

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()