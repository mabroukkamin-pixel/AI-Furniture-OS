from brain.generators.base_generator import BaseGenerator


class NanoBananaGenerator(BaseGenerator):

    def __init__(self):
        self.name = "nano_banana"

    def generate(
        self,
        product_id,
        image,
        prompt,
        state
    ):

        print("==============================")
        print("NANO BANANA ADAPTER")
        print("==============================")

        return {

            "engine": self.name,

            "product_id": product_id,

            "input_image": image,

            "prompt": prompt,

            "brain_state": state,

            "status": "queued"

        }