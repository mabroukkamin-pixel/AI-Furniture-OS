from brain.providers.base_provider import BaseProvider


class ImageProvider(BaseProvider):

    def generate(self, request):

        print("=" * 40)
        print("IMAGE PROVIDER")
        print("=" * 40)

        print("Prompt Ready.")

        return {
            "status": "prompt_ready",
            "prompt": request["prompt"]
        }