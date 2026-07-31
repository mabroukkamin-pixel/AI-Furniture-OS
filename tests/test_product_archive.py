import tempfile
import unittest
from pathlib import Path

from runtime.product_archive import (
    archive_product,
    restore_product,
)


class ProductArchiveTests(unittest.TestCase):

    def create_product_folder(
        self,
        products_directory,
        product_id="Archive001",
    ):
        product_directory = (
            products_directory / product_id
        )

        images_directory = (
            product_directory / "images"
        )

        images_directory.mkdir(
            parents=True
        )

        (
            product_directory / "identity.yaml"
        ).write_text(
            "product:\n"
            f"  id: {product_id}\n"
            "  name: Archive Product\n",
            encoding="utf-8"
        )

        (
            images_directory / "main.png"
        ).write_bytes(
            b"test image"
        )

        return product_directory

    def test_archives_complete_product_folder(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            root = Path(temporary_folder)
            products_directory = root / "products"
            archive_directory = root / "archive"

            products_directory.mkdir()

            product_directory = self.create_product_folder(
                products_directory
            )

            archived_directory = archive_product(
                products_directory,
                archive_directory,
                "Archive001",
            )

            self.assertFalse(
                product_directory.exists()
            )

            self.assertTrue(
                archived_directory.is_dir()
            )

            self.assertTrue(
                (
                    archived_directory
                    / "identity.yaml"
                ).is_file()
            )

            self.assertTrue(
                (
                    archived_directory
                    / "images"
                    / "main.png"
                ).is_file()
            )

            self.assertTrue(
                (
                    archived_directory
                    / ".archive.json"
                ).is_file()
            )

    def test_restores_archived_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            root = Path(temporary_folder)
            products_directory = root / "products"
            archive_directory = root / "archive"

            products_directory.mkdir()

            self.create_product_folder(
                products_directory
            )

            archived_directory = archive_product(
                products_directory,
                archive_directory,
                "Archive001",
            )

            restored_directory = restore_product(
                products_directory,
                archive_directory,
                archived_directory.name,
            )

            self.assertEqual(
                restored_directory,
                (
                    products_directory
                    / "Archive001"
                ).resolve()
            )

            self.assertTrue(
                restored_directory.is_dir()
            )

            self.assertFalse(
                archived_directory.exists()
            )

    def test_rejects_unknown_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            root = Path(temporary_folder)
            products_directory = root / "products"
            archive_directory = root / "archive"

            products_directory.mkdir()

            with self.assertRaises(
                FileNotFoundError
            ):
                archive_product(
                    products_directory,
                    archive_directory,
                    "Missing001",
                )


if __name__ == "__main__":
    unittest.main()