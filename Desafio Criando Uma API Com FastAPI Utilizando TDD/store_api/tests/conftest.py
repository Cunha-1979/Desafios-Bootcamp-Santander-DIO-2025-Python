import os
import asyncio
import pytest
from httpx import AsyncClient
from uuid import UUID

# garanta que os testes usam um banco isolado
os.environ.setdefault("DATABASE_URL", "mongodb://localhost:27017/store_test")

from store.main import app  # noqa: E402
from store.db.mongo import db_client  # noqa: E402
from store.schemas.product import ProductIn, ProductUpdate  # noqa: E402
from store.usecases.product import product_usecase  # noqa: E402
from tests.factories import product_data, products_data  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
def products_url():
    return "/products/"


@pytest.fixture(autouse=True)
async def reset_db():
    # limpa a coleção antes de cada teste
    db = db_client.get().get_database()
    await db.get_collection("products").delete_many({})
    yield


@pytest.fixture
def product_in():
    return ProductIn(**product_data())


@pytest.fixture
def product_update():
    return ProductUpdate(quantity=99, status=False)


@pytest.fixture
async def product_inserted(product_in):
    return await product_usecase.create(body=product_in)


@pytest.fixture
def products_in():
    return [ProductIn(**p) for p in products_data()]


@pytest.fixture
async def products_inserted(products_in):
    return [await product_usecase.create(body=pi) for pi in products_in]
