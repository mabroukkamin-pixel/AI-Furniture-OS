from brain.knowledge_graph.inference_engine import InferenceEngine


class GraphEngine:


    def __init__(self, graph):

        self.engine = InferenceEngine(
            graph
        )


    def run(self, brain):

        material = brain.knowledge.get(
            "material"
        )


        if not material:

            brain.log(
                "Graph",
                "No material found for graph inference"
            )

            return brain


        brain.graph = self.engine.infer(
            material
        )


        brain.log(
            "Graph",
            f"Graph generated from material: {material}"
        )


        return brain