from brain.runtime.executors.base_executor import BaseExecutor
from brain.reasoning.context_resolver import ContextResolver


class ContextFusionExecutor(BaseExecutor):

    def __init__(self):

        self.resolver = ContextResolver()

    def execute(self, state):

        print("CONTEXT FUSION EXECUTOR")

        resolved = self.resolver.resolve(state)

        state.environment = {

            "style":
                resolved.get(
                    "style",
                    ""
                ),

            "colors":
                resolved.get(
                    "colors",
                    []
                ),

            "mood":
                resolved.get(
                    "mood",
                    []
                ) 
                or
                state.graph_reasoning.get(
                    "emotion",
                    [
                        "gulf_luxury",
                        "refined"
                    ]
                ),

            "architecture":
                resolved.get(
                    "architecture",
                    {}
                ),

            "accessories":
                resolved.get(
                    "accessories",
                    {}
                )

        }

        state.lighting = {

            "types": resolved.get(
                "lighting",
                []
            )

        }

        state.camera = resolved.get(
            "camera",
            {
                "lens": "50mm",
                "angle": "eye level",
                "shot": "hero product shot"
            }
        )

        # Composition
        state.composition = {

            "product_position": "center",

            "scale": "75 percent frame",

            "style": "luxury catalog"

        }

        # Marketing
        state.marketing = {

            "audience":
                state.product.get(
                    "target",
                    ""
                ),

            "positioning":
                "premium gulf home furniture"

        }

        return state