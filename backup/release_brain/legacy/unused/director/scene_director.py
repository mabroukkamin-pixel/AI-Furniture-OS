from brain.experts.architecture_expert import ArchitectureExpert
from brain.experts.interior_expert import InteriorExpert
from brain.experts.accessory_expert import AccessoryExpert
from brain.experts.composition_expert import CompositionExpert


class SceneDirector:

    def __init__(self):

        self.architecture = ArchitectureExpert()
        self.interior = InteriorExpert()
        self.accessory = AccessoryExpert()
        self.composition = CompositionExpert()

    def build(self, brain):

        creative = brain.creative or {}

        return {

            "environment":
                creative.get("scene", []),

            "architecture":
                self.architecture.build(brain),

            "interior":
                self.interior.build(brain),

            "accessories":
                self.accessory.build(brain),

            "composition":
                self.composition.build(brain)
        }