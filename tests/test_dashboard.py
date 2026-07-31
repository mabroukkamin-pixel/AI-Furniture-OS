import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from api.main import (
    OUTPUTS_DIR,
    app,
)


class DashboardTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_dashboard_page_loads(self):
        response = self.client.get(
            "/dashboard"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            "منصة إنتاج إعلانات الأثاث",
            response.text
        )

    def test_dashboard_static_files_load(self):
        style_response = self.client.get(
            "/static/styles.css"
        )

        script_response = self.client.get(
            "/static/app.js"
        )

        self.assertEqual(
            style_response.status_code,
            200
        )

        self.assertEqual(
            script_response.status_code,
            200
        )

        self.assertIn(
            "--gold",
            style_response.text
        )

        self.assertIn(
            "loadProducts",
            script_response.text
        )

        self.assertIn(
            "showReferenceImage",
            script_response.text
        )

        self.assertIn(
            "loadProductDetails",
            script_response.text
        )

    def test_products_endpoint_lists_partition(self):
        response = self.client.get(
            "/products"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        product_ids = {
            product["id"]
            for product in response.json()[
                "products"
            ]
        }

        product_names = {
            product["id"]: product["name"]
            for product in response.json()[
                "products"
            ]
        }

        self.assertIn(
            "Partition001",
            product_ids
        )

        self.assertEqual(
            product_names["Partition001"],
            "Rattan Partition"
        )

        self.assertNotIn(
            "_template",
            product_ids
        )
        self.assertNotIn(
            "_template_backup",
            product_ids
        )
        self.assertNotIn(
            "images",
            product_ids
        )

    def test_product_image_endpoint_returns_image(self):
        response = self.client.get(
            "/products/Partition001/image"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTrue(
            response.headers[
                "content-type"
            ].startswith("image/")
        )

        self.assertGreater(
            len(response.content),
            0
        )

    def test_product_details_endpoint(self):
        response = self.client.get(
            "/products/Partition001"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        product = response.json()

        self.assertEqual(
            product["name"],
            "Rattan Partition"
        )

        self.assertEqual(
            product["material"]["primary"],
            "rattan"
        )

        self.assertEqual(
            product["size"]["width"],
            200
        )

        self.assertEqual(
            product["pricing"]["price"],
            15
        )

        self.assertEqual(
            product["pricing"]["currency"],
            "KWD"
        )

    def test_invalid_product_id_is_rejected(self):
        response = self.client.post(
            "/generate",
            json={
                "product_id": "../Partition001"
            },
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_unknown_product_is_rejected(self):
        response = self.client.post(
            "/generate",
            json={
                "product_id":
                    "ProductThatDoesNotExist"
            },
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_output_artifact_is_served_safely(self):
        OUTPUTS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        with tempfile.TemporaryDirectory(
            prefix=".dashboard_artifact_",
            dir=OUTPUTS_DIR,
        ) as temporary_folder:
            output_directory = Path(
                temporary_folder
            )

            artifact_path = (
                output_directory / "sample.txt"
            )

            artifact_path.write_text(
                "artifact test",
                encoding="utf-8"
            )

            product_id = (
                output_directory.name
            )

            response = self.client.get(
                f"/outputs/{product_id}/sample.txt"
            )

            self.assertEqual(
                response.status_code,
                200
            )

            self.assertEqual(
                response.text,
                "artifact test"
            )


if __name__ == "__main__":
    unittest.main()