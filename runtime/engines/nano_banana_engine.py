from runtime.engines.base_engine import BaseEngine
from runtime.generation.generation_router import (
    GenerationRouter,
)


class NanoBananaEngine(BaseEngine):

    def __init__(self, state=None):
        super().__init__(state)

        self.generator = GenerationRouter()

    def generate(self, request):

        product = request.get(
            "product_id"
        )

        output_folder = request.get(
            "output_folder"
        )

        print()
        print("=" * 30)
        print("NANO BANANA ENGINE")
        print("=" * 30)

        response = self.generator.generate(
            request
        )

        if self.state:

            self.state.generation_status = (
                response.get(
                    "status",
                    ""
                )
            )

            self.state.generation_error = (
                response.get(
                    "error",
                    {}
                )
            )

        print(
            "Product:",
            product
        )

        print(
            "Output:",
            output_folder
        )

        return {

            "status": response.get(
                "status",
                "error"
            ),

            "engine": "nano_banana",

            "output": output_folder,

            "image": response.get(
                "image_path"
            ),

            "error": response.get(
                "error"
            ),

            "response": response,

        }