from brain.providers.provider_manager import ProviderManager


class ImageGenerator:

    def __init__(self):
        self.provider = ProviderManager().get_provider()

    def generate(self, context):

        print("========================================")
        print("       IMAGE GENERATOR")
        print("========================================")

        if context is None:
            print("No context received.")
            return context

        image_request = {
            "prompt": context.final_prompt,
            "quality": "ultra_realistic",
            "resolution": "1024x1024",
            "style": "luxury furniture advertising",
            "product": context.product.name
        }

        context.image_request = image_request

        print("Image request prepared.")

        result = self.provider.generate(image_request)
        context.image_result = result
        print("Generation payload created.")

        return context