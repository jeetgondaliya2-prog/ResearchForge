import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

    DATABASE_URL = os.getenv("DATABASE_URL")

    CHROMA_PERSIST_DIRECTORY = os.getenv(
        "CHROMA_PERSIST_DIRECTORY",
        "./vector_db"
    )


settings = Settings()