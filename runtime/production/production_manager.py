class ProductionManager:

    def __init__(self, state):
        self.state = state

    def build_request(self):

        prompt_payload = self.state.prompt

        if not isinstance(prompt_payload, dict):
            prompt_payload = {}

        if "final" in prompt_payload:
            prompt_text = prompt_payload["final"]
        elif "positive" in prompt_payload:
            prompt_text = prompt_payload["positive"]
        else:
            fallback_prompt = getattr(
                self.state,
                "final_prompt",
                None
            )

            if (
                isinstance(fallback_prompt, dict)
                and "final" in fallback_prompt
            ):
                prompt_text = fallback_prompt["final"]
            elif (
                isinstance(fallback_prompt, dict)
                and "positive" in fallback_prompt
            ):
                prompt_text = fallback_prompt["positive"]
            else:
                prompt_text = ""

        return {
            "product_id": getattr(
                self.state,
                "product_id",
                None
            ),
            "prompt": prompt_text,
            "product_image": getattr(
                self.state,
                "product_image",
                None
            ),
            "output_folder": getattr(
                self.state,
                "output_folder",
                None
            ),
            "brain_state": self.state
        }

    def run(self):

        print()
        print("========================================")
        print("PRODUCTION MANAGER")
        print("========================================")

        request = self.build_request()

        from runtime.engines.engine_factory import EngineFactory

        engine = EngineFactory.create(self.state)

        result = engine.generate(request)

        self.state.generation = result

        if isinstance(result, dict):
            image_path = result.get("image")

            if image_path:
                from runtime.output_manager import OutputManager

                output_manager = OutputManager()
                normalized_path = (
                    output_manager.normalize_artifact_path(
                        image_path
                    )
                )

                if normalized_path:
                    generated_images = (
                        self.state.artifacts.setdefault(
                            "generated_images",
                            []
                        )
                    )

                    if normalized_path not in generated_images:
                        generated_images.append(
                            normalized_path
                        )

        return result