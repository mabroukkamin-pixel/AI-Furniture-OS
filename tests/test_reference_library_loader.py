import tempfile
import unittest
from pathlib import Path

from brain.loaders.reference_library_loader import (
    ReferenceLibraryLoader,
)


class ReferenceLibraryLoaderTests(unittest.TestCase):

    def test_loads_metadata_and_sorted_images(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            library_directory = Path(
                temporary_folder
            )
            item_directory = (
                library_directory
                / "materials"
                / "wood"
            )
            item_directory.mkdir(
                parents=True
            )

            (
                item_directory / "meta.yaml"
            ).write_text(
                "material_name: wood\n"
                "finish: natural_oak\n",
                encoding="utf-8"
            )

            (
                item_directory / "b.png"
            ).write_bytes(b"png")

            (
                item_directory / "a.jpg"
            ).write_bytes(b"jpg")

            (
                item_directory / "notes.txt"
            ).write_text(
                "ignore me",
                encoding="utf-8"
            )

            loaded = ReferenceLibraryLoader(
                library_directory
            ).load_item(
                "materials",
                "wood",
            )

            self.assertEqual(
                loaded["category"],
                "materials"
            )

            self.assertEqual(
                loaded["name"],
                "wood"
            )

            self.assertEqual(
                loaded["meta"],
                {
                    "material_name": "wood",
                    "finish": "natural_oak",
                }
            )

            self.assertEqual(
                loaded["images"],
                [
                    str(item_directory / "a.jpg"),
                    str(item_directory / "b.png"),
                ]
            )

    def test_rejects_unknown_category(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            loader = ReferenceLibraryLoader(
                Path(temporary_folder)
            )

            with self.assertRaisesRegex(
                ValueError,
                "Unknown reference category",
            ):
                loader.load_item(
                    "unknown",
                    "wood",
                )


if __name__ == "__main__":
    unittest.main()