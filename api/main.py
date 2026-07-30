from fastapi import FastAPI
from pydantic import BaseModel

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

    return {
        "product": request.product_id,
        "status": "success",
        "result": result
    }