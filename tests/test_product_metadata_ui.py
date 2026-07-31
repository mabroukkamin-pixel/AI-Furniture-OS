import unittest

from fastapi.testclient import TestClient

from api.main import app


class ProductMetadataUiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_product_form_exposes_extended_metadata(self):
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
            "name_ar",
            "name_en",
            "secondary_material",
            "color",
        ):
            self.assertIn(
                f'name="{field_name}"',
                dashboard_response.text
            )

        self.assertIn(
            'formData.set(',
            script_response.text
        )

        self.assertIn(
            '"name_ar"',
            script_response.text
        )

        self.assertIn(
            'input[name="secondary_material"]',
            script_response.text
        )

        self.assertIn(
            'input[name="color"]',
            script_response.text
        )


if __name__ == "__main__":
    unittest.main()