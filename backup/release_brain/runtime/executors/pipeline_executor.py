class PipelineExecutor:

    def __init__(self, executors):

        self.executors = executors

    def execute(self, state):

        for executor in self.executors:

            state = executor.execute(state)

        return state
