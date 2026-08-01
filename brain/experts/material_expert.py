from brain.experts.base_expert import BaseExpert
from brain.services.brain_service import BrainService


class MaterialExpert(BaseExpert):

    def analyze(self, brain):

        service = BrainService(brain)

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

            if (
                not hasattr(brain, "knowledge")
                or brain.knowledge is None
            ):
                brain.knowledge = {}

            brain.knowledge["material"] = {
                "primary": primary,
                "secondary": secondary
            }

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