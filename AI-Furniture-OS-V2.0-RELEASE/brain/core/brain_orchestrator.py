class BrainOrchestrator:

    def __init__(
        self,
        experts,
        graph,
        environment,
        experience
    ):
        self.experts = experts
        self.graph = graph
        self.environment = environment
        self.experience = experience

    def run_experts(self, context):

        for expert in self.experts:
            context = expert.analyze(context)

        return context