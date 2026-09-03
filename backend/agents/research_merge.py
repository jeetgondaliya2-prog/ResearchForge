def research_merge_agent(state):

    print("\n" + "=" * 60)
    print("RESEARCH MERGE AGENT")
    print("=" * 60)

    web_results = state.get("web_results", [])
    academic_results = state.get("academic_results", [])
    document_results = state.get("document_results", [])

    print("[INFO] Merging research sources...")

    merged_research = {
        "web": web_results,
        "academic": academic_results,
        "documents": document_results
    }

    print("[OK] Research sources merged.")

    return {
        "merged_research": merged_research
    }