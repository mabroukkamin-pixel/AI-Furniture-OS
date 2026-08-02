from brain.runtime.executors.base_executor import BaseExecutor


class DesignDNAExecutor(BaseExecutor):

    def execute(self, state):

        print("DESIGN DNA EXECUTOR")

        product = state.product

        decision = state.decision or {}
        reasoning = getattr(
            state,
            "graph_reasoning",
            {}
        )
        environment = state.environment or {}
        lighting = state.lighting or {}
        camera = state.camera or {}
        composition = state.composition or {}

        style = decision.get(
            "style",
            ""
        )

        state.design_dna = {

            "product":
                product.get(
                    "name",
                    ""
                ),

            "design_style":
                style,

            "decision_reasoning":
                reasoning,

            "scene":
                environment.get(
                    "scene",
                    "luxury gulf interior"
                ),

            "material_story":
                f"""
Natural {product.get('material','')} 
material with handcrafted premium texture
""".strip(),

            "brand_language":
                product.get(
                    "brand",
                    ""
                ),

            "architecture":
                environment.get(
                    "architecture",
                    {}
                ),

            "lighting_mood":
                lighting.get(
                    "types",
                    []
                ),

            "camera_language":
                camera,

            "composition":
                composition,

            "emotion":
                environment.get(
                    "mood",
                    []
                )

        }

        print("DESIGN DNA:")
        print(state.design_dna)

        return state