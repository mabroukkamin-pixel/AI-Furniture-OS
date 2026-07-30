class ConfidenceEngine:


    def calculate(self, brain):


        scores = {}


        decision = brain.decision


        ranking = decision.get(
            "style_ranking",
            []
        )


        total = sum(
            score
            for _,score in ranking
        )


        for style,score in ranking:

            if total:

                confidence = round(
                    (score / total) * 100,
                    2
                )

            else:

                confidence = 0


            scores[style] = confidence



        brain.confidence = {


            "ranking":
                scores,


            "best_match":
                decision.get(
                    "primary_style"
                )

        }



        brain.log(
            "Confidence",
            "Confidence calculated"
        )


        return brain