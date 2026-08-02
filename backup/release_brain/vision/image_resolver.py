import os


class ImageResolver:

    def find_product_image(self, product_path):

        images_path = os.path.join(
            product_path,
            "images"
        )

        if not os.path.exists(images_path):

            raise Exception(
                f"No images folder found: {images_path}"
            )

        supported = [
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        ]

        images = []

        for file in os.listdir(images_path):

            ext = os.path.splitext(file)[1].lower()

            if ext in supported:

                images.append(
                    os.path.join(
                        images_path,
                        file
                    )
                )

        if not images:
            raise Exception(
                "No product images found"
            )

        images.sort(
            key=lambda path: (
                os.path.basename(path).casefold()
            )
        )

        main_image = next(
            (
                image
                for image in images
                if (
                    os.path.basename(image).casefold()
                    == "main.png"
                )
            ),
            images[0]
        )

        reference_images = [
            image
            for image in images
            if image != main_image
        ]

        return {
            "main_image": main_image,
            "reference_images": reference_images
        }