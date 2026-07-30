from brain.experts.base_expert import BaseExpert


class CompositionExpert(BaseExpert):

    def analyze(self, context):

        print("========================================")
        print("    COMPOSITION EXPERT")
        print("========================================")

        context.composition = {
            "style": "luxury_minimal",
            "product_position": "center",
            "product_scale": "75%",
            "position": "center",
            "balance": "luxury_minimal",
            "focus": "product_first"
        }

        return context