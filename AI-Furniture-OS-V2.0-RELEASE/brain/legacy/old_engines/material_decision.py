from brain.decision_engine.base_decision import BaseDecision


class MaterialDecision(BaseDecision):

    def run(self, context):

        print("========================================")
        print("       MATERIAL DECISION")
        print("========================================")

        material = context.product.get(
            "material",
            {}
        )

        primary = material.get(
            "primary",
            ""
        )

        print(
            "Primary Material:",
            primary
        )

        context.decision["material"] = {
            "primary": primary
        }

        return context