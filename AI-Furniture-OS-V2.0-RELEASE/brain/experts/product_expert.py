from brain.experts.base_expert import BaseExpert


class ProductExpert(BaseExpert):

    def __init__(self, product_path=None):
        self.product_path = product_path


    def analyze(self, brain):

        print("========================================")
        print("        PRODUCT EXPERT")
        print("========================================")

        data = brain.product

        identity = data.get(
            "identity",
            {}
        )

        behavior = data.get(
            "behavior",
            {}
        )

        marketing = data.get(
            "marketing",
            {}
        )

        pricing = data.get(
            "pricing",
            {}
        )

        photography = data.get(
            "photography",
            {}
        )

        environment = data.get(
            "environment",
            {}
        )

        branding = data.get(
            "branding",
            {}
        )


        product_data = identity.get(
            "product",
            {}
        )


        print("BEFORE:")
        print(brain.product.keys())


        # final product object
        brain.product = product_data


        # keep structured state
        brain.behavior = behavior
        brain.environment = environment
        brain.branding = branding
        brain.marketing = marketing
        brain.photography = photography
        brain.preservation = behavior
        brain.context = {}


        brain.context.update(
            {
                "pricing": pricing
            }
        )


        print("AFTER:")
        print(brain.product.keys())


        print(
            "Loaded :",
            product_data.get("name")
        )


        return brain