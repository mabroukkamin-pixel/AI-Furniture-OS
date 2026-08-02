class FusionService:


    def apply(self, state):

        print("FUSION SERVICE")

        state.fusion = {
            "status": "applied"
        }

        return state
