
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from app.config import settings
from app.schemas.research import ResearchPlan


planner_llm = ChatGroq(
    model=settings.groq_model,
    api_key=settings.groq_api_key,
    temperature=0,
)

structured_planner = planner_llm.with_structured_output(
    ResearchPlan
)


PLANNER_PROMPT = """
You are the planning component of a deep research system.

Convert the user's research question into a structured,
evidence-oriented research plan.

Requirements:
1. Preserve the user's actual research goal.
2. Break the question into independent, useful subquestions.
3. Cover the major dimensions required to answer the question.
4. Specify the evidence needed for each task.
5. Include suitable report sections.
6. Define measurable success criteria.
7. Do not answer the research question yourself.
8. Do not invent research findings or pretend you have
   already searched the web.
9. Use between 3 and 8 subquestions for a substantial
   research request, when appropriate.
"""


def create_research_plan(question: str) -> ResearchPlan:
    if not question.strip():
        raise ValueError("Research question cannot be empty.")

    messages = [
        ("system", PLANNER_PROMPT),
        ("human", question),
    ]

    return structured_planner.invoke(messages)
