class StyleComposer:
    def compose(self, context):
        # يمكن جلب الستايل من composition أو brand حسب المتوفر
        style = context.composition.get("style") or context.brand.get("style", "")
        if isinstance(style, list):
            return ", ".join(style)
        return str(style) if style else ""