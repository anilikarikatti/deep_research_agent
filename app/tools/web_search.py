from tavily import TavilyClient

from app.config import settings


tavily_client = TavilyClient(
    api_key=settings.tavily_api_key
)


def search_web(
    query: str,
    max_results: int = 3,
) -> list[dict]:
    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    response = tavily_client.search(
        query=query,
        max_results=max_results,
        search_depth="basic",
    )

    return response.get("results", [])