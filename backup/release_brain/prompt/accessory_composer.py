class AccessoryComposer:


    def compose(self, context):

        accessories = context.environment.get(
            "accessories",
            {}
        )


        if not accessories:
            return ""


        recommended = accessories.get(
            "recommended",
            []
        )


        avoid = accessories.get(
            "avoid",
            []
        )


        # Support old schema
        if isinstance(recommended, dict):

            furniture = recommended.get(
                "furniture",
                []
            )

            decor = recommended.get(
                "decor",
                []
            )

        else:

            furniture = []

            decor = recommended


        return f"""
STYLING ACCESSORIES

Furniture:
{", ".join(furniture)}

Decor:
{", ".join(decor)}

Avoid:
{", ".join(avoid)}
""".strip()