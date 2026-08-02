
import json
import os
from datetime import datetime


class ExperienceMemory:


    def __init__(self):

        self.path = "brain/learning/experience_memory.json"
        self.memory = []

        self.load()



    def load(self):

        if os.path.exists(self.path):

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as f:

                self.memory = json.load(f)



    def save(self):

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
                self.memory,
                f,
                indent=4,
                ensure_ascii=False
            )



    def store(self, state):

        record = {

            "time": str(datetime.now()),

            "product":
                getattr(
                    state.product,
                    "id",
                    None
                ),

            "decision":
                state.decision,

            "experience":
                state.experience

        }


        self.memory.append(record)

        self.save()

        return record
