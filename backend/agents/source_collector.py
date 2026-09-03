def source_collector_agent(state):

    print("\n" + "=" * 60)
    print("SOURCE COLLECTOR")
    print("=" * 60)

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

    sources = []

    # ========================================================
    # WEB SOURCES
    # ========================================================

    for result in web_results:

        if isinstance(result, dict):

            url = result.get("url")

            title = result.get(
                "title",
                "Web Source"
            )

            if url:

                sources.append({
                    "type": "web",
                    "title": title,
                    "url": url
                })

    # ========================================================
    # ACADEMIC SOURCES
    # ========================================================

    for result in academic_results:

        if isinstance(result, dict):

            url = result.get("url")

            title = result.get(
                "title",
                "Academic Source"
            )

            if url:

                sources.append({
                    "type": "academic",
                    "title": title,
                    "url": url
                })

    # ========================================================
    # DOCUMENT SOURCES
    # ========================================================

    for result in document_results:

        if isinstance(result, dict):

            source = result.get(
                "source"
            )

            if source:

                sources.append({
                    "type": "document",
                    "title": source,
                    "url": None
                })

    print(
        f"[OK] Collected {len(sources)} sources."
    )

    return {
        "sources": sources
    }