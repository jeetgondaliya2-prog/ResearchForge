from backend.rag.loaders import load_pdf
from backend.rag.splitter import split_documents
from backend.rag.vectorstore import get_vectorstore


def ingest_pdf(file_path: str):

    documents = load_pdf(file_path)

    chunks = split_documents(documents)

    vectorstore = get_vectorstore()

    vectorstore.add_documents(chunks)

    return {
        "documents": len(documents),
        "chunks": len(chunks)
    }