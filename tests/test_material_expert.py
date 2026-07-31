import unittest
from types import SimpleNamespace

from brain.experts.material_expert import (
    MaterialExpert
)


class MaterialExpertTests(unittest.TestCase):

    def test_creates_missing_decision_state(self):
        brain = SimpleNamespace(
            product={
                "material": {
                    "primary": "rattan",
                    "secondary": ["wood"],
                }
            },
            decision=None,
        )

        result = MaterialExpert().analyze(
            brain
        )

        self.assertIs(
            result,
            brain
        )

        self.assertEqual(
            brain.decision["material"],
            {
                "primary": "rattan",
                "secondary": ["wood"],
            }
        )


if __name__ == "__main__":
    unittest.main()