from runtime.providers.mock_provider import MockProvider
from runtime.providers.nano_banana_provider import NanoBananaProvider
from runtime.providers.provider_health import ProviderHealth


class ProviderManager:

    def __init__(self):

        self.health = ProviderHealth()

        self.providers = {

            "nano_banana":
                NanoBananaProvider(),

            "mock":
                MockProvider(),

        }

    def get_provider(self, name):

        provider = self.providers.get(name)

        if provider is None:
            raise Exception(
                f"Provider not found: {name}"
            )

        return provider

    def select_provider(self):

        status = self.health.get_status()

        if status.get("nano_banana", {}).get("available"):

            return "nano_banana"

        return "mock"

    def generate(self, request):

        provider_name = self.select_provider()

        print(
            "SELECTED PROVIDER:",
            provider_name
        )

        provider = self.get_provider(
            provider_name
        )

        try:

            result = provider.generate(
                request
            )

            self.health.mark_available(
                provider_name
            )

            return result

        except Exception as e:

            print(
                "PROVIDER FAILED:",
                provider_name
            )

            self.health.mark_failed(
                provider_name,
                str(e)
            )

            if provider_name != "mock":

                print(
                    "FALLBACK TO MOCK"
                )

                return self.providers["mock"].generate(
                    request
                )

            raise