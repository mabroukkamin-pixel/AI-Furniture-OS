from brain.rules.visual_rule_engine import VisualRuleEngine


engine = VisualRuleEngine(
    "brain/rules/visual_rules.yaml"
)


result = engine.analyze(
    "rattan"
)


print(result)