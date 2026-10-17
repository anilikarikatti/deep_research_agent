
from langgraph.graph import StateGraph, START, END

from app.graph.state import ResearchState
from app.graph.nodes import planner_node
from app.graph.researcher import researcher_node
from app.graph.extractor import extractor_node
from app.graph.verifier import verifier_node

from app.graph.controller import research_controller_node

from app.graph.report import report_writer_node

# def route_after_controller(state: ResearchState) -> str:
#     if state.get("research_complete", False):
#         return "finish"

#     return "research"

def route_after_controller(state: ResearchState) -> str:
    if state.get("research_complete", False):
        return "report_writer"

    return "research"

def build_research_graph():
    builder = StateGraph(ResearchState)

    # Register the node
    builder.add_node("planner", planner_node)
    builder.add_node("researcher" , researcher_node)
    builder.add_node("extractor", extractor_node)
    builder.add_node("verifier", verifier_node)
    builder.add_node("controller", research_controller_node)
    builder.add_node("report_writer", report_writer_node)

    # Define execution order
    builder.add_edge(START, "planner")
    builder.add_edge("planner", "researcher")

    builder.add_edge("researcher", "extractor")
    builder.add_edge("extractor", "verifier")

    builder.add_edge("verifier", "controller")

    # builder.add_conditional_edges(
    #     "controller",
    #     route_after_controller,
    #     {
    #         "research": "researcher",
    #         "finish": END,
    #     },
    # )
    
    builder.add_conditional_edges(
    "controller",
    route_after_controller,
    {
        "research": "researcher",
        "report_writer": "report_writer",
    },
    )

    builder.add_edge("report_writer", END)
    # builder.add_edge("researcher", END)


    # Compile into an executable graph
    return builder.compile()


research_graph = build_research_graph()


