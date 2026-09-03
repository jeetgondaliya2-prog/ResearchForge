# -*- coding: utf-8 -*-
import sys
import os

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from backend.tools.web_search import web_search


if __name__ == "__main__":
    result = web_search.invoke(
        {
            "query":
            "latest AI research trends 2026"
        }
    )


    print("\n")
    print("=" * 60)
    print("WEB SEARCH RESULTS")
    print("=" * 60)

    try:
        print(result)
    except UnicodeEncodeError:
        if isinstance(result, str):
            print(result.encode('utf-8', errors='replace').decode('utf-8'))
        else:
            print(str(result).encode('utf-8', errors='replace').decode('utf-8'))