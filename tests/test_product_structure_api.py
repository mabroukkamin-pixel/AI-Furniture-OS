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
        color=(75, 55, 35)
    ).save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


class ProductStructureApiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_creates_and_updates_structure(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            create_data = {
                "product_id": "StructureApi001",
                "name": "Storage Cabinet",
                "category": "cabinet",
                "material": "wood",
                "width": "120",
                "height": "180",
                "depth": "40",
                "price": "50",
                "currency": "KWD",
                "doors": "4",
                "drawers": "2",
                "shelves": "5",
                "legs": "4",
                "handles": "6",
                "panels": "4",
            }

            update_data = dict(create_data)
            update_data.pop("product_id")
            update_data["doors"] = "2"
            update_data["drawers"] = "1"
            update_data["handles"] = "3"

            with patch(
                "api.main.PRODUCTS_DIR",
                products_directory,
            ):
                create_response = self.client.post(
                    "/products",
                    data=create_data,
                    files={
                        "image": (
                            "product.png",
                            make_image(),
                            "image/png",
                        )
                    },
                )

                update_response = self.client.put(
                    "/products/StructureApi001",
                    data=update_data,
                )

                details_response = self.client.get(
                    "/products/StructureApi001"
                )

            self.assertEqual(
                create_response.status_code,
                201
            )

            self.assertEqual(
                update_response.status_code,
                200
            )

            structure = details_response.json()[
                "structure"
            ]

            self.assertEqual(
                structure["doors"],
                2
            )

            self.assertEqual(
                structure["drawers"],
                1
            )

            self.assertEqual(
                structure["shelves"],
                5
            )

            self.assertEqual(
                structure["handles"],
                3
            )

            self.assertEqual(
                structure["panels"],
                4
            )


if __name__ == "__main__":
    unittest.main()