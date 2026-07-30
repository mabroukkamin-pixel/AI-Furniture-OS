class AccessoryComposer:

    def compose(self, context):

        accessories = context.environment.get(
            "accessories",
            {}
        )

        if not accessories:
            return ""

        furniture = accessories.get(
            "recommended",
            {}
        ).get(
            "furniture",
            []
        )

        decor = accessories.get(
            "recommended",
            {}
        ).get(
            "decor",
            []
        )

        avoid = accessories.get(
            "avoid",
            []
        )


        return f"""
STYLING ACCESSORIES

Furniture:
{", ".join(furniture)}

Decor:
{", ".join(decor)}

Avoid:
{", ".join(avoid)}
""".strip()