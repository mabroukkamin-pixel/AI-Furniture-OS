import json
from pathlib import Path

from brain.visual_memory.identity import MemoryIdentity


class MemoryMigrator:


    def __init__(self):

        self.identity = MemoryIdentity()



    def migrate(
        self,
        source,
        output
    ):

        source = Path(source)
        output = Path(output)


        with open(
            source,
            "r",
            encoding="utf-8"
        ) as file:

            memories = json.load(file)



        migrated = []


        for memory in memories:


            image = memory.get(
                "image"
            )


            memory_id = self.identity.generate_id(
                image
            )


            new_memory = {

                "memory_id": memory_id,

                "created_at": None,

                "image": image,

                "product": memory.get(
                    "metadata",
                    {}
                ).get(
                    "product",
                    {}
                ),

                "visual": memory.get(
                    "embedding",
                    {}
                ).get(
                    "visual",
                    {}
                ),

                "metadata": memory.get(
                    "metadata",
                    {}
                ),

                "performance": {

                    "score": 0,

                    "used_count": 0,

                    "success_rate": 0
                },

                "embedding": memory.get(
                    "embedding",
                    {}
                )

            }


            migrated.append(
                new_memory
            )



        with open(
            output,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                migrated,
                file,
                indent=4,
                ensure_ascii=False
            )


        return len(migrated)



if __name__ == "__main__":


    migrator = MemoryMigrator()


    count = migrator.migrate(

        "brain/visual_memory/learned_memory.json",

        "brain/visual_memory/learned_memory_v4.json"

    )


    print(
        f"Migrated memories: {count}"
    )