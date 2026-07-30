from runtime.engines.nano_banana_engine import NanoBananaEngine


class EngineFactory:

    @staticmethod
    def create(state):

        engine_name = "nano_banana"

        if engine_name == "nano_banana":
            return NanoBananaEngine(state)

        raise Exception(f"Unknown engine: {engine_name}")