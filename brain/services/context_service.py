class ContextService:

    def __init__(self, brain):
        self.brain = brain

    def get(self, key, default=None):
        return self.brain.context.get(key, default)

    def set(self, key, value):
        self.brain.context[key] = value