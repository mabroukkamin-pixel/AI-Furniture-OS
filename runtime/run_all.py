import os
import subprocess
import sys

PRODUCTS_DIR = "products"

SKIP = {
    "_template",
    "_template_backup",
    "_reference_library",
    "_test_archive",
    "images",
}

products = []

for item in os.listdir(PRODUCTS_DIR):

    path = os.path.join(PRODUCTS_DIR, item)

    if not os.path.isdir(path):
        continue

    if item in SKIP:
        continue

    products.append(item)

print("=" * 50)
print("FOUND PRODUCTS")
print("=" * 50)

for p in products:
    print("-", p)

print()

success = 0
failed = 0

for product in products:

    print("=" * 50)
    print("RUNNING:", product)
    print("=" * 50)

    result = subprocess.run([
        sys.executable,
        "-m",
        "runtime.run_pipeline",
        "--product",
        product
    ])

    if result.returncode == 0:
        success += 1
    else:
        failed += 1

print()
print("=" * 50)
print("SUMMARY")
print("=" * 50)
print("SUCCESS :", success)
print("FAILED  :", failed)
print("TOTAL   :", len(products))