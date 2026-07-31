from pathlib import Path


class ReferenceSelector:

    def __init__(
        self,
        library_path
    ):

        self.root = Path(library_path)

    def scan_folder(
        self,
        path
    ):

        folder = self.root / path

        if not folder.exists():
            return []

        return [

            str(file)

            for file in folder.rglob("*")

            if file.suffix.lower()
            in [
                ".png",
                ".jpg",
                ".jpeg",
                ".webp"
            ]

        ]

    def select(
        self,
        material=None,
        style=None,
        scene=None,
        product=None
    ):

        product_images = []

        # البحث الذكي عن المنتج
        if product:

            product_root = (
                self.root
                /
                "products"
            )

            for folder in product_root.rglob(product):

                if folder.is_dir():

                    product_images = [

                        str(file)

                        for file in folder.rglob("*")

                        if file.suffix.lower()
                        in [
                            ".png",
                            ".jpg",
                            ".jpeg",
                            ".webp"
                        ]

                    ]

                    break

        return {

            "product_references":
                product_images,

            "material_references":
                self.scan_folder(
                    f"materials/{material}"
                )
                if material else [],

            "style_references":
                self.scan_folder(
                    f"styles/{style}"
                )
                if style else [],

            "scene_references":
                self.scan_folder(
                    f"scenes/{scene}"
                )
                if scene else []

        }