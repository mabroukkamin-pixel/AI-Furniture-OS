from brain.providers.openai_provider import OpenAIProvider


class ProviderManager:

    def __init__(self):

        self.provider = OpenAIProvider()


    def get_provider(self):

        return self.provider