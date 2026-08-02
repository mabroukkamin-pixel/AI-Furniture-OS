from pathlib import Path
import json


class MemoryIndex:


    def __init__(self):

        self.memory_file = (
            Path(__file__).parent /
            "learned_memory.json"
        )

        self.index_file = (
            Path(__file__).parent /
            "index.json"
        )


    def build(self):

        if not self.memory_file.exists():
            return []


        memories = json.loads(
            self.memory_file.read_text(
                encoding="utf-8"
            )
        )


        index = []


        for i, memory in enumerate(memories):

            index.append({

                "id": i,

                "image": memory.get(
                    "image"
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
                )

            })


        self.index_file.write_text(

            json.dumps(
                index,
                indent=4,
                ensure_ascii=False
            ),

            encoding="utf-8"

        )


        print(
            "Visual Index Built:",
            len(index)
        )


        return index


    def load(self):

        if not self.index_file.exists():

            return self.build()


        return json.loads(

            self.index_file.read_text(
                encoding="utf-8"
            )

        )


    def calculate_similarity(
        self,
        query_embedding,
        memory_embedding
    ):

        query_visual = query_embedding.get(
            "visual",
            {}
        )

        memory_visual = memory_embedding.get(
            "visual",
            {}
        )


        score = 0


        weights = {

            "category": 20,

            "material": 25,

            "style": 25,

            "scene": 15,

            "design_style": 10

        }


        for field, weight in weights.items():

            if (
                query_visual.get(field)
                ==
                memory_visual.get(field)
            ):

                score += weight


        query_colors = set(
            query_visual.get(
                "colors",
                []
            )
        )


        memory_colors = set(
            memory_visual.get(
                "colors",
                []
            )
        )


        if query_colors & memory_colors:

            score += 5


        return score


    def search(
        self,
        embedding=None,
        top_k=3
    ):

        index = self.load()

        if embedding is None:
            return []

        if not index:
            return []


        results = []


        for item in index:

            print(
                "QUERY VISUAL:",
                embedding.get(
                    "visual",
                    {}
                )
            )


            print(
                "MEMORY VISUAL:",
                item.get(
                    "visual",
                    {}
                )
            )


            similarity = self.calculate_similarity(
                embedding,
                {
                    "visual": item.get(
                        "visual",
                        {}
                    )
                }
            )


            results.append({

                "image": item.get(
                    "image"
                ),

                "similarity": similarity,

                "visual": item.get(
                    "visual",
                    {}
                ),

                "metadata": item.get(
                    "metadata",
                    {}
                )

            })


        results.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )


        return results[:top_k]


    def add(self, memory):

        memories = []

        if self.memory_file.exists():

            memories = json.loads(
                self.memory_file.read_text(
                    encoding="utf-8"
                )
            )

        memories.append(memory)

        self.memory_file.write_text(

            json.dumps(
                memories,
                indent=4,
                ensure_ascii=False
            ),

            encoding="utf-8"
        )

        self.build()

        return memory