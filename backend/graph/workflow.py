from langgraph.graph import StateGraph, START, END

from backend.graph.state import ResearchState

from backend.graph.nodes import (
    supervisor_node,
    planner_node,
    web_research_node,
    academic_research_node,
    rag_research_node,
    research_merge_node,
    analyst_node,
    feasibility_node,
    critic_node,
    final_writer_node
)


def critic_decision(state):

    critique = state.get(
        "critique",
        ""
    )

    revision_count = state.get(
        "revision_count",
        0
    )

    print("\n" + "=" * 60)
    print("CRITIC DECISION")
    print("=" * 60)

    print(
        f"[INFO] Revision count: {revision_count}"
    )

    # Prevent infinite loops
    if revision_count >= 2:

        print(
            "[INFO] Maximum revisions reached."
        )

        print(
            "[INFO] Moving to final writer."
        )

        return "final_writer"

    # Check critic verdict
    if "VERDICT: REVISE" in critique.upper():

        print(
            "[INFO] Critic requested revision."
        )

        print(
            "[INFO] Sending research back to Analyst."
        )

        return "analyst"

    print(
        "[INFO] Critic approved the research."
    )

    print(
        "[INFO] Moving to final writer."
    )

    return "final_writer"


def build_graph():

    graph = StateGraph(ResearchState)

    # ==========================================
    # NODES
    # ==========================================

    graph.add_node(
        "supervisor",
        supervisor_node
    )

    graph.add_node(
        "planner",
        planner_node
    )

    graph.add_node(
        "web_research",
        web_research_node
    )

    graph.add_node(
        "academic_research",
        academic_research_node
    )

    graph.add_node(
        "rag_research",
        rag_research_node
    )

    graph.add_node(
        "research_merge",
        research_merge_node
    )

    graph.add_node(
        "analyst",
        analyst_node
    )

    graph.add_node(
        "feasibility",
        feasibility_node
    )

    graph.add_node(
        "critic",
        critic_node
    )

    graph.add_node(
        "final_writer",
        final_writer_node
    )

    # ==========================================
    # START
    # ==========================================

    graph.add_edge(
        START,
        "supervisor"
    )

    # ==========================================
    # SUPERVISOR → PLANNER
    # ==========================================

    graph.add_edge(
        "supervisor",
        "planner"
    )

    # ==========================================
    # PLANNER → RESEARCH
    # ==========================================

    graph.add_edge(
        "planner",
        "web_research"
    )

    graph.add_edge(
        "planner",
        "academic_research"
    )

    graph.add_edge(
        "planner",
        "rag_research"
    )

    # ==========================================
    # RESEARCH → MERGE
    # ==========================================

    graph.add_edge(
        "web_research",
        "research_merge"
    )

    graph.add_edge(
        "academic_research",
        "research_merge"
    )

    graph.add_edge(
        "rag_research",
        "research_merge"
    )

    # ==========================================
    # MERGE → ANALYST
    # ==========================================

    graph.add_edge(
        "research_merge",
        "analyst"
    )

    # ==========================================
    # ANALYST → FEASIBILITY
    # ==========================================

    graph.add_edge(
        "analyst",
        "feasibility"
    )

    # ==========================================
    # FEASIBILITY → CRITIC
    # ==========================================

    graph.add_edge(
        "feasibility",
        "critic"
    )

    # ==========================================
    # CRITIC → DECISION
    # ==========================================

    graph.add_conditional_edges(
        "critic",
        critic_decision,
        {
            "analyst": "analyst",
            "final_writer": "final_writer"
        }
    )

    # ==========================================
    # FINAL WRITER → END
    # ==========================================

    graph.add_edge(
        "final_writer",
        END
    )

    return graph.compile()