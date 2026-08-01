from brain.core.brain_state import BrainState
from brain.graph.knowledge_graph import KnowledgeGraph
from brain.graph.graph_builder import GraphBuilder
from brain.graph.edge_builder import EdgeBuilder
from brain.graph.graph_reasoner import GraphReasoner


print("========================================")
print("GRAPH REASONER TEST")
print("========================================")


# Create Graph Memory
knowledge = KnowledgeGraph()


# Build graph
builder = GraphBuilder(
    knowledge
)

builder.build_material_graph(
    "brain/knowledge/materials.yaml"
)


# Build relations
edge_builder = EdgeBuilder(
    knowledge
)

edge_builder.connect()



# Create Brain State

state = BrainState()


state.product = {

    "name": "Rattan Partition",

    "material": "rattan"

}



# Create Reasoner

reasoner = GraphReasoner(
    knowledge
)



# Analyze

state = reasoner.analyze(
    state
)



print("==============================")

print(
    state.graph
)