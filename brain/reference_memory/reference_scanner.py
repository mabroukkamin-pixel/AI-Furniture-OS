from pathlib import Path


class ReferenceScanner:

    def __init__(self, root):

        self.root = Path(root)

    def scan_folder(self, folder):

        path = self.root / folder

        if not path.exists():
            return []

        images = []

        for file in path.iterdir():

            if file.suffix.lower() in [
                ".jpg",
                ".jpeg",
                ".png",
                ".webp"
            ]:
                images.append(
                    str(file)
                )

        return images

    def scan_recursive(self, folder):

        path = self.root / folder

        if not path.exists():
            return []

        images = []

        for file in path.rglob("*"):

            if file.suffix.lower() in [
                ".jpg",
                ".jpeg",
                ".png",
                ".webp"
            ]:
                images.append(
                    str(file)
                )

        return images

    def scan_all(self):

        return {

            "materials":
                self.scan_folder(
                    "materials/rattan"
                ),

            "styles":
                self.scan_folder(
                    "styles/natural"
                ),

            "scenes":
                self.scan_folder(
                    "scenes/luxury_villa"
                ),

            "products":
                self.scan_recursive(
                    "products"
                )
        }