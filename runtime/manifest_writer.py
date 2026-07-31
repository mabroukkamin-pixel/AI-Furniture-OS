import json
import os
from pathlib import Path


class ManifestWriter:

    manifest_version = "1.0"

    def __init__(self):
        self.project_root = Path(
            __file__
        ).resolve().parents[1]

    def _relative_path(self, path):
        resolved_path = Path(path).resolve()

        try:
            relative_path = resolved_path.relative_to(
                self.project_root
            )
        except ValueError as exc:
            raise ValueError(
                "Manifest path must be inside project root"
            ) from exc

        return relative_path.as_posix()

    def build(self, context, artifacts=None):
        prompt = getattr(
            context,
            "prompt",
            {}
        )

        if not isinstance(prompt, dict):
            prompt = {}

        artifact_data = (
            artifacts
            if artifacts is not None
            else dict(
                getattr(
                    context,
                    "artifacts",
                    {}
                )
            )
        )

        return {
            "manifest_version": self.manifest_version,
            "product_id": getattr(
                context,
                "product_id",
                ""
            ),
            "output_folder": getattr(
                context,
                "output_folder",
                ""
            ),
            "run": {
                "run_id": getattr(
                    context,
                    "run_id",
                    ""
                ),
                "started_at": getattr(
                    context,
                    "started_at",
                    ""
                ),
                "completed_at": getattr(
                    context,
                    "completed_at",
                    None
                ),
                "status": getattr(
                    context,
                    "status",
                    "pending"
                ),
                "current_stage": getattr(
                    context,
                    "current_stage",
                    ""
                ),
                "error": getattr(
                    context,
                    "error",
                    None
                ),
                "engine_name": getattr(
                    context,
                    "engine_name",
                    ""
                ),
            },
            "product": {
                "id": getattr(
                    context,
                    "product_id",
                    ""
                ),
                "image": getattr(
                    context,
                    "product_image",
                    ""
                ),
                "reference_images": getattr(
                    context,
                    "reference_images",
                    []
                ),
            },
            "branding": getattr(
                context,
                "branding",
                {}
            ),
            "marketing": getattr(
                context,
                "marketing",
                {}
            ),
            "preservation": getattr(
                context,
                "preservation",
                {}
            ),
            "decision": getattr(
                context,
                "decision",
                {}
            ),
            "environment": getattr(
                context,
                "environment",
                {}
            ),
            "lighting": getattr(
                context,
                "lighting",
                {}
            ),
            "camera": getattr(
                context,
                "camera",
                {}
            ),
            "composition": getattr(
                context,
                "composition",
                {}
            ),
            "design_dna": getattr(
                context,
                "design_dna",
                {}
            ),
            "prompt": {
                "text": (
                    prompt.get("final")
                    or prompt.get("positive", "")
                ),
                "audit": getattr(
                    context,
                    "audit",
                    {}
                ),
            },
            "generation": getattr(
                context,
                "generation",
                {}
            ),
            "artifacts": artifact_data,
            "trace": getattr(
                context,
                "trace",
                []
            ),
        }

    def write(self, context):
        product_id = getattr(
            context,
            "product_id",
            ""
        )

        output_folder_value = getattr(
            context,
            "output_folder",
            ""
        )

        if not output_folder_value:
            output_folder_value = (
                f"outputs/{product_id}"
            )

        output_folder = Path(
            output_folder_value
        )

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        manifest_path = (
            output_folder / "manifest.json"
        )

        temporary_path = (
            output_folder / "manifest.json.tmp"
        )

        relative_manifest_path = (
            self._relative_path(
                manifest_path
            )
        )

        artifacts = dict(
            getattr(
                context,
                "artifacts",
                {}
            )
        )

        artifacts["manifest"] = (
            relative_manifest_path
        )

        manifest = self.build(
            context,
            artifacts=artifacts
        )

        try:
            with open(
                temporary_path,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    manifest,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            os.replace(
                temporary_path,
                manifest_path
            )

        except Exception:
            if temporary_path.exists():
                temporary_path.unlink()
            raise

        context.artifacts["manifest"] = (
            relative_manifest_path
        )

        return manifest_path.as_posix()