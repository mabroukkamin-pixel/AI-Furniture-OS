from datetime import datetime, timezone
from uuid import uuid4

from brain.core.brain_state import BrainState
import argparse


def _utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _initialize_lifecycle_state(product_id):
    state = BrainState()
    state.run_id = f"{product_id}-{uuid4().hex}"
    state.started_at = _utc_now_iso()
    state.status = "running"
    state.current_stage = "initializing"
    return state


def run(product_id, lifecycle_state=None):

    if lifecycle_state is None:
        lifecycle_state = _initialize_lifecycle_state(product_id)
    else:
        if not lifecycle_state.run_id:
            lifecycle_state.run_id = f"{product_id}-{uuid4().hex}"
        if not lifecycle_state.started_at:
            lifecycle_state.started_at = _utc_now_iso()
        if not lifecycle_state.status:
            lifecycle_state.status = "running"
        if not lifecycle_state.current_stage:
            lifecycle_state.current_stage = "initializing"

    product_path = (
        f"products/{product_id}"
    )

    try:
        from brain.loaders.product_loader import ProductLoader
    except Exception:
        class ProductLoader:
            def __init__(self, product_path):
                self.product_path = product_path

            def load(self):
                return {"name": product_id, "branding": {"brand": "demo"}}

    try:
        from runtime.brain_runner import BrainRunner
    except Exception:
        class BrainRunner:
            def __init__(self, product_id):
                self.product_id = product_id

            def run(self, state):
                return state

    try:
        from brain.prompt.prompt_writer import PromptWriter as RealPromptWriter
    except Exception:
        RealPromptWriter = None

    from runtime.pipeline import FurniturePipeline

    loader = ProductLoader(
        product_path
    )

    brain = BrainRunner(
        product_id
    )

    if lifecycle_state is not None and RealPromptWriter is None:
        class PromptWriter:
            def write(self, state):
                return state
    elif lifecycle_state is not None and RealPromptWriter is not None:
        class PromptWriter:
            def __init__(self):
                self._real_writer = RealPromptWriter()

            def write(self, state):
                try:
                    return self._real_writer.write(state)
                except Exception:
                    return state
    else:
        PromptWriter = RealPromptWriter or type("PromptWriter", (), {"write": lambda self, state: state})

    writer = PromptWriter()

    pipeline = FurniturePipeline(
        loader,
        brain,
        writer
    )

    result = pipeline.run(
        product_id,
        lifecycle_state=lifecycle_state
    )

    prompt_text = ""
    if hasattr(result, "prompt") and isinstance(result.prompt, dict):
        prompt_text = result.prompt.get("final", "")

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
            "length": len(prompt_text)
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