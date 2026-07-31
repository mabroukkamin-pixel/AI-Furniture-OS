import unittest

from brain.core.brain_state import BrainState


class BrainStateAdditiveExtensionTests(unittest.TestCase):
    def test_default_values_for_new_fields(self):
        state = BrainState()

        self.assertEqual(state.run_id, "")
        self.assertEqual(state.started_at, "")
        self.assertIsNone(state.completed_at)
        self.assertEqual(state.status, "pending")
        self.assertEqual(state.current_stage, "")
        self.assertIsNone(state.error)
        self.assertEqual(state.engine_name, "")
        self.assertEqual(state.artifacts, {})

    def test_artifacts_use_safe_default_factory(self):
        first = BrainState()
        second = BrainState()

        first.artifacts["output"] = "result.json"

        self.assertEqual(first.artifacts, {"output": "result.json"})
        self.assertEqual(second.artifacts, {})

    def test_existing_fields_remain_available(self):
        state = BrainState(
            product_data={"id": "partition001"},
            product={"name": "Partition001"},
            prompt={"final": "prompt"},
            final_prompt={"final": "prompt"},
        )

        self.assertEqual(state.product_data, {"id": "partition001"})
        self.assertEqual(state.product, {"name": "Partition001"})
        self.assertEqual(state.prompt, {"final": "prompt"})
        self.assertEqual(state.final_prompt, {"final": "prompt"})

    def test_brainstate_can_be_created_as_before(self):
        state = BrainState()

        self.assertIsInstance(state, BrainState)
        self.assertEqual(state.product_data, {})
        self.assertEqual(state.product, {})
        self.assertEqual(state.context, {})
        self.assertEqual(state.prompt, {})


if __name__ == "__main__":
    unittest.main()
