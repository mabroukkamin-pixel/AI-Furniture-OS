class MemoryFusion:

    def apply(
        self,
        state
    ):

        memories = (
            state.memory
            .get(
                "similar_experiences",
                []
            )
        )

        if not memories:

            state.fusion = {
                "memory_used": False,
                "bonus": 0
            }

            return state

        best = memories[0]

        similarity = best.get(
            "similarity",
            0
        )

        bonus = int(
            similarity / 20
        )

        state.fusion = {

            "memory_used": True,

            "best_memory":
                best.get(
                    "memory"
                ),

            "similarity":
                similarity,

            "bonus":
                bonus
        }

        state.history.append(
            {
                "type": "memory_match",
                "memory": best.get("memory"),
                "similarity": similarity,
                "bonus": bonus
            }
        )

        return state