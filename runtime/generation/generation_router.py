from runtime.providers.provider_manager import ProviderManager


class GenerationRouter:

    def __init__(self):

        self.provider_manager = ProviderManager()

        self.health = self.provider_manager.health

        self.priority = [
            "nano_banana",
            "mock",
        ]

    def generate(self, request):

        print()
        print("=" * 30)
        print("GENERATION ROUTER")
        print("=" * 30)

        errors = []

        for provider_name in self.priority:

            if not self.health.is_available(provider_name):

                print(
                    "SKIPPING UNAVAILABLE:",
                    provider_name
                )

                continue

            print(
                "Trying provider:",
                provider_name
            )

            try:

                provider = self.provider_manager.get_provider(
                    provider_name
                )
                response = provider.generate(request)

                response_provider = response.get(
                    "provider",
                    provider_name
                )

                if response.get("image_path"):

                    print(
                        "SUCCESS:",
                        response_provider
                    )

                    return response

                elif response.get("prompt_path"):

                    print(
                        "LOCAL OUTPUT:",
                        response_provider
                    )

                    return response

                errors.append(response)

            except Exception as error:

                import traceback

                print(
                    "FAILED:",
                    provider_name
                )

                traceback.print_exc()

                self.health.mark_failed(
                    provider_name,
                    str(error)
                )

                if provider_name != "mock":
                    print("FALLBACK TO MOCK")
                    response = self.provider_manager.get_provider("mock").generate(request)
                    return response

                errors.append(
                    {
                        "provider": provider_name,
                        "error": str(error)
                    }
                )

        return {

            "status": "failed",

            "image_path": None,

            "errors": errors

        }