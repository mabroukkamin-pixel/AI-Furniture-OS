from pathlib import Path
from PIL import Image


class ImageValidator:

    def validate(self, image_path):

        result = {
            "exists": False,
            "readable": False,
            "width": None,
            "height": None,
            "valid": False,
        }

        path = Path(image_path)

        if not path.exists():
            return result

        result["exists"] = True

        try:
            with Image.open(path) as image:
                image.verify()

            with Image.open(path) as image:
                width, height = image.size

            result["readable"] = True
            result["width"] = width
            result["height"] = height
            result["valid"] = True

        except Exception:
            pass

        return result