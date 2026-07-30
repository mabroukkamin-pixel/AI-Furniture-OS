import os
import json


class OutputManager:

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

        with open(
            os.path.join(folder, filename),
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

        root = f"outputs/{product_id}"

        generation = os.path.join(
            root,
            "generation"
        )

        prompt_folder = os.path.join(
            root,
            "prompt"
        )

        self.save_json(
            generation,
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

        return root

    def export(
        self,
        product_id,
        context
    ):

        root = f"outputs/{product_id}"

        brain = os.path.join(
            root,
            "brain"
        )

        self.save_json(
            brain,
            "product.json",
            context.product
        )

        self.save_json(
            brain,
            "decision.json",
            context.decision
        )

        self.save_json(
            brain,
            "branding.json",
            context.branding
        )

        self.save_json(
            brain,
            "marketing.json",
            context.marketing
        )

        self.save_json(
            brain,
            "preservation.json",
            getattr(
                context,
                "preservation",
                {}
            )
        )

        return root