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
        color=(60, 45, 30)
    ).save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


class ProductPreservationApiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_creates_and_updates_preservation_rules(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            create_data = {
                "product_id": "PreserveApi001",
                "name": "Partition",
                "category": "partition",
                "material": "rattan",
                "width": "200",
                "height": "180",
                "price": "15",
                "currency": "KWD",
                "preserve_rules": (
                    "four panels, rattan weave, brown color"
                ),
                "forbidden_changes": (
                    "add panel, remove panel, recolor"
                ),
            }

            update_data = dict(create_data)
            update_data.pop("product_id")
            update_data["preserve_rules"] = (
                "four panels, original weave"
            )
            update_data["forbidden_changes"] = (
                "change panel count, change color"
            )

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
                    "/products/PreserveApi001",
                    data=update_data,
                )

                details_response = self.client.get(
                    "/products/PreserveApi001"
                )

            self.assertEqual(
                create_response.status_code,
                201
            )

            self.assertEqual(
                update_response.status_code,
                200
            )

            preservation = details_response.json()[
                "preservation"
            ]

            self.assertEqual(
                preservation["preserve"],
                [
                    "four panels",
                    "original weave",
                ]
            )

            self.assertEqual(
                preservation["avoid"],
                [
                    "change panel count",
                    "change color",
                ]
            )


if __name__ == "__main__":
    unittest.main()