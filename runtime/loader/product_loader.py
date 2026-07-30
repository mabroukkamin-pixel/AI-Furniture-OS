import json


class ProductLoader:

    def load(self):

        with open(
            "products/data/product.json",
            encoding="utf-8"
        ) as f:

            return json.load(f)