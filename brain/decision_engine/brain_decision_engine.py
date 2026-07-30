from brain.decision_engine.decision_engine import DecisionEngine


class BrainDecisionEngine:


    def __init__(
        self,
        rule_engine,
        scoring_engine
    ):

        self.rule_engine = rule_engine
        self.scoring_engine = scoring_engine



    def run(self, brain):

        engine = DecisionEngine(

            product=brain.product,

            brand=brain.brand,

            rule_engine=self.rule_engine,

            scoring_engine=self.scoring_engine,

            reference=brain.reference,

            graph=brain.graph

        )


        brain.decision = engine.decide()


        brain.log(
            "Decision",
            "Decision generated"
        )


        return brain