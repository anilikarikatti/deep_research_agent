
from app.graph.state import ResearchState
from app.agents.evidence_extractor import extract_findings


def extractor_node(state: ResearchState) -> dict:
    print("\n[Extractor Node] Started")

    plan = state.get("plan")
    # sources = state.get("sources", [])
    sources = state.get("new_sources", state.get("sources", []))
    findings = list(state.get("findings", []))

    if plan is None:
        return {
            "findings": [],
            "errors": ["Cannot extract evidence without a plan."],
        }

    if not sources:
        print("[Extractor Node] No sources available.")

        return {
            "findings": [],
        }

    # findings = [] 
    errors = list(state.get("errors", []))

    for source in sources:
        print(
            f"[Extractor Node] Processing: {source.title}"
        )

        try:
            source_findings = extract_findings(
                source=source,
                tasks=plan.subquestions,
            )

            findings.extend(source_findings)

            print(
                f"[Extractor Node] Findings extracted: "
                f"{len(source_findings)}"
            )

        except Exception as exc:
            message = (
                f"Extraction failed for "
                f"{source.source_id}: {exc}"
            )

            errors.append(message)
            print(f"[Extractor Node] {message}")

    return {
        "findings": findings,
        "errors": errors,
    }
