import json
from pathlib import Path


MEMORY_FILE = Path(
    "brain/visual_memory/learned_memory.json"
)


class SemanticSearch:

    def __init__(self):
        self.memory = self.load_memory()


    def load_memory(self):

        if not MEMORY_FILE.exists():
            return []

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)


    def search(
        self,
        product_type=None,
        style=None
    ):

        results = []

        for item in self.memory:

            metadata = item.get(
                "metadata",
                {}
            )

            score = 0


            if product_type:

                if metadata.get(
                    "category"
                ) == product_type:
                    score += 10


            if style:

                if metadata.get(
                    "style"
                ) == style:
                    score += 10


            if score > 0:

                results.append(
                    {
                        "score": score,
                        "image": item.get(
                            "image"
                        ),
                        "metadata": metadata
                    }
                )


        results.sort(
            key=lambda x:x["score"],
            reverse=True
        )


        return results



if __name__ == "__main__":

    engine = SemanticSearch()


    result = engine.search(
        product_type="partition",
        style="gulf_villa"
    )


    print("==============================")
    print("SEMANTIC SEARCH")
    print("==============================")

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )