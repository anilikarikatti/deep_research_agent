from datetime import datetime, timezone
from hashlib import sha256

from app.graph.state import ResearchState
from app.schemas.evidence import Source
from app.tools.web_search import search_web
from app.tools.page_retriever import retrieve_page


def researcher_node(state: ResearchState) -> dict:
    print("\n[Researcher Node] Started")

    plan = state["plan"]
    sources_by_url: dict[str, Source] = {}
    errors = list(state.get("errors", []))

    # Bound the first version to three research tasks.
    # tasks = plan.subquestions[:3]

    # for task in tasks:
    #     print(f"[Researcher Node] Searching: {task.question}")

    #     try:
    #         results = search_web(
    #             query=task.question,
    #             max_results=3,
    #         )
    #     except Exception as exc:
    #         errors.append(
    #             f"Search failed for task {task.task_id}: {exc}"
    #         )
    #         continue

    #     for result in results:
    #         url = result.get("url")

    #         if not url or url in sources_by_url:
    #             continue

    #         try:
    #             page = retrieve_page(url)

    #             source_id = sha256(
    #                 page["url"].encode("utf-8")
    #             ).hexdigest()[:12]

    #             sources_by_url[url] = Source(
    #                 source_id=source_id,
    #                 url=page["url"],
    #                 title=page["title"],
    #                 retrieved_at=datetime.now(
    #                     timezone.utc
    #                 ).isoformat(),
    #                 published_at=result.get("published_date"),
    #                 content=page["content"],
    #             )

    #             print(
    #                 f"[Researcher Node] Retrieved: "
    #                 f"{page['title']}"
    #             )

    #         except Exception as exc:
    #             errors.append(
    #                 f"Could not retrieve {url}: {exc}"
    #             )

    # print(
    #     f"[Researcher Node] Collected "
    #     f"{len(sources_by_url)} sources"
    # )

    # return {
    #     "sources": list(sources_by_url.values()),
    #     "errors": errors,
    # }


    # Later second version


    tasks = plan.subquestions

    # First round: search theiginal research tasks. or
    # Later rounds: search the controller's follow-up queries.
    follow_up_queries = state.get("missing_evidence", [])

    if follow_up_queries:
        queries = follow_up_queries[:3]
    else:
        queries = [
            task.question
            for task in tasks[:3]
        ]

    # Preserve sources from earlier rounds and avoid duplicates.
    existing_sources = state.get("sources", [])

    sources_by_url = {
        source.url: source
        for source in existing_sources
    }

    new_sources = []
    errors = list(state.get("errors", []))

    for query in queries:
        print(f"[Researcher Node] Searching: {query}")

        try:
            results = search_web(
                query=query,
                max_results=3,
            )
            print(
                f"[Researcher Node] Search results: {len(results)}"
            )
        except Exception as exc:
            errors.append(f"Search failed for '{query}': {exc}")
            print(f"[Researcher Node] Search error: {exc}")
            continue

        for result in results:
            url = result.get("url")

            if not url or url in sources_by_url:
                continue

            try:
                page = retrieve_page(url)

                source_id = sha256(
                    page["url"].encode("utf-8")
                ).hexdigest()[:12]

                source = Source(
                    source_id=source_id,
                    url=page["url"],
                    title=page["title"],
                    retrieved_at=datetime.now(
                        timezone.utc
                    ).isoformat(),
                    published_at=result.get("published_date"),
                    content=page["content"],
                )

                sources_by_url[url] = source
                new_sources.append(source)

                print(
                    f"[Researcher Node] Retrieved: {page['title']}"
                )

            except Exception as exc:
                errors.append(f"Could not retrieve {url}: {exc}")
                print(f"[Researcher Node] Retrieval error: {exc}")

    print(
        f"[Researcher Node] New sources: {len(new_sources)}"
    )

    return {
        "sources": list(sources_by_url.values()),
        "new_sources": new_sources,
        "errors": errors,
    }
