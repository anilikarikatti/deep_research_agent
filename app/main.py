
# from app.agents.planner import create_research_plan


# def main():
#     question = input("Enter your research question: ")

#     plan = create_research_plan(question)

#     print("\n=== RESEARCH PLAN ===")
#     print(plan.model_dump_json(indent=2))


# if __name__ == "__main__":
#     main()



from uuid import uuid4

from app.graph.workflow import research_graph


def main():
    question = input("Enter your research question: ").strip()

    if not question:
        print("Research question cannot be empty.")
        return

    initial_state = {
        "research_id": str(uuid4()),
        "user_question": question,
        "research_round": 0,
        "max_research_rounds": 3,
        "sources": [],
        "findings": [],
        "verifications": [],
        "missing_evidence": [],
        "research_complete": False,
        "errors": [],
    }

    result = research_graph.invoke(initial_state)

    print("\n=== RESEARCH PLAN ===")
    print(result["plan"].model_dump_json(indent=2))

    print("\n=== RETRIEVED SOURCES ===")

    for source in result.get("sources", []):
        print(f"\nID: {source.source_id}")
        print(f"Title: {source.title}")
        print(f"URL: {source.url}")
        print(f"Content preview: {source.content[:500]}")



    print("\n=== EVIDENCE FINDINGS ===")

    for finding in result.get("findings", []):
        print(f"\nFinding ID: {finding.finding_id}")
        print(f"Task ID: {finding.task_id}")
        print(f"Claim: {finding.claim}")
        print(f"Source IDs: {finding.source_ids}")
        print(f"Supporting quote: {finding.supporting_quote}")
        print(f"Confidence: {finding.confidence}")



    print("\n=== CLAIM VERIFICATIONS ===")

    for verification in result.get("verifications", []):
        print(f"\nFinding ID: {verification.finding_id}")
        print(f"Verdict: {verification.verdict}")
        print(f"Explanation: {verification.explanation}")
        print(
            "More research needed:",
            verification.additional_search_needed,
        )
        print(
            "Follow-up queries:",
            verification.follow_up_queries,
        )

    print("\n=== ERRORS ===")

    for error in result.get("errors", []):
        print(f"- {error}")



    # print(result)

    print("\n" + "=" * 70)
    print("FINAL RESEARCH REPORT")
    print("=" * 70)

    print(result.get("final_report", "No report was generated."))


if __name__ == "__main__":
    main()

# compare js vs python which one good for builtind agentic ai application 