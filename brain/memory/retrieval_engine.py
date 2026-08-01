from brain.memory.memory_store import MemoryStore
from brain.memory.visual_memory import VisualMemory



class RetrievalEngine:


    def __init__(self):

        self.store = MemoryStore()
        self.visual = VisualMemory()



    def retrieve(self, product):


        results = self.visual.find_similar(
            product
        )


        return results