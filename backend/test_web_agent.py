# -*- coding: utf-8 -*-
import sys
import io

# Set UTF-8 encoding for output
if sys.platform.startswith('win'):
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from backend.agents.web_researcher import web_research_agent


if __name__ == "__main__":
    state = {
        "user_query": "AI based crop disease detection using deep learning"
    }


    result = web_research_agent(state)


    print("\n")
    print("=" * 70)
    print("WEB RESEARCH AGENT RESULT")
    print("=" * 70)

    try:
        print(result)
    except UnicodeEncodeError:
        # Handle unicode encoding errors on Windows
        if isinstance(result, str):
            print(result.encode('utf-8', errors='replace').decode('utf-8'))
        else:
            print(str(result).encode('utf-8', errors='replace').decode('utf-8'))