from redis import asyncio as aioredis
from fastapi.testclient import TestClient

from src.conf import REDIS_ADDRESS
from src.contacts import app
from src.db import get_async_session


async def override_session() -> aioredis.Redis:
    """Создание тестовой сессии соединеия с БД"""
    redis = await aioredis.from_url(
        REDIS_ADDRESS, encoding="utf-8", decode_responses=True
    )
    return redis


app.dependency_overrides[get_async_session] = override_session
client = TestClient(app)
