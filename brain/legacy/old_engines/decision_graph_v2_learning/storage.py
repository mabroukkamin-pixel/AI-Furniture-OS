import json
import os
from pathlib import Path


class DecisionGraphStorage:

    def __init__(self):

        self.path = (
            str(Path(__file__).with_name("decision_graph_memory.json"))
        )


    def load(self):

        if not os.path.exists(self.path):

            return {}


        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def save(self, data):

        os.makedirs(
            os.path.dirname(self.path),
            exist_ok=True
        )


        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )
