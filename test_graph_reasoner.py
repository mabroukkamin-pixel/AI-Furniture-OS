import json

from brain.reasoning.graph_reasoner import GraphReasoner


with open(
    "outputs/Partition001/brain/graph_decision.json",
    encoding="utf-8"
) as f:

    graph = json.load(f)


reasoner = GraphReasoner()


result = reasoner.analyze(
    graph
)


print(result)