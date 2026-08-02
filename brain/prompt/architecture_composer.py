class ArchitectureComposer:

    def compose(self, context):

        arch = context.environment.get(
            "architecture",
            {}
        )

        if not arch:
            return ""

        materials = []
        walls = []
        floors = []
        avoid = []

        if isinstance(arch, dict):

            materials = (
                arch.get("materials")
                or
                arch.get("architecture")
                or
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

        elif isinstance(arch, list):

            materials = arch

        if isinstance(materials, list):
            materials = ", ".join(materials)

        if isinstance(walls, list):
            walls = ", ".join(walls)

        if isinstance(floors, list):
            floors = ", ".join(floors)

        if isinstance(avoid, list):

            avoid = ", ".join(avoid)

            if not avoid:
                avoid = "None"

        return f"""
ARCHITECTURE DIRECTION

Materials:
{materials}

Walls:
{walls}

Floor:
{floors}

Avoid:
{avoid}

""".strip()