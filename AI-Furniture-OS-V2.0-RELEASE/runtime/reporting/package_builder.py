import json
import os


class PackageBuilder:

    def build(self, state):

        folder = state.output_folder

        package = {
            "product": state.product_id,
            "status": state.status,
            "engine": state.engine_name,
            "manifest": os.path.join(folder, "manifest.json"),
            "prompt": os.path.join(folder, "positive_prompt.txt"),
            "negative_prompt": os.path.join(folder, "negative_prompt.txt"),
            "design_dna": os.path.join(folder, "design_dna.json"),
            "audit": os.path.join(folder, "audit.json"),
            "generation": os.path.join(folder, "generation.json")
        }

        path = os.path.join(folder, "package.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                package,
                f,
                ensure_ascii=False,
                indent=4
            )

        return path