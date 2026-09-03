from backend.rag.vectorstore import get_vectorstore


def get_retriever():

    vectorstore = get_vectorstore()

    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5
        }
    )