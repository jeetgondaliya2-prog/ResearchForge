from backend.llm.models import get_llm
from backend.tools.document_search import document_search


def rag_research_agent(state):

    llm = get_llm()

    query = state.get(
        "user_query",
        ""
    )

    # Retrieve documents directly
    search_result = document_search.invoke(
        {
            "query": query
        }
    )

    prompt = f"""
You are the RAG Research Agent of ResearchForge AI.

Research question:

{query}

Retrieved information from the user's documents:

{search_result}

Analyze ONLY the retrieved information.

Focus on:

1. Important findings
2. Technical details
3. Existing approaches
4. Algorithms
5. Datasets
6. Limitations
7. Research gaps
8. Evidence supporting the findings

Rules:

- Do not invent information.
- Do not use outside knowledge.
- If the documents do not contain enough information,
  clearly say so.
- Keep the findings useful for the final research report.
"""

    response = llm.invoke(prompt)

    return {
        "document_results": [
            {
                "content": response.content
            }
        ]
    }