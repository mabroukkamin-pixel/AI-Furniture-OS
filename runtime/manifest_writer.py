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

    def _normalize_path(self, path):
        if not path:
            return path

        return str(path).replace("\\", "/")

    def _normalize_generation(self, generation):
        if not isinstance(generation, dict):
            return generation

        normalized = dict(generation)

        for key in ("output", "image"):
            if key in normalized:
                normalized[key] = self._normalize_path(
                    normalized[key]
                )

        response = normalized.get("response")

        if isinstance(response, dict):
            normalized_response = dict(response)

            for key in (
                "image_path",
                "prompt_path",
            ):
                if key in normalized_response:
                    normalized_response[key] = (
                        self._normalize_path(
                            normalized_response[key]
                        )
                    )

            normalized["response"] = (
                normalized_response
            )

        return normalized

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

        trace_value = getattr(
            context,
            "trace",
            []
        )
        if hasattr(trace_value, "export"):
            trace_export = trace_value.export()
        elif hasattr(trace_value, "events"):
            trace_export = trace_value.events
        else:
            trace_export = trace_value

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
                "image": self._normalize_path(
                    getattr(
                        context,
                        "product_image",
                        ""
                    )
                ),
                "reference_images": [
                    self._normalize_path(path)
                    for path in getattr(
                        context,
                        "reference_images",
                        []
                    )
                ],
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
            "generation": self._normalize_generation(
                getattr(
                    context,
                    "generation",
                    {}
                )
            ),
            "artifacts": artifact_data,
            "trace": (
                context.trace.export()
                if hasattr(context.trace, "export")
                else trace_export
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