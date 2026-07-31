import mimetypes
import os
import traceback
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

from runtime.clients.base_client import BaseClient
from runtime.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)


class NanoBananaClient(BaseClient):

    def __init__(self):
        self.enabled = False
        self.client = None

        api_key = (
            GEMINI_API_KEY or ""
        ).strip()

        model = (
            GEMINI_MODEL or ""
        ).strip()

        if (
            api_key.startswith("AIza")
            and len(api_key) > 30
            and model
        ):
            self.client = genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(
                    timeout=300000
                )
            )
            self.enabled = True
        else:
            print(
                "GEMINI API KEY OR MODEL NOT CONFIGURED"
            )
            print(
                "Running in LOCAL MODE"
            )

    def _detect_mime_type(self, image_path):
        with Image.open(image_path) as image:
            image_format = image.format
            image.verify()

        mime_type = Image.MIME.get(
            image_format
        )

        if not mime_type:
            mime_type = mimetypes.guess_type(
                image_path
            )[0]

        return mime_type or "image/png"

    def _save_inline_image(
        self,
        inline_data,
        output_folder
    ):
        mime_type = getattr(
            inline_data,
            "mime_type",
            "image/png"
        )

        extensions = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/webp": ".webp",
        }

        extension = extensions.get(
            mime_type,
            ".png"
        )

        output_image_path = os.path.join(
            output_folder,
            f"generated{extension}"
        )

        temporary_path = (
            f"{output_image_path}.tmp"
        )

        with open(
            temporary_path,
            "wb"
        ) as file:
            file.write(
                inline_data.data
            )

        os.replace(
            temporary_path,
            output_image_path
        )

        return output_image_path

    def generate(
        self,
        prompt,
        image_path,
        output_folder
    ):
        print()
        print("=" * 30)
        print("NANO BANANA CLIENT")
        print("=" * 30)

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        print(
            "Model:",
            GEMINI_MODEL
        )

        print(
            "Prompt:",
            len(prompt),
            "characters"
        )

        if not self.enabled:
            print(
                "LOCAL IMAGE ENGINE MODE"
            )

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

            return {
                "status": "local_only",
                "image_path": None,
                "prompt_path": prompt_file,
            }

        try:
            print(
                "Loading reference image..."
            )

            mime_type = self._detect_mime_type(
                image_path
            )

            image_bytes = Path(
                image_path
            ).read_bytes()

            print(
                "Calling Gemini API..."
            )

            response = (
                self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=[
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=mime_type
                        ),
                        prompt,
                    ],
                    config=types.GenerateContentConfig(
                        response_modalities=[
                            "IMAGE"
                        ]
                    ),
                )
            )

            for candidate in (
                response.candidates or []
            ):
                content = getattr(
                    candidate,
                    "content",
                    None
                )

                for part in (
                    getattr(
                        content,
                        "parts",
                        []
                    ) or []
                ):
                    inline_data = getattr(
                        part,
                        "inline_data",
                        None
                    )

                    if (
                        inline_data
                        and inline_data.data
                    ):
                        output_image_path = (
                            self._save_inline_image(
                                inline_data,
                                output_folder
                            )
                        )

                        return {
                            "status": "success",
                            "image_path":
                                output_image_path,
                        }

            return {
                "status": "error",
                "image_path": None,
                "error":
                    "Gemini returned no image data",
            }

        except Exception as error:
            print(
                "GEMINI ERROR"
            )
            traceback.print_exc()

            return {
                "status": "error",
                "image_path": None,
                "error": str(error),
            }