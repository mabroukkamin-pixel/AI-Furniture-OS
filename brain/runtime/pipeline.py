class BrainPipeline:

    def __init__(self):

        self.steps = []

    def add(self, step):

        self.steps.append(step)

    def __iter__(self):

        return iter(self.steps)