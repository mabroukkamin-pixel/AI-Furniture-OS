import tempfile
import unittest
from pathlib import Path

from brain.vision.image_resolver import (
    ImageResolver,
)


class ImageResolverTests(unittest.TestCase):

    def test_main_png_has_priority(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            product_directory = Path(
                temporary_folder
            )

            images_directory = (
                product_directory / "images"
            )

            images_directory.mkdir()

            main_image = (
                images_directory / "main.png"
            )

            other_image = (
                images_directory / "000-first.png"
            )

            main_image.write_bytes(
                b"main"
            )

            other_image.write_bytes(
                b"other"
            )

            result = ImageResolver().find_product_image(
                str(product_directory)
            )

            self.assertEqual(
                Path(result["main_image"]).resolve(),
                main_image.resolve()
            )

            self.assertNotIn(
                result["main_image"],
                result["reference_images"]
            )

            self.assertIn(
                str(other_image),
                result["reference_images"]
            )


if __name__ == "__main__":
    unittest.main()