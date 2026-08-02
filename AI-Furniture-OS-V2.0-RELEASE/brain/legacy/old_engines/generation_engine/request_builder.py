class GenerationRequest:


    def build(
        self,
        product_image,
        prompt
    ):

        return {

            "reference_image":
                product_image,

            "prompt":
                prompt,

            "settings":
            {

                "aspect_ratio":
                    "1:1",

                "quality":
                    "ultra",

                "preserve_product":
                    True

            }

        }