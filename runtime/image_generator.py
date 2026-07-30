from brain.providers.image_provider import ImageProvider


class ImageGenerator:

    def __init__(self):
        self.provider = ImageProvider()


    def generate(self, context):

        print("=" * 40)
        print("       IMAGE GENERATOR")
        print("=" * 40)


        if context is None:
            print("No context received.")
            return context


        image_request = {

            "prompt": context.final_prompt,

            "quality": "ultra_realistic",

            "resolution": "1024x1024",

            "style":
                "luxury furniture advertising",

            "product":
                context.product.name
        }


        context.image_request = image_request


        print("Image request prepared.")


        result = self.provider.generate(
            image_request
        )


        context.generated_image = result


        print("Generation payload created.")


        return context