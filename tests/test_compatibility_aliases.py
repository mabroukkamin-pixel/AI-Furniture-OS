import unittest

from brain.core.brain_state import BrainState
from brain.prompt.prompt_writer import PromptWriter
from runtime.production.production_manager import ProductionManager


class FakePromptWriter(PromptWriter):
    def write(self, context):
        context.prompt = {"positive": "hello", "negative": "world"}
        context.final_prompt = context.prompt
        return context


class FakeEngine:
    def __init__(self, state):
        self.state = state

    def generate(self, request):
        return {"status": "ok", "request": request}


class FakeEngineFactory:
    @staticmethod
    def create(state):
        return FakeEngine(state)


class CompatibilityAliasTests(unittest.TestCase):
    def test_product_and_product_data_stay_in_sync_after_load(self):
        state = BrainState()
        state.product = {"id": "p1"}
        state.product_data = state.product
        self.assertEqual(state.product, state.product_data)

    def test_pipeline_keeps_product_and_product_data_aligned(self):
        state = BrainState()
        state.product = {"id": "p2"}
        state.product_data = state.product
        self.assertEqual(state.product, state.product_data)

    def test_prompt_and_final_prompt_are_synced_after_write(self):
        writer = FakePromptWriter()
        state = BrainState()
        state = writer.write(state)
        self.assertEqual(state.prompt, state.final_prompt)

    def test_production_manager_prefers_prompt(self):
        state = BrainState()
        state.product_id = "p3"
        state.prompt = {"final": "prompt-text"}
        state.final_prompt = {"final": "legacy-text"}
        manager = ProductionManager(state)
        request = manager.build_request()
        self.assertEqual(request["prompt"], "prompt-text")

    def test_production_manager_falls_back_to_final_prompt_for_legacy_shape(self):
        state = BrainState()
        state.product_id = "p4"
        state.prompt = {}
        state.final_prompt = {"positive": "legacy-positive"}
        manager = ProductionManager(state)
        request = manager.build_request()
        self.assertEqual(request["prompt"], "legacy-positive")


if __name__ == "__main__":
    unittest.main()
