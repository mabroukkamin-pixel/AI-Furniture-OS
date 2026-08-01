from brain.graph.graph_query import GraphQuery


class GraphReasoner:

    def __init__(self, knowledge):

        self.query = GraphQuery(
            knowledge
        )

    def analyze(self, state):

        print("========================================")
        print("        GRAPH REASONER")
        print("========================================")

        material_data = state.product.get(
            "material",
            {}
        )

        if isinstance(material_data, dict):

            material = material_data.get(
                "primary",
                ""
            )

        else:

            material = material_data

        if not material:

            print(
                "No material found"
            )

            return state

        edges = self.query.related(
            material
        )

        styles = []

        for edge in edges:

            styles.append(
                edge["target"]
            )

        state.graph = {

            "material": material,

            "styles": styles

        }

        print(
            "GRAPH RESULT:"
        )

        print(
            state.graph
        )

        return state

    def reason(self, state):

        return self.analyze(
            state
        )