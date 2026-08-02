from brain.providers.base_provider import BaseProvider


class ComfyUIProvider(BaseProvider):

    def generate(self, request):

        print("ComfyUI Provider")
        print("Waiting for local server.")

        return {
            "status": "not_connected",
            "provider": "comfyui",
            "request": request
        }