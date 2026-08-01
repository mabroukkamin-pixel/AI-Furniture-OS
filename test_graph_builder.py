from brain.graph.graph_manager import GraphManager

graph = GraphManager().build()

print("Nodes:", len(graph.knowledge.nodes))
print("Edges:", len(graph.knowledge.edges))

print()

for node in sorted(graph.knowledge.nodes.keys())[:20]:
    print(node)