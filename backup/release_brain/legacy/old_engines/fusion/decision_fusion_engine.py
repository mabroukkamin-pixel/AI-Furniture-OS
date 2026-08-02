class DecisionFusionEngine:

    def process(self, context):

        context.visual_identity = {

            "design_style":
                context.design_dna.get(
                    "design_style",
                    ""
                ),

            "brand_language":
                context.design_dna.get(
                    "brand_language",
                    ""
                ),

            "scene":
                context.design_dna.get(
                    "scene",
                    ""
                ),

            "lighting":
                context.design_dna.get(
                    "lighting_mood",
                    {}
                ),

            "camera":
                context.design_dna.get(
                    "camera_language",
                    {}
                ),

            "composition":
                context.design_dna.get(
                    "composition",
                    {}
                ),

            "emotion":
                context.design_dna.get(
                    "emotion",
                    []
                )

        }

        return context