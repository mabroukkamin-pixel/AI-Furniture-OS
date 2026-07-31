from pathlib import Path

from brain.reference_engine.reference_loader import ReferenceLoader

loader = ReferenceLoader(
    Path("reference")
)

index = loader.load()

print(index.images)