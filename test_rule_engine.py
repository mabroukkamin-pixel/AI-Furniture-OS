from brain.reference_engine.reference_metadata import ReferenceMetadata
from brain.decision_engine.rule_engine import RuleEngine
from brain.decision_engine.decision_engine import DecisionEngine


metadata = ReferenceMetadata(
    "references/partition/reference.yaml"
)

data = metadata.load()


rules = RuleEngine(
    "brain/decision_engine/rules.yaml"
)


engine = DecisionEngine(
    data,
    rules
)


result = engine.decide()


print("="*50)
print(result)
print("="*50)