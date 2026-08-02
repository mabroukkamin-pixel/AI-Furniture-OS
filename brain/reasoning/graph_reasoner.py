class GraphReasoner:


    def analyze(self, graph):

        nodes = graph.get(
            "nodes",
            []
        )

        edges = graph.get(
            "edges",
            []
        )


        evidence = []


        for edge in edges:

            if edge["to"] == "style":

                evidence.append(
                    {
                        "source": edge["from"],
                        "reason": edge["reason"]
                    }
                )


        style = None
        confidence = 0


        for node in nodes:

            if node["node"] == "style":

                style = node["value"]

                confidence = node.get(
                    "score",
                    0
                )


        return {

            "style": style,

            "confidence": confidence,

            "evidence": evidence

        }