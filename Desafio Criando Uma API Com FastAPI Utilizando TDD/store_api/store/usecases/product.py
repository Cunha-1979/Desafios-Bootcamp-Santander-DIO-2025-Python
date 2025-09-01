from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from pymongo import ReturnDocument

from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

        # índice útil (ex.: nome único). remova unique=True se não quiser unicidade
        try:
            self.collection.create_index([("name", pymongo.ASCENDING)], unique=False)
        except Exception:
            # em ambiente CI/local sem permissões, ignore
            pass

    async def create(self, body: ProductIn) -> ProductOut:
        product = ProductModel(**body.model_dump())
        await self.collection.insert_one(product.model_dump())
        return ProductOut.model_validate(product.model_dump())

    async def list(self) -> List[ProductOut]:
        cursor = self.collection.find({}).sort("created_at", pymongo.DESCENDING)
        items: list[ProductOut] = []
        async for doc in cursor:
            items.append(ProductOut.model_validate(doc))
        return items

    async def get(self, id: UUID) -> ProductOut:
        doc = await self.collection.find_one({"id": id})
        if not doc:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        return ProductOut.model_validate(doc)

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        # aplica apenas campos informados
        payload = body.model_dump(exclude_none=True)
        doc = await self.collection.find_one_and_update(
            {"id": id},
            {"$set": payload},
            return_document=ReturnDocument.AFTER,
        )
        if not doc:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        return ProductUpdateOut.model_validate(doc)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0


product_usecase = ProductUsecase()
