import yaml
from pathlib import Path

from brain.reference_engine.reference_selector import ReferenceSelector


class BrainReferenceEngine:


    def __init__(self, database_path):

        self.path = Path(
            database_path
        )

        self.database = self.load()

        self.selector = ReferenceSelector(
            self.database
        )


    def load(self):

        if not self.path.exists():

            return {}

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            data = yaml.safe_load(file) or {}

        return data.get(
            "references",
            {}
        )


    def run(self, brain):

        product = (
            brain.product
            .get("product", {})
            .get("product", {})
        )


        selected = self.selector.select(
            product
        )


        brain.reference = (
            self.selector.extract(
                selected
            )
        )


        brain.log(
            "Reference",
            "Reference selection completed"
        )


        return brain