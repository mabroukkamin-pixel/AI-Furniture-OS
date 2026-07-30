from runtime.engines.base_engine import BaseEngine
from runtime.clients.nano_banana_client import NanoBananaClient


class NanoBananaEngine(BaseEngine):

    def __init__(self, state=None):
        super().__init__(state)
        self.client = NanoBananaClient()

    def generate(self, request):

        prompt = request["prompt"]
        image = request["product_image"]
        output_folder = request["output_folder"]
        product = request["product_id"]

        print()
        print("=" * 30)
        print("NANO BANANA ENGINE")
        print("=" * 30)

        response = self.client.generate(prompt, image)

        print("Product :", product)
        print("Output  :", output_folder)

        return {
            "status": response["status"],
            "engine": "nano_banana",
            "output": output_folder,
            "response": response
        }