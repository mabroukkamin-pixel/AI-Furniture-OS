from pathlib import Path

import yaml


IMAGE_EXTENSIONS = {
    ".jpeg",
    ".jpg",
    ".png",
    ".webp",
}


REFERENCE_CATEGORIES = {
    "materials",
    "products",
    "scenes",
    "styles",
}


class ReferenceLibraryLoader:

    def __init__(self, library_directory):
        self.library_directory = Path(
            library_directory
        )

    def load_item(
        self,
        category,
        name,
    ):
        if category not in REFERENCE_CATEGORIES:
            raise ValueError(
                "Unknown reference category"
            )

        item_directory = (
            self.library_directory
            / category
            / name
        )

        meta_path = (
            item_directory / "meta.yaml"
        )

        meta = yaml.safe_load(
            meta_path.read_text(
                encoding="utf-8"
            )
        ) or {}

        images = sorted(
            (
                path
                for path in item_directory.iterdir()
                if (
                    path.is_file()
                    and path.suffix.lower()
                    in IMAGE_EXTENSIONS
                )
            ),
            key=lambda path: path.name.lower(),
        )

        return {
            "category": category,
            "name": name,
            "meta": meta,
            "images": [
                str(path)
                for path in images
            ],
        }