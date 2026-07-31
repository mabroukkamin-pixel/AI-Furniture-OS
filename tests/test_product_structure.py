import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from PIL import Image

from brain.loaders.product_loader import (
    ProductLoader,
)
from runtime.product_creator import (
    create_product,
    update_product,
)


def make_image():
    buffer = BytesIO()

    Image.new(
        "RGB",
        (32, 32),
        color=(70, 50, 30)
    ).save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


class ProductStructureTests(unittest.TestCase):

    def test_creates_product_structure(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            product_directory = create_product(
                Path(temporary_folder),
                product_id="Structure001",
                name="Storage Cabinet",
                category="cabinet",
                material="wood",
                width=120,
                height=180,
                depth=40,
                price=50,
                currency="KWD",
                image_data=make_image(),
                doors=4,
                drawers=2,
                shelves=5,
                legs=4,
                handles=6,
                panels=4,
            )

            loaded = ProductLoader(
                str(product_directory)
            ).load()

            self.assertEqual(
                loaded["identity"]["product"]["structure"],
                {
                    "doors": 4,
                    "drawers": 2,
                    "shelves": 5,
                    "legs": 4,
                    "handles": 6,
                    "panels": 4,
                }
            )

    def test_updates_product_structure(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            create_product(
                products_directory,
                product_id="Structure002",
                name="Console",
                category="console",
                material="wood",
                width=120,
                height=82,
                depth=35,
                price=35,
                currency="KWD",
                image_data=make_image(),
            )

            product_directory = update_product(
                products_directory,
                product_id="Structure002",
                name="Console",
                category="console",
                material="wood",
                width=120,
                height=82,
                depth=35,
                price=35,
                currency="KWD",
                image_data=None,
                doors=2,
                drawers=1,
                shelves=1,
                legs=4,
                handles=3,
                panels=0,
            )

            loaded = ProductLoader(
                str(product_directory)
            ).load()

            structure = loaded[
                "identity"
            ]["product"]["structure"]

            self.assertEqual(
                structure["doors"],
                2
            )

            self.assertEqual(
                structure["handles"],
                3
            )

            self.assertEqual(
                structure["panels"],
                0
            )

    def test_rejects_negative_structure_count(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            with self.assertRaises(
                ValueError
            ):
                create_product(
                    Path(temporary_folder),
                    product_id="Structure003",
                    name="Invalid Cabinet",
                    category="cabinet",
                    material="wood",
                    width=120,
                    height=180,
                    depth=40,
                    price=50,
                    currency="KWD",
                    image_data=make_image(),
                    doors=-1,
                )


if __name__ == "__main__":
    unittest.main()