from redis import asyncio as aioredis

from src.conf import REDIS_ADDRESS


async def get_async_session() -> aioredis.Redis:
    """Создание новой асинхронной сессии соединеия с БД"""
    redis = await aioredis.from_url(
        REDIS_ADDRESS, encoding="utf-8", decode_responses=True
    )
    return redis
