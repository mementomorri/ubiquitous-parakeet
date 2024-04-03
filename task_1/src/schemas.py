from pydantic import BaseModel, ConfigDict


class SContact(BaseModel):
    """Схема возвращаемых данны"""

    address: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"address": "Москвариум, проспект Мира, Москва, Россия."}]
        }
    )


class SContactAdd(SContact):
    """Схема для добавления контакта"""

    phone_number: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "phone": "+7 (111) 111 11-11",
                    "address": "Москвариум, проспект Мира, Москва, Россия.",
                }
            ]
        },
    )


class SContactUpdate(SContact):
    """
    Схема для обновления адреса контакта.
    Да, она похожа на схему добавления контакта,
    но, если мы захотим расширить информацию о
    контакте, например, добавим дату создания,
    имя, идентификатор, то обновлять потребуется
    не каждое поле, а лишь некоторые из них.
    Для таких целей и нужна отдельная схема.
    """

    phone_number: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "phone": "+7 (111) 111 11-11",
                    "address": "Москвариум, проспект Мира, Москва, Россия.",
                }
            ]
        },
    )


class SResponse(BaseModel):
    """Схема ответа на запросы пользователя"""

    status: str
    details: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "ok",
                    "details": "Операция прошла успешно",
                }
            ]
        }
    )
