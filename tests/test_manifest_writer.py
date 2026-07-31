import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from runtime.manifest_writer import ManifestWriter


class ManifestWriterTests(unittest.TestCase):

    def setUp(self):
        self.project_root = Path(
            __file__
        ).resolve().parents[1]

    def make_context(
        self,
        output_folder,
        status="succeeded",
        error=None,
    ):
        return SimpleNamespace(
            product_id="ManifestTest",
            output_folder=str(output_folder),
            run_id="run-123",
            started_at="2026-07-31T00:00:00Z",
            completed_at="2026-07-31T00:01:00Z",
            status=status,
            current_stage="completed",
            error=error,
            engine_name="nano_banana",
            product_image="products/ManifestTest/input.png",
            reference_images=[],
            branding={"brand": "test"},
            marketing={},
            preservation={},
            decision={},
            environment={},
            lighting={},
            camera={},
            composition={},
            design_dna={"style": "test"},
            prompt={
                "positive": "positive prompt",
                "negative": "negative prompt",
                "final": "final prompt",
            },
            audit={"score": 100},
            generation={"status": status},
            artifacts={},
            trace=[],
        )

    def test_success_manifest_is_written(self):
        with tempfile.TemporaryDirectory(
            prefix=".manifest_test_",
            dir=self.project_root,
        ) as temporary_folder:
            context = self.make_context(
                temporary_folder
            )

            writer = ManifestWriter()
            manifest_path = writer.write(
                context
            )

            path = Path(manifest_path)

            self.assertTrue(path.exists())
            self.assertFalse(
                Path(
                    f"{manifest_path}.tmp"
                ).exists()
            )

            manifest = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            self.assertEqual(
                manifest["manifest_version"],
                "1.0"
            )
            self.assertEqual(
                manifest["product_id"],
                "ManifestTest"
            )
            self.assertEqual(
                manifest["run"]["status"],
                "succeeded"
            )
            self.assertEqual(
                manifest["prompt"]["text"],
                "final prompt"
            )
            self.assertIn(
                "manifest",
                manifest["artifacts"]
            )
            self.assertFalse(
                Path(
                    manifest["artifacts"]["manifest"]
                ).is_absolute()
            )

    def test_failure_manifest_preserves_error(self):
        with tempfile.TemporaryDirectory(
            prefix=".manifest_failure_test_",
            dir=self.project_root,
        ) as temporary_folder:
            error = {
                "type": "RuntimeError",
                "message": "generation failed",
                "stage": "running_production",
            }

            context = self.make_context(
                temporary_folder,
                status="failed",
                error=error,
            )

            context.current_stage = (
                "running_production"
            )

            manifest_path = ManifestWriter().write(
                context
            )

            manifest = json.loads(
                Path(manifest_path).read_text(
                    encoding="utf-8"
                )
            )

            self.assertEqual(
                manifest["run"]["status"],
                "failed"
            )
            self.assertEqual(
                manifest["run"]["error"],
                error
            )

    def test_failed_atomic_replace_leaves_no_files(self):
        with tempfile.TemporaryDirectory(
            prefix=".manifest_atomic_test_",
            dir=self.project_root,
        ) as temporary_folder:
            context = self.make_context(
                temporary_folder
            )

            manifest_path = (
                Path(temporary_folder)
                / "manifest.json"
            )

            temporary_path = (
                Path(temporary_folder)
                / "manifest.json.tmp"
            )

            with patch(
                "runtime.manifest_writer.os.replace",
                side_effect=OSError(
                    "replace failed"
                ),
            ):
                with self.assertRaises(OSError):
                    ManifestWriter().write(
                        context
                    )

            self.assertFalse(
                manifest_path.exists()
            )
            self.assertFalse(
                temporary_path.exists()
            )
            self.assertNotIn(
                "manifest",
                context.artifacts
            )

    def test_manifest_normalizes_path_separators(self):
        context = self.make_context(
            "outputs/ManifestTest"
        )

        context.product_image = (
            r"products\ManifestTest\input.png"
        )

        context.reference_images = [
            r"products\ManifestTest\reference.png"
        ]

        context.generation = {
            "status": "local_only",
            "output": r"outputs\ManifestTest",
            "image": None,
            "response": {
                "image_path": None,
                "prompt_path": (
                    r"outputs\ManifestTest"
                    r"\generated_prompt.txt"
                ),
            },
        }

        manifest = ManifestWriter().build(
            context
        )

        self.assertEqual(
            manifest["product"]["image"],
            "products/ManifestTest/input.png"
        )

        self.assertEqual(
            manifest["product"]["reference_images"],
            [
                "products/ManifestTest/reference.png"
            ]
        )

        self.assertEqual(
            manifest["generation"]["output"],
            "outputs/ManifestTest"
        )

        self.assertEqual(
            manifest["generation"]["response"][
                "prompt_path"
            ],
            (
                "outputs/ManifestTest/"
                "generated_prompt.txt"
            )
        )


if __name__ == "__main__":
    unittest.main()