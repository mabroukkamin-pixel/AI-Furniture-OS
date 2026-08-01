from brain.graph.graph_manager import GraphManager

graph = GraphManager().build()

print(graph.knowledge.nodes.keys())

print()

print(graph.reasoner.walk("rattan"))