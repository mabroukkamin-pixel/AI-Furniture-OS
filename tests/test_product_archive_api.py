import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app


class ProductArchiveApiTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def create_product_folder(
        self,
        products_directory,
        product_id="ArchiveApi001",
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
            "  name: Archived Product\n",
            encoding="utf-8"
        )

        (
            product_directory / "pricing.yaml"
        ).write_text(
            "pricing:\n"
            "  currency: KWD\n"
            "  price: 20\n",
            encoding="utf-8"
        )

        (
            images_directory / "main.png"
        ).write_bytes(
            b"test image"
        )

        return product_directory

    def test_archives_lists_and_restores_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            root = Path(temporary_folder)
            products_directory = root / "products"
            archive_directory = root / "archive"

            products_directory.mkdir()

            product_directory = self.create_product_folder(
                products_directory
            )

            with (
                patch(
                    "api.main.PRODUCTS_DIR",
                    products_directory,
                ),
                patch(
                    "api.main.PRODUCT_ARCHIVE_DIR",
                    archive_directory,
                    create=True,
                ),
            ):
                delete_response = self.client.delete(
                    "/products/ArchiveApi001"
                )

                was_removed_after_delete = (
                    not product_directory.exists()
                )

                archive_response = self.client.get(
                    "/product-archive"
                )

                archive_id = delete_response.json().get(
                    "archive_id",
                    ""
                )

                restore_response = self.client.post(
                    f"/product-archive/{archive_id}/restore"
                )

            self.assertEqual(
                delete_response.status_code,
                200
            )

            self.assertTrue(
                was_removed_after_delete
            )

            self.assertEqual(
                archive_response.status_code,
                200
            )

            archived_ids = {
                product["archive_id"]
                for product in archive_response.json()[
                    "products"
                ]
            }

            self.assertIn(
                archive_id,
                archived_ids
            )

            self.assertEqual(
                restore_response.status_code,
                200
            )

            self.assertEqual(
                restore_response.json()["status"],
                "restored"
            )

            self.assertTrue(
                product_directory.is_dir()
            )

    def test_delete_rejects_unknown_product(self):
        with tempfile.TemporaryDirectory() as temporary_folder:
            root = Path(temporary_folder)
            products_directory = root / "products"
            archive_directory = root / "archive"

            products_directory.mkdir()

            with (
                patch(
                    "api.main.PRODUCTS_DIR",
                    products_directory,
                ),
                patch(
                    "api.main.PRODUCT_ARCHIVE_DIR",
                    archive_directory,
                    create=True,
                ),
            ):
                response = self.client.delete(
                    "/products/Missing001"
                )

            self.assertEqual(
                response.status_code,
                404
            )


if __name__ == "__main__":
    unittest.main()