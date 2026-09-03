# -*- coding: utf-8 -*-
import sys
import os

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from backend.tools.academic_search import academic_search


if __name__ == "__main__":
    query = """
    AI based crop disease detection
    using deep learning
    """


    result = academic_search.invoke(
        {
            "query": query
        }
    )


    print("\n")

    print("=" * 70)

    print("ARXIV ACADEMIC SEARCH RESULTS")

    print("=" * 70)

    try:
        print(result)
    except UnicodeEncodeError:
        if isinstance(result, str):
            print(result.encode('utf-8', errors='replace').decode('utf-8'))
        else:
            print(str(result).encode('utf-8', errors='replace').decode('utf-8'))