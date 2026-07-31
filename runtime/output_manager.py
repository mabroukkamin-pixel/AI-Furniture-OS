import os
import json


class OutputManager:

    def normalize_artifact_path(self, path):
        if not path:
            return None

        project_root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir
            )
        )

        absolute_path = os.path.abspath(path)

        try:
            relative_path = os.path.relpath(
                absolute_path,
                project_root
            )
        except ValueError:
            return None

        if relative_path.startswith(".."):
            return None

        return relative_path.replace("\\", "/")

    def record_artifact(self, context, key, path):
        normalized_path = self.normalize_artifact_path(path)

        if normalized_path:
            context.artifacts[key] = normalized_path

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

        return path.replace("\\", "/")

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

        return path.replace("\\", "/")

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

        design_dna_path = self.save_json(
            root,
            "design_dna.json",
            getattr(
                context,
                "design_dna",
                {}
            )
        )

        self.record_artifact(
            context,
            "design_dna",
            design_dna_path
        )

        audit_path = self.save_json(
            root,
            "audit.json",
            getattr(
                context,
                "audit",
                {}
            )
        )

        self.record_artifact(
            context,
            "audit",
            audit_path
        )

        generation_path = self.save_json(
            root,
            "generation.json",
            getattr(
                context,
                "generation",
                {}
            )
        )

        self.record_artifact(
            context,
            "generation",
            generation_path
        )

        final_prompt = getattr(
            context,
            "final_prompt",
            {}
        )

        if isinstance(final_prompt, dict):

            positive_prompt_path = self.save_text(
                root,
                "positive_prompt.txt",
                final_prompt.get(
                    "positive",
                    ""
                )
            )

            self.record_artifact(
                context,
                "positive_prompt",
                positive_prompt_path
            )

            negative_prompt_path = self.save_text(
                root,
                "negative_prompt.txt",
                final_prompt.get(
                    "negative",
                    ""
                )
            )

            self.record_artifact(
                context,
                "negative_prompt",
                negative_prompt_path
            )

        return root