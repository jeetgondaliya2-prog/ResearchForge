from langchain_chroma import Chroma

from backend.config.settings import settings
from backend.rag.embeddings import get_embeddings


def get_vectorstore():

    embeddings = get_embeddings()

    return Chroma(
        collection_name="researchforge_documents",
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY
    )