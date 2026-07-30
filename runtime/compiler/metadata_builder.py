from datetime import datetime


class MetadataBuilder:

    def build(self, state):

        product = getattr(state, "product", {})

        metadata = {

            "product_id": product.get("id"),

            "product_name": product.get("name"),

            "category": product.get("category"),

            "generated_at": datetime.utcnow().isoformat(),

            "engine": getattr(state, "engine_name", "none"),

            "version": "1.0",

        }

        return metadata