class CompositionComposer:

    def compose(self, context):

        composition = context.composition

        style = composition.get(
            "style",
            ""
        )

        scale = composition.get(
            "product_scale",
            "75%"
        )

        position = composition.get(
            "position",
            "center"
        )

        return f"""
COMPOSITION

Style:
{style}

Product:
Centered

Scale:
Occupies {scale} of frame

Position:
{position}
""".strip()