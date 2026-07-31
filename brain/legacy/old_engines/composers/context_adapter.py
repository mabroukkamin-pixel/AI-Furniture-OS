class ContextAdapter:


    def build(self, context):

        data = {}


        data["product"] = {

            "name": context.product.get(
                "name",
                ""
            ),

            "category": context.product.get(
                "category",
                ""
            ),

            "material": context.product.get(
                "material",
                ""
            ),

            "colors": context.product.get(
                "colors",
                {}
            )
        }


        data["branding"] = context.branding


        data["environment"] = getattr(
            context,
            "environment",
            {}
        )


        data["lighting"] = getattr(
            context,
            "lighting",
            {}
        )


        data["photography"] = {

            "camera": getattr(
                context,
                "camera",
                {}
            ),

            "composition": getattr(
                context,
                "composition",
                {}
            )
        }


        return data