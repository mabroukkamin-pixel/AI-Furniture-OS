class OutputExecutor:

    def __init__(self, output_manager):
        self.output_manager = output_manager

    def execute(self, product_id, state):

        self.output_manager.export(
            product_id,
            state
        )

        return state
