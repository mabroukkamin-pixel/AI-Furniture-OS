from brain.graph.knowledge_graph import KnowledgeGraph
from brain.graph.decision_graph import DecisionGraph
from brain.graph.graph_reasoner import GraphReasoner
from brain.graph.graph_memory import GraphMemory
from brain.graph.graph_loader import GraphLoader
from brain.graph.graph_builder import GraphBuilder
from brain.graph.edge_builder import EdgeBuilder


class GraphManager:

    def __init__(self):

        self.knowledge = KnowledgeGraph()

        self.builder = GraphBuilder(
            self.knowledge
        )

        self.decision = DecisionGraph()

        self.memory = GraphMemory()

        self.reasoner = GraphReasoner(
            self.knowledge
        )

        self.loader = GraphLoader(
            self.knowledge
        )

        self.edge_builder = EdgeBuilder(
            self.knowledge
        )

    def build(self):

        self.builder.build_material_graph(
            "brain/knowledge/materials.yaml"
        )

        self.edge_builder.connect()

        self.decision.add_rule(

            lambda c: c["material"] == "rattan",

            "warm_daylight"

        )

        return self