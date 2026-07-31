import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from PIL import Image

from brain.loaders.product_loader import (
    ProductLoader,
)
from brain.vision.image_resolver import (
    ImageResolver,
)
from runtime.product_creator import (
    create_product,
)


def make_test_image():
    buffer = BytesIO()

    Image.new(
        "RGB",
        (32, 32),
        color=(120, 80, 40)
    ).save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


class ProductCreatorTests(unittest.TestCase):

    def test_creates_loadable_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            product_directory = create_product(
                products_directory,
                product_id="TestProduct001",
                name="Test Product",
                category="table",
                material="wood",
                width=120,
                height=80,
                depth=40,
                price=35,
                currency="KWD",
                image_data=make_test_image(),
            )

            loaded = ProductLoader(
                str(product_directory)
            ).load()

            self.assertEqual(
                loaded["identity"]["product"]["name"],
                "Test Product"
            )

            self.assertEqual(
                loaded["pricing"]["pricing"]["price"],
                35.0
            )

            images = ImageResolver().find_product_image(
                str(product_directory)
            )

            self.assertEqual(
                Path(images["main_image"]).name,
                "main.png"
            )

    def test_rejects_duplicate_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            arguments = {
                "product_id": "Duplicate001",
                "name": "Duplicate",
                "category": "chair",
                "material": "wood",
                "width": 50,
                "height": 90,
                "depth": 50,
                "price": 20,
                "currency": "KWD",
                "image_data": make_test_image(),
            }

            create_product(
                products_directory,
                **arguments
            )

            with self.assertRaises(
                FileExistsError
            ):
                create_product(
                    products_directory,
                    **arguments
                )

    def test_invalid_image_leaves_no_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            with self.assertRaises(Exception):
                create_product(
                    products_directory,
                    product_id="InvalidImage001",
                    name="Invalid Image",
                    category="chair",
                    material="wood",
                    width=50,
                    height=90,
                    depth=50,
                    price=20,
                    currency="KWD",
                    image_data=b"not an image",
                )

            self.assertFalse(
                (
                    products_directory
                    / "InvalidImage001"
                ).exists()
            )


if __name__ == "__main__":
    unittest.main()