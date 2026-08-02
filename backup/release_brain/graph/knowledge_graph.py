class KnowledgeGraph:

    def __init__(self):

        self.nodes = {}

        self.edges = {}

    def add_node(self, name, data):

        self.nodes[name] = data

    def add_edge(self, source, target, relation):

        self.edges.setdefault(
            source,
            []
        ).append({

            "target": target,

            "relation": relation

        })

    def get(self, node):

        return self.nodes.get(
            node,
            {}
        )

    def neighbors(self, node):

        return self.edges.get(
            node,
            []
        )