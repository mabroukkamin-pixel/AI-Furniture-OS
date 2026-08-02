from runtime.clients.base_client import BaseClient


class GeminiClient(BaseClient):

    def generate(self, prompt, image_path):

        print()
        print("=" * 40)
        print("GEMINI CLIENT")
        print("=" * 40)

        print("Input Image:")
        print(image_path)

        print()
        print("Prompt Length:")
        print(len(prompt))

        # API connection will be added here

        return {
            "status": "ready",
            "image": None
        }