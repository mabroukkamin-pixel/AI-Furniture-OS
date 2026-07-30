from brain.reference_engine.reference_metadata import ReferenceMetadata


meta = ReferenceMetadata(
    "references/partition/reference.yaml"
)

data = meta.load()

print("="*50)
print(data)
print("="*50)