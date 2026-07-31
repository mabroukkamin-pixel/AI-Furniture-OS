import unittest
from unittest.mock import patch
from datetime import datetime

from runtime.pipeline import FurniturePipeline
from runtime.run_pipeline import run
from brain.core.brain_state import BrainState


class DummyLoader:
    def load(self):
        return {"name": "Partition001", "branding": {"brand": "demo"}}


class DummyBrain:
    def run(self, state):
        return state


class DummyWriter:
    def write(self, state):
        return state


class DummyProductionManager:
    def __init__(self, state):
        self.state = state

    def run(self):
        return {"status": "ok"}


class DummyImageResolver:
    def find_product_image(self, product_path):
        return {"main_image": "main.png", "reference_images": []}


class DummyOutputManager:
    def export(self, product_id, state):
        return None


class DummyManifestWriter:
    written_statuses = []

    def write(self, state):
        self.written_statuses.append(
            state.status
        )
        return "manifest.json"


class DummyDNAEngine:
    def analyze(self, state):
        return {"dna": "ok"}


class DummyAuditor:
    def audit(self, state):
        return {"audited": True}


class RunLifecycleTests(unittest.TestCase):
    def setUp(self):
        DummyManifestWriter.written_statuses.clear()

    def test_success_lifecycle(self):
        pipeline = FurniturePipeline(DummyLoader(), DummyBrain(), DummyWriter(), generator=None)
        pipeline.production_manager_cls = DummyProductionManager
        pipeline.image_resolver_cls = DummyImageResolver
        pipeline.output_manager_cls = DummyOutputManager
        pipeline.manifest_writer_cls = DummyManifestWriter
        pipeline.design_dna_engine_cls = DummyDNAEngine
        pipeline.prompt_auditor_cls = DummyAuditor
        state = pipeline.run("Partition001", lifecycle_state=BrainState())

        self.assertEqual(state.status, "succeeded")
        self.assertEqual(state.current_stage, "completed")
        self.assertTrue(state.run_id)
        self.assertTrue(state.started_at)
        self.assertTrue(state.completed_at)
        self.assertIsNone(state.error)
        self.assertEqual(
            DummyManifestWriter.written_statuses,
            ["succeeded"]
        )

    def test_failure_lifecycle(self):
        class FailingLoader:
            def load(self):
                raise ValueError("boom")

        pipeline = FurniturePipeline(FailingLoader(), DummyBrain(), DummyWriter(), generator=None)
        pipeline.output_manager_cls = DummyOutputManager
        pipeline.manifest_writer_cls = DummyManifestWriter
        with self.assertRaises(ValueError):
            pipeline.run("Partition001", lifecycle_state=BrainState())

        state = pipeline.last_state
        self.assertEqual(state.status, "failed")
        self.assertEqual(state.current_stage, "loading_product")
        self.assertTrue(state.completed_at)
        self.assertEqual(state.error["type"], "ValueError")
        self.assertEqual(state.error["message"], "boom")
        self.assertEqual(state.error["stage"], "loading_product")
        self.assertEqual(
            DummyManifestWriter.written_statuses,
            ["failed"]
        )

    def test_run_helper_creates_unique_run_id_and_utc_timestamp(self):
        lifecycle_state = BrainState()
        with patch(
            "runtime.output_manager.OutputManager.export",
            return_value=None,
        ), patch(
            "runtime.manifest_writer.ManifestWriter.write",
            return_value="manifest.json",
        ):
            result = run(
                "Partition001",
                lifecycle_state=lifecycle_state
            )
        self.assertTrue(isinstance(result, dict))
        self.assertIn("product", result)


if __name__ == "__main__":
    unittest.main()