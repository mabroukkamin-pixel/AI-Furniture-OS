from brain.decision_graph.scorer import DecisionScorer
from brain.decision_graph.rule_loader import RuleLoader


class DecisionGraphEngine:

    def __init__(self):

        self.rules = []

        self.scorer = DecisionScorer()

        self.rule_loader = RuleLoader(
            "brain/knowledge/decision_rules.yaml"
        )

    def add_rule(self, rule):

        self.rules.append(rule)

    def load_rules(self):

        self.rules = self.rule_loader.load()

    def decide(self, context):

        decisions = []

        for rule in self.rules:

            result = rule.apply(context)

            if result:
                decisions.append(result)

        score = self.scorer.score(context)

        return {
            "decisions": decisions,
            "score": score
        }

    def run(self, brain_state):

        branding = brain_state.branding or {}

        nested_branding = branding.get(
            "branding",
            {}
        )

        context = {
            "material": (
                brain_state.product
                .get("material", {})
                .get("primary")
            ),
            "handmade": (
                brain_state.product.get(
                    "handmade",
                    False
                )
            ),
            "premium": (
                brain_state.product.get(
                    "premium",
                    False
                )
            ),
            "market": (
                branding.get("market")
                or nested_branding.get("market")
            )
        }

        brain_state.decision = self.decide(
            context
        )

        return brain_state
