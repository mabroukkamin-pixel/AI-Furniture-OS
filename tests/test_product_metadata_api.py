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
        color=(80, 60, 40)
    ).save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


class ProductMetadataApiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_creates_and_returns_extended_metadata(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            request = {
                "data": {
                    "product_id": "MetadataApi001",
                    "name": "طاولة تلفزيون",
                    "name_ar": "طاولة تلفزيون",
                    "name_en": "TV Cabinet",
                    "category": "cabinet",
                    "material": "wood",
                    "secondary_material": "metal",
                    "color": "dark_brown",
                    "width": "120",
                    "height": "50",
                    "depth": "40",
                    "price": "25",
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

            with patch(
                "api.main.PRODUCTS_DIR",
                products_directory,
            ):
                create_response = self.client.post(
                    "/products",
                    **request
                )

                details_response = self.client.get(
                    "/products/MetadataApi001"
                )

            self.assertEqual(
                create_response.status_code,
                201
            )

            self.assertEqual(
                details_response.status_code,
                200
            )

            details = details_response.json()

            self.assertEqual(
                details["name_ar"],
                "طاولة تلفزيون"
            )

            self.assertEqual(
                details["name_en"],
                "TV Cabinet"
            )

            self.assertEqual(
                details["material"]["secondary"],
                ["metal"]
            )

            self.assertEqual(
                details["colors"]["primary"],
                ["dark_brown"]
            )


if __name__ == "__main__":
    unittest.main()