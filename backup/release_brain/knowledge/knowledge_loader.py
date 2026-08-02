import os
import yaml


class KnowledgeLoader:

    def __init__(self):

        self.base_path = os.path.dirname(__file__)
        self.cache = {}

    def load(self, name):

        if name in self.cache:
            return self.cache[name]

        path = os.path.join(
            self.base_path,
            f"{name}.yaml"
        )

        print("Loading knowledge file:")
        print(path)

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = yaml.safe_load(file)

        if name == "materials" and isinstance(data, dict):
            data = data.get("materials", data)

        self.cache[name] = data

        return data

    def materials(self):
        return self.load("materials")

    def styles(self):
        return self.load("styles")

    def environments(self):
        return self.load("environments")

    def lighting(self):
        return self.load("lighting")

    def photography(self):
        return self.load("photography")

    def composition(self):
        return self.load("composition")

    def marketing(self):
        return self.load("marketing")