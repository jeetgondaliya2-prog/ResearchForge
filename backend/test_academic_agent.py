# -*- coding: utf-8 -*-
import sys
import os

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from backend.agents.academic_researcher import (
    academic_research_agent
)


if __name__ == "__main__":
    state = {
        "user_query":
            "AI based crop disease detection using deep learning"
    }


    result = academic_research_agent(state)


    print("\n")
    print("=" * 70)
    print("ACADEMIC RESEARCH AGENT")
    print("=" * 70)

    try:
        print(result)
    except UnicodeEncodeError:
        if isinstance(result, str):
            print(result.encode('utf-8', errors='replace').decode('utf-8'))
        else:
            print(str(result).encode('utf-8', errors='replace').decode('utf-8'))