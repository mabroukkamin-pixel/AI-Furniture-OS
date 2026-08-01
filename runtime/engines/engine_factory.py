from runtime.engines.nano_banana_engine import NanoBananaEngine
from runtime.config.settings import DEFAULT_ENGINE


class EngineFactory:

    @staticmethod
    def create(state):

        engine_name = DEFAULT_ENGINE

        if engine_name == "nano_banana":
            return NanoBananaEngine(state)

        raise Exception(
            f"Unknown engine: {engine_name}"
        )