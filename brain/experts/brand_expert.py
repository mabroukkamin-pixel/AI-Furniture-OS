from brain.experts.base_expert import BaseExpert


class BrandExpert(BaseExpert):

    def analyze(self, state):

        print("========================================")
        print("        BRAND EXPERT")
        print("========================================")

        branding = state.branding or {}

        state.branding = {

            "company":
                branding.get(
                    "company",
                    state.product.get("brand", "")
                ),

            "arabic":
                branding.get(
                    "arabic",
                    "السوق الصيني"
                ),

            "style":
                branding.get(
                    "style",
                    "premium gulf lifestyle"
                ),

            "colors":
                branding.get(
                    "colors",
                    [
                        "navy blue",
                        "gold",
                        "white"
                    ]
                )

        }

        print("BRAND RESULT:")
        print(state.branding)

        return state