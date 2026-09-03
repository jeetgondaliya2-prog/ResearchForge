from backend.graph.workflow import build_graph


print("\n" + "=" * 70)
print("BUILDING RESEARCHFORGE AI GRAPH")
print("=" * 70)


graph = build_graph()

print("[OK] Graph built successfully.")


query = """
I want to build an AI-powered crop disease
detection system.

Research existing solutions, datasets,
technologies, research papers, and
project feasibility.
"""


print("\n" + "=" * 70)
print("RUNNING RESEARCH WORKFLOW")
print("=" * 70)

print("[INFO] Query:")
print(query)


result = graph.invoke(
    {
        "user_query": query,
        "revision_count": 0
    }
)


print("\n" + "=" * 70)
print("RESEARCHFORGE AI FINAL RESULT")
print("=" * 70)


print("\nFINAL REPORT:\n")

print(
    result.get(
        "final_report",
        "No final report generated."
    )
)


print("\n" + "=" * 70)
print("WORKFLOW COMPLETED")
print("=" * 70)