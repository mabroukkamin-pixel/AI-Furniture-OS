from brain.models.experience import Experience


class MemoryExecutor:

    def __init__(self, fusion, memory):

        self.fusion = fusion
        self.memory = memory


    def execute(self, state):

        print("=" * 30)
        print("MEMORY EXECUTOR")
        print("=" * 30)


        # Apply memory fusion
        state = self.fusion.apply(state)


        experience = Experience(

            product_id=state.product.get(
                "id",
                state.product.get(
                    "name",
                    "unknown"
                )
            ),

            decision=getattr(
                state,
                "decision",
                {}
            ),

            design_dna=getattr(
                state,
                "design_dna",
                {}
            ),

            generation=getattr(
                state,
                "generation",
                {}
            ),

            evaluation=getattr(
                state,
                "evaluation",
                {}
            )
        )


        self.memory.remember(
            experience
        )


        print(
            "Experience stored:",
            experience.product_id
        )


        return state