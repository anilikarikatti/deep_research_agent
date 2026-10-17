
from uuid import uuid4

# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from app.config import settings
from app.schemas.evidence import Finding, Source
from app.schemas.extraction import EvidenceExtractionResult
from app.schemas.research import ResearchTask


extractor_llm = ChatGroq(
    model=settings.groq_model,
    api_key=settings.groq_api_key,
    temperature=0,
)

structured_extractor = extractor_llm.with_structured_output(
    EvidenceExtractionResult
)


EXTRACTION_PROMPT = """
You are an evidence extraction component in a
deep research system.

Extract factual claims relevant to the research tasks
from the supplied source.

Rules:
1. Use only information explicitly supported by the source.
2. Do not use your own knowledge to fill missing details.
3. Each claim must be specific and useful for answering
   a research task.
4. supporting_quote must be copied exactly from the
   supplied source content.
5. Select a task_id from the provided research tasks.
6. Return no findings if the source contains no relevant
   supported claims.
7. Do not invent numbers, dates, quotations, or facts.
8. Confidence represents how clearly the source supports
   the extracted claim, not whether the claim is universally
   true.
"""


def extract_findings(
    source: Source,
    tasks: list[ResearchTask],
) -> list[Finding]:

    task_descriptions = [
        {
            "task_id": task.task_id,
            "question": task.question,
            "objective": task.objective,
        }
        for task in tasks
    ]

    response = structured_extractor.invoke([
        ("system", EXTRACTION_PROMPT),
        (
            "human",
            f"""
Research tasks:
{task_descriptions}

Source ID:
{source.source_id}

Source title:
{source.title}

Source URL:
{source.url}

Source content:
{source.content[:12000]}
""",
        ),
    ])

    valid_task_ids = {task.task_id for task in tasks}
    findings: list[Finding] = []

    for item in response.findings:
        # Reject invented task references.
        if item.task_id not in valid_task_ids:
            continue

        # Reject empty or unsupported quotations.
        if not item.supporting_quote.strip():
            continue

        if item.supporting_quote not in source.content:
            continue

        if not item.claim.strip():
            continue

        findings.append(
            Finding(
                finding_id=str(uuid4()),
                task_id=item.task_id,
                claim=item.claim,
                source_ids=[source.source_id],
                supporting_quote=item.supporting_quote,
                confidence=item.confidence,
            )
        )

    return findings
