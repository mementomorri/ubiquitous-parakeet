from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from src.schemas import SContact, SContactAdd, SContactUpdate, SResponse
from src.db import get_async_session


# Роутер для обработки запросов к конечным точкам
router = APIRouter(prefix="", tags=["Обработка данных контактной книги"])


@router.get(
    "/check_data",
    response_model=SContact,
)
async def check_contact(
    phone_number: str, session=Depends(get_async_session)
) -> SContact:
    """Возвращает адрес по номеру телефона"""
    address = await session.get(phone_number)
    if not address:
        raise HTTPException(
            status_code=404, detail="Коктакт не найден в контактной книге"
        )
    return SContact.model_validate({"address": address})


@router.post(
    "/write_data",
    response_model=SResponse,
    status_code=status.HTTP_201_CREATED,
)
async def write_contact(
    contact: Annotated[SContactAdd, Depends()], session=Depends(get_async_session)
) -> SResponse:
    """Добавляет новый контакт в контактную книгу"""
    try:
        await session.set(contact.phone_number, contact.address)
        return SResponse.model_validate(
            {
                "status": "ok",
                "details": "Контакт успешно добавлен в контактную книгу",
            }
        )
    except ValidationError:
        raise HTTPException(
            status_code=422,
            detail="Ошибка валидации, переданы некорректные данные, попробуйсте снова",
        )


@router.patch(
    "/write_data", response_model=SResponse, status_code=status.HTTP_202_ACCEPTED
)
async def update_contact(
    updated_contact: Annotated[SContactUpdate, Depends()],
    session=Depends(get_async_session),
) -> SResponse:
    """Изменяет адрес контакта"""
    address = await session.get(updated_contact.phone_number)
    if not address:
        raise HTTPException(
            status_code=404, detail="Коктакт не найден в контактной книге"
        )
    try:
        await session.set(updated_contact.phone_number, updated_contact.address)
        return SResponse.model_validate(
            {"status": "ok", "details": "Адрес контакта успешно обновлен"}
        )
    except ValidationError:
        raise HTTPException(
            status_code=422,
            detail="Ошибка валидации, переданы некорректные данные, попробуйсте снова",
        )
