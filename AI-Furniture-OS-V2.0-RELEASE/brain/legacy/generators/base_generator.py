class BaseGenerator:


    def generate(
        self,
        image,
        prompt
    ):

        raise NotImplementedError(
            "Generator must implement generate()"
        )