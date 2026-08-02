class OutputExecutor:

    def __init__(self, output_manager):
        self.output_manager = output_manager

    def execute(self, state):

        self.output_manager.export(
            state.product_id,
            state
        )

        return state