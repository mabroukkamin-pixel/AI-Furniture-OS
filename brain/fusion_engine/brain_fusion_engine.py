class BrainFusionEngine:

    def __init__(
        self,
        config=None,
        rule_result=None,
        graph_result=None,
        reference_memory=None,
        brand_result=None,
        knowledge_result=None
    ):
        self.config = config or {}
        self.external_data = {
            "rule": rule_result or {},
            "graph": graph_result or {},
            "reference": reference_memory or {},
            "brand": brand_result or {},
            "knowledge": knowledge_result or {}
        }

    def fuse_style(self, brain):

        weights = self.config.get(
            "weights",
            {}
        )

        scores = {}

        # =========================
        # PRODUCT STYLE
        # =========================
        product_info = (
            brain.product
            .get(
                "identity",
                {}
            )
            .get(
                "product",
                {}
            )
        )
        
        product_style = (
            product_info
            .get(
                "style",
                []
            )
        )

        if isinstance(product_style, list):

            for style in product_style:

                scores[style] = (
                    scores.get(style, 0)
                    +
                    weights.get(
                        "product",
                        3
                    )
                )

        # =========================
        # BRAND STYLE
        # =========================
        brand_data = (
            brain.branding
            .get(
                "branding",
                {}
            )
        )
        
        brand_style = (
            brand_data
            .get(
                "style",
                []
            )
        )

        if isinstance(brand_style, list):

            for style in brand_style:

                scores[style] = (
                    scores.get(style, 0)
                    +
                    weights.get(
                        "brand",
                        2
                    )
                )

        def add_style(style, weight):

            if not style:
                return

            if isinstance(style, list):

                for s in style:
                    scores[s] = (
                        scores.get(s, 0)
                        + weight
                    )

            else:

                scores[style] = (
                    scores.get(style, 0)
                    + weight
                )

        # PRODUCT ID / STYLES

        product = brain.product.get(
            "id",
            {}
        )

        styles = (
            brain.product
            .get("style", [])
        )

        add_style(
            styles,
            5
        )

        # MATERIAL STYLE INTELLIGENCE
        material = (
            brain.product
            .get("material", {})
        )
        if isinstance(material, dict):

            material_name = (
                material.get("primary")
            )

            if material_name == "rattan":

                add_style(
                    "natural",
                    8
                )

                add_style(
                    "bohemian",
                    4
                )

                add_style(
                    "luxury",
                    3
                )

        # GRAPH STYLE

        graph_style = (
            brain.graph
            .get("recommended_style")
        )

        add_style(
            graph_style,
            4
        )

        # BRAND STYLE (Legacy helper)

        brand = brain.branding

        if isinstance(brand, dict):

            brand_style_legacy = (
                brand
                .get("style")
            )

            add_style(
                brand_style_legacy,
                3
            )

        # DECISION STYLE

        add_style(
            brain.decision.get(
                "primary_style"
            ),
            2
        )

        if not scores:

            return {
                "primary": "modern",
                "supporting": []
            }

        sorted_styles = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {

            "primary":
                sorted_styles[0][0],

            "supporting":
                [
                    x[0]
                    for x in sorted_styles[1:4]
                ]

        }

    def run(self, brain):

        style_result = self.fuse_style(
            brain
        )

        final_style = style_result["primary"]
        supporting_styles = (
            style_result["supporting"]
        )

        scene = []

        # Reference memory
        reference_scene = (
            brain.reference
            .get(
                "reference_backgrounds",
                []
            )
        )
        if isinstance(reference_scene, list):
            for item in reference_scene:
                if item not in scene:
                    scene.append(item)
        elif reference_scene and reference_scene not in scene:
            scene.append(reference_scene)

        # Knowledge
        knowledge_scene = (
            brain.knowledge
            .get(
                "recommended_scene",
                []
            )
        )
        if isinstance(knowledge_scene, list):
            for item in knowledge_scene:
                if item not in scene:
                    scene.append(item)
        elif knowledge_scene and knowledge_scene not in scene:
            scene.append(knowledge_scene)

        # Graph
        graph_scene = (
            brain.graph
            .get(
                "recommended_scene"
            )
        )
        if isinstance(graph_scene, list):
            for item in graph_scene:
                if item not in scene:
                    scene.append(item)
        elif graph_scene and graph_scene not in scene:
            scene.append(graph_scene)

        # Product Environment / Decision / Rules if any
        decision_scene = (
            brain.decision
            .get(
                "scene",
                []
            )
        )
        if isinstance(decision_scene, list):
            for item in decision_scene:
                if item not in scene:
                    scene.append(item)
        elif decision_scene and decision_scene not in scene:
            scene.append(decision_scene)

        if not scene:

            env = getattr(
                brain,
                "environment",
                {}
            )

            preferred = (
                env.get(
                    "preferred",
                    []
                )
            )

            if preferred:
                scene.extend(
                    preferred
                )

            else:
                scene = [
                    "luxury_villa"
                ]

        camera = (
            getattr(
                brain,
                "camera",
                {}
            )
            .get(
                "angle",
                []
            )
        )
        if not camera:

            camera = (
                brain.reference
                .get(
                    "reference_camera",
                    []
                )
            )

        lighting = (
            getattr(
                brain,
                "lighting",
                {}
            )
        )
        if isinstance(lighting, dict):

            lighting = [
                lighting.get(
                    "type"
                )
            ]

        materials = []
        material_val = (
            brain.product
            .get("material", {})
        )
        if isinstance(material_val, dict):

            material_val = (
                material_val
                .get("primary")
            )

        if material_val:
            if isinstance(material_val, list):
                materials.extend(material_val)
            else:
                materials.append(material_val)

        environment = getattr(
            brain,
            "environment",
            {}
        )

        brain.fusion = {

            "final_style":
                final_style,

            "supporting_styles":
                supporting_styles,

            "scene":
                scene,

            "camera":
                camera,

            "lighting":
                lighting,

            "materials":
                materials,

            "architecture":
                environment.get(
                    "architecture",
                    {}
                ),

            "colors":
                environment.get(
                    "colors",
                    {}
                ),

            "accessories":
                environment.get(
                    "accessories",
                    {}
                ),

            "confidence":
                "calculated_later"

        }

        brain.log(
            "Fusion",
            f"Fusion completed: {final_style}"
        )

        return brain