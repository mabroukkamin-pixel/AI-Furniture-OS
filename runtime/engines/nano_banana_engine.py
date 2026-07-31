from runtime.clients.nano_banana_client import (
    NanoBananaClient,
)
from runtime.engines.base_engine import BaseEngine


class NanoBananaEngine(BaseEngine):

    def __init__(self, state=None):
        super().__init__(state)
        self.client = NanoBananaClient()

    def generate(self, request):
        prompt = request["prompt"]
        image = request["product_image"]
        product = request["product_id"]
        output_folder = request[
            "output_folder"
        ]

        print()
        print("=" * 30)
        print("NANO BANANA ENGINE")
        print("=" * 30)

        response = self.client.generate(
            prompt,
            image,
            output_folder
        )

        image_path = response.get(
            "image_path"
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
            "image": image_path,
            "response": response,
        }