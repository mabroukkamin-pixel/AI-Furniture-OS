import json
import os


class VisualMemory:

    def save(self, state):

        image = None

        if hasattr(state, "generation"):
            image = state.generation.get("image")

        if not image:
            return

        folder = "memory"

        os.makedirs(folder, exist_ok=True)

        product = getattr(state, "product_id", "unknown")

        record = {
            "product": product,
            "image": image,
            "design_dna": getattr(state, "design_dna", {}),
            "decision": getattr(state, "decision", {}),
            "experience": getattr(state, "experience", {})
        }

        filename = os.path.join(
            folder,
            f"{product}.json"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                record,
                f,
                indent=4,
                ensure_ascii=False
            )