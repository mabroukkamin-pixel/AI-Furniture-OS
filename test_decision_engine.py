from brain.reference_engine.reference_metadata import ReferenceMetadata
from brain.decision_engine.decision_engine import DecisionEngine


meta = ReferenceMetadata(
    "references/partition/reference.yaml"
)

data = meta.load()


engine = DecisionEngine(data)

result = engine.decide()


print("="*50)
print(result)
print("="*50)