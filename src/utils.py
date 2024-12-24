from pathlib import Path

from pydantic import TypeAdapter
from pydantic_core import ValidationError
from flask import abort
from flask_sqlalchemy import SQLAlchemy

from src.schemas import CurrencySchemaCreate
from src.repository import RepositoryCurrency


def add_data_from_json(json_path: Path, db: SQLAlchemy) -> None:
    """Добавляет данные из json."""
    currency_repository = RepositoryCurrency(db)
    currency_adapter = TypeAdapter(list[CurrencySchemaCreate])

    if not json_path.is_file():
        raise FileNotFoundError(
            f"Файла по пути {json_path} нет, данные не будут добавлены."
        )

    with open(json_path, mode="r", encoding="utf-8") as json_file:
        json_data = json_file.read()
        if not json_data:
            return

    try:
        obj_data = currency_adapter.validate_json(json_data)
    except ValidationError:
        except_message = (
            f"Файл {json_path} в корне проекта имеет"
            " невалидные данные, получение данных из него невозможно,"
            " пожалуйста перенесите его в другое место."
        )
        raise ValueError(except_message)

    for obj_in in obj_data:
        if not currency_repository.get_obj_for_field_arg(
            "name", obj_in.name, many=False
        ):
            currency_repository.create(obj_in=obj_in)


def validate_currency_code(value: str) -> str:
    """Валидация кода валюты."""
    if len(value) != 3:
        except_message = f"Код {value} должен быть длинной ровно 3 символа."
        abort(400, except_message)

    if not value.isupper():
        except_message = f"У кода {value} должны быть все заглавные символы."
        abort(400, except_message)

    if not (value.isascii() and value.isalpha()):
        except_message = (
            f"У кода {value} все символы должны быть Английской раскладки."
        )
        abort(400, except_message)

    return value


def validate_convert_value(value: str) -> str:
    """Валидация конвертируемого значения."""

    if (isinstance(value, str) and not value.isdigit()):
        except_message = (
            f"Конвертируемое число {value} должно быть числом."
        )
        abort(400, except_message)

    value = int(value)

    if value < 0:
        except_message = (
            f"Конвертируемое число {value} не должно быть меньше нуля."
        )
        abort(400, except_message)

    return value
