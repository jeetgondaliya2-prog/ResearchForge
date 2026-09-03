from backend.llm.models import get_llm
from backend.tools.web_search import web_search


def web_research_agent(state):

    llm = get_llm()

    query = state.get("user_query", "")

    # Search the real internet
    search_results = web_search.invoke(
        {
            "query": query
        }
    )

    prompt = f"""
You are the Web Research Agent of ResearchForge AI.

Your task is to research the following topic using
the provided web search results.

RESEARCH QUESTION:
{query}

========================================
WEB SEARCH RESULTS
========================================

{search_results}

========================================
TASK
========================================

Analyze the search results and extract:

1. Important findings
2. Existing solutions
3. Current technologies
4. Important organizations/projects
5. Datasets
6. Algorithms and approaches
7. Advantages
8. Limitations
9. Research gaps
10. Useful sources

Rules:

- Do not invent information.
- Only use information present in the search results.
- Preserve source URLs whenever possible.
- Clearly distinguish facts from assumptions.
- Prefer recent and technically reliable information.
"""

    response = llm.invoke(prompt)

    return {
        "web_results": [
            {
                "query": query,
                "content": response.content
            }
        ]
    }