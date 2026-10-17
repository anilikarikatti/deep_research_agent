

from typing import Literal

from pydantic import BaseModel, Field


class ResearchTask(BaseModel):
    task_id: str
    question: str
    objective: str

    required_evidence: list[str] = Field(
        default_factory=list
    )

    status: Literal[
        "pending",
        "in_progress",
        "completed",
        "needs_more_research",
    ] = "pending"


class ResearchPlan(BaseModel):
    original_question: str

    subquestions: list[ResearchTask] = Field(
        min_length=1,
        max_length=10,
    )

    report_sections: list[str]
    success_criteria: list[str]
