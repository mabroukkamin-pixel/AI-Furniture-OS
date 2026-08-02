"""
Batch Pipeline Runner
"""

from runtime.pipeline import FurniturePipeline


def run_batch(product_id):
    pipeline = FurniturePipeline()

    return pipeline.run(
        product_id=product_id
    )


if __name__ == "__main__":

    print("BATCH PIPELINE")

    result = run_batch(
        "Partition001"
    )

    print(result)
