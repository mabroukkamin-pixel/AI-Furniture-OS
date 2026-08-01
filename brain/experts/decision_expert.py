from brain.experts.base_expert import BaseExpert


class DecisionExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("        DECISION EXPERT")
        print("========================================")

        if brain.decision is None:
            brain.decision = {}

        material = (
            brain.product
            .get("material", {})
            .get("primary", "unknown")
        )

        style = (
            brain.product
            .get("style", ["modern"])[0]
        )


        brain.decision.update({

            "material": material,

            "primary_style": style

        })


        return brain