from pathlib import Path

from .image_index import ImageIndex
from .reference_models import ReferenceImage


SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}


class ReferenceLoader:

    def __init__(self, reference_root: Path):

        self.reference_root = Path(reference_root)

    def load(self):

        index = ImageIndex()

        if not self.reference_root.exists():
            return index

        for product_folder in self.reference_root.iterdir():

            if not product_folder.is_dir():
                continue

            product_type = product_folder.name

            for image_path in product_folder.iterdir():

                if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue

                image = ReferenceImage(
                    filename=image_path.name,
                    path=image_path,
                    product_type=product_type,
                )

                index.add(image)

        return index