import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient


# ==========================================
# LOAD PROJECT ROOT .ENV
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


@tool
def web_search(query: str) -> str:
    """
    Search the internet for current research information.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "TAVILY_API_KEY is not configured."

    client = TavilyClient(
        api_key=api_key
    )

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    results = []

    for result in response.get("results", []):

        results.append({
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content")
        })

    return str(results)