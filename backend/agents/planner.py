from backend.llm.models import get_llm


def planner_agent(state):

    print("\n" + "=" * 60)
    print("PLANNER AGENT")
    print("=" * 60)

    llm = get_llm()

    query = state["user_query"]

    print(f"[INFO] Creating research plan for: {query}")

    prompt = f"""
You are the planning agent of ResearchForge AI.

User research request:

{query}

Break this request into 4-6 clear research tasks.

Focus on:

1. Existing solutions
2. Current technology
3. Research papers
4. Technical implementation
5. Datasets
6. Limitations and future scope

Return only a numbered list.
"""

    response = llm.invoke(prompt)

    tasks = []

    for line in response.content.split("\n"):

        line = line.strip()

        if line:

            line = line.lstrip("0123456789. ")

            if line:

                tasks.append(line)

    print(f"[OK] Research plan created with {len(tasks)} tasks.")

    # Return BOTH research_tasks (list) and research_plan (string) for compatibility
    return {
        "research_tasks": tasks,
        "research_plan": "\n".join(f"{i+1}. {t}" for i, t in enumerate(tasks))
    }