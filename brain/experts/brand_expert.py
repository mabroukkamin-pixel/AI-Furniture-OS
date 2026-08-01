from brain.experts.base_expert import BaseExpert


class BrandExpert(BaseExpert):

    def analyze(self, state):

        print(__file__)

        print("========================================")
        print("        BRAND EXPERT")
        print("========================================")

        branding = state.branding

        # compatibility fallback
        if isinstance(branding, dict) and "branding" in branding:
            branding = branding.get(
                "branding",
                {}
            )

        state.branding = {
            "company": branding.get(
                "company",
                ""
            ),

            "arabic": branding.get(
                "arabic",
                ""
            ),

            "style": "premium_luxury",

            "colors": branding.get(
                "colors",
                {}
            )
        }


        print("DEBUG STATE BRANDING:")
        print(state.branding)


        state.log(
            "BrandExpert",
            "Brand analysis completed"
        )


        return state