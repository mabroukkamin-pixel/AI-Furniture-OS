class LearningEngine:


    def learn(self, state):


        experience = {

            "product":
                getattr(
                    state.product,
                    "id",
                    None
                ),


            "decision":
                state.decision,


            "experience":
                state.experience

        }


        return experience
