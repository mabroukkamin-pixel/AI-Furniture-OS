class StylingDirector:

    def build(self, brain):

        creative = brain.creative or {}

        return {
            "style": creative.get("style"),
            "material": creative.get("material"),
            "emotion": creative.get("emotion", {})
        }