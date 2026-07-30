from brain.experts.base_expert import BaseExpert


class ProductExpert(BaseExpert):

    def __init__(self, product_path="products/Partition001"):
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

        brain.product = product_data

        print("AFTER:")
        print(brain.product.keys())

        brain.context["identity"] = identity
        brain.context["behavior"] = behavior
        brain.context["pricing"] = pricing
        brain.context["photography"] = photography
        brain.context["environment"] = environment
        brain.context["branding"] = branding

        print(
            "Loaded :",
            product_data.get("name")
        )

        return brain