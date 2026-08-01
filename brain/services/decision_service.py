class DecisionService:

    def __init__(self, brain):
        self.brain = brain

    def get(self, key, default=None):
        return self.brain.decision.get(key, default)

    def set(self, key, value):
        self.brain.decision[key] = value

    def update(self, values):
        self.brain.decision.update(values)

    def clear(self):
        self.brain.decision.clear()