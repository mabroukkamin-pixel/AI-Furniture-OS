from runtime.clients.base_client import BaseClient


class NanoBananaClient(BaseClient):

    def generate(self, prompt, image_path):

        print()
        print("=" * 30)
        print("NANO BANANA CLIENT")
        print("=" * 30)

        print("Sending Request...")
        print("Image :", image_path)
        print("Prompt :", len(prompt), "characters")

        return {
            "status": "success",
            "image": None
        }