import argparse
import json
from datetime import datetime

from brain.runtime.brain_runtime import BrainRuntime


def banner():

    print("=" * 60)
    print("        AI FURNITURE OS - AUTONOMOUS BRAIN")
    print("=" * 60)



def run(product_id):

    banner()

    start = datetime.now()

    print()
    print("PRODUCT:")
    print(product_id)

    print()
    print("STARTING BRAIN...")
    print()


    brain = BrainRuntime(
        product_id
    )


    state = brain.run()


    end = datetime.now()


    print()
    print("=" * 60)
    print("              BRAIN COMPLETE")
    print("=" * 60)


    print()

    print("STATUS:")
    print(
        state.status
    )


    print()

    print("DESIGN STYLE:")

    print(
        state.design_dna.get(
            "design_style"
        )
    )


    print()

    print("CONFIDENCE:")

    print(
        state.graph_reasoning.get(
            "confidence"
        )
    )


    print()

    print("OUTPUT:")

    print(
        state.output_folder
    )


    report = {

        "product":
            product_id,

        "started":
            str(start),

        "completed":
            str(end),

        "style":
            state.design_dna.get(
                "design_style"
            ),

        "confidence":
            state.graph_reasoning.get(
                "confidence"
            ),

        "artifacts":
            state.artifacts

    }


    with open(
        "brain_run_report.json",
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )


    print()

    print(
        "REPORT SAVED:"
    )

    print(
        "brain_run_report.json"
    )



if __name__ == "__main__":


    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--product",
        default="Partition001"
    )


    args = parser.parse_args()


    run(
        args.product
    )