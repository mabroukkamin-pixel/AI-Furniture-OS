from pathlib import Path

from brain.reference_engine.reference_loader import ReferenceLoader
from brain.reference_engine.reference_selector import ReferenceSelector


loader = ReferenceLoader(
    Path("references")
)

index = loader.load()

print("=" * 50)
print("Products :", index.total_products())
print("Images   :", index.total_images())
print("=" * 50)

selector = ReferenceSelector(index)

images = selector.by_product("partition")

for img in images:
    print(img.filename)