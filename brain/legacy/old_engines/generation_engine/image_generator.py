class ImageGenerator:


    def __init__(
        self,
        prompt,
        image
    ):

        self.prompt = prompt
        self.image = image


    def generate(self):

        return {

            "status":
            "ready",

            "prompt":
            self.prompt,

            "reference_image":
            self.image

        }