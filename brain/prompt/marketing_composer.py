class MarketingComposer:

    def compose(self, context):

        marketing = context.marketing

        return f"""
MARKETING STRATEGY

Target Audience:
{marketing.get("audience", "")}

Positioning:
{marketing.get("positioning", "")}

Message:
{marketing.get("message", "")}

Platforms:
{marketing.get("platforms", [])}
"""