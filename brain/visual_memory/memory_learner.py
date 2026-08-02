from pathlib import Path

from brain.visual_memory.embedding_engine import create_embedding
from brain.visual_memory.memory_index import MemoryIndex

from brain.visual_memory.memory_schema import MemorySchema
from brain.visual_memory.identity import MemoryIdentity
from brain.visual_memory.deduplicator import MemoryDeduplicator
from brain.visual_memory.config import ACTIVE_MEMORY


class MemoryLearner:

    """
    Visual Memory Learning System V4

    Adds:
    - Memory Identity
    - Duplicate Protection
    - Structured Memory Schema
    """

    def __init__(self):

        self.index = MemoryIndex()

        self.schema = MemorySchema()

        self.identity = MemoryIdentity()

        self.deduplicator = MemoryDeduplicator(
            ACTIVE_MEMORY
        )

    def learn(self, image_path, metadata=None):

        image_path = Path(image_path)

        if not image_path.exists():
            return None

        memory_id = self.identity.generate_id(
            str(image_path)
        )

        if self.deduplicator.exists(memory_id):

            return {
                "status": "duplicate",
                "memory_id": memory_id
            }

        embedding = create_embedding(
            image_path,
            metadata.get("brain_state")
            if metadata
            else None
        )

        memory = self.schema.create(

            image_path=str(image_path),

            product=(
                metadata.get("product")
                if metadata
                else {}
            ),

            visual=embedding.get(
                "visual",
                {}
            ),

            metadata=metadata or {},

            score=(
                metadata.get("decision", {})
                .get("score", 0)
                if metadata
                else 0
            )

        )

        memory["embedding"] = embedding

        self.index.add(memory)

        return memory


_learner = MemoryLearner()


def learn_visual_memory(image_path, metadata=None):

    return _learner.learn(
        image_path,
        metadata
    )