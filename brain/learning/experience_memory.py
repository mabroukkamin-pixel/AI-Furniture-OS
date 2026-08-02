class ExperienceMemory:


    def __init__(self):

        self.file = "brain/learning/data/experience_memory.json"


    def save(self, experience):

        import json
        import os


        data = {
            "experiences": []
        }


        if os.path.exists(self.file):

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)


        data["experiences"].append(
            experience
        )


        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )


        return True



    def load(self):

        import json


        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)
