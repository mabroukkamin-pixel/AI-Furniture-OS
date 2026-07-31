import unittest

from fastapi.testclient import TestClient

from api.main import app


class ProductArchiveUiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_dashboard_exposes_recoverable_archiving(self):
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

        self.assertEqual(
            style_response.status_code,
            200
        )

        self.assertIn(
            'id="archiveProductButton"',
            dashboard_response.text
        )

        self.assertIn(
            'id="openArchiveDialog"',
            dashboard_response.text
        )

        self.assertIn(
            'id="archiveDialog"',
            dashboard_response.text
        )

        self.assertIn(
            'method: "DELETE"',
            script_response.text
        )

        self.assertIn(
            '"/product-archive"',
            script_response.text
        )

        self.assertIn(
            '"/restore"',
            script_response.text
        )

        self.assertIn(
            "window.confirm",
            script_response.text
        )

        self.assertIn(
            ".danger-button",
            style_response.text
        )

        self.assertIn(
            ".archive-item",
            style_response.text
        )


if __name__ == "__main__":
    unittest.main()