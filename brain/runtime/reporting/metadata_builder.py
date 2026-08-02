from datetime import datetime


class MetadataBuilder:

    def build(self, state):

        product = getattr(state, "product", {}) or {}
        decision = getattr(state, "decision", {}) or {}
        lighting = getattr(state, "lighting", {}) or {}
        branding = getattr(state, "branding", {}) or {}

        metadata = {
            "created_at": datetime.utcnow().isoformat() + "Z",

            "product_id": getattr(
                state,
                "product_id",
                ""
            ),

            "product_name": product.get(
                "name",
                ""
            ),

            "category": product.get(
                "category",
                ""
            ),

            "material": getattr(
                state,
                "material",
                ""
            ),

            "selected_style": decision.get(
                "selected_style",
                ""
            ),

            "lighting": lighting.get(
                "type",
                ""
            ),

            "engine": getattr(
                state,
                "engine_name",
                ""
            ),

            "brand": branding.get(
                "company",
                ""
            ),
        }

        state.metadata = metadata

        return metadata