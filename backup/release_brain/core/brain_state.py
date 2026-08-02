from brain.core.brain_trace import BrainTrace
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BrainState:

    # raw input
    product_data: dict = field(default_factory=dict)

    # final product object
    product: dict = field(default_factory=dict)

    # general context
    context: dict = field(default_factory=dict)

    # analysis layer
    analysis: dict = field(default_factory=dict)

    # decisions
    decision: dict = field(default_factory=dict)

    environment: dict = field(default_factory=dict)

    lighting: dict = field(default_factory=dict)

    camera: dict = field(default_factory=dict)

    composition: dict = field(default_factory=dict)

    # knowledge
    knowledge: dict = field(default_factory=dict)

    graph: dict = field(default_factory=dict)
    graph_decision: dict = field(default_factory=dict)
    graph_reasoning: dict = field(default_factory=dict)

    # reference memory
    reference: dict = field(default_factory=dict)

    fusion: dict = field(default_factory=dict)

    experience: dict = field(default_factory=dict)

    # marketing
    marketing: dict = field(default_factory=dict)

    # branding
    branding: dict = field(default_factory=dict)

    # prompt
    prompt: dict = field(default_factory=dict)

    # execution
    action_plan: dict = field(default_factory=dict)

    # compatibility alias for final prompt payload
    final_prompt: dict = field(default_factory=dict)

    # generation result
    generation: dict = field(default_factory=dict)

    # generated image path
    generated_image: str = ""

    # output folder
    output_folder: str = ""

    # product id
    product_id: str = ""

    # product image
    product_image: str = ""

    # reference images
    reference_images: list = field(default_factory=list)

    # Design DNA
    design_dna: dict = field(default_factory=dict)

    # preservation
    preservation: dict = field(default_factory=dict)

    # audit
    audit: dict = field(default_factory=dict)

    # state validation
    validation: dict = field(default_factory=dict)

    # new reporting and memory fields
    memory: dict = field(default_factory=dict)
    embedding: dict = field(default_factory=dict)
    similarity: dict = field(default_factory=dict)
    history: list = field(default_factory=list)

    # run lifecycle and artifacts
    run_id: str = ""
    started_at: str = ""
    completed_at: Optional[str] = None
    status: str = "pending"
    current_stage: str = ""
    error: Optional[dict] = None
    engine_name: str = ""
    artifacts: dict = field(default_factory=dict)

    # debug
    execution_plan: dict = field(default_factory=dict)
    trace: BrainTrace = field(default_factory=BrainTrace)

    def log(self, engine, message):

        self.trace.record(
            stage=engine,
            output_data=message
        )