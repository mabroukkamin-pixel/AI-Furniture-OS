from runtime.pipeline import FurniturePipeline
from brain.loaders.product_loader import ProductLoader
from runtime.brain_runner import BrainRunner
from brain.composers.prompt_writer import PromptWriter
from brain.generators.generator_manager import GeneratorManager


def main():

    product_id = "Partition001"

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

    generator = GeneratorManager()

    pipeline = FurniturePipeline(
        loader,
        brain,
        writer,
        generator
    )

    result = pipeline.run(
        product_id
    )

    print()
    print("==============================")
    print("PIPELINE FINISHED")
    print("==============================")
    print("Product :", product_id)
    print("Prompt  :", len(result.prompt["final"]))
    print("Output  :", result.output_folder)
    if hasattr(result, "generation"):
        print("Status  :", result.generation.get("status"))


if __name__ == "__main__":

    main()