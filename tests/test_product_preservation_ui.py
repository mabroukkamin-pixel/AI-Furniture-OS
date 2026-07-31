import unittest

from fastapi.testclient import TestClient

from api.main import app


class ProductPreservationUiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_product_form_exposes_preservation_rules(self):
        dashboard_response = self.client.get(
            "/dashboard"
        )

        script_response = self.client.get(
            "/static/app.js"
        )

        style_response = self.client.get(
            "/static/styles.css"
        )

        self.assertEqual(
            dashboard_response.status_code,
            200
        )

        self.assertEqual(
            script_response.status_code,
            200
        )

        self.assertIn(
            'name="preserve_rules"',
            dashboard_response.text
        )

        self.assertIn(
            'name="forbidden_changes"',
            dashboard_response.text
        )

        self.assertIn(
            "body.preservation",
            script_response.text
        )

        self.assertIn(
            "preservation.preserve",
            script_response.text
        )

        self.assertIn(
            "preservation.avoid",
            script_response.text
        )

        self.assertIn(
            ".product-form-grid textarea",
            style_response.text
        )


if __name__ == "__main__":
    unittest.main()