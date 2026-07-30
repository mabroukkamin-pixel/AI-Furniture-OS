import yaml
from pathlib import Path


class ReferenceMetadata:

    def __init__(self, reference_path):
        self.path = Path(reference_path)

    def load(self):

        if not self.path.exists():
            return {}

        with open(self.path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)