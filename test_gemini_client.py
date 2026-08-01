from runtime.clients.nano_banana_client import NanoBananaClient

client = NanoBananaClient()

result = client.generate(
    prompt="Create a luxury furniture product image",
    image_path="products/Partition001/images/main.png",
    output_folder="test_output"
)

print(result)