from pydantic import BaseModel, Field
from typing import List


class CompletedDay(BaseModel):
    day: str
    note: str = ""


class StudyMemory(BaseModel):
    completed_days: List[CompletedDay] = Field(default_factory=list)
    learner_notes: List[str] = Field(default_factory=list)