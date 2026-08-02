from brain.visual_memory.memory_index import MemoryIndex
from brain.visual_memory.embedding_engine import EmbeddingEngine


class VisualMemoryRetriever:

    def __init__(self):

        self.index = MemoryIndex()
        self.embedding = EmbeddingEngine()

    def retrieve(self, image_path, top_k=5):

        embedding = self.embedding.generate(image_path)

        return self.index.search(
            embedding,
            top_k=top_k
        )