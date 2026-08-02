
class RewardSystem:


    def calculate(self,state):

        experience = getattr(
            state,
            "experience",
            {}
        )


        score = experience.get(
            "score",
            0
        )


        return {

            "reward":
                score / 100

        }
