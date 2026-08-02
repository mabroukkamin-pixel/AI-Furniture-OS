import yaml
from pathlib import Path


class RuleEngine:

    def __init__(self, rules_path):

        self.path = Path(rules_path)
        self.rules = self.load_rules()

    def load_rules(self):

        if not self.path.exists():
            return {}

        with open(self.path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def evaluate(self, materials):

        result = {}

        rules = self.rules.get("rules", {})

        for material in materials:

            if material in rules:

                rule = rules[material]

                for key, value in rule.items():

                    if key not in result:
                        result[key] = []

                    result[key].extend(value)

        return result