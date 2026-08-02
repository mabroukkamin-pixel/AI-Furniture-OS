from brain.visual_memory.retriever import VisualMemoryRetriever
from brain.visual_memory.memory_recommender import MemoryRecommender


class VisualMemoryBrain:


    def __init__(self):

        self.retriever = VisualMemoryRetriever()

        self.recommender = MemoryRecommender()



    def analyze(
        self,
        image_path,
        metadata=None
    ):

        memories = self.retriever.retrieve(
            image_path,
            metadata
        )


        recommendation = self.recommender.recommend(
            memories
        )


        return {

            "similar_memories": memories,

            "recommendation": recommendation

        }