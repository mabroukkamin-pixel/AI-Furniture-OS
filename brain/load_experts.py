from brain.registry import register

from brain.experts.product_expert import ProductExpert
from brain.experts.material_expert import MaterialExpert
from brain.experts.lighting_expert import LightingExpert
from brain.experts.environment_expert import EnvironmentExpert
from brain.experts.camera_expert import CameraExpert
from brain.experts.composition_expert import CompositionExpert
from brain.experts.brand_expert import BrandExpert
from brain.experts.preservation_expert import PreservationExpert
from brain.experts.marketing_expert import MarketingExpert


def load():

    register(ProductExpert)
    register(MaterialExpert)
    register(LightingExpert)
    register(EnvironmentExpert)
    register(CameraExpert)
    register(CompositionExpert)
    register(BrandExpert)
    register(PreservationExpert)
    register(MarketingExpert)