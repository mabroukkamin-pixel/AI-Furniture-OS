import argparse
import os

from runtime.pipeline import FurniturePipeline
from runtime.brain_runner import BrainRunner

from brain.loaders.product_loader import ProductLoader
from brain.prompt.prompt_writer import PromptWriter


def find_product_path(product_id):

    locations = [
        f"products/{product_id}",
        f"artifacts/products/{product_id}",
    ]

    for path in locations:

        if os.path.exists(path):
            return path

    raise FileNotFoundError(
        f"Product folder not found: {product_id}"
    )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--product",
        required=True
    )

    args = parser.parse_args()

    product_id = args.product


    print("=" * 60)
    print("        AI FURNITURE OS")
    print("=" * 60)


    product_path = find_product_path(
        product_id
    )


    print(
        "PRODUCT PATH:",
        product_path
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


    state = pipeline.run(
        product_id
    )


    print("=" * 60)
    print("AI FURNITURE OS FINISHED")
    print("=" * 60)

    print(
        "STATUS:",
        state.status
    )


if __name__ == "__main__":
    main()