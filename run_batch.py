import os


class BatchRunner:

    def __init__(self):

        self.products_path = "products"

    def get_products(self):

        if not os.path.exists(
            self.products_path
        ):
            return []

        products = []

        for item in os.listdir(
            self.products_path
        ):

            path = os.path.join(
                self.products_path,
                item
            )

            if not os.path.isdir(path):
                continue

            product_file = os.path.join(
                path,
                "product.yaml"
            )

            if os.path.exists(product_file):

                products.append(item)

        return products

    def run(self):

        print("==============================")
        print("AI FURNITURE BATCH ENGINE")
        print("==============================")

        products = self.get_products()

        if not products:

            print(
                "No products found"
            )

            return

        for product in products:

            print(
                f"Processing: {product}"
            )

            # هنا لاحقاً سنستدعي:
            #
            # Product Loader
            # Brain
            # Prompt Writer
            # Generator
            #
            #

            print(
                f"Completed: {product}"
            )


if __name__ == "__main__":

    runner = BatchRunner()

    runner.run()