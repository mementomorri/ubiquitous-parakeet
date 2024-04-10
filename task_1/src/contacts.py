from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.router import router as contacts_router
from src.db import get_async_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.session_pool = await get_async_session()
    yield
    await app.state.session_pool.close()


app = FastAPI(
    title="Контактная книга - задание первое",
    description="RESTful сервис работающий как контактная книга",
    version="1.0",
    lifespan=lifespan,
)
# Подключение роутера для обработки запросов к контактной книге
app.include_router(contacts_router)
