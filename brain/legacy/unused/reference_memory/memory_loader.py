from pathlib import Path
import yaml


class MemoryLoader:

    def __init__(
        self,
        path="brain/reference_memory/reference_database.yaml"
    ):

        self.path = Path(path)

    def load(self):

        if not self.path.exists():
            return {}

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            return {}

        return data.get(
            "references",
            data
        )