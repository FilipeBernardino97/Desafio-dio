from fastapi import APIRouter, status, HTTPException
from src.schemas.product import ProductIn, ProductOut
from src.usecases.product import product_usecase

product_router = APIRouter(prefix="/products", tags=["Products"])

@product_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def create_product(body: ProductIn):
    try:
        product = await product_usecase.create(body)
        return product
    except Exception as e:
        # Tratamento da exceção personalizada do Use Case
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )