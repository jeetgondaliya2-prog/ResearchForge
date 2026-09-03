from backend.llm.models import get_llm


def final_writer_agent(state):

    print("\n" + "=" * 60)
    print("FINAL WRITER AGENT")
    print("=" * 60)

    llm = get_llm()

    query = state.get("user_query", "")

    analysis = state.get(
        "analysis",
        ""
    )

    feasibility = state.get(
        "feasibility",
        ""
    )

    critique = state.get(
        "critique",
        ""
    )

    prompt = f"""
You are the Final Writer Agent of ResearchForge AI.

Your job is to create a professional research and project proposal.

==================================================
RESEARCH QUESTION
==================================================

{query}

==================================================
ANALYSIS
==================================================

{analysis}

==================================================
FEASIBILITY ANALYSIS
==================================================

{feasibility}

==================================================
CRITIC REVIEW
==================================================

{critique}

==================================================
FINAL REPORT
==================================================

Create a clear and professional report.

Use the following structure:

# ResearchForge AI Research Report

## 1. Executive Summary

Explain the research problem and the most important findings.

## 2. Problem Definition

Clearly define the problem.

## 3. Existing Solutions

Discuss existing approaches and technologies.

## 4. Research Findings

Summarize important findings from the available sources.

## 5. Technical Approaches

Explain possible technical approaches.

## 6. Dataset Analysis

Discuss available datasets and their usefulness.

## 7. Technology Comparison

Compare relevant technologies.

## 8. Recommended Architecture

Explain the recommended system architecture.

## 9. Implementation Plan

Give a practical implementation roadmap.

## 10. Feasibility

Discuss:

- Technical feasibility
- Dataset feasibility
- Cost
- Complexity
- Deployment feasibility

## 11. Challenges

List major technical and research challenges.

## 12. Research Gaps

Identify areas where existing solutions are insufficient.

## 13. Project Opportunities

Suggest practical project ideas.

## 14. Future Improvements

Explain possible future extensions.

## 15. Final Recommendation

Give a concise final recommendation.

IMPORTANT:

- Do not invent research findings.
- Clearly distinguish evidence from assumptions.
- Prefer information present in the provided research.
- Make the report useful for actually building a project.
"""

    print("[LLM] Generating final research report...")

    response = llm.invoke(prompt)

    print("[OK] Final report generated.")

    return {
        "final_report": response.content
    }