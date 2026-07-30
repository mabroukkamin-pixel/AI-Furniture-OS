from brain.experts.base_expert import BaseExpert
from brain.registry import register


class EnvironmentExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("    ENVIRONMENT EXPERT")
        print("========================================")

        if not brain.product:

            print("No product found.")

            return brain

        env = brain.context.get(
            "environment",
            {}
        ).get(
            "environment",
            {}
        )

        preferred = env.get(
            "preferred",
            []
        )

        brain.environment = {
            "primary": preferred[0] if preferred else "modern_interior",
            "options": preferred,
            "atmosphere": env.get(
                "atmosphere",
                []
            ),
            "architecture": env.get(
                "architecture",
                []
            )
        }

        print("Environment decided.")

        return brain


register(
    lambda: EnvironmentExpert()
)