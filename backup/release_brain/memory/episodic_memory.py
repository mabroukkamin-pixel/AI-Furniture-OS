import json
import os


class EpisodicMemory:


    def __init__(self, path="memory/experiences.json"):

        self.path = path

        self._ensure()


    def _ensure(self):

        folder = os.path.dirname(self.path)

        if folder:
            os.makedirs(
                folder,
                exist_ok=True
            )

        if not os.path.exists(self.path):

            with open(
                self.path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=4
                )


    def remember(self, experience):

        data = self.load()

        data.append(
            experience.to_dict()
        )

        self.save(data)



    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def save(self, data):

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