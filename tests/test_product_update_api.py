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


class ProductUpdateApiTests(unittest.TestCase):

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

    def test_updates_existing_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            create_request = self.product_request()

            update_data = dict(
                create_request["data"]
            )

            update_data.pop("product_id")
            update_data["name"] = "Updated Product"
            update_data["material"] = "metal"
            update_data["price"] = "45"

            with patch(
                "api.main.PRODUCTS_DIR",
                products_directory,
            ):
                create_response = self.client.post(
                    "/products",
                    **create_request
                )

                update_response = self.client.put(
                    "/products/NewProduct001",
                    data=update_data,
                )

                details_response = self.client.get(
                    "/products/NewProduct001"
                )

            self.assertEqual(
                create_response.status_code,
                201
            )

            self.assertEqual(
                update_response.status_code,
                200
            )

            self.assertEqual(
                update_response.json()["status"],
                "updated"
            )

            details = details_response.json()

            self.assertEqual(
                details["name"],
                "Updated Product"
            )

            self.assertEqual(
                details["material"]["primary"],
                "metal"
            )

            self.assertEqual(
                details["pricing"]["price"],
                45.0
            )

    def test_rejects_unknown_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            update_data = dict(
                self.product_request()["data"]
            )

            update_data.pop("product_id")

            with patch(
                "api.main.PRODUCTS_DIR",
                Path(temporary_folder),
            ):
                response = self.client.put(
                    "/products/Missing001",
                    data=update_data,
                )

            self.assertEqual(
                response.status_code,
                404
            )


if __name__ == "__main__":
    unittest.main()