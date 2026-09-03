from backend.llm.models import get_llm


def critic_agent(state):

    llm = get_llm()

    query = state.get("user_query", "")

    analysis = state.get("analysis", "")

    feasibility = state.get("feasibility", "")

    prompt = f"""
You are the Critic Agent of ResearchForge AI.

Research Question:
{query}

========================================
ANALYSIS
========================================

{analysis}

========================================
FEASIBILITY
========================================

{feasibility}

========================================
TASK
========================================

Critically evaluate the research.

Check:

1. Factual consistency
2. Missing evidence
3. Weak reasoning
4. Unsupported assumptions
5. Technical feasibility
6. Dataset assumptions
7. Research gaps
8. Practical project value

Return:

VERDICT: PASS or REVISE

Then provide detailed feedback.
"""

    response = llm.invoke(prompt)

    critique = response.content

    revision_count = state.get("revision_count", 0)

    return {
        "critique": critique,
        "revision_count": revision_count + 1
    }