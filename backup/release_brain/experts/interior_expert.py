class InteriorExpert:

    def build(self, brain):

        environment = brain.environment

        return environment.get(
            "interior",
            {}
        )