from runtime.models.context import DecisionContext

class CreativeContextBuilder:

    def build(self, brain):

        creative = brain.creative

        product = (
            brain.product
            .get("product", {})
            .get("product", {})
        )

        identity = (
            brain.product
            .get("identity", {})
            .get("product", {})
        )

        behavior = (
            brain.product
            .get("behavior", {})
            .get("behavior", {})
        )

        branding = (
            brain.brand
            .get("branding", {})
        )

        context = {

            "product":

            {

                "name":
                    product.get("name_ar")
                    or product.get("name"),

                "material":
                    product.get("material"),

                "category":
                    product.get("category"),

                "color":
                    product.get("color"),

                "dimensions":
                    product.get("dimensions"),

                "premium":
                    identity.get(
                        "premium",
                        False
                    ),

                "handmade":
                    identity.get(
                        "handmade",
                        False
                    )

            },

            "material":

            {

                "name":
                    product.get("material")

            },

            "environment":

            {

                "primary":
                    creative.get(
                        "scene",
                        []
                    )

            },

            "lighting":

            {

                "type":
                    creative.get(
                        "lighting",
                        []
                    )

            },

            "camera":

            {

                "shot":
                    creative.get(
                        "camera",
                        []
                    ),

                "lens":
                    "50mm",

                "angle":
                    "eye level"

            },

            "composition":

            {

                "style":
                    creative.get(
                        "style"
                    ),

                "product_scale":
                    "75%",

                "position":
                    "center hero placement"

            },

            "brand":

            {

                "name":
                    branding.get(
                        "company"
                    ),

                "arabic_name":
                    branding.get(
                        "arabic"
                    ),

                "market":
                    branding.get(
                        "market"
                    ),

                "colors":
                    branding.get(
                        "colors",
                        {}
                    ),
                    
                # التعديل الثاني: إضافة style داخل brand
                "style":
                    creative.get("style", "")

            },

            "preservation":

            {

                "rules":
                    behavior.get(
                        "preserve",
                        [
                            "keep exact product geometry",
                            "preserve materials",
                            "preserve colors",
                            "preserve dimensions"
                        ]
                    ),

                "emphasize":
                    behavior.get(
                        "emphasize",
                        []
                    ),

                "forbidden":
                    behavior.get(
                        "avoid",
                        []
                    )

            },

            "marketing":

            {

                # التعديل الثالث: إضافة بيانات التسويق الجديدة
                "target_customer":
                    "Kuwaiti women who love luxury home decor",

                "customer_emotion":
                    creative
                    .get("emotion", {})
                    .get("feeling"),

                "purchase_reason":
                    creative
                    .get("emotion", {})
                    .get("buyer_trigger"),

                "selling_angle":
                    "handmade natural premium decoration",

                "platform":
                    "Instagram"

            }

        }

        return DecisionContext(
            product=context["product"],
            material=context["material"],  # تمت إضافتها لتتوافق مع context.material
            environment=context["environment"],
            lighting=context["lighting"],
            camera=context["camera"],
            composition=context["composition"],
            brand=context["brand"],
            preservation=context["preservation"],
            marketing=context["marketing"]
        )