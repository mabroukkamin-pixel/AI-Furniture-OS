from pathlib import Path
import yaml


class MarketingEngine:

    def __init__(self, rules_path):

        self.path = Path(rules_path)
        self.rules = self.load()


    def load(self):

        if not self.path.exists():
            return {}

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file) or {}


    def generate(self, category):

        data = self.rules.get(
            category,
            {}
        )

        return {

            "audience":
                data.get(
                    "audience",
                    []
                ),

            "emotion":
                data.get(
                    "emotion",
                    []
                ),

            "selling_points":
                data.get(
                    "selling_points",
                    []
                )
        }