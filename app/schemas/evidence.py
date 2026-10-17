

from typing import Literal

from pydantic import BaseModel, Field


class Source(BaseModel):
    source_id: str
    url: str
    title: str
    retrieved_at: str
    published_at: str | None = None
    content: str


class Finding(BaseModel):
    finding_id: str
    task_id: str
    claim: str
    source_ids: list[str] = Field(min_length=1)
    supporting_quote: str
    confidence: float = Field(ge=0, le=1)


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
