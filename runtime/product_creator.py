import re
import shutil
from io import BytesIO
from pathlib import Path

import yaml
from fastapi import Form, UploadFile, File, HTTPException
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
    name_ar=None,
    name_en=None,
    secondary_material=None,
    color=None,
):
    product_id = product_id.strip()
    name = name.strip()
    category = category.strip()
    material = material.strip()
    currency = currency.strip().upper()

    name_ar = (
        None
        if name_ar is None
        else name_ar.strip()
    )

    name_en = (
        None
        if name_en is None
        else name_en.strip()
    )

    secondary_material = (
        None
        if secondary_material is None
        else secondary_material.strip()
    )

    color = (
        None
        if color is None
        else color.strip()
    )

    display_name = (
        name_ar
        or name_en
        or name
    )

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

    if not display_name:
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
                    "name": display_name,
                    "name_ar": (
                        name_ar or display_name
                    ),
                    "name_en": name_en,
                    "category": category,
                    "family": [
                        "furniture",
                    ],
                    "material": {
                        "primary": material,
                        "secondary": (
                            [secondary_material]
                            if secondary_material
                            else []
                        ),
                    },
                    "style": [
                        "modern",
                        "luxury",
                    ],
                    "usage": [],
                    "size": size,
                    "colors": {
                        "primary": (
                            [color]
                            if color
                            else []
                        ),
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


def update_product(
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
    image_data=None,
    name_ar=None,
    name_en=None,
    secondary_material=None,
    color=None,
):
    product_id = product_id.strip()
    name = name.strip()
    category = category.strip()
    material = material.strip()
    currency = currency.strip().upper()

    name_ar = (
        None
        if name_ar is None
        else name_ar.strip()
    )

    name_en = (
        None
        if name_en is None
        else name_en.strip()
    )

    secondary_material = (
        None
        if secondary_material is None
        else secondary_material.strip()
    )

    color = (
        None
        if color is None
        else color.strip()
    )

    display_name = (
        name_ar
        or name_en
        or name
    )

    if (
        not PRODUCT_ID_PATTERN.fullmatch(product_id)
        or product_id.startswith((".", "_"))
    ):
        raise ValueError("Invalid product ID")

    if not display_name:
        raise ValueError("Product name is required")

    if not category:
        raise ValueError("Product category is required")

    if not material:
        raise ValueError("Primary material is required")

    if not currency:
        raise ValueError("Currency is required")

    width = _positive_number(width, "width")
    height = _positive_number(height, "height")
    price = _positive_number(price, "price")

    if depth in (None, ""):
        depth = None
    else:
        depth = _positive_number(
            depth,
            "depth"
        )

    products_directory = Path(
        products_directory
    ).resolve()

    product_directory = (
        products_directory / product_id
    )

    if not product_directory.is_dir():
        raise FileNotFoundError(
            f"Product not found: {product_id}"
        )

    prepared_image = None

    if image_data:
        with Image.open(
            BytesIO(image_data)
        ) as uploaded_image:
            uploaded_image.verify()

        with Image.open(
            BytesIO(image_data)
        ) as uploaded_image:
            product_image = ImageOps.exif_transpose(
                uploaded_image
            )

            product_image.load()

            image_buffer = BytesIO()

            product_image.save(
                image_buffer,
                format="PNG"
            )

            prepared_image = image_buffer.getvalue()

    identity_path = (
        product_directory / "identity.yaml"
    )

    pricing_path = (
        product_directory / "pricing.yaml"
    )

    identity = yaml.safe_load(
        identity_path.read_text(
            encoding="utf-8"
        )
    ) or {}

    pricing = yaml.safe_load(
        pricing_path.read_text(
            encoding="utf-8"
        )
    ) or {}

    product = identity.setdefault(
        "product",
        {}
    )

    material_data = product.setdefault(
        "material",
        {}
    )

    size = {
        "width": width,
        "height": height,
    }

    if depth is not None:
        size["depth"] = depth

    product["id"] = product_id
    product["name"] = display_name

    if name_ar is not None:
        product["name_ar"] = name_ar
    else:
        product.setdefault(
            "name_ar",
            display_name
        )

    if name_en is not None:
        product["name_en"] = name_en
    else:
        product.setdefault(
            "name_en",
            ""
        )

    product["category"] = category
    material_data["primary"] = material

    if secondary_material is not None:
        material_data["secondary"] = (
            [secondary_material]
            if secondary_material
            else []
        )
    else:
        material_data.setdefault(
            "secondary",
            []
        )

    product["size"] = size

    colors_data = product.setdefault(
        "colors",
        {}
    )

    if color is not None:
        colors_data["primary"] = (
            [color]
            if color
            else []
        )
    else:
        colors_data.setdefault(
            "primary",
            []
        )

    pricing_data = pricing.setdefault(
        "pricing",
        {}
    )

    pricing_data["currency"] = currency
    pricing_data["price"] = price
    pricing_data.setdefault(
        "category",
        "standard"
    )

    _write_yaml(
        identity_path,
        identity
    )

    _write_yaml(
        pricing_path,
        pricing
    )

    if prepared_image is not None:
        images_directory = (
            product_directory / "images"
        )

        images_directory.mkdir(
            exist_ok=True
        )

        (
            images_directory / "main.png"
        ).write_bytes(
            prepared_image
        )

    return product_directory


async def create_product_endpoint(
    product_id: str = Form(...),
    name: str = Form(...),
    name_ar: str | None = Form(None),
    name_en: str | None = Form(None),
    category: str = Form(...),
    material: str = Form(...),
    secondary_material: str | None = Form(None),
    color: str | None = Form(None),
    width: float = Form(...),
    height: float = Form(...),
    depth: float | None = Form(None),
    price: float = Form(...),
    currency: str = Form(...),
    image: UploadFile = File(...),
):
    try:
        image_bytes = await image.read()
        product_dir = Path("products")
        create_product(
            product_dir,
            product_id=product_id,
            name=name,
            name_ar=name_ar,
            name_en=name_en,
            category=category,
            material=material,
            secondary_material=secondary_material,
            color=color,
            width=width,
            height=height,
            depth=depth,
            price=price,
            currency=currency,
            image_data=image_bytes,
        )
        return {"status": "success", "product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def update_product_endpoint(
    product_id: str = Form(...),
    name: str = Form(...),
    name_ar: str | None = Form(None),
    name_en: str | None = Form(None),
    category: str = Form(...),
    material: str = Form(...),
    secondary_material: str | None = Form(None),
    color: str | None = Form(None),
    width: float = Form(...),
    height: float = Form(...),
    depth: float | None = Form(None),
    price: float = Form(...),
    currency: str = Form(...),
    image: UploadFile | None = File(None),
):
    try:
        image_bytes = await image.read() if image else None
        product_dir = Path("products")
        update_product(
            product_dir,
            product_id=product_id,
            name=name,
            name_ar=name_ar,
            name_en=name_en,
            category=category,
            material=material,
            secondary_material=secondary_material,
            color=color,
            width=width,
            height=height,
            depth=depth,
            price=price,
            currency=currency,
            image_data=image_bytes,
        )
        return {"status": "success", "product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))