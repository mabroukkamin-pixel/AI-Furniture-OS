import os
import json
from datetime import datetime


class ImageManager:

    def __init__(self):
        self.base = "outputs/products"


    def save(self, context):

        product_name = context.product.name.replace(" ", "_")

        product_path = os.path.join(
            self.base,
            product_name
        )

        os.makedirs(
            product_path,
            exist_ok=True
        )


        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )


        version_path = os.path.join(
            product_path,
            "versions",
            "v001"
        )

        os.makedirs(
            version_path,
            exist_ok=True
        )


        # Save Prompt

        with open(
            os.path.join(
                product_path,
                "prompt.txt"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(context.final_prompt)


        # Save Context

        with open(
            os.path.join(
                product_path,
                "context.json"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                context.__dict__,
                f,
                indent=4,
                ensure_ascii=False,
                default=str
            )


        # Save Image Result

        if hasattr(context, "generated_image"):

            with open(
                os.path.join(
                    product_path,
                    "image_result.json"
                ),
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    context.generated_image,
                    f,
                    indent=4,
                    ensure_ascii=False
                )


        print("=" * 40)
        print("IMAGE MANAGER")
        print("=" * 40)
        print("Assets saved:")
        print(product_path)


        return product_path