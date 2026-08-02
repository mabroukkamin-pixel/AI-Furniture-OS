
class LearningEngine:


    def improve(self, state):

        experience = getattr(
            state,
            "experience",
            {}
        )


        if experience.get("score",0) >= 75:

            state.learning = {

                "status":"positive",

                "message":
                "Experience approved"

            }


        else:

            state.learning = {

                "status":"needs_improvement"

            }


        return state
