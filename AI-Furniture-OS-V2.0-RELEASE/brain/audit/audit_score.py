class AuditScore:

    WEIGHTS = {

        "product": 20,

        "environment": 10,

        "lighting": 10,

        "camera": 10,

        "composition": 10,

        "branding": 10,

        "marketing": 5,

        "preservation": 10,

        "quality": 5,

        "design_dna": 5,

        "negative": 5

    }


    def calculate(self, rules):

        score = 0

        maximum = sum(
            self.WEIGHTS.values()
        )

        for key, weight in self.WEIGHTS.items():

            if rules.get(key):

                score += weight

        return {

            "score": score,

            "maximum": maximum,

            "percentage": round(
                score / maximum * 100,
                2
            )

        }