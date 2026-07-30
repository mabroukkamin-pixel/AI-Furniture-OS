import yaml
from pathlib import Path


class KnowledgeLoader:


    def __init__(self, file):

        self.file = Path(file)



    def load(self):

        if not self.file.exists():
            return {}

        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as f:

            return yaml.safe_load(f) or {}