from pathlib import Path


class EmbeddingEngine:

    """
    Visual Memory Encoder V3

    Creates rich visual embeddings
    from BrainState intelligence.
    """

    def generate(
        self,
        image_path,
        context=None
    ):

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(image_path)

        embedding = {

            "file": {

                "filename": image_path.name,

                "suffix": image_path.suffix.lower(),

                "size": image_path.stat().st_size
            },

            "visual": {

                "category": "furniture",

                "material": "unknown",

                "style": "unknown",

                "scene": "unknown",

                "colors": [],

                "composition": {},

                "lighting": {},

                "camera": {},

                "design_style": ""

            }

        }

        if context:

            if isinstance(context, dict):

                product = context.get(
                    "product",
                    {}
                )

                decision = context.get(
                    "decision",
                    {}
                )

                design = context.get(
                    "design_dna",
                    {}
                )

            else:

                product = getattr(
                    context,
                    "product",
                    {}
                )

                decision = getattr(
                    context,
                    "decision",
                    {}
                )

                design = getattr(
                    context,
                    "design_dna",
                    {}
                )

            if isinstance(product, dict):
                identity = (
                    product.get(
                        "identity",
                        product
                    )
                ) if "identity" in product else product
            else:
                identity = getattr(product, "identity", product)

            embedding["visual"]["category"] = (
                identity.get(
                    "category",
                    "furniture"
                )
                if isinstance(identity, dict)
                else getattr(identity, "category", "furniture")
            )

            material_data = (
                identity.get("material", {})
                if isinstance(identity, dict)
                else getattr(identity, "material", {})
            )
            embedding["visual"]["material"] = (
                material_data.get(
                    "primary",
                    "unknown"
                )
                if isinstance(material_data, dict)
                else getattr(material_data, "primary", "unknown")
            )

            embedding["visual"]["style"] = (
                decision.get(
                    "selected_style",
                    decision.get(
                        "style",
                        "unknown"
                    )
                )
                if isinstance(decision, dict)
                else getattr(
                    decision,
                    "selected_style",
                    getattr(decision, "style", "unknown")
                )
            )

            embedding["visual"]["scene"] = (
                design.get(
                    "scene",
                    design.get(
                        "environment",
                        "unknown"
                    )
                )
                if isinstance(design, dict)
                else getattr(
                    design,
                    "scene",
                    getattr(design, "environment", "unknown")
                )
            )

            embedding["visual"]["design_style"] = (
                design.get(
                    "design_style",
                    ""
                )
                if isinstance(design, dict)
                else getattr(design, "design_style", "")
            )

            embedding["visual"]["lighting"] = (
                design.get(
                    "lighting_mood",
                    {}
                )
                if isinstance(design, dict)
                else getattr(design, "lighting_mood", {})
            )

            embedding["visual"]["composition"] = (
                design.get(
                    "composition",
                    {}
                )
                if isinstance(design, dict)
                else getattr(design, "composition", {})
            )

            embedding["visual"]["camera"] = (
                design.get(
                    "camera_language",
                    {}
                )
                if isinstance(design, dict)
                else getattr(design, "camera_language", {})
            )

            colors_data = (
                identity
                .get("colors", {})
                if isinstance(identity, dict)
                else getattr(identity, "colors", {})
            )
            colors = (
                colors_data
                .get(
                    "primary",
                    []
                )
                if isinstance(colors_data, dict)
                else getattr(colors_data, "primary", [])
            )

            embedding["visual"]["colors"] = colors

        return embedding


_engine = EmbeddingEngine()


def create_embedding(
    image_path,
    context=None
):

    return _engine.generate(
        image_path,
        context
    )