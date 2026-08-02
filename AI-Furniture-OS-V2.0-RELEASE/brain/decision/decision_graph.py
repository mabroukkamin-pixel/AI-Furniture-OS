class DecisionGraph:

    def __init__(self):

        self.nodes = []
        self.edges = []

    def add_node(self, node, value, **metadata):

        data = {
            "node": node,
            "value": value
        }

        data.update(metadata)

        self.nodes.append(data)

    def add_edge(
        self,
        source,
        target,
        reason="",
        confidence=None
    ):

        self.edges.append({

            "from": source,

            "to": target,

            "reason": reason,

            "confidence": confidence

        })

    def export(self):

        return {

            "nodes": self.nodes,

            "edges": self.edges

        }