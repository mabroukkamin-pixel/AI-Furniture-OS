from brain.graph.graph_score import GraphScore


class DecisionEngineV2:

    def __init__(self):

        self.scorer = GraphScore()

    def get_memory_bonus(self, state):

        memories = (
            state.memory
            .get(
                "similar_experiences",
                []
            )
        )

        if not memories:

            return 0

        best_similarity = max(
            item.get(
                "similarity",
                0
            )
            for item in memories
        )

        # Maximum bonus = 5
        bonus = round(
            best_similarity / 20
        )

        return bonus

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

        memory_bonus = (
            state.fusion
            .get(
                "bonus",
                0
            )
        )

        if not material or not styles:

            print(
                "No graph data available"
            )

            return state

        ranking = self.scorer.rank(
            material,
            styles
        )

        for item in ranking:

            item["base_score"] = item["score"]

            item["memory_bonus"] = memory_bonus

            item["score"] += memory_bonus

        ranking.sort(
            key=lambda x: x["score"],
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

            "score":
                winner["score"],

            "memory_used":
                memory_bonus > 0,

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