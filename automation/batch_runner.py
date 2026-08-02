import os


class BatchRunner:

    def __init__(self):
        pass


    def create_pipeline(self, product):

        from brain.loaders.product_loader import ProductLoader
        from runtime.brain_runner import BrainRunner
        from brain.prompt.prompt_writer import PromptWriter
        from runtime.pipeline import FurniturePipeline

        product_path = os.path.join(
            "products",
            product
        )

        loader = ProductLoader(
            product_path
        )

        brain = BrainRunner(
            product
        )

        writer = PromptWriter()

        return FurniturePipeline(
            loader=loader,
            brain=brain,
            writer=writer
        )


    def run_product(self, product):

        pipeline = self.create_pipeline(product)

        state = pipeline.run(
            product
        )

        return state


    def run_all(self, products_path="products"):

        products = []

        for name in os.listdir(products_path):

            path = os.path.join(
                products_path,
                name
            )

            if os.path.isdir(path):

                identity = os.path.join(
                    path,
                    "identity.yaml"
                )

                if os.path.exists(identity):
                    products.append(name)

        for product in products:

            self.run_product(product)