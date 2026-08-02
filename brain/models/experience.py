from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Experience:

    product_id: str

    decision: dict = field(default_factory=dict)

    design_dna: dict = field(default_factory=dict)

    generation: dict = field(default_factory=dict)

    evaluation: dict = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )


    def to_dict(self):

        return {
            "product_id": self.product_id,
            "decision": self.decision,
            "design_dna": self.design_dna,
            "generation": self.generation,
            "evaluation": self.evaluation,
            "created_at": self.created_at
        }