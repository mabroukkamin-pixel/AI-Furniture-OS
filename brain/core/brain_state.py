from dataclasses import dataclass, field


@dataclass
class BrainState:

    # raw input
    product_data: dict = field(default_factory=dict)

    # final product object
    product: dict = field(default_factory=dict)

    # general context
    context: dict = field(default_factory=dict)

    # decisions
    decision: dict = field(default_factory=dict)

    environment: dict = field(default_factory=dict)

    lighting: dict = field(default_factory=dict)

    camera: dict = field(default_factory=dict)

    composition: dict = field(default_factory=dict)

    # knowledge
    knowledge: dict = field(default_factory=dict)

    graph: dict = field(default_factory=dict)

    # reference memory
    reference: dict = field(default_factory=dict)

    fusion: dict = field(default_factory=dict)

    # marketing
    marketing: dict = field(default_factory=dict)

    # branding
    branding: dict = field(default_factory=dict)

    # prompt
    prompt: dict = field(default_factory=dict)

    # debug
    trace: list = field(default_factory=list)

    def log(self, engine, message):

        self.trace.append(
            {
                "engine": engine,
                "message": message
            }
        )