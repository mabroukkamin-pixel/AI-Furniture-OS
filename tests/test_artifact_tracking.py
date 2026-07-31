import os
import sys
import types
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from runtime.output_manager import OutputManager


class ArtifactTrackingTests(unittest.TestCase):

    def setUp(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.outputs_root = self.project_root / "outputs"
        self.outputs_root.mkdir(exist_ok=True)

        self.context = SimpleNamespace(
            product={"name": "Test Product"},
            decision={},
            branding={},
            marketing={},
            preservation={},
            design_dna={"style": "test"},
            audit={"score": 100},
            generation={},
            final_prompt={
                "positive": "positive test",
                "negative": "negative test",
            },
            artifacts={},
        )

    def test_export_records_written_artifacts(self):
        with tempfile.TemporaryDirectory(
            prefix="artifact_test_",
            dir=self.outputs_root,
        ) as temporary_folder:
            product_id = Path(temporary_folder).name

            manager = OutputManager()
            manager.export(product_id, self.context)

            expected_keys = {
                "design_dna",
                "audit",
                "generation",
                "positive_prompt",
                "negative_prompt",
            }

            self.assertEqual(
                set(self.context.artifacts),
                expected_keys,
            )

            for artifact_path in self.context.artifacts.values():
                self.assertFalse(os.path.isabs(artifact_path))
                self.assertNotIn("\\", artifact_path)
                self.assertTrue(
                    (self.project_root / artifact_path).exists()
                )

    def test_external_path_is_not_recorded(self):
        manager = OutputManager()

        with tempfile.TemporaryDirectory() as external_folder:
            external_file = Path(external_folder) / "external.txt"
            external_file.write_text("test", encoding="utf-8")

            manager.record_artifact(
                self.context,
                "external",
                str(external_file),
            )

        self.assertNotIn("external", self.context.artifacts)

    def test_failed_write_does_not_record_artifact(self):
        manager = OutputManager()

        with patch.object(
            manager,
            "save_json",
            side_effect=OSError("write failed"),
        ):
            with self.assertRaises(OSError):
                manager.export(
                    "ArtifactFailureTest",
                    self.context,
                )

        self.assertEqual(self.context.artifacts, {})

    def test_local_generated_image_is_recorded(self):
        from runtime.production.production_manager import (
            ProductionManager,
        )

        with tempfile.TemporaryDirectory(
            prefix="generated_image_test_",
            dir=self.outputs_root,
        ) as temporary_folder:
            image_path = Path(temporary_folder) / "generated.png"
            image_path.write_bytes(b"image")

            state = SimpleNamespace(
                product_id="GeneratedImageTest",
                prompt={"final": "test prompt"},
                final_prompt={"final": "legacy prompt"},
                product_image="input.png",
                output_folder=temporary_folder,
                generation={},
                artifacts={},
            )

            class FakeEngine:
                def generate(self, request):
                    return {
                        "status": "success",
                        "image": str(image_path),
                        "response": {
                            "image_url": "https://example.com/image.png"
                        },
                    }

            class FakeEngineFactory:
                @staticmethod
                def create(current_state):
                    return FakeEngine()

            fake_module = types.ModuleType(
                "runtime.engines.engine_factory"
            )
            fake_module.EngineFactory = FakeEngineFactory

            with patch.dict(
                sys.modules,
                {
                    "runtime.engines.engine_factory":
                        fake_module
                },
            ):
                ProductionManager(state).run()

            generated_images = state.artifacts[
                "generated_images"
            ]

            self.assertEqual(len(generated_images), 1)
            self.assertFalse(
                os.path.isabs(generated_images[0])
            )
            self.assertNotIn("\\", generated_images[0])

    def test_remote_url_is_not_recorded_as_local_artifact(self):
        from runtime.production.production_manager import (
            ProductionManager,
        )

        state = SimpleNamespace(
            product_id="RemoteOnlyTest",
            prompt={"final": "test prompt"},
            final_prompt={"final": "legacy prompt"},
            product_image="input.png",
            output_folder="outputs/RemoteOnlyTest",
            generation={},
            artifacts={},
        )

        class FakeEngine:
            def generate(self, request):
                return {
                    "status": "success",
                    "image": None,
                    "response": {
                        "image_url":
                            "https://example.com/image.png"
                    },
                }

        class FakeEngineFactory:
            @staticmethod
            def create(current_state):
                return FakeEngine()

        fake_module = types.ModuleType(
            "runtime.engines.engine_factory"
        )
        fake_module.EngineFactory = FakeEngineFactory

        with patch.dict(
            sys.modules,
            {
                "runtime.engines.engine_factory":
                    fake_module
            },
        ):
            ProductionManager(state).run()

        self.assertNotIn(
            "generated_images",
            state.artifacts,
        )


if __name__ == "__main__":
    unittest.main()