class ArchitectureExpert:

    def build(self, brain):

        environment = brain.environment

        return environment.get(
            "architecture",
            {}
        )