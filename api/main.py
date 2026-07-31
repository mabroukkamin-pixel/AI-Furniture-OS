from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from runtime.run_pipeline import run


app = FastAPI(
    title="AI Furniture OS API",
    version="1.0.0"
)


class ProductRequest(BaseModel):
    product_id: str


@app.get("/")
def home():

    return {
        "system": "AI Furniture OS",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/generate")
def generate_product(request: ProductRequest):

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