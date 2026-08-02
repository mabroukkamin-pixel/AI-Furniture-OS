from pathlib import Path


class ImageIndex:
    """
    Index للصور المرجعية حسب المنتج.
    """

    def __init__(self):

        self.collections = {}


    def add_product_images(
        self,
        product_type,
        images
    ):

        if product_type not in self.collections:

            self.collections[product_type] = []


        self.collections[product_type].extend(
            images
        )


    def get(
        self,
        product_type
    ):

        return self.collections.get(
            product_type,
            []
        )


    def has(
        self,
        product_type
    ):

        return product_type in self.collections


    def total_products(self):

        return len(
            self.collections
        )


    def total_images(self):

        return sum(
            len(images)
            for images in self.collections.values()
        )