from brain.experts.base_expert import BaseExpert


class MaterialExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("        MATERIAL EXPERT")
        print("========================================")

        if brain.product:

            material = brain.product.get(
                "material",
                {}
            )

            primary = material.get(
                "primary",
                "unknown"
            )

            secondary = material.get(
                "secondary",
                []
            )

            brain.decision["material"] = {
                "primary": primary,
                "secondary": secondary
            }

            print(
                "Primary Material:",
                primary
            )

        return brain