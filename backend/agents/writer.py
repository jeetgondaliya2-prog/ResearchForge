from backend.llm.models import get_llm


def writer_agent(state):

    print("\n" + "=" * 60)
    print("FINAL WRITER AGENT")
    print("=" * 60)

    query = state.get(
        "user_query",
        ""
    )

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

    prompt = f"""
You are the Final Writer Agent of ResearchForge AI.

Your job is to create a professional research and
project proposal using the research collected by
multiple agents.

==================================================
RESEARCH QUESTION
==================================================

{query}


==================================================
WEB RESEARCH
==================================================

{web_results}


==================================================
ACADEMIC RESEARCH
==================================================

{academic_results}


==================================================
DOCUMENT / RAG RESEARCH
==================================================

{document_results}


==================================================
ANALYSIS
==================================================

{analysis}


==================================================
FEASIBILITY ANALYSIS
==================================================

{feasibility}


==================================================
CRITIC FEEDBACK
==================================================

{critique}


==================================================
TASK
==================================================

Create a professional research report.

The report must contain:

1. Executive Summary

2. Problem Statement

3. Motivation

4. Existing Solutions

5. Research Findings

6. Proposed Solution

7. System Architecture

8. Technical Approach

9. Technologies and Tools

10. Dataset Requirements

11. AI / ML Approach

12. Implementation Plan

13. Feasibility Analysis

14. Expected Results

15. Major Challenges

16. Research Gaps

17. Future Improvements

18. Conclusion

19. Recommended Project Roadmap


==================================================
IMPORTANT RULES
==================================================

- Do not invent research results.
- Do not invent datasets.
- Do not invent papers.
- Do not invent statistics.
- Clearly distinguish facts from assumptions.
- Use the critic feedback to improve the report.
- Make the project technically practical.
- Give specific technology recommendations.
- Use Markdown headings.
- Keep the report structured and easy to read.
"""

    print("[INFO] Generating final research report...")

    llm = get_llm()

    response = llm.invoke(prompt)

    print("[OK] Final research report generated.")

    return {
        "final_report": response.content
    }