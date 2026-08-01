from runtime.clients.nano_banana_client import (
    NanoBananaClient,
)
from runtime.providers.base_provider import (
    BaseProvider,
)


class NanoBananaProvider(BaseProvider):

    def __init__(self):

        self.client = NanoBananaClient()

    def generate(self, request):

        prompt = request.get(
            "prompt",
            ""
        )

        image = request.get(
            "product_image"
        )

        output_folder = request.get(
            "output_folder"
        )

        try:

            response = self.client.generate(
                prompt,
                image,
                output_folder
            )

            if response.get("status") in [
                "queued",
                "error",
                "failed",
            ]:

                from runtime.providers.mock_provider import (
                    MockProvider,
                )

                print()
                print(
                    "NANO BANANA FAILED"
                )
                print(
                    "SWITCHING TO MOCK PROVIDER"
                )

                return MockProvider().generate(
                    request
                )

            return response

        except Exception as error:

            from runtime.providers.mock_provider import (
                MockProvider,
            )

            print()
            print(
                "NANO BANANA EXCEPTION"
            )
            print(error)
            print(
                "SWITCHING TO MOCK PROVIDER"
            )

            return MockProvider().generate(
                request
            )