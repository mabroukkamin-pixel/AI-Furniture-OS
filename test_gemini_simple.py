from runtime.clients.nano_banana_client import NanoBananaClient

client = NanoBananaClient()

result = client.generate(
    prompt="luxury interior room with rattan furniture",
    image_path="products/Partition001/images/main.png",
    output_folder="outputs/test"
)

print(result)