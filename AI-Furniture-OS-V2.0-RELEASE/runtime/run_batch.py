import os
import json

from runtime.run_pipeline import run


PRODUCTS_FOLDER = "products"

OUTPUT_FOLDER = os.path.join(
    "outputs",
    "batch"
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


def discover_products():

    products = []

    if not os.path.exists(PRODUCTS_FOLDER):
        return products

    ignored = {
        "_reference_library",
        "_template",
        "_template_backup",
        "_test_archive",
        "images",
        "__pycache__"
    }

    for item in os.listdir(PRODUCTS_FOLDER):

        path = os.path.join(
            PRODUCTS_FOLDER,
            item
        )

        if (
            os.path.isdir(path)
            and item not in ignored
            and not item.startswith("_")
        ):
            identity_path = os.path.join(
                path,
                "identity.yaml"
            )

            if not os.path.exists(identity_path):
                continue

            products.append(item)

    return sorted(products)


def main():

    report = {
        "success": [],
        "failed": []
    }

    products = discover_products()

    print("=" * 40)
    print("BATCH PRODUCTION")
    print("=" * 40)

    for product in products:

        print(f"\nRunning: {product}")

        try:

            run(product)

            report["success"].append(product)

        except Exception as e:

            print(e)

            report["failed"].append(
                {
                    "product": product,
                    "error": str(e)
                }
            )

    report_path = os.path.join(
        OUTPUT_FOLDER,
        "report.json"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\n")
    print("=" * 40)
    print("BATCH COMPLETE")
    print("=" * 40)

    print("Success :", len(report["success"]))
    print("Failed  :", len(report["failed"]))
    print("Report  :", report_path)


if __name__ == "__main__":
    main()