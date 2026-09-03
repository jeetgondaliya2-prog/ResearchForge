from backend.agents.researcher import create_research_agent


if __name__ == "__main__":
    agent = create_research_agent()


    response = agent.invoke(
        "Explain what RAG is and why it is useful."
    )


    print("\nAI RESPONSE:\n")
    print(response.content)