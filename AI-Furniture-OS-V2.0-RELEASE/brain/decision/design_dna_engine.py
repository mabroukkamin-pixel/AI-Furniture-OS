class DesignDNAEngine:

    def analyze(self, brain):

        print("========================================")
        print("        DESIGN DNA ENGINE")
        print("========================================")

        product = brain.product
        branding = brain.branding
        environment = getattr(
            brain,
            "environment",
            {}
        )
        lighting = getattr(
            brain,
            "lighting",
            {}
        )
        photography = {
            "camera": getattr(
                brain,
                "camera",
                {}
            ),
            "composition": getattr(
                brain,
                "composition",
                {}
            )
        }

        material = product.get(
            "material",
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