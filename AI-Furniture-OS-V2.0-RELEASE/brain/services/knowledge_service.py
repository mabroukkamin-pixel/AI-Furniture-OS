class KnowledgeService:

    def __init__(self, brain):
        self.brain = brain

    def get(self, key, default=None):
        return self.brain.knowledge.get(key, default)

    def set(self, key, value):
        self.brain.knowledge[key] = value

    def has(self, key):
        return key in self.brain.knowledge

    def clear(self):
        self.brain.knowledge.clear()