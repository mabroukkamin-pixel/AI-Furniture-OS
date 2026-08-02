class PromptExecutor:

    def __init__(self, writer):
        self.writer = writer

    def execute(self, state):

        return self.writer.write(state)
