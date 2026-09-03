from backend.llm.models import get_llm


def feasibility_agent(state):

    print("\n" + "=" * 60)
    print("FEASIBILITY AGENT")
    print("=" * 60)

    llm = get_llm()

    analysis = state.get("analysis", "")
    query = state.get("user_query", "")

    print(f"[INFO] Evaluating feasibility for: {query}")

    prompt = f"""
You are the Feasibility Agent of ResearchForge AI.

Project idea:
{query}

Research analysis:
{analysis}

Evaluate whether this project is realistically buildable.

Evaluate the following:

1. Technical feasibility
2. Dataset availability
3. Required hardware
4. Required software
5. Model complexity
6. Development difficulty
7. Development stages
8. Major risks
9. Cost considerations
10. Expected performance
11. Scalability
12. Future improvements

Give each major category a score from 1 to 10.

Finally provide:

OVERALL FEASIBILITY: HIGH / MEDIUM / LOW

Explain your reasoning clearly.
"""

    print("[LLM] Feasibility Agent calling Mistral...")

    try:
        response = llm.invoke(prompt)

        print("[OK] Feasibility evaluation completed.")

        # Return as string (not dict) to match ResearchState.feasibility: str
        return {
            "feasibility": response.content
        }

    except Exception as e:
        error_message = str(e)

        if "429" in error_message:
            print("[ERROR] Mistral rate limit reached in Feasibility Agent.")
            return {
                "feasibility": (
                    "Feasibility Agent temporarily unavailable because "
                    "the LLM API rate limit was reached. "
                    "\n\nOVERALL FEASIBILITY: MEDIUM"
                )
            }

        raise