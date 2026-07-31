from brain.product_engine.product_loader import ProductLoader


loader = ProductLoader(
    "products/Partition001/product.yaml"
)


product = loader.load()


print("="*50)
print(product)
print("="*50)