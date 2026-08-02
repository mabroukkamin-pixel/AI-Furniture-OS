from brain.experts.base_expert import BaseExpert


class CompositionExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("    COMPOSITION EXPERT")
        print("========================================")

        brain.composition = {

            "style": "luxury_minimal",

            "product_position": "center",

            "product_scale": "75%",

            "position": "center",

            "balance": "luxury_minimal",

            "focus": "product_first"

        }

        return brain