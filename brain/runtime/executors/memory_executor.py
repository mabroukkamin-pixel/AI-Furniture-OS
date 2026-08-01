class MemoryExecutor:

    def __init__(self, fusion):
        self.fusion = fusion

    def execute(self, state):

        return self.fusion.apply(state)
