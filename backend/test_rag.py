# -*- coding: utf-8 -*-
import sys
import os

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from backend.rag.ingestion import ingest_pdf
from backend.rag.retriever import get_retriever


if __name__ == "__main__":
    PDF_PATH = "data/documents/sample.pdf"


    result = ingest_pdf(PDF_PATH)

    print("Ingestion result:")
    print(result)


    retriever = get_retriever()

    docs = retriever.invoke(
        "What is the main topic of this document?"
    )

    print("\nRetrieved documents:")

    for doc in docs:

        print(doc.page_content[:500])
        print("-" * 50)