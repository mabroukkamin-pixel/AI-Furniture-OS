import os
import yaml


class ProductLoader:

    def __init__(self, product_path):
        self.product_path = product_path

    def _load_yaml(self, filename, required=True):

        path = os.path.join(
            self.product_path,
            filename
        )

        if not os.path.exists(path):

            if required:
                raise FileNotFoundError(path)

            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file) or {}

    def load(self):

        print("========================================")
        print("       PRODUCT LOADER")
        print("========================================")

        data = {

            "identity": self._load_yaml("identity.yaml"),

            "behavior": self._load_yaml("behavior.yaml"),

            "marketing": self._load_yaml("marketing.yaml"),

            "pricing": self._load_yaml("pricing.yaml"),

            "photography": self._load_yaml("photography.yaml"),

            "environment": self._load_yaml("environment.yaml"),

            "branding": self._load_yaml(
                "branding.yaml",
                required=False
            )

        }

        print(
            "Loaded Product:",
            data["identity"]["product"]["name"]
        )

        return data