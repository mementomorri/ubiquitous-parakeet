from fastapi import FastAPI

from src.router import router as contacts_router


app = FastAPI(
    title="Контактная книга - задание первое",
    description="RESTful сервис работающий как контактная книга",
    version="1.0",
)
# Подключение роутера для обработки запросов к контактной книге
app.include_router(contacts_router)
