from backend.llm.models import get_llm
from backend.tools.academic_search import academic_search


def academic_research_agent(state):

    llm = get_llm()

    query = state.get(
        "user_query",
        ""
    )

    # ==========================================
    # SEARCH ACADEMIC PAPERS
    # ==========================================

    papers = academic_search.invoke(
        {
            "query": query
        }
    )

    # ==========================================
    # ANALYZE PAPERS
    # ==========================================

    prompt = f"""
You are the Academic Research Agent
of ResearchForge AI.

Your job is to analyze academic papers
related to the research question.

RESEARCH QUESTION:

{query}


========================================
ACADEMIC PAPERS
========================================

{papers}


========================================
TASK
========================================

Analyze the retrieved academic papers.

Extract:

1. Important research findings

2. Existing approaches

3. Algorithms and models

4. Datasets used

5. Experimental results

6. Advantages

7. Limitations

8. Common methodologies

9. Research gaps

10. Possible improvements

11. Important papers

12. Emerging research directions


========================================
RULES
========================================

- Do NOT invent papers.

- Do NOT invent authors.

- Do NOT invent experimental results.

- Only use information contained
  in the retrieved papers.

- Clearly identify information that
  is missing from the abstracts.

- Preserve paper titles and URLs.

- Prefer recent research when relevant.

Provide a structured academic
literature analysis.
"""

    response = llm.invoke(prompt)

    return {
        "academic_results": [
            {
                "query": query,
                "papers": papers,
                "analysis": response.content
            }
        ],

        "sources": [
            {
                "source_type": "academic",
                "query": query,
                "content": papers
            }
        ]
    }