class ArchitectureComposer:

    def compose(self, context):

        arch = context.environment.get(
            "architecture",
            {}
        )

        if not arch:
            return ""

        architecture = arch.get(
            "architecture",
            []
        )

        walls = arch.get(
            "walls",
            []
        )

        floors = arch.get(
            "floors",
            []
        )

        avoid = arch.get(
            "avoid",
            []
        )


        if isinstance(architecture, list):
            architecture = ", ".join(architecture)

        if isinstance(walls, list):
            walls = ", ".join(walls)

        if isinstance(floors, list):
            floors = ", ".join(floors)

        if isinstance(avoid, list):
            avoid = ", ".join(avoid)


        return f"""
ARCHITECTURE DIRECTION

Style:
{architecture}

Walls:
{walls}

Floor:
{floors}

Avoid:
{avoid}
""".strip()