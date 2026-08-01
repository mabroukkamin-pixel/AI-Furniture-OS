from brain.core.brain_state import BrainState
from runtime.artifacts.artifact_registry import ArtifactRegistry


state = BrainState()

state.product_id = "Partition001"
state.status = "success"
state.engine_name = "mock"


registry = ArtifactRegistry()

artifact = registry.register(state)


print("==============================")
print("ARTIFACT CREATED")
print("==============================")

print(artifact)