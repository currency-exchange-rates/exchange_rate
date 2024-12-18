from pathlib import Path

from pydantic import TypeAdapter
from pydantic_core import ValidationError
from flask_sqlalchemy import SQLAlchemy

from src.schemas import CurrencySchemaCreate
from src.repository import RepositoryCurrency


def add_data_from_json(
    json_path: Path,
    db: SQLAlchemy
) -> None:
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


def add_rates_from_json(
    json_path: Path,
    db: SQLAlchemy
) -> None:
    """Добавляет данные из json."""
    pass
