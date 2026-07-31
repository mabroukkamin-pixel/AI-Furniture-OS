import unittest

from fastapi.testclient import TestClient

from api.main import app


class ProductUpdateUiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_dashboard_exposes_product_editing(self):
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

        self.assertIn(
            'id="editProductButton"',
            dashboard_response.text
        )

        self.assertIn(
            'id="productDialogMode"',
            dashboard_response.text
        )

        self.assertIn(
            'method = "PUT"',
            script_response.text
        )

        self.assertIn(
            "editingProductId",
            script_response.text
        )

        self.assertIn(
            "productImageInput.required = false",
            script_response.text
        )

        self.assertIn(
            "productImageInput.required = true",
            script_response.text
        )


if __name__ == "__main__":
    unittest.main()