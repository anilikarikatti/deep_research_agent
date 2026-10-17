
from app.graph.state import ResearchState
from app.agents.claim_verifier import verify_finding


def verifier_node(state: ResearchState) -> dict:
    print("\n[Verifier Node] Started")

    findings = state.get("findings", [])
    sources = state.get("sources", [])
    errors = list(state.get("errors", []))

    verifications = []

    for finding in findings:
        print(
            f"[Verifier Node] Checking: {finding.claim}"
        )

        try:
            result = verify_finding(
                finding=finding,
                sources=sources,
            )

            verifications.append(result)

            print(
                f"[Verifier Node] Verdict: {result.verdict}"
            )

        except Exception as exc:
            message = (
                f"Verification failed for "
                f"{finding.finding_id}: {exc}"
            )

            errors.append(message)
            print(f"[Verifier Node] {message}")

    return {
        "verifications": verifications,
        "errors": errors,
    }
