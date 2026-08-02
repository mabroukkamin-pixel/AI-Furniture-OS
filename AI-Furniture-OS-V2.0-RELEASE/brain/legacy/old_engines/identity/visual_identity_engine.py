class VisualIdentityEngine:

    def build(self, context):

        dna = getattr(
            context,
            "design_dna",
            {}
        )

        context.visual_identity = {

            "style":
                dna.get(
                    "design_style",
                    ""
                ),

            "brand":
                dna.get(
                    "brand_language",
                    ""
                ),

            "scene":
                dna.get(
                    "scene",
                    ""
                ),

            "emotion":
                dna.get(
                    "emotion",
                    []
                ),

            "lighting":
                dna.get(
                    "lighting_mood",
                    {}
                ),

            "camera":
                dna.get(
                    "camera_language",
                    {}
                ),

            "composition":
                dna.get(
                    "composition",
                    {}
                )

        }

        return context