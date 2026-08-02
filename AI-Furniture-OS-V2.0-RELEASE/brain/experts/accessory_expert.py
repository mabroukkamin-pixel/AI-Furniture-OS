class AccessoryExpert:

    def build(self, brain):

        environment = brain.environment

        return environment.get(
            "accessories",
            {}
        )