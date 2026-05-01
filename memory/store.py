import json
from pathlib import Path

from config import MEMORY_FILE
from memory.schema import StudyMemory, CompletedDay


def _normalize_memory_dict(raw: object) -> dict:
    """Coerce legacy JSON (e.g. string completed_days, `notes` list) into StudyMemory-compatible dict."""
    data = raw if isinstance(raw, dict) else {}
    merged: dict[str, str] = {}

    cd = data.get("completed_days")
    if isinstance(cd, list):
        for item in cd:
            if isinstance(item, str):
                merged.setdefault(item, "")
            elif isinstance(item, dict) and isinstance(item.get("day"), str):
                d = item["day"]
                nt = item.get("note", "") or ""
                merged[d] = str(nt or merged.get(d, ""))

    legacy_notes = data.get("notes")
    if isinstance(legacy_notes, list):
        for n in legacy_notes:
            if isinstance(n, dict) and isinstance(n.get("day"), str):
                d = n["day"]
                nt = n.get("note", "") or ""
                if nt:
                    merged[d] = str(nt)
                else:
                    merged.setdefault(d, merged.get(d, ""))

    learner_notes = data.get("learner_notes") or []
    out_ln = [str(x) for x in learner_notes] if isinstance(learner_notes, list) else []

    return {
        "completed_days": [{"day": k, "note": v} for k, v in sorted(merged.items())],
        "learner_notes": out_ln,
    }


def load_memory() -> StudyMemory:
    path = Path(MEMORY_FILE)

    if not path.exists():
        return StudyMemory()

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return StudyMemory(**_normalize_memory_dict(data))


def save_memory(memory: StudyMemory) -> None:
    path = Path(MEMORY_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory.model_dump(), f, indent=2, ensure_ascii=False)


def mark_day_completed(day: str, note: str = "") -> StudyMemory:
    memory = load_memory()

    existing_days = [item.day for item in memory.completed_days]

    if day not in existing_days:
        memory.completed_days.append(
            CompletedDay(day=day, note=note)
        )

    save_memory(memory)
    return memory