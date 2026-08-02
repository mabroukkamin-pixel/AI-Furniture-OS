import os
import sys

ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(
    0,
    ROOT
)

import argparse
from brain.runtime.brain_runtime import BrainRuntime


def main():

    parser = argparse.ArgumentParser(
        description="AI Furniture OS Brain Launcher"
    )

    parser.add_argument(
        "--product",
        default="Partition001"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("        AI FURNITURE OS V2")
    print("        BRAIN LAUNCHER")
    print("=" * 60)

    brain = BrainRuntime(
        args.product
    )

    state = brain.run()

    print("=" * 60)
    print("            RUN COMPLETE")
    print("=" * 60)

    print("STATUS:")
    print(state.status)

    print()

    print("PRODUCT:")
    print(
        state.product.get(
            "name",
            ""
        )
    )

    print()

    print("FINAL STYLE:")
    print(
        state.decision
    )

    print()

    print("OUTPUT:")
    print(
        state.output_folder
    )


if __name__ == "__main__":
    main()