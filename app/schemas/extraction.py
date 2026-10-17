

from pydantic import BaseModel, Field


class ExtractedClaim(BaseModel):
    task_id: str
    claim: str
    supporting_quote: str
    confidence: float = Field(ge=0, le=1)


class EvidenceExtractionResult(BaseModel):
    findings: list[ExtractedClaim] = Field(
        default_factory=list
    )
