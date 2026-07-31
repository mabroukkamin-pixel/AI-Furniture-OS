class LightingComposer:

    def compose(self, context):

        lighting_data = getattr(
            context,
            "lighting",
            {}
        )

        lighting = lighting_data.get(
            "type",
            "warm_daylight"
        )

        if isinstance(lighting, list):

            lighting = ", ".join(
                lighting
            )

        direction = lighting_data.get(
            "direction",
            ""
        )

        quality = lighting_data.get(
            "quality",
            ""
        )

        return f"""
LIGHTING

Type:
{lighting}

Direction:
{direction}

Quality:
{quality}
""".strip()