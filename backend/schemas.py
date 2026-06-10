from pydantic import BaseModel


class ReviewRequest(BaseModel):
    review: str


class ProductRequest(BaseModel):
    product_id: str


class HealthResponse(BaseModel):
    status: str