import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from PIL import Image

from api.main import app


def make_image():
    buffer = BytesIO()

    Image.new(
        "RGB",
        (32, 32),
        color=(110, 70, 30)
    ).save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


class ProductApiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def product_request(self):
        return {
            "data": {
                "product_id": "NewProduct001",
                "name": "New Product",
                "category": "table",
                "material": "wood",
                "width": "120",
                "height": "80",
                "depth": "40",
                "price": "35",
                "currency": "KWD",
            },
            "files": {
                "image": (
                    "product.png",
                    make_image(),
                    "image/png",
                )
            },
        }

    def test_creates_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            with patch(
                "api.main.PRODUCTS_DIR",
                products_directory,
            ):
                response = self.client.post(
                    "/products",
                    **self.product_request()
                )

            self.assertEqual(
                response.status_code,
                201
            )

            self.assertEqual(
                response.json()["status"],
                "created"
            )

            self.assertTrue(
                (
                    products_directory
                    / "NewProduct001"
                    / "images"
                    / "main.png"
                ).is_file()
            )

    def test_rejects_duplicate_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            with patch(
                "api.main.PRODUCTS_DIR",
                products_directory,
            ):
                first_response = self.client.post(
                    "/products",
                    **self.product_request()
                )

                second_response = self.client.post(
                    "/products",
                    **self.product_request()
                )

            self.assertEqual(
                first_response.status_code,
                201
            )

            self.assertEqual(
                second_response.status_code,
                409
            )

    def test_rejects_corrupt_image(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            request = self.product_request()

            request["files"]["image"] = (
                "corrupt.png",
                b"not a real image",
                "image/png",
            )

            with patch(
                "api.main.PRODUCTS_DIR",
                products_directory,
            ):
                response = self.client.post(
                    "/products",
                    **request
                )

            self.assertEqual(
                response.status_code,
                400
            )

            self.assertFalse(
                (
                    products_directory
                    / "NewProduct001"
                ).exists()
            )

    def test_rejects_oversized_image(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            request = self.product_request()

            request["files"]["image"] = (
                "large.png",
                b"12345",
                "image/png",
            )

            with (
                patch(
                    "api.main.PRODUCTS_DIR",
                    products_directory,
                ),
                patch(
                    "api.main.MAX_PRODUCT_IMAGE_BYTES",
                    4,
                ),
            ):
                response = self.client.post(
                    "/products",
                    **request
                )

            self.assertEqual(
                response.status_code,
                413
            )

            self.assertFalse(
                (
                    products_directory
                    / "NewProduct001"
                ).exists()
            )


if __name__ == "__main__":
    unittest.main()