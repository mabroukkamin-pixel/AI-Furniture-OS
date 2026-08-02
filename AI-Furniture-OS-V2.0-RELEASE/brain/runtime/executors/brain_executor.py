class BrainExecutor:

    def __init__(self, brain):
        self.brain = brain

    def execute(self, state):

        return self.brain.run(state)
