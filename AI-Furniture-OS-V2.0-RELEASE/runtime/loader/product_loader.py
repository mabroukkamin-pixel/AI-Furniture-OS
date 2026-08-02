import json
import os


class ProductLoader:

    def __init__(
        self,
        product_path="products/data"
    ):
        self.product_path = product_path


    def load(self):

        candidates = [

            os.path.join(
                self.product_path,
                "product.json"
            ),

            os.path.join(
                self.product_path,
                "data",
                "product.json"
            )

        ]


        for product_file in candidates:

            if os.path.exists(product_file):

                with open(
                    product_file,
                    encoding="utf-8"
                ) as f:

                    return json.load(f)


        raise FileNotFoundError(
            f"Product json not found in {self.product_path}"
        )