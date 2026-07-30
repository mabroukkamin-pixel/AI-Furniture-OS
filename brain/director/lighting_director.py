class LightingDirector:

    def build(self, brain):

        creative = brain.creative or {}

        return {
            "lighting": creative.get("lighting", [])
        }