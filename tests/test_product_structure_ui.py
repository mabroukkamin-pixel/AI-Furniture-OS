import unittest

from fastapi.testclient import TestClient

from api.main import app


class ProductStructureUiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_product_form_exposes_structure_fields(self):
        dashboard_response = self.client.get(
            "/dashboard"
        )

        script_response = self.client.get(
            "/static/app.js"
        )

        self.assertEqual(
            dashboard_response.status_code,
            200
        )

        self.assertEqual(
            script_response.status_code,
            200
        )

        for field_name in (
            "doors",
            "drawers",
            "shelves",
            "legs",
            "handles",
            "panels",
        ):
            self.assertIn(
                f'name="{field_name}"',
                dashboard_response.text
            )

            self.assertIn(
                f'"{field_name}"',
                script_response.text
            )

        self.assertIn(
            "body.structure",
            script_response.text
        )

        self.assertIn(
            "structure[fieldName] ?? 0",
            script_response.text
        )


if __name__ == "__main__":
    unittest.main()