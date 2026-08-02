import os


class Validator:

    def validate(self, state):

        results = {}

        results["product"] = bool(state.product)

        results["design_dna"] = bool(
            getattr(state, "design_dna", {})
        )

        results["audit"] = bool(
            getattr(state, "audit", {})
        )

        results["branding"] = bool(
            getattr(state, "branding", {})
        )

        results["marketing"] = bool(
            getattr(state, "marketing", {})
        )

        results["generation"] = bool(
            getattr(state, "generation", {})
        )

        image = (
            state.generation.get("image")
            if isinstance(state.generation, dict)
            else None
        )

        results["image"] = (
            bool(image)
            and os.path.exists(image)
        )

        results["success"] = all(results.values())

        return results