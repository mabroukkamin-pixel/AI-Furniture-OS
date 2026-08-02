class BrainPipeline:


    def __init__(
        self,
        knowledge_engine,
        graph_engine,
        reference_engine,
        decision_engine,
        fusion_engine,
        creative_engine,
        context_builder,
        prompt_writer
    ):

        self.knowledge_engine = knowledge_engine
        self.graph_engine = graph_engine
        self.reference_engine = reference_engine
        self.decision_engine = decision_engine
        self.fusion_engine = fusion_engine
        self.creative_engine = creative_engine
        self.context_builder = context_builder
        self.prompt_writer = prompt_writer



    def run(self, brain):


        # 1 Knowledge

        brain = self.knowledge_engine.run(
            brain
        )



        # 2 Graph

        brain = self.graph_engine.run(
            brain
        )



        # 3 Reference

        brain = self.reference_engine.run(
            brain
        )



        # 4 Decision

        brain = self.decision_engine.run(
            brain
        )



        # 5 Fusion

        brain = self.fusion_engine.run(
            brain
        )



        # 6 Creative

        brain = self.creative_engine.run(
            brain
        )



        # 7 Prompt Context

        context = (
            self.context_builder.build(
                brain
            )
        )


        # 8 Prompt

        brain.final_prompt = (
            self.prompt_writer.write(
                context
            )
        )


        brain.log(
            "Pipeline",
            "Complete AI production pipeline finished"
        )


        return brain