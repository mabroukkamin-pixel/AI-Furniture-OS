import json
from pathlib import Path


class MemoryStore:

    def __init__(self):

        self.memory_dir = Path(
            "brain/memory/database"
        )

        self.memory_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    def save(self, product_id, data):

        file_path = (
            self.memory_dir /
            f"{product_id}.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return file_path.as_posix()



    def load(self, product_id):

        file_path = (
            self.memory_dir /
            f"{product_id}.json"
        )

        if not file_path.exists():
            return None


        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)



    def list_all(self):

        memories = []


        for file in self.memory_dir.glob("*.json"):

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                memories.append(
                    json.load(f)
                )


        return memories