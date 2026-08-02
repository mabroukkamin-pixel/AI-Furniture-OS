from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict


@dataclass
class ReferenceImage:
    """
    يمثل صورة مرجعية واحدة داخل النظام.
    """

    filename: str
    path: Path

    product_type: str

    tags: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    score: float = 0.0


@dataclass
class ReferenceCollection:
    """
    يمثل جميع الصور الخاصة بنوع منتج واحد.
    """

    product_type: str

    images: List[ReferenceImage] = field(default_factory=list)

    def add(self, image: ReferenceImage):
        self.images.append(image)

    def count(self):
        return len(self.images)