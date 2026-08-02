class CameraDirector:

    def build(self, brain):

        creative = brain.creative or {}

        return {
            "camera": creative.get("camera", []),
            "lens": "50mm",
            "angle": "eye level"
        }