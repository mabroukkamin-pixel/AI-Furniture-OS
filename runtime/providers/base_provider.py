class BaseProvider:

    def generate(self, request):
        raise NotImplementedError(
            "Provider must implement generate()"
        )