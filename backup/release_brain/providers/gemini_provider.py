from brain.providers.base_provider import BaseProvider


class GeminiProvider(BaseProvider):

    def generate(self, request):

        print("Gemini Provider")
        print("Not connected yet.")

        return {
            "status": "not_connected",
            "provider": "gemini",
            "request": request
        }