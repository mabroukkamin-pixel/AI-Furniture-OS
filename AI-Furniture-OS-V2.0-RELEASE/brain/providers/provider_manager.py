import os

from brain.providers.openai_provider import OpenAIProvider
from brain.providers.gemini_provider import GeminiProvider
from brain.providers.comfyui_provider import ComfyUIProvider
from brain.providers.image_provider import ImageProvider


class ProviderManager:


    def __init__(self):

        provider_name = os.getenv(
            "IMAGE_PROVIDER",
            "mock"
        )


        providers = {

            "openai":
                OpenAIProvider(),

            "gemini":
                GeminiProvider(),

            "comfyui":
                ComfyUIProvider(),

            "mock":
                ImageProvider(),

        }


        self.provider = providers.get(
            provider_name,
            ImageProvider()
        )


        print(
            "ACTIVE IMAGE PROVIDER:",
            provider_name
        )



    def get_provider(self):

        return self.provider