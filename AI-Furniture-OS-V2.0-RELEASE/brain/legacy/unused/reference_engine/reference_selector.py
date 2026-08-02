from pathlib import Path


class ReferenceSelector:

    def __init__(self, database=None):
        self.database = database or {}


    def select(self, product):

        product_id = product.get(
            "id"
        )

        category = product.get(
            "category"
        )

        material = product.get(
            "material",
            ""
        )


        best_match = None
        best_score = 0


        for ref_id, ref in self.database.items():

            score = 0


            tags = ref.get(
                "tags",
                {}
            )


            if category in tags.get(
                "category",
                []
            ):
                score += 5


            for mat in tags.get(
                "material",
                []
            ):

                if mat in material:
                    score += 3


            if score > best_score:

                best_score = score
                best_match = ref_id



        if not best_match:
            return {}


        reference = self.database[best_match]


        return {

            "selected_reference":
                best_match,

            "score":
                best_score,

            "images":
                reference.get(
                    "images",
                    []
                ),

            "styles":
                reference.get(
                    "tags",
                    {}
                ).get(
                    "style",
                    []
                ),

            "scenes":
                reference.get(
                    "tags",
                    {}
                ).get(
                    "scene",
                    []
                ),

            "lighting":
                reference.get(
                    "preferences",
                    {}
                ).get(
                    "preferred_light",
                    []
                ),

            "camera":
                reference.get(
                    "preferences",
                    {}
                ).get(
                    "preferred_camera",
                    []
                )
        }


    def extract(self, scanned_data):

        if not scanned_data:
            return {
                "meta": {},
                "images": []
            }


        return {

            "reference_styles":
                scanned_data.get(
                    "styles",
                    []
                ),


            "reference_backgrounds":
                scanned_data.get(
                    "scenes",
                    []
                ),


            "reference_lighting":
                scanned_data.get(
                    "lighting",
                    []
                ),


            "reference_camera":
                scanned_data.get(
                    "camera",
                    []
                ),


            "reference_images":
                scanned_data.get(
                    "images",
                    []
                ),


            "meta": {

                "selected_reference":
                    scanned_data.get(
                        "selected_reference"
                    ),

                "score":
                    scanned_data.get(
                        "score"
                    )
            },


            "images":
                scanned_data.get(
                    "images",
                    []
                )
        }