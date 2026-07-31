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
        color=(65, 45, 30)
    ).save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


class ProductPreservationRuleTests(unittest.TestCase):

    def test_creates_custom_preservation_rules(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            product_directory = create_product(
                Path(temporary_folder),
                product_id="Preserve001",
                name="Shoe Cabinet",
                category="cabinet",
                material="wood",
                width=120,
                height=90,
                depth=40,
                price=50,
                currency="KWD",
                image_data=make_image(),
                preserve_rules=(
                    "four doors, black handles,\n"
                    "dark brown color"
                ),
                forbidden_changes=(
                    "add legs, remove shelves,\n"
                    "change wood color"
                ),
            )

            loaded = ProductLoader(
                str(product_directory)
            ).load()

            behavior = loaded[
                "behavior"
            ]["behavior"]

            self.assertEqual(
                behavior["preserve"],
                [
                    "four doors",
                    "black handles",
                    "dark brown color",
                ]
            )

            self.assertEqual(
                behavior["avoid"],
                [
                    "add legs",
                    "remove shelves",
                    "change wood color",
                ]
            )

    def test_updates_custom_preservation_rules(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            create_product(
                products_directory,
                product_id="Preserve002",
                name="Partition",
                category="partition",
                material="rattan",
                width=200,
                height=180,
                depth=None,
                price=15,
                currency="KWD",
                image_data=make_image(),
            )

            product_directory = update_product(
                products_directory,
                product_id="Preserve002",
                name="Partition",
                category="partition",
                material="rattan",
                width=200,
                height=180,
                depth=None,
                price=15,
                currency="KWD",
                image_data=None,
                preserve_rules=(
                    "four panels, rattan weave, brown color"
                ),
                forbidden_changes=(
                    "add panel, remove panel, recolor"
                ),
            )

            loaded = ProductLoader(
                str(product_directory)
            ).load()

            behavior = loaded[
                "behavior"
            ]["behavior"]

            self.assertEqual(
                behavior["preserve"],
                [
                    "four panels",
                    "rattan weave",
                    "brown color",
                ]
            )

            self.assertEqual(
                behavior["avoid"],
                [
                    "add panel",
                    "remove panel",
                    "recolor",
                ]
            )


if __name__ == "__main__":
    unittest.main()