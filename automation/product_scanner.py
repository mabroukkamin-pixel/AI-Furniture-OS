import os


class ProductScanner:

    def __init__(self, products_path="products"):
        self.products_path = products_path


    def scan(self):

        products = []

        if not os.path.exists(self.products_path):
            return products


        for item in os.listdir(self.products_path):

            path = os.path.join(
                self.products_path,
                item
            )

            if os.path.isdir(path):

                if item.startswith("_"):
                    continue

                products.append(item)


        return sorted(products)