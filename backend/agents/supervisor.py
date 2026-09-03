from backend.llm.models import get_llm


def supervisor_agent(state):

    print("\n" + "=" * 60)
    print("SUPERVISOR AGENT")
    print("=" * 60)

    llm = get_llm()

    query = state["user_query"]

    print(f"[INFO] Supervisor coordinating research for: {query}")

    prompt = f"""
You are the Supervisor Agent of ResearchForge AI.

Your job is to decide how a research request should be handled.

User request:
{query}

Decide whether this request requires:

1. Web research
2. Academic research
3. Document/RAG research
4. Technical analysis
5. Project feasibility analysis

Return a short plan describing which types of research are required.
"""

    response = llm.invoke(prompt)

    print("[OK] Supervisor plan created.")

    return {
        "supervisor_plan": response.content
    }