
from app.graph.state import ResearchState


def research_controller_node(state: ResearchState) -> dict:
    print("\n[Controller Node] Evaluating research progress")

    verifications = state.get("verifications", [])
    current_round = state.get("research_round", 0)
    max_rounds = state.get("max_research_rounds", 3)

    missing_evidence = []

    for verification in verifications:
        if not verification.additional_search_needed:
            continue

        # Prefer focused queries suggested by the verifier.
        if verification.follow_up_queries:
            missing_evidence.extend(
                verification.follow_up_queries
            )
        else:
            # Fallback if the verifier did not suggest a query.
            missing_evidence.append(
                verification.explanation
            )

    # Remove duplicate queries while preserving order.
    missing_evidence = list(dict.fromkeys(missing_evidence))

    should_continue = (
        bool(missing_evidence)
        and current_round < max_rounds
    )

    if should_continue:
        print("[Controller Node] More research is needed")
        print(f"[Controller Node] Next queries: {missing_evidence}")

        return {
            "missing_evidence": missing_evidence,
            "research_round": current_round + 1,
            "research_complete": False,
        }

    if missing_evidence:
        print("[Controller Node] Research budget reached")
    else:
        print("[Controller Node] No further searches requested")

    return {
        "missing_evidence": missing_evidence,
        "research_complete": True,
    }
