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


        # أول صورة تعتبر الصورة الرئيسية

        return {
            "main_image": images[0],
            "reference_images": images
        }