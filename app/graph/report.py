

from app.graph.state import ResearchState
from app.agents.report_writer import generate_research_report


def report_writer_node(state: ResearchState) -> dict:
    print("\n[Report Writer Node] Generating report")

    report = generate_research_report(state)

    print("[Report Writer Node] Report generated")

    return {"final_report": report}
