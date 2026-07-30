from pathlib import Path
import yaml


class GraphLoader:


    def __init__(
        self,
        path="brain/knowledge_graph/graph.yaml"
    ):

        self.path = Path(path)



    def load(self):

        if not self.path.exists():

            return {}



        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            return yaml.safe_load(file) or {}