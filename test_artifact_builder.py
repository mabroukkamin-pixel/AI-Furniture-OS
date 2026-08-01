from brain.core.brain_state import BrainState
from runtime.artifacts.artifact_builder import ArtifactBuilder

state = BrainState()

state.product_id = "Partition001"

state.output_folder = "outputs/Partition001"

state.status = "success"

state.engine_name = "mock"

state.product = {
    "name": "Rattan Partition",
    "category": "partition"
}

builder = ArtifactBuilder()

artifacts = builder.build(state)

print(artifacts)