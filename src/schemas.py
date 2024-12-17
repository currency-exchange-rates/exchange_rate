from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class CurrencySchemaBase(BaseModel):
    """Базоваия pydantic схема для модели Currency."""

    code: Optional[str] = Field(
        ...,
        title="Code currency",
        description=(
            "Код валюты для API, длина кода ровно 3 символа"
        )
    )
    name: Optional[str] = Field(
        ...,
        title="Name currency",
        description="Название валюты, длина имени до 50 символов",
    )
    country: Optional[str] = Field(
        ...,
        title="name country",
        description="Страна,длина имени страны до 100 символов"
    )

    class Config:
        schema_extra: dict[str, Any] = {
            "example": {
                "code": "USD",
                "name": "United States Dollar",
                "country": "United States"
            }
        }

    @field_validator("code")
    def validate_code(cls, value: str) -> str | ValueError:
        """Валидация поля code."""
        if len(value) != 3:
            except_message = (
                f"Код {value} должен быть длинной ровно 3 символа."
            )
            raise ValueError(except_message)

        if not value.isupper():
            except_message = (
                f"У кода {value} должны быть все заглавные символы."
            )
            raise ValueError(except_message)

        if not (value.isascii() and value.isalpha()):
            except_message = (
                f"У кода {value} все символы должны быть Английской раскладки."
            )
            raise ValueError(except_message)

        return value

    @field_validator("name")
    def validate_name(cls, value: str) -> str | ValueError:
        """Валидация поля name."""
        if 0 < len(value) <= 50:
            return value
        except_message = (
            f"У длины имени валюты {value} должно быть до 50 символов."
        )
        raise ValueError(except_message)

    @field_validator("country")
    def validate_country(cls, value: str) -> str | ValueError:
        """Валидация поля country."""
        if 0 < len(value) <= 100:
            return value
        except_message = (
            f"У длины имени страны {value} должно быть до 100 символов."
        )
        raise ValueError(except_message)


class CurrencySchemaCreate(CurrencySchemaBase):
    """Схема для создания объекта"""
    code: Optional[str] = Field(
        title="Code currency",
        description=(
            "Код валюты для API, обязателен, длина кода ровно 3 символа"
        )
    )
    name: Optional[str] = Field(
        title="Name currency",
        description="Название валюты, обязателен, длина имени до 50 символов",
    )
    country: Optional[str] = Field(
        title="name country",
        description="Страна, обязательно, длина имени страны до 100 символов"
    )


class CurrencySchemaUpdate(CurrencySchemaBase):
    """Схема для обновления объекта."""
    pass


class CurrencySchemaDB(CurrencySchemaBase):
    """Схема объекта из базы данных"""
    id: int = Field(
        title="Id Currency in db",
        description="Айди валюты в базе данных.",
    )

    class Config:
        """Config for this schemas."""

        orm_mode: bool = True
