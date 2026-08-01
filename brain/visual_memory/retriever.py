from brain.visual_memory.memory_index import MemoryIndex
from brain.visual_memory.embedding_engine import create_embedding
from brain.visual_memory.similarity_engine import compare_visual_memory


class VisualMemoryRetriever:


    """
    Visual Memory Retrieval System V2
    """


    def __init__(self):

        self.index = MemoryIndex()



    def retrieve(
        self,
        image_path,
        metadata=None
    ):


        try:

            current_embedding = create_embedding(
                image_path,
                metadata or {}
            )

            print("==============================")
            print("CURRENT EMBEDDING")
            print(current_embedding)
            print("==============================")


            memories = self.index.load()

            print("==============================")
            if memories:
                print("FIRST MEMORY")
                print(memories[0])
            else:
                print("NO MEMORY FOUND")
            print("==============================")


            if not memories:

                return []


            results = compare_visual_memory(
                current_embedding,
                memories
            )


            return results



        except Exception as e:

            print(
                "Retriever Error:",
                e
            )

            return []