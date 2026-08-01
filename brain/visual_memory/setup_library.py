from pathlib import Path

LIBRARY = [
    "partition",
    "console",
    "cabinet",
    "sofa",
    "table",
    "chair",
    "bed",
    "dining",
]

BASE_DIR = Path(__file__).parent / "library"


def setup_library():

    BASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    for category in LIBRARY:

        (
            BASE_DIR / category
        ).mkdir(
            exist_ok=True
        )

    print("Visual Memory Library Ready")
    print(BASE_DIR)


if __name__ == "__main__":
    setup_library()