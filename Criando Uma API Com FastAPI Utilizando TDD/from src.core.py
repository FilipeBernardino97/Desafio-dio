from src.core.database import db_client
from src.schemas.product import ProductIn, ProductOut
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Dict, Any

class ProductUsecase:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = db_client.db.products

    async def create(self, body: ProductIn) -> ProductOut:
        try:
            insert_result = await self.collection.insert_one(body.dict())
            product_data = await self.collection.find_one({"_id": insert_result.inserted_id})
            return ProductOut.parse_obj(product_data)
        except Exception as e:
            # Capturando um erro genérico do banco e transformando em uma exceção amigável
            print(f"Erro ao inserir produto: {e}")
            raise Exception("Erro ao criar produto. Por favor, tente novamente mais tarde.")

product_usecase = ProductUsecase()