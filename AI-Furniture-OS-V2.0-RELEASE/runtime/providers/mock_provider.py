from runtime.providers.base_provider import BaseProvider
import os
from PIL import Image, ImageDraw, ImageFont


class MockProvider(BaseProvider):

    def generate(self, request):

        output_folder = request.get(
            "output_folder"
        )

        prompt = request.get(
            "prompt",
            ""
        )

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        # Save prompt
        prompt_file = os.path.join(
            output_folder,
            "generated_prompt.txt"
        )

        with open(
            prompt_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(prompt)


        # Create local mock image
        image_path = os.path.join(
            output_folder,
            "mock_generated_image.png"
        )

        image = Image.new(
            "RGB",
            (1024, 1024),
            "white"
        )

        draw = ImageDraw.Draw(image)

        text = (
            "AI Furniture OS\n\n"
            "MOCK GENERATION\n\n"
            "Prompt Generated Successfully"
        )

        draw.multiline_text(
            (150, 400),
            text,
            fill="black"
        )

        image.save(
            image_path
        )


        return {

            "status": "success",

            "image": image_path,

            "image_path": image_path,

            "prompt_path": prompt_file,

            "provider": "mock",

            "fallback": True
        }