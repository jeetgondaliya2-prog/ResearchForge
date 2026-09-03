from typing import TypedDict, List, Dict, Any, Optional


class ResearchState(TypedDict, total=False):

    # ==========================================
    # USER INPUT
    # ==========================================

    user_query: str

    # ==========================================
    # SUPERVISOR
    # ==========================================

    supervisor_plan: str

    # ==========================================
    # PLANNING
    # ==========================================

    research_plan: str          # joined string version of the plan
    research_tasks: List[str]   # list version (from planner_agent)

    # ==========================================
    # RESEARCH RESULTS
    # ==========================================

    web_results: List[Any]

    academic_results: List[Any]

    document_results: List[Any]

    merged_research: Dict[str, Any]

    # ==========================================
    # SOURCES (for citation display)
    # ==========================================

    sources: List[Dict[str, Any]]

    # ==========================================
    # ANALYSIS
    # ==========================================

    analysis: str

    # ==========================================
    # FEASIBILITY
    # ==========================================

    feasibility: str            # must be a plain string

    # ==========================================
    # CRITIC
    # ==========================================

    critique: str

    revision_count: int

    # ==========================================
    # FINAL RESULT
    # ==========================================

    final_report: str