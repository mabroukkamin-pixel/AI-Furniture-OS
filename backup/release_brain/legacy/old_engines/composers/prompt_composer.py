from runtime.models.context import DecisionContext


class PromptComposer:

    def compose(self, context: DecisionContext):

        print("========================================")
        print("      PROMPT COMPOSER")
        print("========================================")

        if context is None:
            return DecisionContext()

        product = context.product
        material = context.material
        lighting = context.lighting
        environment = context.environment
        camera = context.camera
        composition = context.composition
        brand = context.brand
        preservation = context.preservation

        prompt = {

            "product": 
                f"{product.name}",

            "material":
                material.get("name", ""),

            "scene":
                environment.get("primary", ""),

            "lighting":
                lighting,

            "camera":
                camera,

            "composition":
                composition,

            "brand":
                brand,

            "preservation":
                preservation,

            "instruction":
                "Create a premium luxury furniture advertising image while preserving the product exactly."

        }

        context.prompt = prompt

        print("Prompt composed.")

        return context