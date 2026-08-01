from brain.experts.base_expert import BaseExpert
from brain.registry import register


class EnvironmentExpert(BaseExpert):

    def analyze(self, brain):

        print("========================================")
        print("    ENVIRONMENT EXPERT")
        print("========================================")


        environment = brain.environment or {}


        preferred = environment.get(
            "preferred",
            []
        )


        brain.environment = {

            "primary":
                preferred[0]
                if preferred
                else "modern_interior",


            "options":
                preferred,


            "atmosphere":
                environment.get(
                    "atmosphere",
                    []
                ),


            "architecture":
                environment.get(
                    "architecture",
                    []
                ),


            "forbidden":
                environment.get(
                    "forbidden",
                    []
                ),


            "source":
                "BrainState"

        }


        print(
            "Environment:",
            brain.environment
        )


        return brain



register(
    lambda: EnvironmentExpert()
)