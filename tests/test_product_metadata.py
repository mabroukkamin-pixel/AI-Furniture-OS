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
        color=(90, 60, 30)
    ).save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()


class ProductMetadataTests(unittest.TestCase):

    def test_creates_bilingual_product_metadata(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            product_directory = create_product(
                Path(temporary_folder),
                product_id="Metadata001",
                name="طاولة تلفزيون",
                name_ar="طاولة تلفزيون",
                name_en="TV Cabinet",
                category="cabinet",
                material="wood",
                secondary_material="metal",
                color="dark_brown",
                width=120,
                height=50,
                depth=40,
                price=25,
                currency="KWD",
                image_data=make_image(),
            )

            loaded = ProductLoader(
                str(product_directory)
            ).load()

            product = loaded[
                "identity"
            ]["product"]

            self.assertEqual(
                product["name_ar"],
                "طاولة تلفزيون"
            )

            self.assertEqual(
                product["name_en"],
                "TV Cabinet"
            )

            self.assertEqual(
                product["material"]["secondary"],
                ["metal"]
            )

            self.assertEqual(
                product["colors"]["primary"],
                ["dark_brown"]
            )

    def test_updates_bilingual_product_metadata(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            products_directory = Path(
                temporary_folder
            )

            create_product(
                products_directory,
                product_id="Metadata002",
                name="Original",
                category="table",
                material="wood",
                width=100,
                height=70,
                depth=40,
                price=20,
                currency="KWD",
                image_data=make_image(),
            )

            product_directory = update_product(
                products_directory,
                product_id="Metadata002",
                name="طاولة جانبية",
                name_ar="طاولة جانبية",
                name_en="Side Table",
                category="table",
                material="wood",
                secondary_material="glass",
                color="beige",
                width=100,
                height=70,
                depth=40,
                price=22,
                currency="KWD",
                image_data=None,
            )

            loaded = ProductLoader(
                str(product_directory)
            ).load()

            product = loaded[
                "identity"
            ]["product"]

            self.assertEqual(
                product["name"],
                "طاولة جانبية"
            )

            self.assertEqual(
                product["name_en"],
                "Side Table"
            )

            self.assertEqual(
                product["material"]["secondary"],
                ["glass"]
            )

            self.assertEqual(
                product["colors"]["primary"],
                ["beige"]
            )


if __name__ == "__main__":
    unittest.main()