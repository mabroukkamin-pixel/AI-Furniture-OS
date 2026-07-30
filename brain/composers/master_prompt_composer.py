from brain.composers.environment_composer import EnvironmentComposer
from brain.composers.scene_composer import SceneComposer
from brain.composers.architecture_composer import ArchitectureComposer
from brain.composers.accessory_composer import AccessoryComposer
from brain.composers.lighting_composer import LightingComposer
from brain.composers.camera_composer import CameraComposer
from brain.composers.marketing_composer import MarketingComposer
from brain.composers.product_composer import ProductComposer
from brain.composers.composition_composer import CompositionComposer
from brain.composers.brand_composer import BrandComposer
from brain.composers.preservation_composer import PreservationComposer
from brain.composers.quality_composer import QualityComposer
from brain.composers.negative_prompt_composer import NegativePromptComposer
from brain.composers.design_dna_composer import DesignDNAComposer
from brain.composers.creative_direction_composer import CreativeDirectionComposer


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

            self.creative_direction.compose(context),

            self.negative.compose(context)

        ])