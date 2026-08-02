class ExperienceRanker:

    def best(self, history):

        if not history:
            return None

        history = sorted(

            history,

            key=lambda x: x.get(
                "score",
                0
            ),

            reverse=True

        )

        return history[0]