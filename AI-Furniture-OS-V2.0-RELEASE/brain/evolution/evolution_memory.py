import json
import os
from datetime import datetime


class EvolutionMemory:


    def save(self,data):

        os.makedirs(
            "docs/evolution",
            exist_ok=True
        )


        file = (
            "docs/evolution/evolution_"
            +
            datetime.now().strftime("%Y%m%d_%H%M%S")
            +
            ".json"
        )


        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )


        return file
