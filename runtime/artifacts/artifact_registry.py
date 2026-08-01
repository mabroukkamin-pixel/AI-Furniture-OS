import os
import json
from datetime import datetime


class ArtifactRegistry:

    def __init__(self, root="artifacts"):

        self.root = root

    def create_artifact_path(self, state):

        product_id = getattr(
            state,
            "product_id",
            "unknown"
        )

        product_path = os.path.join(
            self.root,
            "products",
            product_id
        )

        versions_path = os.path.join(
            product_path,
            "versions"
        )

        os.makedirs(
            versions_path,
            exist_ok=True
        )

        version = self._next_version(
            versions_path
        )

        artifact_path = os.path.join(
            versions_path,
            version
        )

        os.makedirs(
            artifact_path,
            exist_ok=True
        )

        return artifact_path, version

    def _next_version(self, path):

        versions = []

        for item in os.listdir(path):

            if item.startswith("v"):

                try:
                    number = int(
                        item.replace(
                            "v",
                            ""
                        )
                    )

                    versions.append(number)

                except ValueError:
                    pass

        if not versions:
            return "v001"

        return f"v{max(versions)+1:03d}"

    def save_manifest(
        self,
        state,
        artifact_path,
        version
    ):

        manifest = {

            "artifact_version": version,

            "product_id": getattr(
                state,
                "product_id",
                ""
            ),

            "status": getattr(
                state,
                "status",
                ""
            ),

            "engine": getattr(
                state,
                "engine_name",
                ""
            ),

            "created_at":
                datetime.utcnow()
                .isoformat()
                + "Z",

            "files": {},

            "trace": getattr(
                state,
                "trace",
                []
            )

        }

        path = os.path.join(
            artifact_path,
            "manifest.json"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                manifest,
                f,
                indent=4,
                ensure_ascii=False
            )

        return path

    def register(self, state):

        artifact_path, version = (
            self.create_artifact_path(
                state
            )
        )

        manifest = self.save_manifest(
            state,
            artifact_path,
            version
        )

        state.artifacts = {

            "path": artifact_path,

            "version": version,

            "manifest": manifest

        }

        return state.artifacts