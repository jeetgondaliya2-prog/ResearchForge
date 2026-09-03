from langchain_core.tools import tool

from backend.rag.retriever import get_retriever


@tool
def document_search(query: str) -> str:
    """
    Search the user's uploaded research documents
    for information relevant to a research question.
    """

    retriever = get_retriever()

    documents = retriever.invoke(query)

    if not documents:
        return "No relevant information found in the uploaded documents."

    results = []

    for i, doc in enumerate(documents, start=1):

        content = doc.page_content

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        results.append(
            f"""
SOURCE {i}

File: {source}
Page: {page}

Content:
{content}
"""
        )

    return "\n".join(results)