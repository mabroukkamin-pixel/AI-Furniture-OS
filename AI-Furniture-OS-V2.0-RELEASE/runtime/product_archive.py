import json
import re
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from runtime.product_creator import (
    PRODUCT_ID_PATTERN,
)


ARCHIVE_ENTRY_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9_-]{1,127}$"
)


def _safe_child_directory(root, name):
    root = Path(root).resolve()
    candidate = (root / name).resolve()

    if candidate.parent != root:
        raise ValueError(
            "Invalid directory name"
        )

    return candidate


def _validate_product_id(product_id):
    product_id = product_id.strip()

    if (
        not PRODUCT_ID_PATTERN.fullmatch(product_id)
        or product_id.startswith((".", "_"))
    ):
        raise ValueError(
            "Invalid product ID"
        )

    return product_id


def archive_product(
    products_directory,
    archive_directory,
    product_id,
):
    product_id = _validate_product_id(
        product_id
    )

    products_directory = Path(
        products_directory
    ).resolve()

    archive_directory = Path(
        archive_directory
    ).resolve()

    product_directory = _safe_child_directory(
        products_directory,
        product_id
    )

    if not product_directory.is_dir():
        raise FileNotFoundError(
            f"Product not found: {product_id}"
        )

    archive_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    archived_at = datetime.now(
        timezone.utc
    ).replace(
        microsecond=0
    ).isoformat().replace(
        "+00:00",
        "Z"
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    archive_id = (
        f"{product_id}"
        f"--{timestamp}"
        f"--{uuid.uuid4().hex[:8]}"
    )

    archived_directory = _safe_child_directory(
        archive_directory,
        archive_id
    )

    shutil.move(
        str(product_directory),
        str(archived_directory)
    )

    try:
        metadata = {
            "archive_id": archive_id,
            "original_product_id": product_id,
            "archived_at": archived_at,
        }

        (
            archived_directory / ".archive.json"
        ).write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )
    except Exception:
        if archived_directory.exists():
            shutil.move(
                str(archived_directory),
                str(product_directory)
            )
        raise

    return archived_directory


def restore_product(
    products_directory,
    archive_directory,
    archive_id,
):
    archive_id = archive_id.strip()

    if not ARCHIVE_ENTRY_PATTERN.fullmatch(
        archive_id
    ):
        raise ValueError(
            "Invalid archive ID"
        )

    products_directory = Path(
        products_directory
    ).resolve()

    archive_directory = Path(
        archive_directory
    ).resolve()

    archived_directory = _safe_child_directory(
        archive_directory,
        archive_id
    )

    if not archived_directory.is_dir():
        raise FileNotFoundError(
            f"Archived product not found: {archive_id}"
        )

    metadata_path = (
        archived_directory / ".archive.json"
    )

    if not metadata_path.is_file():
        raise ValueError(
            "Archive metadata is missing"
        )

    metadata = json.loads(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )

    product_id = _validate_product_id(
        str(
            metadata.get(
                "original_product_id",
                ""
            )
        )
    )

    products_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    product_directory = _safe_child_directory(
        products_directory,
        product_id
    )

    if product_directory.exists():
        raise FileExistsError(
            f"Product already exists: {product_id}"
        )

    shutil.move(
        str(archived_directory),
        str(product_directory)
    )

    restored_metadata = (
        product_directory / ".archive.json"
    )

    if restored_metadata.exists():
        restored_metadata.unlink()

    return product_directory


def list_archived_products(
    archive_directory,
):
    archive_directory = Path(
        archive_directory
    ).resolve()

    if not archive_directory.is_dir():
        return []

    archived_products = []

    for archived_directory in sorted(
        archive_directory.iterdir(),
        key=lambda item: item.name.casefold(),
    ):
        if not archived_directory.is_dir():
            continue

        metadata_path = (
            archived_directory / ".archive.json"
        )

        if not metadata_path.is_file():
            continue

        try:
            metadata = json.loads(
                metadata_path.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            ValueError,
        ):
            continue

        if not isinstance(metadata, dict):
            continue

        archived_products.append(
            {
                "archive_id":
                    archived_directory.name,
                "product_id":
                    metadata.get(
                        "original_product_id"
                    ),
                "archived_at":
                    metadata.get(
                        "archived_at"
                    ),
            }
        )

    return archived_products