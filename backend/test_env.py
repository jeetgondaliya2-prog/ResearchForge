# -*- coding: utf-8 -*-
import sys
import os

if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()


    key = os.getenv("MISTRAL_API_KEY")


    if key:
        print("MISTRAL_API_KEY is loaded")
        print("Key length:", len(key))
        print("First characters:", key[:5])
    else:
        print("MISTRAL_API_KEY NOT FOUND")