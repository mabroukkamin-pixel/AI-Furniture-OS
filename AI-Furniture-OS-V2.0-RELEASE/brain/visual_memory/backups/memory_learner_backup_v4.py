from pathlib import Path

from brain.visual_memory.embedding_engine import create_embedding
from brain.visual_memory.memory_index import MemoryIndex


class MemoryLearner:

    """
    Visual Memory Learning System V2
    Stores generated visual experiences
    """

    def __init__(self):

        self.index = MemoryIndex()


    def learn(self, image_path, metadata=None):

        image_path = Path(image_path)

        if not image_path.exists():
            return None


        embedding = create_embedding(
            image_path,
            metadata.get("brain_state")
            if metadata
            else None
        )


        memory = {

            "image": str(image_path),

            "embedding": embedding,

            "metadata": metadata or {}

        }


        self.index.add(memory)


        return memory



_learner = MemoryLearner()


def learn_visual_memory(image_path, metadata=None):

    return _learner.learn(
        image_path,
        metadata
    )