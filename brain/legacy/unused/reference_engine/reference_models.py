from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ReferenceImage:
    filename: str
    path: Path
    product_type: str