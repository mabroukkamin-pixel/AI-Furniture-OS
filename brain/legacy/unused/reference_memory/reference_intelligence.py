class ReferenceIntelligence:

    def __init__(self, database):
        self.database = database

    def analyze(self, product_id):

        ref = self.database.get(product_id)

        if not ref:
            return {}

        return {

            "reference_images":
                ref.get("images", []),

            "reference_styles":
                ref.get("tags", {}).get(
                    "style", []
                ),

            "reference_materials":
                ref.get("tags", {}).get(
                    "material", []
                ),

            "reference_scenes":
                ref.get("tags", {}).get(
                    "scene", []
                ),
        }