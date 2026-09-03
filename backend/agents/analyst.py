from backend.llm.models import get_llm
import time


def analyst_agent(state):

    llm = get_llm()

    query = state.get(
        "user_query",
        ""
    )

    web_results = state.get(
        "web_results",
        []
    )

    academic_results = state.get(
        "academic_results",
        []
    )

    document_results = state.get(
        "document_results",
        []
    )

    print("\n" + "=" * 60)
    print("ANALYST AGENT")
    print("=" * 60)

    print("[INFO] Preparing research analysis...")
    print(f"[INFO] Query: {query}")

    prompt = f"""
You are the Analyst Agent of ResearchForge AI.

Research Question:
{query}

========================================
WEB RESEARCH
========================================

{web_results}


========================================
ACADEMIC RESEARCH
========================================

{academic_results}


========================================
DOCUMENT / RAG RESEARCH
========================================

{document_results}


========================================
YOUR TASK
========================================

Combine all available research.

Produce a structured analysis containing:

1. Problem understanding
2. Existing solutions
3. Research findings
4. Technical approaches
5. Dataset availability
6. Technology comparison
7. Recommended approach
8. Major challenges
9. Research gaps
10. Project opportunities

IMPORTANT:

- Do not invent information.
- Separate evidence from assumptions.
- Identify conflicting information.
- Give priority to reliable research.
- Make the result useful for building a real project.
- If some research source is empty, continue using the available sources.
"""

    print("[LLM] Analyst calling Mistral...")

    try:

        response = llm.invoke(prompt)

        print("[OK] Analyst completed successfully.")

        return {
            "analysis": response.content
        }

    except Exception as e:

        error_message = str(e)

        if "429" in error_message:

            print("[ERROR] Mistral rate limit reached.")
            print("[INFO] Analyst could not complete this request.")

            return {
                "analysis": (
                    "Analyst temporarily unavailable because "
                    "the LLM API rate limit was reached."
                )
            }

        raise