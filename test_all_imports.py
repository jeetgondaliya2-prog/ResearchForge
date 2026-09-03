#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""

import sys

def test_imports():
    agents = ['analyst', 'planner', 'supervisor', 'web_researcher', 'academic_researcher', 'rag_researcher', 'critic', 'feasibility', 'researcher']
    tools = ['web_search', 'academic_search', 'calculator', 'document_search']
    
    print('=== AGENT IMPORTS ===')
    failed = []
    for agent in agents:
        try:
            exec(f'from backend.agents.{agent} import *')
            print(f'[OK] {agent}')
        except Exception as e:
            print(f'[ERROR] {agent}: {str(e)[:60]}')
            failed.append((agent, str(e)))
    
    print('\n=== TOOL IMPORTS ===')
    for tool in tools:
        try:
            exec(f'from backend.tools.{tool} import *')
            print(f'[OK] {tool}')
        except Exception as e:
            print(f'[ERROR] {tool}: {str(e)[:60]}')
            failed.append((tool, str(e)))
    
    print('\n=== RAG MODULES ===')
    rag_modules = ['ingestion', 'retriever', 'vectorstore', 'embeddings', 'splitter', 'loaders']
    for mod in rag_modules:
        try:
            exec(f'from backend.rag.{mod} import *')
            print(f'[OK] {mod}')
        except Exception as e:
            print(f'[ERROR] {mod}: {str(e)[:60]}')
            failed.append((mod, str(e)))
    
    print('\n=== SUMMARY ===')
    if failed:
        print(f'Failed imports: {len(failed)}')
        for name, err in failed:
            print(f'  - {name}')
        return False
    else:
        print('All imports successful!')
        return True

if __name__ == '__main__':
    success = test_imports()
    sys.exit(0 if success else 1)
