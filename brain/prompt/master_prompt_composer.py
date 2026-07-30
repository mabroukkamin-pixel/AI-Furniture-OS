from brain.prompt.environment_composer import EnvironmentComposer
from brain.prompt.scene_composer import SceneComposer
from brain.prompt.architecture_composer import ArchitectureComposer
from brain.prompt.accessory_composer import AccessoryComposer
from brain.prompt.lighting_composer import LightingComposer
from brain.prompt.camera_composer import CameraComposer
from brain.prompt.marketing_composer import MarketingComposer
from brain.prompt.product_composer import ProductComposer
from brain.prompt.composition_composer import CompositionComposer
from brain.prompt.brand_composer import BrandComposer
from brain.prompt.preservation_composer import PreservationComposer
from brain.prompt.quality_composer import QualityComposer
from brain.prompt.negative_prompt_composer import NegativePromptComposer
from brain.prompt.design_dna_composer import DesignDNAComposer
from brain.prompt.creative_direction_composer import CreativeDirectionComposer


class MasterPromptComposer:

    def __init__(self):
        self.product = ProductComposer()

        self.environment = EnvironmentComposer()
        self.scene = SceneComposer()
        self.architecture = ArchitectureComposer()
        self.accessory = AccessoryComposer()

        self.lighting = LightingComposer()
        self.camera = CameraComposer()
        self.composition = CompositionComposer()
        self.brand = BrandComposer()
        self.marketing = MarketingComposer()
        self.preservation = PreservationComposer()
        self.quality = QualityComposer()
        self.negative = NegativePromptComposer()
        self.design_dna = DesignDNAComposer()
        self.creative_direction = CreativeDirectionComposer()

    def compose(self, context):

        return "\n\n".join([

            self.product.compose(context),

            self.environment.compose(context),

            self.scene.compose(context),

            self.architecture.compose(context),

            self.accessory.compose(context),

            self.lighting.compose(context),

            self.camera.compose(context),

            self.composition.compose(context),

            self.brand.compose(context),

            self.marketing.compose(context),

            self.preservation.compose(context),

            self.quality.compose(context),

            self.design_dna.compose(context),

            self.creative_direction.compose(context)

        ])