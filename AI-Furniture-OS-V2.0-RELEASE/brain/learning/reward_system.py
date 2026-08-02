class RewardSystem:


    def calculate(self, experience):


        reward = 0


        score = experience.get(
            "experience",
            {}
        ).get(
            "score",
            0
        )


        reward = score


        return {

            "reward":
                reward,

            "quality":
                "high"
                if reward >= 75
                else "low"

        }
