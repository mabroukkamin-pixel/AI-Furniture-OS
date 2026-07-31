from dataclasses import dataclass


@dataclass
class Context:

    market: str = "Kuwait"

    season: str = "summer"

    campaign: str = "normal"

    platform: str = "instagram"

    language: str = "arabic"

    time: str = "golden_hour"

    luxury_level: str = "premium"

    usage: str = "social_media"

    material: str = None

    category: str = None

    product_name: str = None



class ContextEngine:


    def __init__(
        self,
        product=None,
        brand=None
    ):

        self.product = product or {}

        self.brand = brand or {}



    def build(self):

        product_data = (
            self.product
                .get("product", {})
                .get("product", {})
        )

        return Context(

            market=
                self.brand
                .get("branding", {})
                .get(
                    "market",
                    "Kuwait"
                ),

            material=
                product_data.get(
                    "material"
                ),

            category=
                product_data.get(
                    "category"
                ),

            product_name=
                product_data.get(
                    "name_ar",
                    product_data.get(
                        "name"
                    )
                )
        )