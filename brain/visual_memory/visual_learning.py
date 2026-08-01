from pathlib import Path
import json

from brain.visual_memory.embedding_engine import create_embedding
from brain.visual_memory.memory_index import MemoryIndex


class VisualLearning:

    """
    Visual Learning Engine V2

    Converts generated images into
    permanent visual memory.
    """

    def __init__(self):

        self.memory_file = (
            Path(__file__).parent /
            "learned_memory.json"
        )

        self.index = MemoryIndex()

        if not self.memory_file.exists():

            self.memory_file.write_text(
                "[]",
                encoding="utf-8"
            )

    def clean_metadata(self, metadata):

        """
        Convert Brain objects into
        JSON safe knowledge.
        """

        if not metadata:
            return {}

        product = metadata.get(
            "product",
            {}
        )

        if isinstance(product, str):
            product = {
                "id": product
            }

        decision = metadata.get(
            "decision",
            {}
        )

        design = metadata.get(
            "design_dna",
            {}
        )

        return {

            "product": {

                "id": product.get(
                    "id"
                ),

                "name": product.get(
                    "name"
                ),

                "category": product.get(
                    "category"
                ),

                "material": product.get(
                    "material"
                ),

                "style": product.get(
                    "style"
                )

            },

            "decision": {

                "selected_style": decision.get(
                    "selected_style"
                ),

                "score": decision.get(
                    "score"
                )

            },

            "design_dna": design

        }

    def learn(
        self,
        image_path,
        metadata=None
    ):

        if metadata is None:
            metadata = {}

        safe_metadata = self.clean_metadata(
            metadata
        )

        print("==============================")
        print("VISUAL MEMORY METADATA")
        print("==============================")
        print(
            safe_metadata
        )

        embedding = create_embedding(
            image_path,
            metadata
        )

        print("==============================")
        print("CREATED EMBEDDING")
        print("==============================")
        print(
            embedding
        )

        data = json.loads(
            self.memory_file.read_text(
                encoding="utf-8"
            )
        )


        for item in data:

            if item.get("image") == str(image_path):

                print(
                    "Memory already exists:",
                    image_path
                )

                return item


        memory_record = {

            "image": str(image_path),

            "embedding": embedding,

            "metadata": safe_metadata

        }


        data.append(
            memory_record
        )

        self.memory_file.write_text(

            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            ),

            encoding="utf-8"

        )

        print(
            "Visual Memory Learned:",
            image_path
        )

        self.index.build()

        return memory_record