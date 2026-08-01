from brain.experts.base_expert import BaseExpert
from brain.services.brain_service import BrainService


class MaterialExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("        MATERIAL EXPERT")
        print("========================================")

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


        brain.knowledge["material"] = {

            "primary": primary,
            "secondary": secondary

        }


        service = BrainService(brain)

        service.decision.set(
            "material",
            {
                "primary": primary,
                "secondary": secondary
            }
        )


        print(
            "Primary Material:",
            primary
        )


        return brain