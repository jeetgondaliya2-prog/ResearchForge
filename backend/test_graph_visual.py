from backend.graph.workflow import build_graph


graph = build_graph()

print("\n" + "=" * 60)
print("RESEARCHFORGE AI GRAPH")
print("=" * 60)

print(
    graph.get_graph().draw_ascii()
)