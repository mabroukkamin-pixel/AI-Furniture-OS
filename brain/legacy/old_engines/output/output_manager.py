import os
import json


class OutputManager:

    def __init__(
        self,
        base_folder="outputs"
    ):

        self.base_folder = base_folder

    def save_json(
        self,
        folder,
        filename,
        data
    ):

        os.makedirs(
            folder,
            exist_ok=True
        )

        path = os.path.join(
            folder,
            filename
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    def save_text(
        self,
        folder,
        filename,
        text
    ):

        os.makedirs(
            folder,
            exist_ok=True
        )

        path = os.path.join(
            folder,
            filename
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

    def save_request(
        self,
        product_id,
        image,
        prompt
    ):

        root = os.path.join(
            self.base_folder,
            product_id
        )

        generation_folder = os.path.join(
            root,
            "generation"
        )

        prompt_folder = os.path.join(
            root,
            "prompt"
        )

        images_folder = os.path.join(
            root,
            "images"
        )

        self.save_json(
            generation_folder,
            "input.json",
            {
                "image": image,
                "prompt": prompt
            }
        )

        self.save_text(
            prompt_folder,
            "final_prompt.txt",
            prompt
        )

        os.makedirs(
            images_folder,
            exist_ok=True
        )

        return root

    def export(
        self,
        product_id,
        context
    ):

        root = os.path.join(
            self.base_folder,
            product_id
        )

        brain_folder = os.path.join(
            root,
            "brain"
        )

        prompt_folder = os.path.join(
            root,
            "prompt"
        )

        self.save_json(
            brain_folder,
            "product.json",
            context.product
        )

        self.save_json(
            brain_folder,
            "decision.json",
            context.decision
        )

        self.save_json(
            brain_folder,
            "branding.json",
            context.branding
        )

        self.save_json(
            brain_folder,
            "marketing.json",
            context.marketing
        )

        self.save_json(
            brain_folder,
            "preservation.json",
            getattr(
                context,
                "preservation",
                {}
            )
        )

        if hasattr(
            context,
            "prompt"
        ):

            self.save_text(
                prompt_folder,
                "final_prompt.txt",
                context.prompt.get(
                    "final",
                    ""
                )
            )

        return root