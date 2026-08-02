import json
import os
from datetime import datetime


class ManifestManager:

    def save(self, state):

        manifest = {
            "product": getattr(state, "product_id", None),
            "status": getattr(state, "generation_status", ""),
            "engine": getattr(state, "engine_name", ""),
            "artifacts": getattr(state, "artifacts", {}),
            "experience": getattr(state, "experience", {}),
            "created_at": datetime.utcnow().isoformat()
        }

        folder = getattr(state, "output_folder", None)

        if not folder:
            return

        os.makedirs(folder, exist_ok=True)

        with open(
            os.path.join(folder, "manifest.json"),
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                manifest,
                f,
                indent=4,
                ensure_ascii=False
            )