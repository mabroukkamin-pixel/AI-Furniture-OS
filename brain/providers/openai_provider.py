from openai import OpenAI
import os


class OpenAIProvider:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, request):

        print("Connecting to OpenAI...")

        response = self.client.images.generate(
            model="gpt-image-1",
            prompt=request["prompt"],
            size=request["resolution"],
        )

        image_base64 = response.data[0].b64_json

        return {"status": "completed", "image": image_base64}