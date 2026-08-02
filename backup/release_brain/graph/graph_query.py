class GraphQuery:

    def __init__(

        self,

        graph

    ):

        self.graph = graph

    def related(

        self,

        node,

        relation=None

    ):

        edges = self.graph.neighbors(
            node
        )

        if relation is None:

            return edges

        return [

            edge

            for edge

            in edges

            if edge["relation"] == relation

        ]