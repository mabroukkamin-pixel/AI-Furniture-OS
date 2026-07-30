import yaml
from pathlib import Path


class ProductLoader:

    def __init__(self, product_dir):
        # نقوم بتعريف المسار كـمجلد وليس ملفاً مفرداً
        self.dir_path = Path(product_dir)

    def _load_yaml(self, filename):
        file_path = self.dir_path / filename
        if not file_path.exists():
            return {}
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def load(self):
        if not self.dir_path.exists():
            return {}

        # تجميع كافة ملفات الـ YAML الخاصة بالمنتج في قاموس واحد شامل
        data = {
            "product": self._load_yaml("product.yaml"),
            "identity": self._load_yaml("identity.yaml"),
            "behavior": self._load_yaml("behavior.yaml"),
            "marketing": self._load_yaml("marketing.yaml"),
            "pricing": self._load_yaml("pricing.yaml"),
            "photography": self._load_yaml("photography.yaml"),
            "environment": self._load_yaml("environment.yaml"),
            "branding": self._load_yaml("branding.yaml"),
        }
        
        return data