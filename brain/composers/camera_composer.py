class CameraComposer:

    def compose(self, context):

        shot = context.camera.get("shot", [])
        lens = context.camera.get("lens", "")
        angle = context.camera.get("angle", "")

        if isinstance(shot, list):
            shot = ", ".join(shot)

        return f"""
CAMERA

Shot:
{shot}

Lens:
{lens}

Angle:
{angle}
""".strip()