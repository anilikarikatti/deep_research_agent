

from app.graph.state import ResearchState
from app.agents.planner import create_research_plan


def planner_node(state: ResearchState) -> dict:
    """
    Read the research question, generate a plan,
    and return the state update.
    """
    question = state["user_question"]

    # print("Planner node prints this question " , question)

    plan = create_research_plan(question)

    return {
        "plan": plan,
    }
