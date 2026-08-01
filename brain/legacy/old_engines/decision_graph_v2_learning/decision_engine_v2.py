from brain.graph.graph_score import GraphScore
from brain.visual_memory.retriever import VisualMemoryRetriever


class DecisionEngineV2:

    def __init__(self):

        self.scorer = GraphScore()
        self.visual_memory = VisualMemoryRetriever()


    def get_visual_memory_bonus(self, state):

        try:

            if hasattr(state, "product_image") and state.product_image:

                results = self.visual_memory.retrieve(
                    state.product_image,
                    state
                )

            else:

                results = []

            if not results:

                return 0, []


            best = results[0]


            similarity = best.get(
                "similarity",
                0
            )


            bonus = round(
                similarity / 10
            )


            if bonus > 10:
                bonus = 10


            return bonus, results


        except Exception as e:

            print(
                "Visual Memory Error:",
                e
            )

            return 0, []


    def analyze(self, state):

        print("========================================")
        print("        DECISION ENGINE V2")
        print("========================================")


        material = state.graph.get(
            "material",
            ""
        )


        styles = state.graph.get(
            "styles",
            []
        )

        # Graph Reasoner V2 compatibility
        if not styles:

            styles = state.graph.get(
                "recommended_styles",
                []
            )


        if not material or not styles:

            print(
                "No graph data available"
            )

            return state



        # GRAPH SCORE

        ranking = self.scorer.rank(
            material,
            styles
        )


        # OLD MEMORY

        memory_bonus = (
            state.fusion
            .get(
                "bonus",
                0
            )
        )


        # VISUAL MEMORY

        visual_bonus, visual_results = (
            self.get_visual_memory_bonus(
                state
            )
        )


        print(
            "Visual Memory Bonus:",
            visual_bonus
        )


        for item in ranking:


            item["base_score"] = item["score"]


            item["memory_bonus"] = (
                memory_bonus
            )


            item["visual_memory_bonus"] = (
                visual_bonus
            )


            item["score"] += (
                memory_bonus
                +
                visual_bonus
            )



        ranking.sort(
            key=lambda x:x["score"],
            reverse=True
        )



        winner = ranking[0]



        state.decision = {

            "selected_style":
                winner["style"],


            "base_score":
                winner["base_score"],


            "memory_bonus":
                memory_bonus,


            "visual_memory_bonus":
                visual_bonus,


            "score":
                winner["score"],


            "memory_used":
                (
                    memory_bonus > 0
                    or
                    visual_bonus > 0
                ),


            "visual_matches":
                visual_results,


            "ranking":
                ranking
        }



        print(
            "DECISION RESULT:"
        )


        print(
            state.decision
        )


        return state