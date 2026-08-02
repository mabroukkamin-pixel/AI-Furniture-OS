from runtime.pipeline import FurniturePipeline

from brain.loaders.product_loader import ProductLoader
from runtime.brain_runner import BrainRunner
from brain.prompt.prompt_writer import PromptWriter


def find_product_path(product_id):

    locations = [
        f"products/{product_id}",
        f"artifacts/products/{product_id}",
    ]

    for path in locations:
        import os

        if os.path.exists(path):
            return path

    raise FileNotFoundError(
        f"Product folder not found: {product_id}"
    )


class AutomationBootstrap:


    def create_pipeline(self, product_id):

        product_path = find_product_path(
            product_id
        )

        pipeline = FurniturePipeline(

            loader=ProductLoader(
                product_path
            ),

            brain=BrainRunner(
                product_id
            ),

            writer=PromptWriter()

        )

        return pipeline