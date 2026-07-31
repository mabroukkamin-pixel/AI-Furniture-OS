class SceneComposer:


    def compose(self, context):

        environment = (
            context.environment
            or {}
        )


        primary = environment.get(
            "primary",
            ""
        )


        atmosphere = environment.get(
            "atmosphere",
            []
        )


        options = environment.get(
            "options",
            []
        )


        if isinstance(atmosphere, list):

            atmosphere = ", ".join(
                atmosphere
            )


        if isinstance(options, list):

            options = ", ".join(
                options
            )


        return f"""
SCENE DIRECTION

Main Scene:
{primary}

Atmosphere:
{atmosphere}

Alternative Scenes:
{options}

Creative Direction:

Create a premium interior environment
with a luxury lifestyle feeling.

The scene must support the product
as the hero furniture element.

Use realistic architectural details,
balanced composition,
and high-end interior styling.
""".strip()