# -*- coding: utf-8 -*-
import sys
import os

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from backend.rag.retriever import get_retriever


if __name__ == "__main__":
    retriever = get_retriever()

    query = """
    AI crop disease detection
    """

    documents = retriever.invoke(query)

    print("\n")
    print("=" * 60)
    print("RETRIEVED DOCUMENTS")
    print("=" * 60)

    print("Number of documents:", len(documents))

    for i, doc in enumerate(documents, start=1):

        print("\n")
        print("-" * 60)
        print(f"DOCUMENT {i}")
        print("-" * 60)

        print("Source:")
        print(doc.metadata.get("source"))

        print("\nContent:")
        print(doc.page_content[:1000])
    