# -*- coding: utf-8 -*-
import sys
import os

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from backend.agents.rag_researcher import rag_research_agent


if __name__ == "__main__":
    state = {
        "user_query": """
        What are the main approaches for
        AI-based crop disease detection?
        """
    }


    result = rag_research_agent(state)


    print("\n")
    print("=" * 60)
    print("RAG RESEARCH RESULT")
    print("=" * 60)

    try:
        print(result)
    except UnicodeEncodeError:
        if isinstance(result, str):
            print(result.encode('utf-8', errors='replace').decode('utf-8'))
        else:
            print(str(result).encode('utf-8', errors='replace').decode('utf-8'))