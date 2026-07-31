import json
from pathlib import Path

import yaml
from fastapi import (
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.responses import (
    FileResponse,
    JSONResponse,
)
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from runtime.run_pipeline import run
from runtime.product_creator import (
    create_product,
    update_product,
)
from runtime.product_archive import (
    archive_product,
    list_archived_products,
    restore_product,
)
from runtime.config.settings import (
    GEMINI_MODEL,
    is_gemini_configured,
)


PROJECT_ROOT = Path(
    __file__
).resolve().parents[1]

PRODUCTS_DIR = (
    PROJECT_ROOT / "products"
)

PRODUCT_ARCHIVE_DIR = (
    PROJECT_ROOT / "product_archive"
)

OUTPUTS_DIR = (
    PROJECT_ROOT / "outputs"
)

UI_DIR = (
    PROJECT_ROOT / "ui"
)

MAX_PRODUCT_IMAGE_BYTES = (
    20 * 1024 * 1024
)


app = FastAPI(
    title="AI Furniture OS API",
    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(
        directory=UI_DIR / "static"
    ),
    name="static"
)


class ProductRequest(BaseModel):
    product_id: str


def _safe_child_directory(
    root: Path,
    name: str
):
    if (
        not name
        or Path(name).name != name
        or name in {".", ".."}
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid product ID"
        )

    resolved_root = root.resolve()
    candidate = (
        resolved_root / name
    ).resolve()

    try:
        candidate.relative_to(
            resolved_root
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid path"
        ) from exc

    return candidate


def _require_product(
    product_id: str
):
    product_directory = (
        _safe_child_directory(
            PRODUCTS_DIR,
            product_id
        )
    )

    if not product_directory.is_dir():
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product_directory


def _read_yaml_mapping(path: Path):

    try:
        data = yaml.safe_load(
            path.read_text(
                encoding="utf-8"
            )
        )
    except (
        OSError,
        UnicodeError,
        yaml.YAMLError
    ):
        return {}

    if isinstance(data, dict):
        return data

    return {}


def _product_display_name(
    product_directory: Path
):
    identity_path = (
        product_directory / "identity.yaml"
    )

    identity = _read_yaml_mapping(
        identity_path
    )

    if not isinstance(identity, dict):
        return product_directory.name

    product = identity.get(
        "product",
        {}
    )

    if not isinstance(product, dict):
        return product_directory.name

    name = product.get(
        "name"
    )

    if (
        isinstance(name, str)
        and name.strip()
    ):
        return name.strip()

    return product_directory.name


@app.get("/")
def home():

    return {
        "system": "AI Furniture OS",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/system/readiness")
def system_readiness():

    configured = (
        is_gemini_configured()
    )

    return {
        "api": "ready",
        "image_engine": {
            "name": "nano_banana",
            "configured": configured,
            "mode": (
                "remote"
                if configured
                else "local"
            ),
            "model": GEMINI_MODEL,
        }
    }


@app.get(
    "/dashboard",
    include_in_schema=False
)
def dashboard():

    return FileResponse(
        UI_DIR / "index.html"
    )


@app.get("/products")
def list_products():

    products = []

    if PRODUCTS_DIR.is_dir():

        for product_directory in sorted(
            PRODUCTS_DIR.iterdir(),
            key=lambda item: (
                item.name.casefold()
            )
        ):

            if (
                product_directory.is_dir()
                and not product_directory.name.startswith(
                    (".", "_")
                )
                and product_directory.name != "images"
            ):
                products.append(
                    {
                        "id":
                            product_directory.name,
                        "name":
                            _product_display_name(
                                product_directory
                            )
                    }
                )

    return {
        "products": products
    }


@app.post(
    "/products",
    status_code=201
)
async def create_product_endpoint(
    product_id: str = Form(...),
    name: str = Form(...),
    category: str = Form(...),
    material: str = Form(...),
    width: float = Form(...),
    height: float = Form(...),
    depth: float | None = Form(None),
    price: float = Form(...),
    currency: str = Form("KWD"),
    image: UploadFile = File(...),
):
    image_data = await image.read(
        MAX_PRODUCT_IMAGE_BYTES + 1
    )

    await image.close()

    if len(image_data) > MAX_PRODUCT_IMAGE_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Product image is too large"
        )

    try:
        product_directory = create_product(
            PRODUCTS_DIR,
            product_id=product_id,
            name=name,
            category=category,
            material=material,
            width=width,
            height=height,
            depth=depth,
            price=price,
            currency=currency,
            image_data=image_data,
        )
    except FileExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail="Product already exists"
        ) from exc
    except (
        ValueError,
        OSError
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    return {
        "status": "created",
        "product": {
            "id": product_directory.name,
            "name": name.strip(),
            "image_url": (
                f"/products/"
                f"{product_directory.name}"
                "/image"
            ),
        }
    }


@app.put("/products/{product_id}")
async def update_product_endpoint(
    product_id: str,
    name: str = Form(...),
    category: str = Form(...),
    material: str = Form(...),
    width: float = Form(...),
    height: float = Form(...),
    depth: float | None = Form(None),
    price: float = Form(...),
    currency: str = Form("KWD"),
    image: UploadFile | None = File(None),
):
    image_data = None

    if image is not None:
        image_data = await image.read(
            MAX_PRODUCT_IMAGE_BYTES + 1
        )

        await image.close()

        if len(image_data) > MAX_PRODUCT_IMAGE_BYTES:
            raise HTTPException(
                status_code=413,
                detail="Product image is too large"
            )

    try:
        product_directory = update_product(
            PRODUCTS_DIR,
            product_id=product_id,
            name=name,
            category=category,
            material=material,
            width=width,
            height=height,
            depth=depth,
            price=price,
            currency=currency,
            image_data=image_data,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        ) from exc
    except (
        ValueError,
        OSError
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    return {
        "status": "updated",
        "product": {
            "id": product_directory.name,
            "name": name.strip(),
            "image_url": (
                f"/products/"
                f"{product_directory.name}"
                "/image"
            ),
        }
    }


@app.delete("/products/{product_id}")
def archive_product_endpoint(
    product_id: str
):
    try:
        archived_directory = archive_product(
            PRODUCTS_DIR,
            PRODUCT_ARCHIVE_DIR,
            product_id,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        ) from exc
    except (
        ValueError,
        OSError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    return {
        "status": "archived",
        "product_id": product_id,
        "archive_id": archived_directory.name,
    }


@app.get("/product-archive")
def get_product_archive():

    return {
        "products": list_archived_products(
            PRODUCT_ARCHIVE_DIR
        )
    }


@app.post(
    "/product-archive/{archive_id}/restore"
)
def restore_product_endpoint(
    archive_id: str
):
    try:
        product_directory = restore_product(
            PRODUCTS_DIR,
            PRODUCT_ARCHIVE_DIR,
            archive_id,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Archived product not found"
        ) from exc
    except FileExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail="Product already exists"
        ) from exc
    except (
        ValueError,
        OSError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    return {
        "status": "restored",
        "product": {
            "id": product_directory.name,
            "image_url": (
                f"/products/"
                f"{product_directory.name}"
                "/image"
            ),
        }
    }


@app.get("/products/{product_id}")
def get_product(product_id: str):

    product_directory = _require_product(
        product_id
    )

    identity_data = _read_yaml_mapping(
        product_directory / "identity.yaml"
    )

    pricing_data = _read_yaml_mapping(
        product_directory / "pricing.yaml"
    )

    product = identity_data.get(
        "product",
        {}
    )

    pricing = pricing_data.get(
        "pricing",
        {}
    )

    if not isinstance(product, dict):
        product = {}

    if not isinstance(pricing, dict):
        pricing = {}

    return {
        "id": product_directory.name,
        "name": (
            product.get("name")
            or product_directory.name
        ),
        "category": product.get(
            "category"
        ),
        "material": product.get(
            "material",
            {}
        ),
        "size": product.get(
            "size",
            {}
        ),
        "colors": product.get(
            "colors",
            {}
        ),
        "pricing": pricing,
        "image_url": (
            f"/products/{product_directory.name}/image"
        )
    }


@app.get("/products/{product_id}/image")
def get_product_image(product_id: str):

    product_directory = _require_product(
        product_id
    )

    images_directory = (
        product_directory / "images"
    )

    supported_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    }

    main_image = (
        images_directory / "main.png"
    )
    if main_image.is_file():
        image_files = [
            main_image
        ]
    elif images_directory.is_dir():
        image_files = sorted(
            path
            for path in images_directory.iterdir()
            if (
                path.is_file()
                and path.suffix.lower()
                in supported_extensions
            )
        )
    else:
        image_files = []

    if not image_files:
        raise HTTPException(
            status_code=404,
            detail="Product image not found"
        )

    return FileResponse(
        image_files[0]
    )


@app.get("/runs/{product_id}/latest")
def get_latest_run(product_id: str):

    _require_product(product_id)

    output_directory = _safe_child_directory(
        OUTPUTS_DIR,
        product_id
    )

    manifest_path = (
        output_directory / "manifest.json"
    )

    if not manifest_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="No saved run found"
        )

    try:
        manifest = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError
    ) as exc:
        raise HTTPException(
            status_code=500,
            detail="Saved run manifest is invalid"
        ) from exc

    if not isinstance(manifest, dict):
        raise HTTPException(
            status_code=500,
            detail="Saved run manifest is invalid"
        )

    return manifest


@app.get(
    "/outputs/{product_id}/{artifact_path:path}",
    include_in_schema=False
)
def get_output_artifact(
    product_id: str,
    artifact_path: str
):

    product_output = (
        _safe_child_directory(
            OUTPUTS_DIR,
            product_id
        )
    )

    resolved_output = (
        product_output.resolve()
    )

    requested_file = (
        resolved_output
        / artifact_path
    ).resolve()

    try:
        requested_file.relative_to(
            resolved_output
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid artifact path"
        ) from exc

    if not requested_file.is_file():
        raise HTTPException(
            status_code=404,
            detail="Artifact not found"
        )

    return FileResponse(
        requested_file
    )


@app.post("/generate")
def generate_product(
    request: ProductRequest
):

    _require_product(
        request.product_id
    )

    result = run(
        request.product_id
    )

    generation = result.get(
        "generation",
        {}
    )

    generation_status = generation.get(
        "status",
        "unknown"
    )

    api_status = (
        "succeeded"
        if generation_status == "success"
        else "failed"
    )

    response_data = {
        "product": request.product_id,
        "status": api_status,
        "generation_status": generation_status,
        "result": result
    }

    if generation_status == "local_only":
        return JSONResponse(
            status_code=503,
            content=response_data
        )

    if generation_status != "success":
        return JSONResponse(
            status_code=502,
            content=response_data
        )

    return response_data