from brain.graph.graph_manager import GraphManager

graph = GraphManager().build()

print(graph.knowledge.neighbors("rattan"))
print()
print(graph.reasoner.walk("rattan"))