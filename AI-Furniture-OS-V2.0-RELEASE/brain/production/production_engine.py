class ProductionEngine:


    def __init__(
        self,
        client,
        output_manager
    ):

        self.client = client
        self.output_manager = output_manager



    def generate(
        self,
        product_id,
        image,
        prompt,
        context
    ):


        result = self.client.generate(
            image,
            prompt
        )


        folder = (
            self.output_manager.save_request(
                product_id,
                image,
                prompt
            )
        )


        self.output_manager.export(
            product_id,
            context
        )


        return {

            "product": product_id,

            "output": folder,

            "result": result

        }