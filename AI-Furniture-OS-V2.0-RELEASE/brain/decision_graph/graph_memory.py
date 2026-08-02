class GraphMemory:

    def __init__(self):

        self.nodes = []
        self.edges = []

        self._nodes_by_id = {}
        self._edge_keys = set()

    def add_node(self, node):

        existing = self._nodes_by_id.get(
            node.id
        )

        if existing is not None:

            existing.attributes.update(
                node.attributes
            )

            return existing

        self.nodes.append(node)

        self._nodes_by_id[node.id] = node

        return node

    def add_edge(self, edge):

        edge_key = (
            edge.source,
            edge.target,
            edge.relation
        )

        if edge_key in self._edge_keys:
            return None

        self.edges.append(edge)
        self._edge_keys.add(edge_key)

        return edge

    def get_node(self, node_id):

        return self._nodes_by_id.get(
            node_id
        )

    def find_by_type(self, node_type):

        return [
            node
            for node in self.nodes
            if node.type == node_type
        ]

    def find_edges(
        self,
        source=None,
        target=None,
        relation=None
    ):

        results = []

        for edge in self.edges:

            if (
                source is not None
                and edge.source != source
            ):
                continue

            if (
                target is not None
                and edge.target != target
            ):
                continue

            if (
                relation is not None
                and edge.relation != relation
            ):
                continue

            results.append(edge)

        return results

    def neighbors(
        self,
        node_id,
        relation=None
    ):

        results = []

        edges = self.find_edges(
            source=node_id,
            relation=relation
        )

        for edge in edges:

            node = self.get_node(
                edge.target
            )

            if node is not None:

                results.append(
                    {
                        "node": node,
                        "edge": edge
                    }
                )

        return results

    def clear(self):

        self.nodes.clear()
        self.edges.clear()

        self._nodes_by_id.clear()
        self._edge_keys.clear()

    def stats(self):

        node_types = {}

        for node in self.nodes:

            node_types[node.type] = (
                node_types.get(
                    node.type,
                    0
                )
                + 1
            )

        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "node_types": node_types
        }

    def export(self):

        return {
            "nodes": [
                node.to_dict()
                for node in self.nodes
            ],
            "edges": [
                edge.to_dict()
                for edge in self.edges
            ]
        }