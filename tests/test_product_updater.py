import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from PIL import Image

from brain.loaders.product_loader import ProductLoader
from runtime.product_creator import (
    create_product,
    update_product,
)


def make_test_image(color=(120, 80, 40)):
    buffer = BytesIO()

    Image.new(
        "RGB",
        (32, 32),
        color=color
    ).save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


class ProductUpdaterTests(unittest.TestCase):

    def test_updates_without_replacing_image(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            product_directory = create_product(
                products_directory,
                product_id="Editable001",
                name="Original Product",
                category="table",
                material="wood",
                width=120,
                height=80,
                depth=40,
                price=35,
                currency="KWD",
                image_data=make_test_image(),
            )

            image_path = (
                product_directory
                / "images"
                / "main.png"
            )

            original_image = image_path.read_bytes()

            update_product(
                products_directory,
                product_id="Editable001",
                name="Updated Product",
                category="console",
                material="metal",
                width=140,
                height=90,
                depth=None,
                price=45,
                currency="KWD",
                image_data=None,
            )

            loaded = ProductLoader(
                str(product_directory)
            ).load()

            product = loaded["identity"]["product"]

            self.assertEqual(
                product["name"],
                "Updated Product"
            )

            self.assertEqual(
                product["material"]["primary"],
                "metal"
            )

            self.assertEqual(
                product["size"],
                {
                    "width": 140.0,
                    "height": 90.0,
                }
            )

            self.assertEqual(
                loaded["pricing"]["pricing"]["price"],
                45.0
            )

            self.assertEqual(
                image_path.read_bytes(),
                original_image
            )

    def test_replaces_product_image(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            product_directory = create_product(
                products_directory,
                product_id="ReplaceImage001",
                name="Image Product",
                category="chair",
                material="wood",
                width=50,
                height=90,
                depth=50,
                price=20,
                currency="KWD",
                image_data=make_test_image(
                    (120, 80, 40)
                ),
            )

            image_path = (
                product_directory
                / "images"
                / "main.png"
            )

            original_image = image_path.read_bytes()

            update_product(
                products_directory,
                product_id="ReplaceImage001",
                name="Image Product",
                category="chair",
                material="wood",
                width=50,
                height=90,
                depth=50,
                price=20,
                currency="KWD",
                image_data=make_test_image(
                    (20, 100, 180)
                ),
            )

            self.assertNotEqual(
                image_path.read_bytes(),
                original_image
            )

            with Image.open(image_path) as image:
                self.assertEqual(
                    image.getpixel((0, 0)),
                    (20, 100, 180)
                )

    def test_rejects_unknown_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            with self.assertRaises(
                FileNotFoundError
            ):
                update_product(
                    Path(temporary_folder),
                    product_id="Missing001",
                    name="Missing Product",
                    category="chair",
                    material="wood",
                    width=50,
                    height=90,
                    depth=50,
                    price=20,
                    currency="KWD",
                    image_data=None,
                )


if __name__ == "__main__":
    unittest.main()