# -*- coding: utf-8 -*-
import sys
import os

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from backend.llm.models import get_llm


if __name__ == "__main__":
    llm = get_llm()


    response = llm.invoke(
        "Say hello in one sentence."
    )


    print("=" * 60)
    print("LLM TEST")
    print("=" * 60)

    print(response.content)