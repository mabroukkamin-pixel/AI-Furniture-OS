from google import genai
from google.genai import types

from runtime.clients.base_client import BaseClient
from runtime.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

import os
import traceback
from PIL import Image


class NanoBananaClient(BaseClient):

    def __init__(self):

        self.enabled = False
        self.client = None

        # check API key

        if (
            GEMINI_API_KEY
            and GEMINI_API_KEY != "ضع_مفتاح_Gemini_الحقيقي_هنا"
            and len(GEMINI_API_KEY) > 20
        ):

            self.client = genai.Client(
                api_key=GEMINI_API_KEY,
                http_options=types.HttpOptions(
                    timeout=300000
                )
            )

            self.enabled = True

        else:

            print(
                "GEMINI API KEY NOT FOUND"
            )

            print(
                "Running in LOCAL MODE"
            )


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


        # ============================
        # LOCAL MODE
        # ============================

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
            ) as f:

                f.write(prompt)


            return {

                "status":
                "success_local",

                "image_url":
                None,

                "prompt":
                prompt_file
            }



        # ============================
        # GEMINI MODE
        # ============================


        try:

            print(
                "Loading reference image..."
            )


            Image.open(
                image_path
            )


            print(
                "Calling Gemini API..."
            )


            response = self.client.models.generate_content(

                model=GEMINI_MODEL,

                contents=[

                    types.Part.from_bytes(

                        data=open(
                            image_path,
                            "rb"
                        ).read(),

                        mime_type="image/png"

                    ),

                    prompt
                ],

                config=types.GenerateContentConfig(

                    response_modalities=[
                        "IMAGE"
                    ]

                )

            )


            output_image_path = os.path.join(
                output_folder,
                "generated.png"
            )


            if response.candidates:

                for part in response.candidates[0].content.parts:


                    if hasattr(part,"inline_data"):

                        with open(
                            output_image_path,
                            "wb"
                        ) as f:

                            f.write(
                                part.inline_data.data
                            )


                        return {

                            "status":
                            "success",

                            "image_url":
                            output_image_path

                        }



            return {

                "status":
                "success",

                "image_url":
                None

            }


        except Exception as e:


            print(
                "GEMINI ERROR"
            )

            traceback.print_exc()


            return {

                "status":
                "error",

                "error":
                str(e)

            }