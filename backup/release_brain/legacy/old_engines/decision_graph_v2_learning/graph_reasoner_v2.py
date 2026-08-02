from brain.graph.graph_query import GraphQuery


class GraphReasoner:

    def __init__(self, knowledge):

        self.query = GraphQuery(
            knowledge
        )


    def analyze(self, state):

        print("========================================")
        print("        GRAPH REASONER V2")
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


        recommendations = []


        for edge in edges:

            style = edge.get(
                "target"
            )


            if style:

                recommendations.append(

                    {

                        "style": style,

                        "score": self.calculate_score(
                            material,
                            style
                        ),

                        "reason": [

                            "material compatibility",

                            "visual style match",

                            "furniture category relation"

                        ]

                    }

                )



        recommendations.sort(

            key=lambda x: x["score"],

            reverse=True

        )



        state.graph = {


            "material": material,


            "recommendations": recommendations,


            "recommended_styles":

                [

                    item["style"]

                    for item in recommendations

                ],


            "avoid": [

                "warehouse",

                "industrial",

                "low_quality"

            ],


            "confidence": 0.95,


            "source":

                "KnowledgeGraph + GraphReasonerV2"


        }



        print(
            "GRAPH RESULT:"
        )


        print(
            state.graph
        )


        return state



    def calculate_score(
        self,
        material,
        style
    ):

        score = 80


        if material in [

            "rattan",

            "wood"

        ]:

            score += 10


        if style in [

            "gulf_villa",

            "luxury_resort"

        ]:

            score += 5


        return score



    def reason(self, state):

        return self.analyze(
            state
        )