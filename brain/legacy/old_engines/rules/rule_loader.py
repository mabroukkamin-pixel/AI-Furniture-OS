import os
import yaml

class RuleLoader:
    """
    Loads rule cards from a given directory.
    """
    def __init__(self, rules_dir: str):
        self.rules_dir = rules_dir

    def load(self) -> list:
        rules = []
        if not os.path.exists(self.rules_dir):
            return rules

        for file_name in os.listdir(self.rules_dir):
            if file_name.endswith(".yaml") or file_name.endswith(".yml"):
                file_path = os.path.join(self.rules_dir, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data:
                        rules.append(data)
        
        return rules