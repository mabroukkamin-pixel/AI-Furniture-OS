import yaml
from pathlib import Path


class BrandLoader:

    def __init__(self, branding_file):
        self.branding_file = Path(branding_file)

    def load(self):

        if not self.branding_file.exists():
            return {}

        with open(
            self.branding_file,
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file) or {}