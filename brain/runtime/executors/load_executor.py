class LoadExecutor:

    def __init__(self, loader):
        self.loader = loader

    def execute(self, state, product_id):

        product = self.loader.load()

        state.product = product
        state.product_data = product
        state.product_id = product_id

        state.branding = product.get(
            "branding",
            {}
        )

        return state