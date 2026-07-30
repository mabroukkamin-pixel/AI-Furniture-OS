from dataclasses import dataclass, field


@dataclass
class DecisionContext:
    """
    Shared context between all experts and reasoners.
    """

    # Raw Product Files
    product_data: dict = field(default_factory=dict)

    # Product Intelligence
    product: object = None

    # Knowledge
    material: dict = field(default_factory=dict)
    style: dict = field(default_factory=dict)

    # Visual Decisions
    environment: dict = field(default_factory=dict)
    lighting: dict = field(default_factory=dict)
    photography: dict = field(default_factory=dict)

    # New Advertising Intelligence Layers
    camera: dict = field(default_factory=dict)
    composition: dict = field(default_factory=dict)
    brand: dict = field(default_factory=dict)

    # Product Protection Intelligence
    preservation: dict = field(default_factory=dict)

    # Marketing Intelligence
    marketing: dict = field(default_factory=dict)

    # Vision
    product_image: str = ""
    reference_images: list = field(default_factory=list)

    # Final Outputs
    prompt: dict = field(default_factory=dict)
    final_prompt: str = ""
    image_path: str = ""