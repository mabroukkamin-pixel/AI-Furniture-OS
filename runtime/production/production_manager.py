from runtime.engines.engine_factory import EngineFactory


class ProductionManager:

    def __init__(self, state):
        self.state = state

    def build_request(self):

        return {

            "product_id":
                self.state.product_id,

            "prompt":
                self.state.prompt["final"],

            "product_image":
                self.state.product_image,

            "output_folder":
                self.state.output_folder,

            "brain_state":
                self.state

        }

    def run(self):

        print()
        print("========================================")
        print("PRODUCTION MANAGER")
        print("========================================")

        request = self.build_request()

        engine = EngineFactory.create(self.state)

        result = engine.generate(request)

        self.state.generation = result

        return result