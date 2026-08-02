from collections import defaultdict

from .reference_models import ReferenceImage


class ImageIndex:

    def __init__(self):
        self._images = defaultdict(list)

    def add(self, image: ReferenceImage):
        self._images[image.product_type].append(image)

    def get(self, product_type: str):
        return self._images.get(product_type, [])

    def all_types(self):
        return list(self._images.keys())

    def count(self):
        return sum(len(v) for v in self._images.values())

    def total_products(self):
        return len(self._images)

    def total_images(self):
        return self.count()