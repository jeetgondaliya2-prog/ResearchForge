import arxiv

from langchain_core.tools import tool


@tool
def academic_search(query: str) -> str:
    """
    Search arXiv for relevant academic research papers.
    No API key is required.
    """

    try:
        client = arxiv.Client(
            page_size=5,
            delay_seconds=3,
            num_retries=2
        )

        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []

        for i, paper in enumerate(
            client.results(search),
            start=1
        ):

            authors = [
                author.name
                for author in paper.authors
            ]

            results.append({
                "paper_number": i,
                "title": paper.title,
                "authors": authors,
                "published": str(paper.published),
                "updated": str(paper.updated),
                "abstract": paper.summary,
                "url": paper.entry_id,
                "pdf_url": paper.pdf_url,
                "categories": paper.categories
            })

        if not results:
            return (
                "No academic papers found "
                f"for query: {query}"
            )

        return str(results)

    except Exception as e:
        return f"Academic search failed: {str(e)}"