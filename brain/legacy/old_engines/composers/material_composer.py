class MarketingComposer:

    def compose(self, brain):
        marketing = brain.direction.get("marketing", {})
        if isinstance(marketing, dict):
            parts = [f"{k}: {v}" for k, v in marketing.items() if v]
            return f"Marketing: {', '.join(parts)}"
        return f"Marketing: {marketing}"