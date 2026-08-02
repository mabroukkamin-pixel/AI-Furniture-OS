import os
import json

from brain.visual_memory.embedding_engine import create_embedding

LIBRARY = os.path.join(
    os.path.dirname(__file__),
    "library"
)

INDEX_FILE = os.path.join(
    os.path.dirname(__file__),
    "index.json"
)


def build_index():

    database = []

    if not os.path.exists(LIBRARY):
        print("Library not found.")
        return

    for root, _, files in os.walk(LIBRARY):

        for file in files:

            if not file.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            ):
                continue

            path = os.path.join(root, file)

            database.append(
                {
                    "image": path,
                    "embedding": create_embedding(path)
                }
            )

    with open(
        INDEX_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            database,
            f,
            indent=4
        )

    print("=" * 40)
    print("VISUAL MEMORY INDEX")
    print("=" * 40)
    print("Images Indexed:", len(database))
    print("Saved:", INDEX_FILE)


if __name__ == "__main__":
    build_index()