class PromptValidator:

    REQUIRED = [
        "PRODUCT",
        "ENVIRONMENT",
        "LIGHTING",
        "CAMERA",
        "QUALITY"
    ]

    def validate(self, prompt):

        missing = []

        for item in self.REQUIRED:

            if item not in prompt:

                missing.append(item)

        return missing