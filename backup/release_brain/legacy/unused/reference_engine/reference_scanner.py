import yaml
from pathlib import Path


class ReferenceScanner:

    def __init__(self, base_path):
        self.base_path = Path(base_path)

    def scan_folder(self, category_name, item_name):
        item_path = self.base_path / category_name / item_name
        meta_path = item_path / "meta.yaml"

        meta_data = {}
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                meta_data = yaml.safe_load(f) or {}

        # جمع مسارات الصور المتاحة
        image_extensions = {".png", ".jpg", ".jpeg", ".webp"}
        images = [
            str(p) for p in item_path.iterdir() if p.suffix.lower() in image_extensions
        ]

        return {
            "meta": meta_data,
            "images": images
        }