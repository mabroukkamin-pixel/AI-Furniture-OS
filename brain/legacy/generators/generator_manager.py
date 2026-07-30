from brain.generators.nano_banana import NanoBananaGenerator


class GeneratorManager:

    def __init__(self):

        self.generators = {
            "nano_banana":
                NanoBananaGenerator()
        }

    def generate(
        self,
        engine,
        product_id,
        image,
        prompt,
        state
    ):

        generator = self.generators.get(engine)

        if generator is None:
            raise Exception(f"Unknown generator: {engine}")

        return generator.generate(
            product_id,
            image,
            prompt,
            state
        )