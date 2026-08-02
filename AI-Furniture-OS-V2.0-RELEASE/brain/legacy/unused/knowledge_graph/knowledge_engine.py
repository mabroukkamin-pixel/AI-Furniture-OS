class KnowledgeEngine:

    def __init__(self, knowledge):

        self.knowledge = knowledge

    def analyze(self, product):

        product_info = (
            product
                .get("product", {})
                .get("product", {})
        )
        
        material = product_info.get(
            "material",
            ""
        )

        category = product_info.get(
            "category",
            ""
        )

        result = {

            "material": material,

            "recommended_style": [],

            "recommended_scene": [],

            "recommended_lighting": [],

            "recommended_camera": [],

            "architecture": {},
            "colors": {},
            "accessories": {},
            "emotion": {},
            "negative": {}

        }

        materials = self.knowledge.get(
            "materials",
            {}
        )

        categories = self.knowledge.get(
            "categories",
            {}
        )

        for key, value in materials.items():

            if key in material:

                result["recommended_style"] += (
                    value.get(
                        "preferred_styles",
                        []
                    )
                )

                result["recommended_scene"] += (
                    value.get(
                        "preferred_scenes",
                        []
                    )
                )

                result["recommended_lighting"] += (
                    value.get(
                        "preferred_lighting",
                        []
                    )
                )

                result["recommended_camera"] += (
                    value.get(
                        "preferred_camera",
                        []
                    )
                )

                if "architecture" in value:
                    result["architecture"] = value.get("architecture")

                if "colors" in value:
                    result["colors"] = value.get("colors")

                if "accessories" in value:
                    result["accessories"] = value.get("accessories")

                if "emotion" in value:
                    result["emotion"] = value.get("emotion")

                if "negative" in value:
                    result["negative"] = value.get("negative")

        if category in categories:

            result["recommended_style"] += (
                categories[category]
                .get("styles", [])
            )

            result["recommended_scene"] += (
                categories[category]
                .get("scenes", [])
            )

        return result

    def run(self, brain):

        brain.knowledge = self.analyze(
            brain.product
        )

        material = brain.knowledge.get(
            "material"
        )

        if material:

            brain.log(
                "Knowledge",
                f"Material detected: {material}"
            )

        brain.log(
            "Knowledge",
            "Knowledge analysis completed"
        )

        return brain