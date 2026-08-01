from brain.graph.graph_manager import GraphManager

graph = GraphManager().build()

print("=" * 40)
print("GRAPH TEST")
print("=" * 40)

print("\nStyles:")
print(graph.reasoner.recommend("rattan"))

print("\nWalk:")
print(graph.reasoner.walk("rattan"))

print("\nNeighbors:")
for edge in graph.knowledge.neighbors("rattan"):
    print(edge)