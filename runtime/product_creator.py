import re
import shutil
from io import BytesIO
from pathlib import Path

import yaml
from PIL import Image, ImageOps


PRODUCT_ID_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9_-]{1,63}$"
)


def _write_yaml(path, data):
    path.write_text(
        yaml.safe_dump(
            data,
            allow_unicode=True,
            sort_keys=False
        ),
        encoding="utf-8"
    )


def _positive_number(value, field_name):
    number = float(value)

    if number <= 0:
        raise ValueError(
            f"{field_name} must be greater than zero"
        )

    return number


def create_product(
    products_directory,
    *,
    product_id,
    name,
    category,
    material,
    width,
    height,
    depth,
    price,
    currency,
    image_data,
):
    product_id = product_id.strip()
    name = name.strip()
    category = category.strip()
    material = material.strip()
    currency = currency.strip().upper()

    if not PRODUCT_ID_PATTERN.fullmatch(
        product_id
    ):
        raise ValueError(
            "Invalid product ID"
        )

    if product_id.startswith(
        (".", "_")
    ):
        raise ValueError(
            "Invalid product ID"
        )

    if not name:
        raise ValueError(
            "Product name is required"
        )

    if not category:
        raise ValueError(
            "Product category is required"
        )

    if not material:
        raise ValueError(
            "Primary material is required"
        )

    if not currency:
        raise ValueError(
            "Currency is required"
        )

    width = _positive_number(
        width,
        "width"
    )

    height = _positive_number(
        height,
        "height"
    )

    price = _positive_number(
        price,
        "price"
    )

    if depth in (
        None,
        "",
    ):
        depth = None
    else:
        depth = _positive_number(
            depth,
            "depth"
        )

    if not image_data:
        raise ValueError(
            "Product image is required"
        )

    products_directory = Path(
        products_directory
    ).resolve()

    product_directory = (
        products_directory / product_id
    )

    if product_directory.exists():
        raise FileExistsError(
            f"Product already exists: {product_id}"
        )

    try:
        with Image.open(
            BytesIO(image_data)
        ) as uploaded_image:
            uploaded_image.verify()

        with Image.open(
            BytesIO(image_data)
        ) as uploaded_image:
            product_image = (
                ImageOps.exif_transpose(
                    uploaded_image
                )
            )

            product_image.load()

            product_directory.mkdir(
                parents=False
            )

            images_directory = (
                product_directory / "images"
            )

            images_directory.mkdir()

            size = {
                "width": width,
                "height": height,
            }

            if depth is not None:
                size["depth"] = depth

            identity = {
                "product": {
                    "id": product_id,
                    "name": name,
                    "category": category,
                    "family": [
                        "furniture",
                    ],
                    "material": {
                        "primary": material,
                        "secondary": [],
                    },
                    "style": [
                        "modern",
                        "luxury",
                    ],
                    "usage": [],
                    "size": size,
                    "colors": {
                        "primary": [],
                    },
                    "handmade": False,
                    "premium": True,
                    "transparent": False,
                    "movable": True,
                }
            }

            behavior = {
                "behavior": {
                    "preserve": [
                        "dimensions",
                        "proportions",
                        "texture",
                        "color",
                        "construction",
                    ],
                    "emphasize": [
                        "material",
                        "quality",
                        "premium",
                    ],
                    "avoid": [
                        "redesign",
                        "extra_objects",
                        "plastic_look",
                    ],
                },
                "preferred_backgrounds": [
                    "luxury_villa",
                ],
                "preferred_lighting": [
                    "warm",
                    "soft_daylight",
                ],
                "preferred_camera": [
                    "furniture_standard",
                ],
                "output": {
                    "feeling": "luxury",
                    "realism": "maximum",
                },
            }

            marketing = {
                "marketing": {
                    "audience": [
                        "gulf_home",
                        "luxury_buyers",
                    ],
                    "emotion": [
                        "luxury",
                        "comfort",
                        "elegance",
                    ],
                    "platform": [
                        "instagram",
                        "facebook",
                    ],
                    "selling_points": [
                        material,
                        "premium_quality",
                    ],
                }
            }

            pricing = {
                "pricing": {
                    "currency": currency,
                    "price": price,
                    "category": "standard",
                }
            }

            photography = {
                "photography": {
                    "shot": "hero",
                    "lens": "auto",
                    "angle": "auto",
                    "composition": "auto",
                }
            }

            environment = {
                "environment": {
                    "preferred": [
                        "luxury_villa",
                        "resort",
                    ],
                    "forbidden": [
                        "warehouse",
                    ],
                }
            }

            branding = {
                "branding": {
                    "company": "Chinese Market",
                    "arabic": "السوق الصيني",
                    "market": "Kuwait",
                    "audience": [
                        "gulf_home",
                        "luxury_buyers",
                    ],
                    "colors": {
                        "primary": [
                            "royal_blue",
                            "gold",
                            "white",
                        ]
                    },
                    "style": [
                        "premium",
                        "luxury",
                        "modern",
                    ],
                    "communication": {
                        "tone": "elegant",
                        "message":
                            "quality_home_furniture",
                    },
                }
            }

            _write_yaml(
                product_directory / "identity.yaml",
                identity
            )

            _write_yaml(
                product_directory / "behavior.yaml",
                behavior
            )

            _write_yaml(
                product_directory / "marketing.yaml",
                marketing
            )

            _write_yaml(
                product_directory / "pricing.yaml",
                pricing
            )

            _write_yaml(
                product_directory / "photography.yaml",
                photography
            )

            _write_yaml(
                product_directory / "environment.yaml",
                environment
            )

            _write_yaml(
                product_directory / "branding.yaml",
                branding
            )

            product_image.save(
                images_directory / "main.png",
                format="PNG"
            )

    except Exception:
        if product_directory.exists():
            shutil.rmtree(
                product_directory
            )
        raise

    return product_directory