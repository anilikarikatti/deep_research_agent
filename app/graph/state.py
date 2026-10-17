

from typing import TypedDict

from app.schemas.research import ResearchPlan

from app.schemas.evidence import (
    Source,
    Finding,
    ClaimVerification,
)


class ResearchState(TypedDict, total=False):
    # User input
    research_id: str
    user_question: str

    # Planning
    plan: ResearchPlan

    # Research evidence
    sources: list[Source]
    # add the new_sources field to your existing ResearchState:
    new_sources: list[Source] 
    findings: list[Finding]
    verifications: list[ClaimVerification]

    # Adaptive control
    research_round: int
    max_research_rounds: int
    missing_evidence: list[str]
    research_complete: bool

    # Final output and errors
    final_report: str
    errors: list[str]
