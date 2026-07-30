from runtime.pipeline import FurniturePipeline
from brain.loaders.product_loader import ProductLoader
from runtime.brain_runner import BrainRunner
from brain.prompt.prompt_writer import PromptWriter
import argparse


def run(product_id):

    product_path = (
        f"products/{product_id}"
    )

    loader = ProductLoader(
        product_path
    )

    brain = BrainRunner(
        product_id
    )

    writer = PromptWriter()

    pipeline = FurniturePipeline(
        loader,
        brain,
        writer
    )

    result = pipeline.run(
        product_id
    )

    return {
        "product": product_id,

        "product_data": result.product,

        "branding": (
            result.branding
            if hasattr(result, "branding")
            else {}
        ),

        "design_dna": (
            result.design_dna
            if hasattr(result, "design_dna")
            else {}
        ),

        "audit": (
            result.audit
            if hasattr(result, "audit")
            else {}
        ),

        "generation": {
            "status": (
                result.generation.get("status")
                if hasattr(result, "generation")
                else "unknown"
            ),
            "output_folder": str(result.output_folder)
        },

        "prompt": {
            "length": len(result.prompt["final"])
        }
    }


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--product",
        required=True
    )

    args = parser.parse_args()

    product_id = args.product

    result = run(product_id)

    print()
    print("==============================")
    print("PIPELINE FINISHED")
    print("==============================")
    print("Product :", result["product"])
    print("Prompt  :", result["prompt"]["length"])
    print("Output  :", result["generation"]["output_folder"])
    print("Status  :", result["generation"]["status"])


if __name__ == "__main__":

    main()