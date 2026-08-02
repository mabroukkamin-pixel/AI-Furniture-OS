import os
import json
import datetime


class ExperienceCollector:


    def __init__(self):

        self.file = "brain/learning/experience_memory.json"

        os.makedirs(
            "brain/learning",
            exist_ok=True
        )


        if not os.path.exists(self.file):

            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=4
                )


    def add_experience(self, data):

        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as f:

            memory = json.load(f)


        data["date"] = str(
            datetime.datetime.now()
        )


        memory.append(data)


        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                memory,
                f,
                indent=4,
                ensure_ascii=False
            )


        return data


if __name__ == "__main__":

    collector = ExperienceCollector()

    print(
        collector.add_experience(
            {
                "product":"Partition001",
                "material":"rattan",
                "style":"gulf_villa",
                "score":95,
                "success":True
            }
        )
    )

