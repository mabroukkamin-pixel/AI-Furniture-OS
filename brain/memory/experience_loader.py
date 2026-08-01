from brain.memory.experience_memory import ExperienceMemory
from brain.memory.experience_ranker import ExperienceRanker


class ExperienceLoader:

    def __init__(self):

        self.memory = ExperienceMemory()

        self.ranker = ExperienceRanker()