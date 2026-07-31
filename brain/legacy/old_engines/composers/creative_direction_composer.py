class CreativeDirectionComposer:

    def compose(self, context):

        creative = getattr(
            context,
            "creative_direction",
            {}
        )

        if not creative:
            return ""

        return f"""
========================================
CREATIVE DIRECTION
========================================

VISUAL STYLE:
{creative.get("visual_style", "")}

MOOD:
{creative.get("mood", "")}

ARTISTIC GOAL:
{creative.get("goal", "")}

COLOR DIRECTION:
{creative.get("color_direction", "")}

STORY:
{creative.get("story", "")}
"""