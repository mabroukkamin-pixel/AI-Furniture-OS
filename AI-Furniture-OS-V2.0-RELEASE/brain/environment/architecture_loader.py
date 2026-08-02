import yaml
import os


class ArchitectureBrain:

    def __init__(self, path):

        self.path = path

        self.data = self.load()


    def load(self):

        if not os.path.exists(self.path):
            return {}

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file)


    def analyze(self, material):

        materials = self.data.get(
            "materials",
            {}
        )

        info = materials.get(
            material,
            {}
        )

        return {

            "architecture":
                info.get(
                    "preferred_architecture",
                    []
                ),

            "walls":
                info.get(
                    "walls",
                    []
                ),

            "floors":
                info.get(
                    "floors",
                    []
                ),

            "avoid":
                info.get(
                    "avoid",
                    []
                )
        }