class DesignDNAEngine:

    def analyze(self, context):

        print("========================================")
        print("        DESIGN DNA ENGINE")
        print("========================================")

        product = context.get(
            "product",
            {}
        )

        material = product.get(
            "material",
            {}
        )

        branding = context.get(
            "branding",
            {}
        )

        environment = context.get(
            "environment",
            {}
        )

        lighting = context.get(
            "lighting",
            {}
        )

        photography = context.get(
            "photography",
            {}
        )

        accessories = environment.get(
            "accessories",
            {}
        )

        architecture = environment.get(
            "architecture",
            []
        )
        if isinstance(architecture, dict):

            architecture = (
                architecture.get(
                    "architecture",
                    []
                )
                +
                architecture.get(
                    "walls",
                    []
                )
                +
                architecture.get(
                    "floors",
                    []
                )
            )

        dna = {

            "design_style":
                "Modern Gulf Natural Luxury",

            "scene":
                environment.get(
                    "primary",
                    "luxury_villa"
                ),

            "material_story":
                f"Handcrafted {material.get('primary','natural material')} furniture",

            "brand_language":
                branding.get(
                    "style",
                    "premium"
                ),

            "architecture":
                architecture,

            "accessories":
                accessories,

            "lighting_mood":
                lighting,

            "camera_language":
                photography.get(
                    "camera",
                    {}
                ),

            "composition":
                photography.get(
                    "composition",
                    {}
                ),

            "emotion":
                [
                    "luxury",
                    "comfort",
                    "elegance"
                ]
        }

        return dna