class LoadExecutor:

    def __init__(self, loader):
        self.loader = loader

    def execute(self, state):

        product = self.loader.load()

        state.product = product
        state.product_data = product

        state.branding = product.get(
            "branding",
            {}
        )

        return state