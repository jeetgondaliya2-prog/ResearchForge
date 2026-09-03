from langchain_mistralai import MistralAIEmbeddings
from backend.config.settings import settings


def get_embeddings():

    return MistralAIEmbeddings(
        model="mistral-embed",
        api_key=settings.MISTRAL_API_KEY
    )