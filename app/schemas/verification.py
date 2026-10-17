
from typing import Literal

from pydantic import BaseModel, Field

class ClaimVerification(BaseModel):
    finding_id: str
    verdict: Literal[
        "supported",
        "partially_supported",
        "contradicted",
        "insufficient_evidence",
    ]
    explanation: str
    additional_search_needed: bool = False
    follow_up_queries: list[str] = Field(
        default_factory=list,
        max_length=3,
    )