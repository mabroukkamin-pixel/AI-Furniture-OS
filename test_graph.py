from brain.graph.knowledge_graph import KnowledgeGraph
from brain.graph.graph_reasoner import GraphReasoner

kg = KnowledgeGraph()
reasoner = GraphReasoner(kg)

print(reasoner.walk("rattan"))