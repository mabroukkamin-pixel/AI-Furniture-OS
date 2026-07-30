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

            brain.decision["material"] = {
                "name": material
            }

        return brain